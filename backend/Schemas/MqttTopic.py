from pydantic import BaseModel, Field
from typing import Optional, Dict
from .MqttClient import MqttClientResponseSchema
from datetime import datetime

class MqttTopicCreateSchema(BaseModel):
    mqtt_client_id: int = Field(..., description="The ID of the MQTT client")
    name: str = Field(..., description="The name of the MQTT topic")
    description: Optional[str] = Field(None, description="The description of the MQTT topic")
    config: Dict = Field(..., description="Configuration for the MQTT topic")
    status: bool = Field(..., description="The status of the MQTT topic")
    is_default: Optional[bool] = Field(False, description="Indicates if this is a default topic")

class MqttTopicUpdateSchema(BaseModel):
    mqtt_client_id: Optional[int] = Field(None, description="The ID of the MQTT client")
    name: Optional[str] = Field(None, description="The name of the MQTT topic")
    description: Optional[str] = Field(None, description="The description of the MQTT topic")
    config: Optional[Dict] = Field(None, description="Configuration for the MQTT topic")
    status: Optional[bool] = Field(None, description="The status of the MQTT topic")

class MqttTopicResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the MQTT topic")
    mqtt_client_id: int = Field(..., description="The ID of the MQTT client")
    name: str = Field(..., description="The name of the MQTT topic")
    description: Optional[str] = Field(None, description="The description of the MQTT topic")
    config: Dict = Field(..., description="Configuration for the MQTT topic")
    status: bool = Field(..., description="The status of the MQTT topic")
    is_default: bool = Field(False)
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(..., description="Updated timestamp")
    mqtt_client: MqttClientResponseSchema = Field(..., description="The MQTT client associated with the topic")
    class Config:
        orm_mode = True