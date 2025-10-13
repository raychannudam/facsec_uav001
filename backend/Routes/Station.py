from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import get_db, StationModel
from Schemas.Station import StationCreateSchema, StationUpdateSchema, StationResponseSchema
from Services.Station import StationService
from Security.jwt import get_current_user
from Models import UserModel

router = APIRouter()

@router.post("/stations", response_model=StationResponseSchema)
def create_station(station: StationCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result = StationService.create_station(station, db)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return StationResponseSchema(
        id=result.id,
        name=result.name,
        description=result.description,
        lat=result.lat,
        long=result.long,
        created_at=str(result.created_at),
        updated_at=str(result.updated_at)
    )

@router.get("/stations", response_model=list[StationResponseSchema])
def get_stations(query="", db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    stations = StationService.get_stations(db, query=query)
    return stations

@router.get("/stations/{station_id}", response_model=StationResponseSchema)
def get_station(station_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    station = StationService.get_station_by_id(station_id, db)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    return StationResponseSchema(
        id=station.id,
        name=station.name,
        description=station.description,
        lat=station.lat,
        long=station.long,
        created_at=str(station.created_at),
        updated_at=str(station.updated_at)
    )

@router.put("/stations/{station_id}", response_model=StationResponseSchema)
def update_station(station_id: int, station_update: StationUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in station_update.dict().items() if v is not None}
    station = StationService.update_station(station_id, update_data, db)
    if isinstance(station, dict) and "error" in station:
        raise HTTPException(status_code=400, detail=station["error"])
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    return StationResponseSchema(
        id=station.id,
        name=station.name,
        description=station.description,
        lat=station.lat,
        long=station.long,
        created_at=str(station.created_at),
        updated_at=str(station.updated_at)
    )

@router.delete("/stations/{station_id}", response_model=StationResponseSchema)
def delete_station(station_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    station = StationService.delete_station(station_id, db)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    return StationResponseSchema(
        id=station.id,
        name=station.name,
        description=station.description,
        lat=station.lat,
        long=station.long,
        created_at=str(station.created_at),
        updated_at=str(station.updated_at)
    )