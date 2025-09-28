from sqlalchemy.orm import Session
from Models import MqttClientModel
from Schemas.MqttClient import MqttClientCreateSchema, MqttClientUpdateSchema

class MqttClientService:
    @staticmethod
    def create_mqtt_client(mqtt_client_data: MqttClientCreateSchema, db: Session):
        mqtt_client = MqttClientModel(**mqtt_client_data.dict())
        db.add(mqtt_client)
        db.commit()
        db.refresh(mqtt_client)
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
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(mqtt_client, key, value)
        db.commit()
        db.refresh(mqtt_client)
        return mqtt_client

    @staticmethod
    def delete_mqtt_client(mqtt_client_id: int, db: Session):
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_client_id).first()
        if not mqtt_client:
            return None
        db.delete(mqtt_client)
        db.commit()
        return mqtt_client