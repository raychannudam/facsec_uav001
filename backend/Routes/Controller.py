from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Models import get_db, UserModel
from Services.Controller import ControllerService
from Schemas.Controller import ControllerResponseSchema, ControllerCreateSchema, ControllerUpdateSchema
from Security.jwt import get_current_user

router = APIRouter(
    prefix="/controllers",
    tags=["controllers"]
)

@router.post("/", response_model=ControllerResponseSchema)
def create_controller(controller: ControllerCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    created = ControllerService.create_controller(controller, db, current_user)
    return created

@router.get("/", response_model=List[ControllerResponseSchema])
def get_controllers(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return ControllerService.get_controllers(db)

@router.get("/{controller_id}", response_model=ControllerResponseSchema)
def get_controller_by_id(controller_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    controller = ControllerService.get_controller_by_id(controller_id, db)
    if not controller:
        raise HTTPException(status_code=404, detail="Controller not found")
    return controller

@router.put("/{controller_id}", response_model=ControllerResponseSchema)
def update_controller(controller_id: int, update_data: ControllerUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    updated = ControllerService.update_controller(controller_id, update_data, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Controller not found")
    return updated

@router.delete("/{controller_id}", response_model=ControllerResponseSchema)
def delete_controller(controller_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    deleted = ControllerService.delete_controller(controller_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Controller not found")
    return deleted
