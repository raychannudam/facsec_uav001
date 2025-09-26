from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Models import Base

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    fullname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    created_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    creator = relationship("UserModel", remote_side=[id], backref="created_users", lazy='joined')
    roles = relationship("RoleModel", secondary="users_roles", back_populates="users", lazy='dynamic')