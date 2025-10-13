from sqlalchemy.orm import Session
from Models import MqttTopicModel, UserModel
from Schemas.MqttTopic import MqttTopicCreateSchema, MqttTopicUpdateSchema

class MqttTopicService:
    @staticmethod
    def create_mqtt_topic(mqtt_topic_data: MqttTopicCreateSchema, db: Session):
        mqtt_topic = MqttTopicModel(**mqtt_topic_data.dict())
        db.add(mqtt_topic)
        db.commit()
        db.refresh(mqtt_topic)
        return mqtt_topic

    @staticmethod
    def get_mqtt_topics(mqtt_client_id, db: Session):
        return db.query(MqttTopicModel).filter(MqttTopicModel.mqtt_client_id == mqtt_client_id).all()

    @staticmethod
    def get_mqtt_topic_by_id(mqtt_topic_id: int, db: Session):
        return db.query(MqttTopicModel).filter(MqttTopicModel.id == mqtt_topic_id).first()

    @staticmethod
    def update_mqtt_topic(mqtt_topic_id: int, update_data: MqttTopicUpdateSchema, db: Session):
        mqtt_topic = db.query(MqttTopicModel).filter(MqttTopicModel.id == mqtt_topic_id).first()
        if not mqtt_topic:
            return None
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(mqtt_topic, key, value)
        db.commit()
        db.refresh(mqtt_topic)
        return mqtt_topic

    @staticmethod
    def delete_mqtt_topic(mqtt_topic_id: int, db: Session):
        mqtt_topic = db.query(MqttTopicModel).filter(MqttTopicModel.id == mqtt_topic_id).first()
        if not mqtt_topic:
            return None
        db.delete(mqtt_topic)
        db.commit()
        return mqtt_topic