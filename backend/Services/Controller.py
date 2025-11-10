from Models import Controller
from Schemas.Controller import ControllerCreateSchema, ControllerUpdateSchema
from sqlalchemy.orm import Session
from Models.Controller import ControllerModel
from Models import UserModel
from Models import MqttClientModel
from Models import MqttTopicModel
from datetime import datetime

class ControllerService:
    @staticmethod
    def create_controller(controller_data: ControllerCreateSchema, db: Session, current_user: UserModel):
        controller = ControllerModel(
            user_id=current_user.id,
            name=controller_data.name,
            description=controller_data.description,
            config=controller_data.config
        )
        db.add(controller)
        db.commit()
        db.refresh(controller)
        return controller

    @staticmethod
    def get_controllers(db: Session, current_user: UserModel):
        return db.query(ControllerModel).filter(ControllerModel.user_id == current_user.id).all()

    @staticmethod
    def get_controller_by_id(controller_id: int, db: Session):
        return db.query(ControllerModel).filter(ControllerModel.id == controller_id).first()
    
    @staticmethod
    def get_controller_by_user_id(user_id: int, db: Session):
        return db.query(ControllerModel).filter(ControllerModel.user_id == user_id).first()

    @staticmethod
    def update_controller(controller_id: int, update_data: ControllerUpdateSchema, db: Session):
        controller = db.query(ControllerModel).filter(ControllerModel.id == controller_id).first()
        if not controller:
            return None
        update_dict = update_data.dict(exclude_unset=True)
        mqtt_topics = db.query(MqttTopicModel).filter(MqttTopicModel.mqtt_client_id==update_dict['config']['selectedDrone']['mqtt_client']['id']).all()
        default_mqtt_topics = []
        for mqtt_topic in mqtt_topics:
            if (mqtt_topic.name == f"drsys/{update_dict['config']['selectedDrone']['mqtt_client']['username']}/altitude" or
                mqtt_topic.name == f"drsys/{update_dict['config']['selectedDrone']['mqtt_client']['username']}/battery" or 
                mqtt_topic.name == f"drsys/{update_dict['config']['selectedDrone']['mqtt_client']['username']}/gps_latlng" or 
                mqtt_topic.name == f"drsys/{update_dict['config']['selectedDrone']['mqtt_client']['username']}/speed" or
                mqtt_topic.name == f"drsys/{update_dict['config']['selectedDrone']['mqtt_client']['username']}/temperature"):
                # Convert datetime fields to ISO format for JSON serialization
                default_mqtt_topics.append({
                    'id': mqtt_topic.name.split('/')[-1],
                    'name': mqtt_topic.name,
                })
        for key, value in update_dict.items():
            setattr(controller, key, value)
            if key == "config":
                value['default'] = {
                    'mqttTopics': default_mqtt_topics
                }
        controller.updated_at = datetime.utcnow()  # Force update timestamp
        db.commit()
        db.refresh(controller)
        return controller

    @staticmethod
    def delete_controller(controller_id: int, db: Session):
        controller = db.query(ControllerModel).filter(ControllerModel.id == controller_id).first()
        if not controller:
            return None
        db.delete(controller)
        db.commit()
        return controller