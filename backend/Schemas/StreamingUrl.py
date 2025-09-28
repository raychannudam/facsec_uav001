from pydantic import BaseModel, Field
from typing import Optional, Dict
from .StreamingClient import StreamingClientResponseSchema

class StreamingUrlCreateSchema(BaseModel):
    streaming_client_id: int = Field(..., description="The ID of the streaming client")
    name: str = Field(..., description="The name of the streaming URL")
    description: Optional[str] = Field(None, description="The description of the streaming URL")
    config: Dict = Field(..., description="Configuration for the streaming URL")
    status: bool = Field(..., description="The status of the streaming URL")

class StreamingUrlUpdateSchema(BaseModel):
    streaming_client_id: Optional[int] = Field(None, description="The ID of the streaming client")
    name: Optional[str] = Field(None, description="The name of the streaming URL")
    description: Optional[str] = Field(None, description="The description of the streaming URL")
    config: Optional[Dict] = Field(None, description="Configuration for the streaming URL")
    status: Optional[bool] = Field(None, description="The status of the streaming URL")

class StreamingUrlResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the streaming URL")
    streaming_client_id: int = Field(..., description="The ID of the streaming client")
    name: str = Field(..., description="The name of the streaming URL")
    description: Optional[str] = Field(None, description="The description of the streaming URL")
    config: Dict = Field(..., description="Configuration for the streaming URL")
    status: bool = Field(..., description="The status of the streaming URL")
    created_at: str = Field(..., description="Created timestamp")
    updated_at: str = Field(..., description="Updated timestamp")
    streaming_client: StreamingClientResponseSchema = Field(..., description="The streaming client associated with the URL")