from sqlalchemy.orm import Session
from Models import StationModel, UavModel
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
    def get_stations(db: Session, query=""):
        if query != "":
            return db.query(StationModel).filter(StationModel.name.like(f"%{query}%")).all()
        return db.query(StationModel).all()


    @staticmethod
    def get_station_by_id(station_id: int, db: Session):
        station = db.query(StationModel).filter(StationModel.id == station_id).first()
        
        if station:
            # Check if UAVs are associated with this station
            if hasattr(station, 'uavs') and station.uavs:
                print(f"Station ID {station_id}: {len(station.uavs)} UAV(s) associated")
                for uav in station.uavs:
                    print(f"  - UAV ID: {uav.id}, Name: {uav.name if hasattr(uav, 'name') else 'N/A'}")
            else:
                print(f"Station ID {station_id}: No UAVs associated")
        else:
            print(f"Station ID {station_id}: Not found")
        
        return station

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

        # Set station_id to null for associated UAVs
        db.query(UavModel).filter(UavModel.station_id == station_id).update({"station_id": None})

        db.delete(station)
        db.commit()
        return station