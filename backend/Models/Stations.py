from datetime import datetime
from sqlalchemy import Column, Integer, Text, Float, DateTime, String
from sqlalchemy.orm import relationship
from Models import Base

class StationModel(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    uavs = relationship("UavModel", back_populates="station", cascade="all, delete-orphan")