from sqlalchemy.orm import Session
from fastapi import HTTPException
from Models.Chat import ChatMessageModel, ChatConversationModel, ChatSessionModel
from Schemas.Chat import ChatMessageCreateSchema, ChatConversationCreateSchema, ChatSessionCreateSchema

class ChatService:

    @staticmethod
    def create_chat_session(user_id: int, db: Session) -> ChatSessionModel:
        session = ChatSessionModel(user_id=user_id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_chat_session(session_id: int, db: Session) -> ChatSessionModel:
        return db.query(ChatSessionModel).filter(ChatSessionModel.id == session_id).first()

    @staticmethod
    def create_chat_conversation(session_id: int, user_id: int, name: str = "New Conversation", db: Session = None) -> ChatConversationModel:
        conversation = ChatConversationModel(session_id=session_id, user_id=user_id, name=name)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def get_chat_conversation(conversation_id: int, db: Session) -> ChatConversationModel:
        return db.query(ChatConversationModel).filter(ChatConversationModel.id == conversation_id).first()

    @staticmethod
    def create_chat_message(conversation_id: int, user_id: int, user_prompt: str, db: Session) -> ChatMessageModel:
        # Simple echo bot for now
        bot_response = f"Echo: {user_prompt}"
        message = ChatMessageModel(
            conversation_id=conversation_id, 
            user_id=user_id, 
            user_prompt=user_prompt, 
            response=bot_response
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
