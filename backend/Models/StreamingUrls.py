from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from Models import Base

class StreamingUrlModel(Base):
    __tablename__ = "streaming_urls"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    streaming_client_id = Column(Integer, ForeignKey("streaming_clients.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    config = Column(JSON, nullable=False)
    status = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    streaming_client = relationship("StreamingClientModel", back_populates="streaming_urls")