from sqlalchemy.orm import Session
from Models import StreamingClientModel, UserModel
from Schemas.StreamingClient import StreamingClientCreateSchema
from Services.Mail import MailService
from passlib.context import CryptContext
import random
import string

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
        
        # Assign random code to validation_code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        client_data["validation_code"] = code
        
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
            
        # Update fields
        for key, value in update_data.items():
            setattr(client, key, value)
            
        db.commit()
        db.refresh(client)
        return client
    
    @staticmethod
    def update_streaming_client_password(client_id: int, validation_code: str, new_password: str, db: Session):
        client = db.query(StreamingClientModel).filter(StreamingClientModel.id == client_id).first()
        if not client:
            return None
        
        if client.validation_code != validation_code:
            return None
        
        client.password = pwd_context.hash(new_password)
        
        # Generate new validation code after password change
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        client.validation_code = code
        
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    async def request_validation_code(client_id: int, db: Session):
        client = db.query(StreamingClientModel).filter(StreamingClientModel.id == client_id).first()
        
        if not client:
            return None
        
        email = client.user.email
        
        if not client.validation_code:
            # Generate new validation code if not present
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            client.validation_code = code
            db.commit()
            db.refresh(client)
            
        # Send email with the validation code
        await MailService.send_email(email, client.validation_code, subject="Your Email Validation Code")
        
        return True

    @staticmethod
    def delete_streaming_client(client_id: int, db: Session):
        client = db.query(StreamingClientModel).filter(StreamingClientModel.id == client_id).first()
        if not client:
            return None
        db.delete(client)
        db.commit()
        return client