from sqlalchemy.orm import Session
from Models.Chat import ChatSessionModel, ChatMessageModel

class ChatService:

    @staticmethod
    def create_session(user_id: int, session_name: str, db: Session):
        session = ChatSessionModel(user_id=user_id, session_name=session_name)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_session(session_id: int, db: Session):
        return db.query(ChatSessionModel).filter(ChatSessionModel.id == session_id).first()

    @staticmethod
    def update_session(session_id: int, update_data: dict, db: Session):
        session = db.query(ChatSessionModel).filter(ChatSessionModel.id == session_id).first()
        if not session:
            return None
        for key, value in update_data.items():
            setattr(session, key, value)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def delete_session(session_id: int, db: Session):
        session = db.query(ChatSessionModel).filter(ChatSessionModel.id == session_id).first()
        if not session:
            return None
        db.delete(session)
        db.commit()
        return True

    @staticmethod
    def add_message(session_id: int, role: str, message: str, db: Session):
        msg = ChatMessageModel(session_id=session_id, role=role, message=message)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg

    @staticmethod
    def get_message(message_id: int, db: Session):
        return db.query(ChatMessageModel).filter(ChatMessageModel.id == message_id).first()

    @staticmethod
    def update_message(message_id: int, new_text: str, db: Session):
        msg = db.query(ChatMessageModel).filter(ChatMessageModel.id == message_id).first()
        if not msg:
            return None
        msg.message = new_text
        db.commit()
        db.refresh(msg)
        return msg

    @staticmethod
    def delete_message(message_id: int, db: Session):
        msg = db.query(ChatMessageModel).filter(ChatMessageModel.id == message_id).first()
        if not msg:
            return None
        db.delete(msg)
        db.commit()
        return True
