from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import get_db, UavModel
from Schemas.Uav import UavCreateSchema, UavUpdateSchema, UavResponseSchema
from Services.Uav import UavService
from Security.jwt import get_current_user
from Models import UserModel

router = APIRouter()

@router.post("/uavs", response_model=UavResponseSchema)
def create_uav(uav: UavCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result = UavService.create_uav(uav, db)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return UavResponseSchema(
        id=result.id,
        type=result.type,
        name=result.name,
        mqtt_client_id=result.mqtt_client_id,
        streaming_client_id=result.streaming_client_id,
        station_id=result.station_id,
        last_lat=result.last_lat,
        last_long=result.last_long,
        operation_data=result.operation_data,
        created_at=str(result.created_at),
        updated_at=str(result.updated_at),
        mqtt_client=result.mqtt_client,
        streaming_client=result.streaming_client,
        station=result.station
    )

@router.get("/uavs", response_model=list[UavResponseSchema])
def get_uavs(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    uavs = UavService.get_uavs(db)
    return [UavResponseSchema(
        id=u.id,
        type=u.type,
        name=u.name,
        mqtt_client_id=u.mqtt_client_id,
        streaming_client_id=u.streaming_client_id,
        station_id=u.station_id,
        last_lat=u.last_lat,
        last_long=u.last_long,
        operation_data=u.operation_data,
        created_at=str(u.created_at),
        updated_at=str(u.updated_at),
        mqtt_client=u.mqtt_client,
        streaming_client=u.streaming_client,
        station=u.station
    ) for u in uavs]

@router.get("/uavs/{uav_id}", response_model=UavResponseSchema)
def get_uav(uav_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    uav = UavService.get_uav_by_id(uav_id, db)
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    return UavResponseSchema(
        id=uav.id,
        type=uav.type,
        name=uav.name,
        mqtt_client_id=uav.mqtt_client_id,
        streaming_client_id=uav.streaming_client_id,
        station_id=uav.station_id,
        last_lat=uav.last_lat,
        last_long=uav.last_long,
        operation_data=uav.operation_data,
        created_at=str(uav.created_at),
        updated_at=str(uav.updated_at),
        mqtt_client=uav.mqtt_client,
        streaming_client=uav.streaming_client,
        station=uav.station
    )

@router.put("/uavs/{uav_id}", response_model=UavResponseSchema)
def update_uav(uav_id: int, uav_update: UavUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in uav_update.dict().items() if v is not None}
    uav = UavService.update_uav(uav_id, update_data, db)
    if isinstance(uav, dict) and "error" in uav:
        raise HTTPException(status_code=400, detail=uav["error"])
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    return UavResponseSchema(
        id=uav.id,
        type=uav.type,
        name=uav.name,
        mqtt_client_id=uav.mqtt_client_id,
        streaming_client_id=uav.streaming_client_id,
        station_id=uav.station_id,
        last_lat=uav.last_lat,
        last_long=uav.last_long,
        operation_data=uav.operation_data,
        created_at=str(uav.created_at),
        updated_at=str(uav.updated_at),
        mqtt_client=uav.mqtt_client,
        streaming_client=uav.streaming_client,
        station=uav.station
    )

@router.delete("/uavs/{uav_id}", response_model=UavResponseSchema)
def delete_uav(uav_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    uav = UavService.delete_uav(uav_id, db)
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    return UavResponseSchema(
        id=uav.id,
        type=uav.type,
        name=uav.name,
        mqtt_client_id=uav.mqtt_client_id,
        streaming_client_id=uav.streaming_client_id,
        station_id=uav.station_id,
        last_lat=uav.last_lat,
        last_long=uav.last_long,
        operation_data=uav.operation_data,
        created_at=str(uav.created_at),
        updated_at=str(uav.updated_at),
        mqtt_client=uav.mqtt_client,
        streaming_client=uav.streaming_client,
        station=uav.station
    )