from sqlalchemy.orm import Session
from Models import UavModel, MqttClientModel, StreamingClientModel, StationModel
from Schemas.Uav import UavCreateSchema, UavUpdateSchema

class UavService:
    
    @staticmethod
    def create_uav(uav: UavCreateSchema, db: Session):
        # Check if UAV name already exists
        if db.query(UavModel).filter(UavModel.name == uav.name).first():
            return {"error": "UAV name already exists"}
        
        # Validate mqtt_client_id if provided
        if uav.mqtt_client_id is not None:
            mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == uav.mqtt_client_id).first()
            if not mqtt_client:
                return {"error": "MQTT client not found"}
        
        # Validate streaming_client_id if provided
        if uav.streaming_client_id is not None:
            streaming_client = db.query(StreamingClientModel).filter(StreamingClientModel.id == uav.streaming_client_id).first()
            if not streaming_client:
                return {"error": "Streaming client not found"}
        
        # Validate station_id if provided
        if uav.station_id is not None:
            station = db.query(StationModel).filter(StationModel.id == uav.station_id).first()
            if not station:
                return {"error": "Station not found"}
        
        uav_data = uav.dict()
        new_uav = UavModel(**uav_data)
        db.add(new_uav)
        db.commit()
        db.refresh(new_uav)
        return new_uav

    @staticmethod
    def get_uavs(db: Session):
        return db.query(UavModel).all()

    @staticmethod
    def get_uav_by_id(uav_id: int, db: Session):
        return db.query(UavModel).filter(UavModel.id == uav_id).first()

    @staticmethod
    def update_uav(uav_id: int, update_data: dict, db: Session):
        uav = db.query(UavModel).filter(UavModel.id == uav_id).first()
        if not uav:
            return None
        
        # Check if name is unique if provided
        if "name" in update_data and update_data["name"] is not None:
            existing_uav = db.query(UavModel).filter(
                UavModel.name == update_data["name"],
                UavModel.id != uav_id
            ).first()
            if existing_uav:
                return {"error": "UAV name already exists"}
        
        # Validate mqtt_client_id if provided
        if "mqtt_client_id" in update_data and update_data["mqtt_client_id"] is not None:
            mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == update_data["mqtt_client_id"]).first()
            if not mqtt_client:
                return {"error": "MQTT client not found"}
        
        # Validate streaming_client_id if provided
        if "streaming_client_id" in update_data and update_data["streaming_client_id"] is not None:
            streaming_client = db.query(StreamingClientModel).filter(StreamingClientModel.id == update_data["streaming_client_id"]).first()
            if not streaming_client:
                return {"error": "Streaming client not found"}
        
        # Validate station_id if provided
        if "station_id" in update_data and update_data["station_id"] is not None:
            station = db.query(StationModel).filter(StationModel.id == update_data["station_id"]).first()
            if not station:
                return {"error": "Station not found"}
        
        # Update fields
        for key, value in update_data.items():
            setattr(uav, key, value)
            
        db.commit()
        db.refresh(uav)
        return uav

    @staticmethod
    def delete_uav(uav_id: int, db: Session):
        uav = db.query(UavModel).filter(UavModel.id == uav_id).first()
        if not uav:
            return None
        db.delete(uav)
        db.commit()
        return uav