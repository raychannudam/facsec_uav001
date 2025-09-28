from sqlalchemy.orm import Session
from Models import StreamingUrlModel, StreamingClientModel
from Schemas import StreamingUrlCreateSchema

class StreamingUrlService:
    
    @staticmethod
    def create_streaming_url(url: StreamingUrlCreateSchema, db: Session):
        # Check if streaming client exists
        streaming_client = db.query(StreamingClientModel).filter(StreamingClientModel.id == url.streaming_client_id).first()
        if not streaming_client:
            return {"error": "Streaming client not found"}
        
        # Check if name is unique within the streaming client
        if db.query(StreamingUrlModel).filter(
            StreamingUrlModel.streaming_client_id == url.streaming_client_id,
            StreamingUrlModel.name == url.name
        ).first():
            return {"error": "Streaming URL name already exists for this streaming client"}
        
        url_data = url.dict()
        new_url = StreamingUrlModel(**url_data)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return new_url

    @staticmethod
    def get_streaming_urls(db: Session):
        return db.query(StreamingUrlModel).all()

    @staticmethod
    def get_streaming_url_by_id(url_id: int, db: Session):
        return db.query(StreamingUrlModel).filter(StreamingUrlModel.id == url_id).first()

    @staticmethod
    def update_streaming_url(url_id: int, update_data: dict, db: Session):
        url = db.query(StreamingUrlModel).filter(StreamingUrlModel.id == url_id).first()
        if not url:
            return None
            
        # Check if streaming_client_id exists if provided
        if "streaming_client_id" in update_data and update_data["streaming_client_id"] is not None:
            streaming_client = db.query(StreamingClientModel).filter(
                StreamingClientModel.id == update_data["streaming_client_id"]
            ).first()
            if not streaming_client:
                return {"error": "Streaming client not found"}
        
        # Check if name is unique within the streaming client if provided
        if "name" in update_data and update_data["name"] is not None:
            streaming_client_id = update_data.get("streaming_client_id", url.streaming_client_id)
            existing_url = db.query(StreamingUrlModel).filter(
                StreamingUrlModel.streaming_client_id == streaming_client_id,
                StreamingUrlModel.name == update_data["name"],
                StreamingUrlModel.id != url_id
            ).first()
            if existing_url:
                return {"error": "Streaming URL name already exists for this streaming client"}
        
        # Update fields
        for key, value in update_data.items():
            setattr(url, key, value)
            
        db.commit()
        db.refresh(url)
        return url

    @staticmethod
    def delete_streaming_url(url_id: int, db: Session):
        url = db.query(StreamingUrlModel).filter(StreamingUrlModel.id == url_id).first()
        if not url:
            return None
        db.delete(url)
        db.commit()
        return url