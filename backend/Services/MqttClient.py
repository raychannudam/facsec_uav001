import os
from sqlalchemy.orm import Session
from Models import MqttClientModel
from Schemas.MqttClient import MqttClientCreateSchema, MqttClientUpdateSchema, MqttClientResetPasswordSchema
import subprocess
from fastapi import HTTPException

MOSQUITTO_CONFIG_DIR = "/app/mosquitto/config"  # inside container
PWFILE_PATH = os.path.join(MOSQUITTO_CONFIG_DIR, "pwfile")
ACLFILE_PATH = os.path.join(MOSQUITTO_CONFIG_DIR, "aclfile")

class MqttClientService:
    @staticmethod
    def create_mqtt_client(mqtt_client_data: MqttClientCreateSchema, db: Session):
        # Check if client name already exists
        existing_client_name = db.query(MqttClientModel).filter(MqttClientModel.name == mqtt_client_data.name).first()
        if existing_client_name:
            raise HTTPException(status_code=400, detail="Client name already exists")
        
        # Check if client username already exists
        existing_client_username = db.query(MqttClientModel).filter(MqttClientModel.username == mqtt_client_data.username).first()
        if existing_client_username:
            raise HTTPException(status_code=400, detail="Client username already exists")

        # Add user to Mosquitto password file (Mosquitto handles hashing)
        subprocess.run([
            "mosquitto_passwd", "-b", PWFILE_PATH,
            mqtt_client_data.username, mqtt_client_data.password
        ], check=True)

        # Retrieve hashed password from pwfile
        hashed_password = None
        with open(PWFILE_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(mqtt_client_data.username + ":"):
                    hashed_password = line.split(":", 1)[1]
                    break

        if hashed_password is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve hashed password from pwfile")

        # Create client in DB with hashed password and other fields
        mqtt_client = MqttClientModel(
            user_id=mqtt_client_data.user_id,
            name=mqtt_client_data.name,
            description=mqtt_client_data.description,
            username=mqtt_client_data.username,
            password=hashed_password,
            status=mqtt_client_data.status,
            config=mqtt_client_data.config
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
                f.write(f"topic readwrite #\n\n")
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
            raise HTTPException(status_code=404, detail="MQTT client not found")

        # Check for duplicate name if name is being updated
        if "name" in update_data and update_data["name"] != mqtt_client.name:
            existing_client_name = db.query(MqttClientModel).filter(
                MqttClientModel.name == update_data["name"],
                MqttClientModel.id != mqtt_client_id
            ).first()
            if existing_client_name:
                raise HTTPException(status_code=400, detail="Client name already exists")

        # Check for duplicate username if username is being updated
        if "username" in update_data and update_data["username"] != mqtt_client.username:
            existing_client_username = db.query(MqttClientModel).filter(
                MqttClientModel.username == update_data["username"],
                MqttClientModel.id != mqtt_client_id
            ).first()
            if existing_client_username:
                raise HTTPException(status_code=400, detail="Client username already exists")

        # Store old username for comparison
        old_username = mqtt_client.username
        
        # Handle username change if provided
        username_changed = False
        if "username" in update_data and update_data["username"] != old_username:
            new_username = update_data["username"]
            username_changed = True

        # If username changed, update password file entry to copy password to new username
        if username_changed:
            # Read the current password for old username
            old_hashed_password = None
            with open(PWFILE_PATH, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(old_username + ":"):
                        old_hashed_password = line.split(":", 1)[1]
                        break
            
            if old_hashed_password:
                # Create new entry with new username and old password
                subprocess.run([
                    "mosquitto_passwd", "-b", PWFILE_PATH,
                    new_username, "temp_password_placeholder"
                ], check=True)
                
                # Replace the temp password with the actual hashed password
                with open(PWFILE_PATH, "r") as f:
                    lines = f.readlines()
                
                with open(PWFILE_PATH, "w") as f:
                    for line in lines:
                        if line.startswith(new_username + ":"):
                            # Replace the line with old hashed password
                            f.write(f"{new_username}:{old_hashed_password}\n")
                        else:
                            f.write(line)

        # Update DB fields
        for key in ["name", "description", "username", "status", "config"]:
            if key in update_data:
                setattr(mqtt_client, key, update_data[key])

        db.commit()
        db.refresh(mqtt_client)

        # Handle ACL update if username changed
        if username_changed:
            # Read current ACL content
            if os.path.exists(ACLFILE_PATH):
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
            
            # Remove old username from password file
            subprocess.run([
                "mosquitto_passwd", "-D", PWFILE_PATH, old_username
            ], check=True)

        return mqtt_client

    @staticmethod
    def delete_mqtt_client(mqtt_client_id: int, db: Session):
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()
        if not mqtt_client:
            raise HTTPException(status_code=404, detail="MQTT client not found")

        # Remove from pwfile only if user exists
        user_exists = False
        if os.path.exists(PWFILE_PATH):
            with open(PWFILE_PATH, "r") as f:
                for line in f:
                    if line.startswith(mqtt_client.username + ":"):
                        user_exists = True
                        break
        if user_exists:
            subprocess.run([
                "mosquitto_passwd", "-D", PWFILE_PATH, mqtt_client.username
            ], check=True)

        # Remove from ACL
        if os.path.exists(ACLFILE_PATH):
            with open(ACLFILE_PATH, "r") as f:
                lines = f.readlines()
            with open(ACLFILE_PATH, "w") as f:
                skip = False
                for line in lines:
                    if line.strip() == f"user {mqtt_client.username}":
                        skip = True
                        continue
                    if skip:
                        if line.strip().startswith("topic"):
                            continue
                        else:
                            skip = False
                    f.write(line)

        # Delete from DB
        db.delete(mqtt_client)
        db.commit()
        return mqtt_client

    @staticmethod
    def reset_mqtt_client_password(mqtt_client_id: int, password_data: MqttClientResetPasswordSchema, db: Session):
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()
        if not mqtt_client:
            raise HTTPException(status_code=404, detail="MQTT client not found")

        # Update password in Mosquitto password file
        try:
            subprocess.run([
                "mosquitto_passwd", "-b", PWFILE_PATH,
                mqtt_client.username, password_data.password
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Failed to update password in Mosquitto: {str(e)}")

        # Retrieve hashed password from pwfile
        hashed_password = None
        with open(PWFILE_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(mqtt_client.username + ":"):
                    hashed_password = line.split(":", 1)[1]
                    break

        if hashed_password is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve hashed password from pwfile")

        # Update password in database
        mqtt_client.password = hashed_password
        db.commit()
        db.refresh(mqtt_client)

        return mqtt_client