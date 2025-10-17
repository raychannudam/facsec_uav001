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
        existing_client_name = db.query(MqttClientModel).filter(MqttClientModel.name == mqtt_client_data.name).first()
        if existing_client_name:
            return {"error": "Client name already exists"}
        
        existing_client_username = db.query(MqttClientModel).filter(MqttClientModel.username == mqtt_client_data.username).first()
        if existing_client_username:
            return {"error": "Client username already exists"}

        # 1. Add user to Mosquitto password file (Mosquitto handles hashing)
        subprocess.run([
            "mosquitto_passwd", "-b", PWFILE_PATH,
            mqtt_client_data.username, mqtt_client_data.password
        ], check=True)

        # 2. Retrieve hashed password from pwfile
        hashed_password = None
        with open(PWFILE_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(mqtt_client_data.username + ":"):
                    hashed_password = line.split(":", 1)[1]
                    break

        if hashed_password is None:
            raise ValueError("Failed to retrieve hashed password from pwfile")

        # 3. Create client in DB with hashed password and other fields
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

        # 4. Append ACL entry if it doesn't exist
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
    def get_mqtt_client_by_id(mqtt_client_id: int, db: Session):
        return db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()

    @staticmethod
    def update_mqtt_client(mqtt_client_id: int, update_data: MqttClientUpdateSchema, db: Session):
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()
        if not mqtt_client:
            return None

        # Support both Pydantic model and dict
        if hasattr(update_data, "dict"):
            update_dict = update_data.dict(exclude_unset=True)
        else:
            update_dict = update_data

        # # Store old username for comparison
        # old_username = mqtt_client.username
        # new_username = update_dict.get("username", old_username)
        
        # 1. Handle password update if provided
        # if "password" in update_dict:
        #     # Update password file with NEW username (in case username also changed)
        #     subprocess.run([
        #         "mosquitto_passwd", "-b", PWFILE_PATH,
        #         new_username, update_dict["password"]
        #     ], check=True)

        #     # Retrieve hashed password from pwfile
        #     hashed_password = None
        #     with open(PWFILE_PATH, "r") as f:
        #         for line in f:
        #             line = line.strip()
        #             if line.startswith(new_username + ":"):
        #                 hashed_password = line.split(":", 1)[1]
        #                 break

        #     if hashed_password is None:
        #         raise ValueError("Failed to retrieve hashed password from pwfile")

        #     update_dict["password"] = hashed_password
        # else:
        #     # If password is NOT provided but username is changing, we need to copy the password
        #     if "username" in update_dict and old_username != new_username:
        #         # Read the current password for old username
        #         old_hashed_password = None
        #         with open(PWFILE_PATH, "r") as f:
        #             for line in f:
        #                 line = line.strip()
        #                 if line.startswith(old_username + ":"):
        #                     old_hashed_password = line.split(":", 1)[1]
        #                     break
                
        #         if old_hashed_password:
        #             # Create new entry with new username and old password
        #             subprocess.run([
        #                 "mosquitto_passwd", "-b", PWFILE_PATH,
        #                 new_username, "temp_password_placeholder"
        #             ], check=True)
                    
        #             # Now replace the temp password with the actual hashed password
        #             with open(PWFILE_PATH, "r") as f:
        #                 lines = f.readlines()
                    
        #             with open(PWFILE_PATH, "w") as f:
        #                 for line in lines:
        #                     if line.startswith(new_username + ":"):
        #                         # Replace the line with old hashed password
        #                         f.write(f"{new_username}:{old_hashed_password}\n")
        #                     else:
        #                         f.write(line)
                    
        #             # Update the update_dict with the hashed password for database
        #             update_dict["password"] = old_hashed_password

        # 2. Update DB fields explicitly - only update password if it's in update_dict
        # for key in ["user_id", "name", "description", "username", "status", "config"]:
        for key in ["name", "description", "status", "config"]:
            if key in update_dict:
                setattr(mqtt_client, key, update_dict[key])
        
        # # Only update password if we have a new value in update_dict
        # if "password" in update_dict:
        #     setattr(mqtt_client, "password", update_dict["password"])

        db.commit()
        db.refresh(mqtt_client)

        # # 3. Handle ACL update if username changed
        # if "username" in update_dict and old_username != new_username:
        #     # Read current ACL content
        #     with open(ACLFILE_PATH, "r") as f:
        #         acl_lines = f.readlines()
            
        #     # Find and replace username in ACL file
        #     updated_acl_lines = []
        #     i = 0
        #     while i < len(acl_lines):
        #         line = acl_lines[i].strip()
        #         if line.startswith(f"user {old_username}"):
        #             # Replace the user line
        #             updated_acl_lines.append(f"user {new_username}\n")
        #             i += 1  # Move to next line (topic line)
        #             # Keep the topic permissions as is
        #             if i < len(acl_lines):
        #                 updated_acl_lines.append(acl_lines[i])
        #             i += 1  # Move to next line (empty line)
        #             # Keep the empty line if exists
        #             if i < len(acl_lines) and acl_lines[i].strip() == "":
        #                 updated_acl_lines.append(acl_lines[i])
        #                 i += 1
        #         else:
        #             updated_acl_lines.append(acl_lines[i])
        #             i += 1
            
        #     # Write updated ACL content back to file
        #     with open(ACLFILE_PATH, "w") as f:
        #         f.writelines(updated_acl_lines)
            
        #     # Remove old username from password file if username changed
        #     # Only remove if old username exists and is different from new username
        #     if old_username != new_username:
        #         # Check if old username exists in password file before trying to delete
        #         old_user_exists = False
        #         with open(PWFILE_PATH, "r") as f:
        #             for line in f:
        #                 if line.startswith(old_username + ":"):
        #                     old_user_exists = True
        #                     break
                
        #         # Only delete if the old user actually exists
        #         if old_user_exists:
        #             subprocess.run([
        #                 "mosquitto_passwd", "-D", PWFILE_PATH, old_username
        #             ], check=True)

        return mqtt_client

    @staticmethod
    def delete_mqtt_client(mqtt_client_id: int, db: Session):
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()
        if not mqtt_client:
            return None

        # 1. Remove from pwfile only if user exists
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

        # 2. Remove from ACL
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

        # 3. Delete from DB
        db.delete(mqtt_client)
        db.commit()
        return mqtt_client

    @staticmethod
    def reset_mqtt_client_password(mqtt_client_id: int, password_data: MqttClientResetPasswordSchema, db: Session):
        """
        Reset password for an MQTT client
        """
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()
        if not mqtt_client:
            return None

        # 1. Update password in Mosquitto password file
        try:
            subprocess.run([
                "mosquitto_passwd", "-b", PWFILE_PATH,
                mqtt_client.username, password_data.password
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Failed to update password in Mosquitto: {str(e)}")

        # 2. Retrieve hashed password from pwfile
        hashed_password = None
        with open(PWFILE_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(mqtt_client.username + ":"):
                    hashed_password = line.split(":", 1)[1]
                    break

        if hashed_password is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve hashed password from pwfile")

        # 3. Update password in database
        mqtt_client.password = hashed_password
        db.commit()
        db.refresh(mqtt_client)

        return mqtt_client