from pydantic import BaseModel, Field
from .Role import RoleResponseSchema
from typing import List, Optional

class UserCreateSchema(BaseModel):
    email: str = Field(..., description="The email of the user")
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password of the user")
    fullname: str = Field(..., description="The full name of the user")
    age: int = Field(..., description="The age of the user")
    gender: str = Field(..., description="The gender of the user")
    roles: List[str] = Field(default_factory=list, description="List of role names for the user")

class UserUpdateSchema(BaseModel):
    email: Optional[str] = Field(None, description="The email of the user")
    username: Optional[str] = Field(None, description="The username of the user")
    password: Optional[str] = Field(None, description="The password of the user")
    fullname: Optional[str] = Field(None, description="The full name of the user")
    age: Optional[int] = Field(None, description="The age of the user")
    gender: Optional[str] = Field(None, description="The gender of the user")
    roles: Optional[List[str]] = Field(None, description="List of role names for the user")

class UserResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the user")
    email: str = Field(..., description="The email of the user")
    username: str = Field(..., description="The username of the user")
    fullname: str = Field(..., description="The full name of the user")
    age: int = Field(..., description="The age of the user")
    gender: str = Field(..., description="The gender of the user")
    roles: List[RoleResponseSchema] = Field(..., description="List of roles assigned to the user")
    class Config:
        orm_mode = True