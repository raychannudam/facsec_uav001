import os
import random
import string
from sqlalchemy.orm import Session
from Models import MqttClientModel
from Schemas.MqttClient import MqttClientCreateSchema, MqttClientUpdateSchema, MqttClientResetPasswordSchema
from Schemas.MqttTopic import MqttTopicCreateSchema
import subprocess
from fastapi import HTTPException
from Services.Mail import MailService
from passlib.context import CryptContext
from Services.MqttTopic import MqttTopicService

MOSQUITTO_CONFIG_DIR = "/app/mosquitto/config"  # inside container
PWFILE_PATH = os.path.join(MOSQUITTO_CONFIG_DIR, "pwfile")
ACLFILE_PATH = os.path.join(MOSQUITTO_CONFIG_DIR, "aclfile")

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MqttClientService:
    
    @staticmethod
    def _generate_password(length: int = 12) -> str:
        """Generate a random password"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(characters) for i in range(length))

    @staticmethod
    def _get_hashed_password_from_pwfile(username: str) -> str:
        """Retrieve hashed password from pwfile for a given username"""
        if not os.path.exists(PWFILE_PATH):
            return None
            
        with open(PWFILE_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(username + ":"):
                    return line.split(":", 1)[1]
        return None

    @staticmethod
    def _update_password_file(username: str, password: str):
        """Update or create password entry in mosquitto password file"""
        try:
            subprocess.run([
                "mosquitto_passwd", "-b", PWFILE_PATH,
                username, password
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Failed to update password in Mosquitto: {str(e)}")

    @staticmethod
    def _remove_user_from_password_file(username: str):
        """Remove user from mosquitto password file"""
        if not os.path.exists(PWFILE_PATH):
            return
            
        # Check if user exists in password file
        user_exists = False
        with open(PWFILE_PATH, "r") as f:
            for line in f:
                if line.startswith(username + ":"):
                    user_exists = True
                    break
        
        if user_exists:
            try:
                subprocess.run([
                    "mosquitto_passwd", "-D", PWFILE_PATH, username
                ], check=True)
            except subprocess.CalledProcessError as e:
                raise HTTPException(status_code=500, detail=f"Failed to remove user from password file: {str(e)}")

    @staticmethod
    def _update_acl_file(old_username: str, new_username: str):
        """Update ACL file when username changes"""
        if not os.path.exists(ACLFILE_PATH):
            return
            
        with open(ACLFILE_PATH, "r") as f:
            acl_lines = f.readlines()
        
        # Find and replace username in ACL file
        updated_acl_lines = []
        i = 0
        while i < len(acl_lines):
            line = acl_lines[i].strip()
            if line.startswith(f"user {old_username}"):
                # Replace the user line
                updated_acl_lines.append(f"user {new_username}\n")
                i += 1  # Move to next line (topic line)
                # Keep the topic permissions as is
                if i < len(acl_lines):
                    updated_acl_lines.append(acl_lines[i])
                i += 1  # Move to next line (empty line)
                # Keep the empty line if exists
                if i < len(acl_lines) and acl_lines[i].strip() == "":
                    updated_acl_lines.append(acl_lines[i])
                    i += 1
            else:
                updated_acl_lines.append(acl_lines[i])
                i += 1
        
        # Write updated ACL content back to file
        with open(ACLFILE_PATH, "w") as f:
            f.writelines(updated_acl_lines)

    @staticmethod
    def _remove_user_from_acl_file(username: str):
        """Remove user and their permissions from ACL file"""
        if not os.path.exists(ACLFILE_PATH):
            return
            
        with open(ACLFILE_PATH, "r") as f:
            lines = f.readlines()
        
        with open(ACLFILE_PATH, "w") as f:
            skip = False
            for line in lines:
                if line.strip() == f"user {username}":
                    skip = True
                    continue
                if skip:
                    if line.strip().startswith("topic"):
                        continue
                    else:
                        skip = False
                f.write(line)

    @staticmethod
    def create_mqtt_client(mqtt_client_data: MqttClientCreateSchema, db: Session):
        # Check if client name already exists
        existing_client_name = db.query(MqttClientModel).filter(MqttClientModel.name == mqtt_client_data.name).first()
        if existing_client_name:
            return {"error": "Client name already exists"}
        
        # Check if client username already exists
        existing_client_username = db.query(MqttClientModel).filter(MqttClientModel.username == mqtt_client_data.username).first()
        if existing_client_username:
            return {"error": "Client username already exists"}

        # Generate password if not provided
        if not mqtt_client_data.password:
            generated_password = MqttClientService._generate_password()
            password_to_use = generated_password
            raw_password_to_store = generated_password
        else:
            password_to_use = mqtt_client_data.password
            raw_password_to_store = mqtt_client_data.password

        # Add user to Mosquitto password file
        MqttClientService._update_password_file(mqtt_client_data.username, password_to_use)

        # Retrieve hashed password from pwfile
        hashed_password = MqttClientService._get_hashed_password_from_pwfile(mqtt_client_data.username)
        if hashed_password is None:
            return {"error": "Failed to retrieve hashed password from pwfile"}

        # Generate validation code
        validation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Create client in DB with hashed password, raw_password and other fields
        mqtt_client = MqttClientModel(
            user_id=mqtt_client_data.user_id,
            name=mqtt_client_data.name,
            description=mqtt_client_data.description,
            username=mqtt_client_data.username,
            password=hashed_password,
            raw_password=raw_password_to_store,  # Store the raw password
            status=mqtt_client_data.status,
            config=mqtt_client_data.config,
            validation_code=validation_code
        )
        db.add(mqtt_client)
        db.commit()
        db.refresh(mqtt_client)

        # Append ACL entry if it doesn't exist
        if not os.path.exists(ACLFILE_PATH):
            open(ACLFILE_PATH, "w").close()

        with open(ACLFILE_PATH, "r") as f:
            acl_content = f.read()

        if f"user {mqtt_client.username}" not in acl_content:
            with open(ACLFILE_PATH, "a") as f:
                f.write(f"user {mqtt_client.username}\n")
                
                
        # create default topics for the client
        try:
            default_topics = [
                {'name': 'altitude', 'topic': f'drsys/{mqtt_client.username}/altitude'},
                {'name': 'battery', 'topic': f'drsys/{mqtt_client.username}/battery'},
                {'name': 'gps_latlng', 'topic': f'drsys/{mqtt_client.username}/gps_latlng'},
                {'name': 'speed', 'topic': f'drsys/{mqtt_client.username}/speed'},
            ]
            for topic in default_topics:
                MqttTopicService.create_mqtt_topic(
                    MqttTopicCreateSchema(
                        mqtt_client_id=mqtt_client.id,
                        name=topic['topic'],
                        description=topic['description'] if 'description' in topic else "",
                        config={},
                        status=True
                    ),
                    db
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create default topics: {str(e)}")
        
        return mqtt_client

    @staticmethod
    def get_mqtt_clients(db: Session):
        return db.query(MqttClientModel).all()

    @staticmethod
    def get_mqtt_clients_by_user(user_id: int, db: Session):
        return db.query(MqttClientModel).filter(MqttClientModel.user_id == user_id).all()

    @staticmethod
    def get_mqtt_client_by_id(mqtt_client_id: int, db: Session):
        return db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()

    @staticmethod
    def update_mqtt_client(mqtt_client_id: int, update_data: dict, db: Session):
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()
        if not mqtt_client:
            return None

        # Check for duplicate name if name is being updated
        if "name" in update_data and update_data["name"] != mqtt_client.name:
            existing_client_name = db.query(MqttClientModel).filter(
                MqttClientModel.name == update_data["name"],
                MqttClientModel.id != mqtt_client_id
            ).first()
            if existing_client_name:
                return {"error": "Client name already exists"}

        # Check for duplicate username if username is being updated
        if "username" in update_data and update_data["username"] != mqtt_client.username:
            existing_client_username = db.query(MqttClientModel).filter(
                MqttClientModel.username == update_data["username"],
                MqttClientModel.id != mqtt_client_id
            ).first()
            if existing_client_username:
                return {"error": "Client username already exists"}

        # Store old username for comparison
        old_username = mqtt_client.username
        
        # Handle username change if provided
        username_changed = False
        if "username" in update_data and update_data["username"] != old_username:
            new_username = update_data["username"]
            username_changed = True

        # If username changed, handle password file and ACL updates
        if username_changed:
            # Get the current password hash for the old username
            current_password_hash = MqttClientService._get_hashed_password_from_pwfile(old_username)
            
            if current_password_hash:
                # Remove old username from password file
                MqttClientService._remove_user_from_password_file(old_username)
                
                # Create new entry with new username and current password
                # We need to use a temporary password first, then manually update the hash
                temp_password = "temp_" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                MqttClientService._update_password_file(new_username, temp_password)
                
                # Now replace the temp password entry with the actual hash
                with open(PWFILE_PATH, "r") as f:
                    lines = f.readlines()
                
                with open(PWFILE_PATH, "w") as f:
                    for line in lines:
                        if line.startswith(new_username + ":"):
                            # Replace the line with the old hashed password
                            f.write(f"{new_username}:{current_password_hash}\n")
                        else:
                            f.write(line)
                
                # Update ACL file
                MqttClientService._update_acl_file(old_username, new_username)

        # Update DB fields
        for key in ["name", "description", "username", "status", "config"]:
            if key in update_data:
                setattr(mqtt_client, key, update_data[key])

        db.commit()
        db.refresh(mqtt_client)

        return mqtt_client

    @staticmethod
    def delete_mqtt_client(mqtt_client_id: int, db: Session):
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()
        if not mqtt_client:
            return None

        # Remove from password file
        MqttClientService._remove_user_from_password_file(mqtt_client.username)

        # Remove from ACL
        MqttClientService._remove_user_from_acl_file(mqtt_client.username)

        # Delete from DB
        db.delete(mqtt_client)
        db.commit()
        return mqtt_client

    @staticmethod
    def update_mqtt_client_password(client_id: int, validation_code: str, new_password: str, db: Session):
        client = db.query(MqttClientModel).filter(MqttClientModel.id == client_id).first()
        if not client:
            return None
        
        if client.validation_code != validation_code:
            return None
        
        # Update password in Mosquitto password file
        MqttClientService._update_password_file(client.username, new_password)
        
        # Retrieve hashed password from pwfile
        hashed_password = MqttClientService._get_hashed_password_from_pwfile(client.username)
        if hashed_password is None:
            return {"error": "Failed to retrieve hashed password from pwfile"}
        
        # Update password and raw_password in database
        client.password = hashed_password
        client.raw_password = new_password
        
        # Generate new validation code after password change
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        client.validation_code = code
        
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    async def request_validation_code(client_id: int, db: Session):
        client = db.query(MqttClientModel).filter(MqttClientModel.id == client_id).first()
        
        if not client:
            return None
        
        email = client.user.email
        
        if not client.validation_code:
            # Generate new validation code if not present
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            client.validation_code = code
            db.commit()
            db.refresh(client)
            
        # Send email with the validation code
        await MailService.send_email(email, client.validation_code, subject=f"MQTT Client: {client.name}, Validation Code")
        
        return True