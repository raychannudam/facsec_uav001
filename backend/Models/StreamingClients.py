from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from Models import Base

class StreamingClientModel(Base):
    __tablename__ = "streaming_clients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    config = Column(JSON, nullable=False)
    status = Column(Boolean, nullable=False)
    validation_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", back_populates="streaming_clients")
    streaming_urls = relationship("StreamingUrlModel", back_populates="streaming_client", cascade="all, delete-orphan")
    uavs = relationship("UavModel", back_populates="streaming_client", cascade="all, delete-orphan")