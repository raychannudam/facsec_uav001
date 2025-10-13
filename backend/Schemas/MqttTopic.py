from pydantic import BaseModel, Field
from typing import Optional, Dict
from .MqttClient import MqttClientResponseSchema

class MqttTopicCreateSchema(BaseModel):
    mqtt_client_id: int = Field(..., description="The ID of the MQTT client")
    name: str = Field(..., description="The name of the MQTT topic")
    description: Optional[str] = Field(None, description="The description of the MQTT topic")
    config: Dict = Field(..., description="Configuration for the MQTT topic")
    status: bool = Field(..., description="The status of the MQTT topic")

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
    created_at: str = Field(..., description="Created timestamp")
    updated_at: str = Field(..., description="Updated timestamp")
    mqtt_client: MqttClientResponseSchema = Field(..., description="The MQTT client associated with the topic")