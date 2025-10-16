from pydantic import BaseModel, Field
from datetime import datetime
from Schemas.User import UserResponseSchema
from typing import Optional

class ControllerResponseSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    description: str = Field(...)
    config: dict = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    user: UserResponseSchema = Field(...)
    
class ControllerCreateSchema(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field(None)
    config: dict = Field(...)
    
class ControllerUpdateSchema(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    config: Optional[str] = Field(None)
    