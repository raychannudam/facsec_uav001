from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class StationCreateSchema(BaseModel):
    name: str = Field(..., description="The unique name of the station")
    description: Optional[str] = Field(None, description="The description of the station")
    lat: float = Field(..., description="The latitude of the station")
    long: float = Field(..., description="The longitude of the station")

class StationUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="The unique name of the station")
    description: Optional[str] = Field(None, description="The description of the station")
    lat: Optional[float] = Field(None, description="The latitude of the station")
    long: Optional[float] = Field(None, description="The longitude of the station")

class StationResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the station")
    name: str = Field(..., description="The unique name of the station")
    description: Optional[str] = Field(None, description="The description of the station")
    lat: float = Field(..., description="The latitude of the station")
    long: float = Field(..., description="The longitude of the station")
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(..., description="Updated timestamp")
    class Config:
        orm_mode = True