from pydantic import BaseModel, Field

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
    created_at: str = Field(..., description="Created timestamp")
    updated_at: str = Field(..., description="Updated timestamp")
