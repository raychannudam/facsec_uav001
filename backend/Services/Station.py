from sqlalchemy.orm import Session
from Models import StationModel
from Schemas.Station import StationCreateSchema, StationUpdateSchema

class StationService:
    
    @staticmethod
    def create_station(station: StationCreateSchema, db: Session):
        # Check if station name already exists
        if db.query(StationModel).filter(StationModel.name == station.name).first():
            return {"error": "Station name already exists"}
        
        station_data = station.dict()
        new_station = StationModel(**station_data)
        db.add(new_station)
        db.commit()
        db.refresh(new_station)
        return new_station

    @staticmethod
    def get_stations(db: Session):
        return db.query(StationModel).all()

    @staticmethod
    def get_station_by_id(station_id: int, db: Session):
        return db.query(StationModel).filter(StationModel.id == station_id).first()

    @staticmethod
    def update_station(station_id: int, update_data: dict, db: Session):
        station = db.query(StationModel).filter(StationModel.id == station_id).first()
        if not station:
            return None
            
        # Check if name is unique if provided
        if "name" in update_data and update_data["name"] is not None:
            existing_station = db.query(StationModel).filter(
                StationModel.name == update_data["name"],
                StationModel.id != station_id
            ).first()
            if existing_station:
                return {"error": "Station name already exists"}
        
        # Update fields
        for key, value in update_data.items():
            setattr(station, key, value)
            
        db.commit()
        db.refresh(station)
        return station

    @staticmethod
    def delete_station(station_id: int, db: Session):
        station = db.query(StationModel).filter(StationModel.id == station_id).first()
        if not station:
            return None
        db.delete(station)
        db.commit()
        return station