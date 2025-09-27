from sqlalchemy.orm import Session
from Models import UserModel, RoleModel

class UserService:
    
    @staticmethod
    def register(user_data, db: Session):
        role_ids = user_data.pop("role_ids", [])
        user = UserModel(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)

        # Assign roles if provided
        if role_ids:
            roles = db.query(RoleModel).filter(RoleModel.id.in_(role_ids)).all()
            user.roles.extend(roles)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def update_user(user_id: int, update_data: dict, db: Session):
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None

        role_ids = update_data.pop("role_ids", None)
        for key, value in update_data.items():
            setattr(user, key, value)

        if role_ids is not None:
            # Clear existing roles and assign new roles
            user.roles = []
            roles = db.query(RoleModel).filter(RoleModel.id.in_(role_ids)).all()
            user.roles.extend(roles)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_users(db: Session):
        return db.query(UserModel).all()

    @staticmethod
    def get_user_by_id(user_id: int, db: Session):
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def delete_user(user_id: int, db: Session):
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        db.delete(user)
        db.commit()
        return user