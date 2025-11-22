import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from Models import Base

class ChatConversationModel(Base):
    __tablename__ = 'chat_conversations'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_id = Column(Integer, ForeignKey('chat_sessions.id'), nullable=True)
    name = Column(String(255), nullable=True, default="New Conversation")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    messages = relationship("ChatMessageModel", back_populates="conversation", cascade="all, delete-orphan")
    user = relationship("UserModel", back_populates="chat_conversations")
    session = relationship("ChatSessionModel", back_populates="conversations")


class ChatMessageModel(Base):
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    conversation_id = Column(Integer, ForeignKey('chat_conversations.id'))
    user_prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("ChatConversationModel", back_populates="messages")
    user = relationship("UserModel", back_populates="chat_messages")


class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="active")  # active, closed, expired

    user = relationship("UserModel", back_populates="chat_sessions")
    conversations = relationship("ChatConversationModel", back_populates="session", cascade="all, delete-orphan")
