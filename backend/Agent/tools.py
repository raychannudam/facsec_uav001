from langchain.tools import tool
from sqlalchemy.orm import Session
from Models import get_db, StationModel
from Services.Station import StationService
from Services.Uav import UavService

@tool
def search_name() -> str:
    """Search the secondary drone name when user ask for a name.
    """
    return f"Whatanak"

@tool
def get_station_data() -> str:
    """Get station data from the database.
    """
    db: Session = next(get_db())
    stations = StationService.get_stations(db)
    if not stations:
        return "No stations found."
    
    return f"Found {len(stations)} stations:\n {stations}"