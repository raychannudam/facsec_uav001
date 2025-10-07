from pydantic import BaseModel, Field
from datetime import datetime

class RoleCreateSchema(BaseModel):
    name: str = Field(..., description="The name of the role")
    description: str = Field(..., description="The description of the role")

class RoleUpdateSchema(BaseModel):
    name: str | None = Field(None, description="The name of the role")
    description: str | None = Field(None, description="The description of the role")

class RoleResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the role")
    name: str = Field(..., description="The name of the role")
    description: str = Field(..., description="The description of the role")
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(..., description="Updated timestamp")
    class Config:
        orm_mode = True
