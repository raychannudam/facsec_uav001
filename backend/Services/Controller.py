from Models import Controller
from Schemas.Controller import ControllerCreateSchema, ControllerUpdateSchema
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
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
    @staticmethod
    @staticmethod
    def update_mqtt_topic_additional_config(controller_id: int, control_widget_id: str, additionalConfig: dict, db: Session):
        # Debug: Print the received additionalConfig
        print("DEBUG: Received additionalConfig:", additionalConfig)

        # Retrieve the controller by ID
        controller = db.query(ControllerModel).filter(ControllerModel.id == controller_id).first()
        if not controller:
            return {"error": "Controller not found"}

        # Track if the update was successful
        updated = False

        # Ensure config is mutable and modify the mqttTopics in the controller's config
        mqtt_topics = controller.config.get("mqttTopics", [])
        for topic in mqtt_topics:
            if topic["id"] == control_widget_id:
                topic["additionalConfig"] = additionalConfig
                updated = True
                break

        if not updated:
            return {"error": f"Control widget with ID {control_widget_id} not found"}
        controller.updated_at = datetime.utcnow()

        # **Flag the config as dirty** (this is the key part)
        flag_modified(controller, "config")  # Signal that `config` has been modified

        db.flush()  # Force the session to push changes to the database
        try:
            db.commit()
            db.refresh(controller)
        except Exception as e:
            db.rollback()
            return {"error": f"Failed to commit changes: {str(e)}"}
        
        return {
            "message": "Success",
            "data": controller 
        }
            


    @staticmethod
    def delete_controller(controller_id: int, db: Session):
        controller = db.query(ControllerModel).filter(ControllerModel.id == controller_id).first()
        if not controller:
            return None
        db.delete(controller)
        db.commit()
        return controller