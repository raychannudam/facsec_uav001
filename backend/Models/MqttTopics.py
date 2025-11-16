from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from Models import Base

class MqttTopicModel(Base):
    __tablename__ = "mqtt_topics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mqtt_client_id = Column(Integer, ForeignKey("mqtt_clients.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    config = Column(JSON, nullable=False)
    status = Column(Boolean, nullable=False)

    # FIXED: default + server_default so DB and SQLAlchemy stay consistent
    is_default = Column(Boolean,nullable=True,default=False,server_default="false")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mqtt_client = relationship("MqttClientModel", back_populates="mqtt_topics")
