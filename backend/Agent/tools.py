import json
from langchain.tools import tool
from sqlalchemy.orm import Session
from Models import get_db, StationModel
from Services.Station import StationService
from Services.Uav import UavService
from fastapi.encoders import jsonable_encoder

@tool
def get_station_data() -> str:
    """Get station data from the database.
    """
    db: Session = next(get_db())
    stations = StationService.get_stations(db)
    if not stations:
        return "No stations found."

    stations_data = jsonable_encoder(stations)
    
    return f"Found {len(stations)} stations:\n{json.dumps(stations_data, indent=2)}"