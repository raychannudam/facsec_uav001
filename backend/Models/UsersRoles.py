from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from Models import Base

class UserRoleModel(Base):
    __tablename__ = "users_roles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
