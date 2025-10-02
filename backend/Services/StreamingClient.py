from sqlalchemy.orm import Session
from Models import StreamingClientModel, UserModel
from Schemas.StreamingClient import StreamingClientCreateSchema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class StreamingClientService:
    
    @staticmethod
    def create_streaming_client(client: StreamingClientCreateSchema, db: Session, current_user: UserModel):    
        # Check if username already exists
        if db.query(StreamingClientModel).filter(StreamingClientModel.username == client.username).first():
            return {"error": "Streaming client username already exists"}
        
        # Hash the password
        client_data = client.dict()
        client_data["password"] = pwd_context.hash(client_data["password"])
        
        # Assign the current user's ID as the owner of the streaming client
        client_data["user_id"] = current_user.id
        
        new_client = StreamingClientModel(**client_data)
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client

    @staticmethod
    def get_streaming_clients(db: Session):
        return db.query(StreamingClientModel).all()

    @staticmethod
    def get_streaming_client_by_id(client_id: int, db: Session):
        return db.query(StreamingClientModel).filter(StreamingClientModel.id == client_id).first()

    @staticmethod
    def update_streaming_client(client_id: int, update_data: dict, db: Session):
        client = db.query(StreamingClientModel).filter(StreamingClientModel.id == client_id).first()
        if not client:
            return None
            
        # Check if user_id exists if provided
        if "user_id" in update_data and update_data["user_id"] is not None:
            user = db.query(UserModel).filter(UserModel.id == update_data["user_id"]).first()
            if not user:
                return {"error": "User not found"}
        
        # Check if username is unique if provided
        if "username" in update_data and update_data["username"] is not None:
            existing_client = db.query(StreamingClientModel).filter(
                StreamingClientModel.username == update_data["username"],
                StreamingClientModel.id != client_id
            ).first()
            if existing_client:
                return {"error": "Streaming client username already exists"}
        
        # Update fields
        for key, value in update_data.items():
            if key == "password" and value:
                value = pwd_context.hash(value)
            setattr(client, key, value)
            
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def delete_streaming_client(client_id: int, db: Session):
        client = db.query(StreamingClientModel).filter(StreamingClientModel.id == client_id).first()
        if not client:
            return None
        db.delete(client)
        db.commit()
        return client