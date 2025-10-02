from pydantic import BaseModel, Field
from typing import Optional, Dict
from .User import UserResponseSchema

class StreamingClientCreateSchema(BaseModel):
    name: str = Field(..., description="The name of the streaming client")
    description: Optional[str] = Field(None, description="The description of the streaming client")
    username: str = Field(..., description="The username for the streaming client")
    password: str = Field(..., description="The password for the streaming client")
    config: Dict = Field(..., description="Configuration for the streaming client")
    status: bool = Field(..., description="The status of the streaming client")

class StreamingClientUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="The name of the streaming client")
    description: Optional[str] = Field(None, description="The description of the streaming client")
    config: Optional[Dict] = Field(None, description="Configuration for the streaming client")
    status: Optional[bool] = Field(None, description="The status of the streaming client")

class StreamingClientResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the streaming client")
    user_id: int = Field(..., description="The ID of the user owning the streaming client")
    name: str = Field(..., description="The name of the streaming client")
    description: Optional[str] = Field(None, description="The description of the streaming client")
    username: str = Field(..., description="The username for the streaming client")
    password: str = Field(..., description="The password for the streaming client")
    config: Dict = Field(..., description="Configuration for the streaming client")
    status: bool = Field(..., description="The status of the streaming client")
    created_at: str = Field(..., description="Created timestamp")
    updated_at: str = Field(..., description="Updated timestamp")
    user: UserResponseSchema = Field(..., description="The user owning the streaming client")
    
class StreamingLoginSchema(BaseModel):
    user: Optional[str] = Field("", description="The username for the streaming client")
    password: Optional[str] = Field("", description="The password for the streaming client")
    token: Optional[str] = Field(None, description="token from mediamtx")
    ip: Optional[str] = Field(None, description="ip address of the client")
    action: Optional[str] = Field(None, description="action of the client, e.g., publish, read, playback") 
    path: Optional[str] = Field(None, description="path of the stream")
    protocol: Optional[str] = Field(None, description="protocol used, e.g., rtsp, rtmp")
    id: Optional[str] = Field(None, description="unique id for the session")
    query: Optional[str] = Field(None, description="additional query parameters")
    