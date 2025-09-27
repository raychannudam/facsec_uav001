from pydantic import BaseModel, Field
from typing import List, Optional
from Schemas.Role import RoleResponseSchema  # import Role schema

class UserCreateSchema(BaseModel):
    email: str = Field(..., description="The email of the user")
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password of the user")
    fullname: str = Field(..., description="The full name of the user")
    age: int = Field(..., description="The age of the user")
    gender: str = Field(..., description="The gender of the user")
    role_ids: Optional[List[int]] = Field([], description="List of role IDs assigned to the user")

class UserUpdateSchema(BaseModel):
    email: Optional[str] = Field(None, description="The email of the user")
    username: Optional[str] = Field(None, description="The username of the user")
    fullname: Optional[str] = Field(None, description="The full name of the user")
    age: Optional[int] = Field(None, description="The age of the user")
    gender: Optional[str] = Field(None, description="The gender of the user")
    role_ids: Optional[List[int]] = Field(None, description="List of role IDs assigned to the user")

class UserResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the user")
    email: str = Field(..., description="The email of the user")
    username: str = Field(..., description="The username of the user")
    fullname: str = Field(..., description="The full name of the user")
    age: int = Field(..., description="The age of the user")
    gender: str = Field(..., description="The gender of the user")
    roles: List[RoleResponseSchema] = Field([], description="List of roles assigned to the user")