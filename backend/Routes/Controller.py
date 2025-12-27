from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Models import get_db, UserModel
from Services.Controller import ControllerService
from Schemas.Controller import ControllerResponseSchema, ControllerCreateSchema, ControllerUpdateSchema, ControllerAdditionalConfigSchema
from Security.jwt import get_current_user

router = APIRouter(
    prefix="/controllers",
    tags=["controllers"]
)

@router.post("", response_model=ControllerResponseSchema)
def create_controller(controller: ControllerCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    created = ControllerService.create_controller(controller, db, current_user)
    return created

@router.get("", response_model=List[ControllerResponseSchema])
def get_controllers(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return ControllerService.get_controllers(db, current_user)

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

@router.put("/update_mqtt_topic_additional_config/{controller_id}")
def update_mqtt_topic_additional_config(controller_id: int, control_widget_id: str, additional_config: ControllerAdditionalConfigSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    updated = ControllerService.update_mqtt_topic_additional_config(controller_id, control_widget_id, additional_config.additionalConfig, db)
    if not updated:
        raise HTTPException(status_code=500, detail="Error on Update Additional Config")
    return updated

@router.delete("/{controller_id}", response_model=ControllerResponseSchema)
def delete_controller(controller_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    deleted = ControllerService.delete_controller(controller_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Controller not found")
    return deleted
