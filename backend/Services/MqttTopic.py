from sqlalchemy.orm import Session
from Models import MqttTopicModel, UserModel, MqttClientModel
from Schemas.MqttTopic import MqttTopicCreateSchema, MqttTopicUpdateSchema
from fastapi import HTTPException
import os

MOSQUITTO_CONFIG_DIR = "/app/mosquitto/config"  # inside container
ACLFILE_PATH = os.path.join(MOSQUITTO_CONFIG_DIR, "aclfile")

class MqttTopicService:
    @staticmethod
    def _update_acl_file(db: Session):
        """Update the ACL file with all topics from the database"""
        if not os.path.exists(ACLFILE_PATH):
            open(ACLFILE_PATH, "w").close()

        # Get all clients with their topics
        clients = db.query(MqttClientModel).all()
        
        acl_content = ""
        for client in clients:
            acl_content += f"user {client.username}\n"
            
            # Get all topics for this client
            topics = db.query(MqttTopicModel).filter(MqttTopicModel.mqtt_client_id == client.id).all()
            
            if topics:
                for topic in topics:
                    # Use static access type (readwrite) since the model doesn't have access attribute
                    acl_content += f"topic readwrite {topic.name}\n"
            else:
                # Default topic access if no specific topics are defined
                acl_content += "topic readwrite #\n"
            
            acl_content += "\n"

        # Write the complete ACL content
        with open(ACLFILE_PATH, "w") as f:
            f.write(acl_content)

    @staticmethod
    def create_mqtt_topic(mqtt_topic_data: MqttTopicCreateSchema, db: Session):
        # Check if topic name already exists for the same client
        existing_topic = db.query(MqttTopicModel).filter(
            MqttTopicModel.name == mqtt_topic_data.name,
            MqttTopicModel.mqtt_client_id == mqtt_topic_data.mqtt_client_id
        ).first()
        if existing_topic:
            return {"error": "Topic name already exists for this client"}
        
        mqtt_topic = MqttTopicModel(**mqtt_topic_data.dict())
        db.add(mqtt_topic)
        db.commit()
        db.refresh(mqtt_topic)
        
        # Update ACL file after creating topic
        MqttTopicService._update_acl_file(db)
        
        return mqtt_topic

    @staticmethod
    def get_mqtt_topics(db: Session):
        return db.query(MqttTopicModel).all()

    @staticmethod
    def get_mqtt_topics_by_user(user_id: int, db: Session):
        # Join MqttTopicModel with MqttClientModel to filter by user_id
        return db.query(MqttTopicModel).join(MqttClientModel).filter(MqttClientModel.user_id == user_id).all()

    @staticmethod
    def get_mqtt_topic_by_id(mqtt_topic_id: int, db: Session):
        return db.query(MqttTopicModel).filter(MqttTopicModel.id == mqtt_topic_id).first()

    @staticmethod
    def update_mqtt_topic(mqtt_topic_id: int, update_data: MqttTopicUpdateSchema, db: Session):
        mqtt_topic = db.query(MqttTopicModel).filter(MqttTopicModel.id == mqtt_topic_id).first()
        if not mqtt_topic:
            return None
        
        # Check if topic name already exists for the same client (if name is being updated)
        if update_data.name and update_data.name != mqtt_topic.name:
            existing_topic = db.query(MqttTopicModel).filter(
                MqttTopicModel.name == update_data.name,
                MqttTopicModel.mqtt_client_id == mqtt_topic.mqtt_client_id,
                MqttTopicModel.id != mqtt_topic_id
            ).first()
            if existing_topic:
                return {"error": "Topic name already exists for this client"}

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(mqtt_topic, key, value)
        
        db.commit()
        db.refresh(mqtt_topic)
        
        # Update ACL file after updating topic
        MqttTopicService._update_acl_file(db)
        
        return mqtt_topic

    @staticmethod
    def delete_mqtt_topic(mqtt_topic_id: int, db: Session):
        mqtt_topic = db.query(MqttTopicModel).filter(MqttTopicModel.id == mqtt_topic_id).first()
        if not mqtt_topic:
            return None
        
        db.delete(mqtt_topic)
        db.commit()
        
        # Update ACL file after deleting topic
        MqttTopicService._update_acl_file(db)
        
        return mqtt_topic