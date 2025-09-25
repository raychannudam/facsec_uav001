
from sqlalchemy.orm import Session
from Models import UserModel, RoleModel
from Schemas import UserCreateSchema, UserResponseSchema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    
    @staticmethod
    def register(user: UserCreateSchema, db: Session):
        # Check if user already exists
        if db.query(UserModel).filter(UserModel.username == user.username).first():
            return {"error": "Username already exists"}
        user.password = pwd_context.hash(user.password)  # Hash the password
        new_user = UserModel(**user.dict())
        # Assign default role 'user'
        user_role = db.query(RoleModel).filter(RoleModel.name == "user").first()
        if user_role:
            new_user.roles.append(user_role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponseSchema(**new_user.__dict__)

    @staticmethod
    def get_users(db: Session):
        return db.query(UserModel).all()

    @staticmethod
    def get_user_by_id(user_id: int, db: Session):
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def update_user(user_id: int, update_data: dict, db: Session):
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        for key, value in update_data.items():
            if key == "password":
                value = pwd_context.hash(value)
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(user_id: int, db: Session):
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        db.delete(user)
        db.commit()
        return user
