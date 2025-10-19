from pydantic import BaseModel, Field
from typing import Optional, Dict
from .User import UserResponseSchema
from datetime import datetime

class MqttClientCreateSchema(BaseModel):
    user_id: int = Field(..., description="The ID of the user owning the MQTT client")
    name: str = Field(..., description="The name of the MQTT client")
    description: Optional[str] = Field(None, description="The description of the MQTT client")
    username: str = Field(..., description="The username for the MQTT client")
    password: Optional[str] = Field(None, description="The password for the MQTT client")
    config: Dict = Field(..., description="Configuration for the MQTT client")
    status: bool = Field(..., description="The status of the MQTT client")

class MqttClientUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="The name of the MQTT client")
    description: Optional[str] = Field(None, description="The description of the MQTT client")
    config: Optional[Dict] = Field(None, description="Configuration for the MQTT client")
    status: Optional[bool] = Field(None, description="The status of the MQTT client")

class MqttClientResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the MQTT client")
    user_id: int = Field(..., description="The ID of the user owning the MQTT client")
    name: str = Field(..., description="The name of the MQTT client")
    description: Optional[str] = Field(None, description="The description of the MQTT client")
    username: str = Field(..., description="The username for the MQTT client")
    password: str = Field(..., description="The password for the MQTT client")
    raw_password: str = Field(..., description="The raw password for the MQTT client")
    config: Dict = Field(..., description="Configuration for the MQTT client")
    status: bool = Field(..., description="The status of the MQTT client")
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(..., description="Updated timestamp")
    user: UserResponseSchema = Field(..., description="The user owning the MQTT client")
    
    class Config:
        orm_mode = True

class MqttClientAllResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the MQTT client")
    user_id: int = Field(..., description="The ID of the user owning the MQTT client")
    name: str = Field(..., description="The name of the MQTT client")
    description: Optional[str] = Field(None, description="The description of the MQTT client")
    username: str = Field(..., description="The username for the MQTT client")
    config: Dict = Field(..., description="Configuration for the MQTT client")
    status: bool = Field(..., description="The status of the MQTT client")
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(..., description="Updated timestamp")
    user: UserResponseSchema = Field(..., description="The user owning the MQTT client")
    
    class Config:
        orm_mode = True
    
class MqttClientResetPasswordSchema(BaseModel):
    password: str = Field(..., description="The new password for the MQTT client")