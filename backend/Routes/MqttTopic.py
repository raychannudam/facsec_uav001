from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import MqttTopicModel, MqttClientModel, get_db, UserModel
from Schemas.MqttTopic import MqttTopicCreateSchema, MqttTopicUpdateSchema, MqttTopicResponseSchema
from Schemas.MqttClient import MqttClientResponseSchema
from Schemas.User import UserResponseSchema
from Schemas.Role import RoleResponseSchema
from Services.MqttTopic import MqttTopicService
from Security.jwt import get_current_user
from Services.Controller import ControllerService
from Models.Controller import ControllerModel

router = APIRouter()

def is_admin(user: UserModel) -> bool:
    """Check if the user has an admin role."""
    return any(role.name.lower() == "admin" for role in user.roles)

# Create MQTT Topic
@router.post("/mqtt-topics", response_model=MqttTopicResponseSchema)
def create_mqtt_topic(
    mqtt_topic: MqttTopicCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if the MQTT client exists and belongs to the user (unless admin)
    mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == mqtt_topic.mqtt_client_id).first()
    if not mqtt_client:
        raise HTTPException(status_code=404, detail="MQTT Client not found")
    if not is_admin(current_user) and mqtt_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create topic for this MQTT client")

    new_mqtt_topic = MqttTopicService.create_mqtt_topic(mqtt_topic, db)
    if isinstance(new_mqtt_topic, dict) and "error" in new_mqtt_topic:
        raise HTTPException(status_code=400, detail=new_mqtt_topic["error"])
    
    return MqttTopicResponseSchema(
        id=new_mqtt_topic.id,
        mqtt_client_id=new_mqtt_topic.mqtt_client_id,
        name=new_mqtt_topic.name,
        description=new_mqtt_topic.description,
        config=new_mqtt_topic.config,
        status=new_mqtt_topic.status,
        created_at=str(new_mqtt_topic.created_at),
        updated_at=str(new_mqtt_topic.updated_at),
        mqtt_client=MqttClientResponseSchema(
            id=new_mqtt_topic.mqtt_client.id,
            user_id=new_mqtt_topic.mqtt_client.user_id,
            name=new_mqtt_topic.mqtt_client.name,
            description=new_mqtt_topic.mqtt_client.description,
            username=new_mqtt_topic.mqtt_client.username,
            password=new_mqtt_topic.mqtt_client.password,
            raw_password=result.mqtt_client.raw_password,
            config=new_mqtt_topic.mqtt_client.config,
            status=new_mqtt_topic.mqtt_client.status,
            created_at=str(new_mqtt_topic.mqtt_client.created_at),
            updated_at=str(new_mqtt_topic.mqtt_client.updated_at),
            user=UserResponseSchema(
                id=new_mqtt_topic.mqtt_client.user.id,
                email=new_mqtt_topic.mqtt_client.user.email,
                username=new_mqtt_topic.mqtt_client.user.username,
                fullname=new_mqtt_topic.mqtt_client.user.fullname,
                age=new_mqtt_topic.mqtt_client.user.age,
                gender=new_mqtt_topic.mqtt_client.user.gender,
                created_at=str(new_mqtt_topic.mqtt_client.user.created_at),
                updated_at=str(new_mqtt_topic.mqtt_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in new_mqtt_topic.mqtt_client.user.roles
                ]
            )
        )
    )

# Get all MQTT Topics
@router.get("/mqtt-topics", response_model=list[MqttTopicResponseSchema])
def get_mqtt_topics(
    mqtt_client_id: int = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Admins see all topics; regular users see only topics linked to their MQTT clients
    if is_admin(current_user):
        mqtt_topics = MqttTopicService.get_mqtt_topics(db=db)
    else:
        # mqtt_topics = MqttTopicService.get_mqtt_topics_by_user(current_user.id, db)
        mqtt_topics = MqttTopicService.get_mqtt_topics(db=db, mqtt_client_id=mqtt_client_id)
    return mqtt_topics

# Get MQTT Topic by ID
@router.get("/mqtt-topics/{mqtt_topic_id}", response_model=MqttTopicResponseSchema)
def get_mqtt_topic(
    mqtt_topic_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    mqtt_topic = MqttTopicService.get_mqtt_topic_by_id(mqtt_topic_id, db)
    if not mqtt_topic:
        raise HTTPException(status_code=404, detail="MQTT Topic not found")
    
    # Regular users can only access topics linked to their MQTT clients
    if not is_admin(current_user) and mqtt_topic.mqtt_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this MQTT topic")
    
    return mqtt_topic

# Update MQTT Topic
@router.put("/mqtt-topics/{mqtt_topic_id}", response_model=MqttTopicResponseSchema)
def update_mqtt_topic(
    mqtt_topic_id: int,
    mqtt_topic_update: MqttTopicUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    mqtt_topic = MqttTopicService.get_mqtt_topic_by_id(mqtt_topic_id, db)
    if not mqtt_topic:
        raise HTTPException(status_code=404, detail="MQTT Topic not found")
    
    # Regular users can only update topics linked to their MQTT clients
    if not is_admin(current_user) and mqtt_topic.mqtt_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this MQTT topic")
    
    mqtt_topic = MqttTopicService.update_mqtt_topic(mqtt_topic_id, mqtt_topic_update, db)
    if not mqtt_topic:
        raise HTTPException(status_code=404, detail="MQTT Topic not found")
    
    return mqtt_topic

# Delete MQTT Topic
@router.delete("/mqtt-topics/{mqtt_topic_id}", response_model=MqttTopicResponseSchema)
def delete_mqtt_topic(
    mqtt_topic_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    mqtt_topic = MqttTopicService.get_mqtt_topic_by_id(mqtt_topic_id, db)
    if not mqtt_topic:
        raise HTTPException(status_code=404, detail="MQTT Topic not found")
    
    # Regular users can only delete topics linked to their MQTT clients
    if not is_admin(current_user) and mqtt_topic.mqtt_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this MQTT topic")
    
    controllers: list[ControllerModel] = ControllerService.get_controllers(db=db, current_user=current_user)
    controller_config = controllers[0].config if len(controllers) > 0 else None
    if controller_config:
        if len(controller_config['mqttTopics']) > 0:
            found_topic = next(
                (
                    item for item in controller_config['mqttTopics']
                    if 'selectedTopic' in item and item['selectedTopic'] and item['selectedTopic'].get('id') == mqtt_topic_id
                ),
                None
            )
            if found_topic:
                raise HTTPException(status_code=403, detail="This MQTT Topic is existed in controller")
    
    # Build the response object BEFORE deleting
    response_data = mqtt_topic
    
    # Now delete the topic
    MqttTopicService.delete_mqtt_topic(mqtt_topic_id, db)
    
    return response_data