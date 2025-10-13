from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime, String
from sqlalchemy.orm import relationship
from Models import Base

class UavModel(Base):
    __tablename__ = "uavs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=False, index=True)
    mqtt_client_id = Column(Integer, ForeignKey("mqtt_clients.id", ondelete="CASCADE"), nullable=True)
    streaming_client_id = Column(Integer, ForeignKey("streaming_clients.id", ondelete="CASCADE"), nullable=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=True)
    last_lat = Column(Float)
    last_long = Column(Float)
    operation_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mqtt_client = relationship("MqttClientModel", back_populates="uavs")
    streaming_client = relationship("StreamingClientModel", back_populates="uavs")
    station = relationship("StationModel", back_populates="uavs")