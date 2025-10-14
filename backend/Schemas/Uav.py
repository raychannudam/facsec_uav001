from pydantic import BaseModel, Field
from typing import Optional, Dict
from .MqttClient import MqttClientResponseSchema
from .StreamingClient import StreamingClientResponseSchema
from .Station import StationResponseSchema

class UavCreateSchema(BaseModel):
    type: str = Field(..., description="The type of the UAV")
    name: str = Field(..., description="The unique name of the UAV")
    mqtt_client_id: Optional[int] = Field(None, description="The ID of the MQTT client")
    streaming_client_id: Optional[int] = Field(None, description="The ID of the streaming client")
    station_id: Optional[int] = Field(None, description="The ID of the station")
    last_lat: Optional[float] = Field(None, description="The last latitude of the UAV")
    last_long: Optional[float] = Field(None, description="The last longitude of the UAV")
    operation_data: Dict = Field(..., description="Operational data for the UAV")

class UavUpdateSchema(BaseModel):
    type: Optional[str] = Field(None, description="The type of the UAV")
    name: Optional[str] = Field(None, description="The unique name of the UAV")
    mqtt_client_id: Optional[int] = Field(None, description="The ID of the MQTT client")
    streaming_client_id: Optional[int] = Field(None, description="The ID of the streaming client")
    station_id: Optional[int] = Field(None, description="The ID of the station")
    last_lat: Optional[float] = Field(None, description="The last latitude of the UAV")
    last_long: Optional[float] = Field(None, description="The last longitude of the UAV")
    operation_data: Optional[Dict] = Field(None, description="Operational data for the UAV")

class UavResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the UAV")
    type: str = Field(..., description="The type of the UAV")
    name: str = Field(..., description="The unique name of the UAV")
    mqtt_client_id: Optional[int] = Field(None, description="The ID of the MQTT client")
    streaming_client_id: Optional[int] = Field(None, description="The ID of the streaming client")
    station_id: Optional[int] = Field(None, description="The ID of the station")
    last_lat: Optional[float] = Field(None, description="The last latitude of the UAV")
    last_long: Optional[float] = Field(None, description="The last longitude of the UAV")
    operation_data: Dict = Field(..., description="Operational data for the UAV")
    created_at: str = Field(..., description="Created timestamp")
    updated_at: str = Field(..., description="Updated timestamp")
    # mqtt_client: Optional[MqttClientResponseSchema] = Field(None, description="The MQTT client associated with the UAV")
    # streaming_client: Optional[StreamingClientResponseSchema] = Field(None, description="The streaming client associated with the UAV")
    # station: Optional[StationResponseSchema] = Field(None, description="The station associated with the UAV")
    class Config:
        orm_mode = True