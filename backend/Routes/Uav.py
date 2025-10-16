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
    
    return result

@router.get("/uavs", response_model=list[UavResponseSchema])
def get_uavs(query="", db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    uavs = UavService.get_uavs(db, query)
    return uavs

@router.get("/uavs/{uav_id}", response_model=UavResponseSchema)
def get_uav(uav_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    uav = UavService.get_uav_by_id(uav_id, db)
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    return uav

@router.put("/uavs/{uav_id}", response_model=UavResponseSchema)
def update_uav(uav_id: int, uav_update: UavUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in uav_update.dict().items() if v is not None}
    uav = UavService.update_uav(uav_id, update_data, db)
    if isinstance(uav, dict) and "error" in uav:
        raise HTTPException(status_code=400, detail=uav["error"])
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    return uav

@router.delete("/uavs/{uav_id}", response_model=UavResponseSchema)
def delete_uav(uav_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    uav = UavService.delete_uav(uav_id, db)
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    return uav