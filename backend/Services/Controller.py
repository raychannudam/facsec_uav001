from Models import Controller
from Schemas.Controller import ControllerCreateSchema, ControllerUpdateSchema
from sqlalchemy.orm import Session
from Models.Controller import ControllerModel
from Models import UserModel
from datetime import datetime

class ControllerService:
    @staticmethod
    def create_controller(controller_data: ControllerCreateSchema, db: Session, current_user: UserModel):
        controller = ControllerModel(
            user_id=current_user.id,
            name=controller_data.name,
            description=controller_data.description,
            config=controller_data.config
        )
        db.add(controller)
        db.commit()
        db.refresh(controller)
        return controller

    @staticmethod
    def get_controllers(db: Session, current_user: UserModel):
        return db.query(ControllerModel).filter(ControllerModel.user_id == current_user.id).all()

    @staticmethod
    def get_controller_by_id(controller_id: int, db: Session):
        return db.query(ControllerModel).filter(ControllerModel.id == controller_id).first()

    @staticmethod
    def update_controller(controller_id: int, update_data: ControllerUpdateSchema, db: Session):
        controller = db.query(ControllerModel).filter(ControllerModel.id == controller_id).first()
        if not controller:
            return None
        update_dict = update_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(controller, key, value)
        controller.updated_at = datetime.utcnow()  # Force update timestamp
        db.commit()
        db.refresh(controller)
        return controller

    @staticmethod
    def delete_controller(controller_id: int, db: Session):
        controller = db.query(ControllerModel).filter(ControllerModel.id == controller_id).first()
        if not controller:
            return None
        db.delete(controller)
        db.commit()
        return controller