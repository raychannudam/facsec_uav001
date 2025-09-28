from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from Models import Base

class MqttClientModel(Base):
    __tablename__ = "mqtt_clients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    config = Column(JSON, nullable=False)
    status = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", back_populates="mqtt_clients")
    mqtt_topics = relationship("MqttTopicModel", back_populates="mqtt_client", cascade="all, delete-orphan")
    uavs = relationship("UavModel", back_populates="mqtt_client", cascade="all, delete-orphan")