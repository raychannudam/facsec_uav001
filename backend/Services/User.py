from sqlalchemy.orm import Session
from Models import UserModel, RoleModel
from Schemas import UserCreateSchema, UserResponseSchema
from passlib.context import CryptContext
from Services.Controller import ControllerService
from Schemas.Controller import ControllerCreateSchema
from uuid import uuid4

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    
    @staticmethod
    def register(user: UserCreateSchema, db: Session):
        # Check if user already exists
        if db.query(UserModel).filter(UserModel.username == user.username).first():
            return {"error": "Username already exists"}
        # Hash the password
        user_data = user.dict(exclude={"roles"})
        user_data["password"] = pwd_context.hash(user_data["password"])
        new_user = UserModel(**user_data)
        # Assign roles by name
        if user.roles:
            roles = db.query(RoleModel).filter(RoleModel.name.in_(user.roles)).all()
            if len(roles) != len(user.roles):
                return {"error": "One or more roles not found"}
            new_user.roles.extend(roles)
        # Assign default 'user' role if no roles provided
        else:
            user_role = db.query(RoleModel).filter(RoleModel.name == "user").first()
            if user_role:
                new_user.roles.append(user_role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # create default controller
        # create default controller (cleanup user if controller creation fails)
        try:
            controller_name = str(uuid4())
            controller_description = "Default controller"
            controller_config = {
                'selectedDrone': {},
                'streamingUrls': [],
                'mqttTopics': [],
            }
            
            controller_data = ControllerCreateSchema(
                name=controller_name,
                description=controller_description,
                config=controller_config
            )
            
            ControllerService.create_controller(
                controller_data=controller_data,
                db=db,
                current_user=new_user
            )
        except Exception:
            print("Controller creation failed, attempting to remove created user")
            try:
                db.delete(new_user)
                db.commit()
            except Exception:
                db.rollback()
                print("Failed to cleanup user after controller creation failure")
            raise
            
        return new_user

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
        # Handle role updates
        if "roles" in update_data:
            roles = update_data.pop("roles")
            if roles is not None:
                new_roles = db.query(RoleModel).filter(RoleModel.name.in_(roles)).all()
                if len(new_roles) != len(roles):
                    return {"error": "One or more roles not found"}
                user.roles = new_roles
        # Update other fields
        for key, value in update_data.items():
            if key == "password" and value:
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