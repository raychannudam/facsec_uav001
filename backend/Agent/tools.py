from langchain.tools import tool
from sqlalchemy.orm import Session
from Services.Uav import UavService

# ------------------------------
# Tools now require db: Session
# ------------------------------

@tool
def get_uavs(db: Session, query: str = ""):
    """Returns a list of all UAVs, optionally filtered by a query."""
    uavs = UavService.get_uavs(db, query=query)
    return [uav.name for uav in uavs]


@tool
def get_uav_by_id(db: Session, uav_id: int):
    """Returns detailed information about a specific UAV by its ID."""
    uav = UavService.get_uav_by_id(uav_id, db)

    if not uav:
        return "UAV not found."

    return {
        "id": uav.id,
        "name": uav.name,
        "station": uav.station.name if uav.station else None,
        "mqtt_client": uav.mqtt_client.username if uav.mqtt_client else None,
        "streaming_client": uav.streaming_client.username if uav.streaming_client else None,
    }


@tool
def get_uavs_by_user(db: Session, user_id: int, query: str = ""):
    """Returns a list of UAVs assigned to a specific user."""
    uavs = UavService.get_uavs_by_user(user_id, db, query=query)
    return [uav.name for uav in uavs]


@tool
def get_available_uavs(db: Session):
    """Returns a list of UAVs that are not currently assigned to a station."""
    uavs = UavService.get_available_uavs(db)
    return [uav.name for uav in uavs]
