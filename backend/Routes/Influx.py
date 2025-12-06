from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import UserModel, get_db
from Security.jwt import get_current_user
from Services.Influx import InfluxService

router = APIRouter()

def is_admin(user: UserModel) -> bool:
    """Check if the user has an admin role."""
    return any(role.name.lower() == "admin" for role in user.roles)

# Initialize Influx service
influx_service = InfluxService()

# -----------------------------
# GET: Latest telemetry field
# -----------------------------
@router.get("/influx/latest")
def get_latest_value(
    measurement: str,
    field: str,
    current_user: UserModel = Depends(get_current_user)
):
    result = influx_service.get_latest_value(
        measurement=measurement,
        field=field
    )

    if not result:
        raise HTTPException(status_code=404, detail="No data found")

    return {"data": result}

# -----------------------------
# GET: Telemetry history
# -----------------------------
@router.get("/influx/history")
def get_telemetry_history(
    measurement: str,
    field: str,
    range_str: str = "30m",
    current_user: UserModel = Depends(get_current_user)
):
    result = influx_service.get_measurement_history(
        measurement=measurement,
        field=field,
        range_str=range_str
    )

    if not result:
        raise HTTPException(status_code=404, detail="No history found")

    return {"data": result}

# -----------------------------
# GET: All drone telemetry (all fields)
# -----------------------------
@router.get("/influx/telemetry/{drone_username}")
def get_drone_telemetry(
    drone_username: str,
    range_str: str = "10m",
    current_user: UserModel = Depends(get_current_user)
):
    result = influx_service.get_drone_telemetry(
        drone_username=drone_username,
        range_str=range_str
    )

    return {"drone": drone_username, "telemetry": result}

# -----------------------------
# ADMIN: Run raw Flux queries
# -----------------------------
@router.post("/influx/raw")
def run_raw_flux_query(
    query: str,
    current_user: UserModel = Depends(get_current_user)
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Only admins can run raw Flux queries")

    try:
        result = influx_service.query(query)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
