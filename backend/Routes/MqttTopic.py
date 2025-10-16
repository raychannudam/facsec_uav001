from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import MqttTopicModel, get_db
from Schemas.MqttTopic import MqttTopicCreateSchema, MqttTopicUpdateSchema, MqttTopicResponseSchema
from Schemas.MqttClient import MqttClientResponseSchema
from Schemas.User import UserResponseSchema
from Schemas.Role import RoleResponseSchema
from Services.MqttTopic import MqttTopicService
from Security.jwt import get_current_user
from Models import UserModel

router = APIRouter()

# Create MQTT Topic
@router.post("/mqtt-topics", response_model=MqttTopicResponseSchema)
def create_mqtt_topic(mqtt_topic: MqttTopicCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_mqtt_topic = MqttTopicService.create_mqtt_topic(mqtt_topic, db)
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
def get_mqtt_topics(mqtt_client_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    mqtt_topics = MqttTopicService.get_mqtt_topics(mqtt_client_id, db)
    return [
        MqttTopicResponseSchema(
            id=m.id,
            mqtt_client_id=m.mqtt_client_id,
            name=m.name,
            description=m.description,
            config=m.config,
            status=m.status,
            created_at=str(m.created_at),
            updated_at=str(m.updated_at),
            mqtt_client=MqttClientResponseSchema(
                id=m.mqtt_client.id,
                user_id=m.mqtt_client.user_id,
                name=m.mqtt_client.name,
                description=m.mqtt_client.description,
                username=m.mqtt_client.username,
                password=m.mqtt_client.password,
                config=m.mqtt_client.config,
                status=m.mqtt_client.status,
                created_at=str(m.mqtt_client.created_at),
                updated_at=str(m.mqtt_client.updated_at),
                user=UserResponseSchema(
                    id=m.mqtt_client.user.id,
                    email=m.mqtt_client.user.email,
                    username=m.mqtt_client.user.username,
                    fullname=m.mqtt_client.user.fullname,
                    age=m.mqtt_client.user.age,
                    gender=m.mqtt_client.user.gender,
                    created_at=str(m.mqtt_client.user.created_at),
                    updated_at=str(m.mqtt_client.user.updated_at),
                    roles=[
                        RoleResponseSchema(
                            id=role.id,
                            name=role.name,
                            description=role.description,
                            created_at=str(role.created_at),
                            updated_at=str(role.updated_at)
                        ) for role in m.mqtt_client.user.roles
                    ]
                )
            )
        ) for m in mqtt_topics
    ]

# Get MQTT Topic by ID
@router.get("/mqtt-topics/{mqtt_topic_id}", response_model=MqttTopicResponseSchema)
def get_mqtt_topic(mqtt_topic_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    mqtt_topic = MqttTopicService.get_mqtt_topic_by_id(mqtt_topic_id, db)
    if not mqtt_topic:
        raise HTTPException(status_code=404, detail="MQTT Topic not found")
    return MqttTopicResponseSchema(
        id=mqtt_topic.id,
        mqtt_client_id=mqtt_topic.mqtt_client_id,
        name=mqtt_topic.name,
        description=mqtt_topic.description,
        config=mqtt_topic.config,
        status=mqtt_topic.status,
        created_at=str(mqtt_topic.created_at),
        updated_at=str(mqtt_topic.updated_at),
        mqtt_client=MqttClientResponseSchema(
            id=mqtt_topic.mqtt_client.id,
            user_id=mqtt_topic.mqtt_client.user_id,
            name=mqtt_topic.mqtt_client.name,
            description=mqtt_topic.mqtt_client.description,
            username=mqtt_topic.mqtt_client.username,
            password=mqtt_topic.mqtt_client.password,
            config=mqtt_topic.mqtt_client.config,
            status=mqtt_topic.mqtt_client.status,
            created_at=str(mqtt_topic.mqtt_client.created_at),
            updated_at=str(mqtt_topic.mqtt_client.updated_at),
            user=UserResponseSchema(
                id=mqtt_topic.mqtt_client.user.id,
                email=mqtt_topic.mqtt_client.user.email,
                username=mqtt_topic.mqtt_client.user.username,
                fullname=mqtt_topic.mqtt_client.user.fullname,
                age=mqtt_topic.mqtt_client.user.age,
                gender=mqtt_topic.mqtt_client.user.gender,
                created_at=str(mqtt_topic.mqtt_client.user.created_at),
                updated_at=str(mqtt_topic.mqtt_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in mqtt_topic.mqtt_client.user.roles
                ]
            )
        )
    )

# Update MQTT Topic
@router.put("/mqtt-topics/{mqtt_topic_id}", response_model=MqttTopicResponseSchema)
def update_mqtt_topic(mqtt_topic_id: int, mqtt_topic_update: MqttTopicUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in mqtt_topic_update.dict(exclude_unset=True).items()}
    mqtt_topic = MqttTopicService.update_mqtt_topic(mqtt_topic_id, update_data, db)
    if not mqtt_topic:
        raise HTTPException(status_code=404, detail="MQTT Topic not found")
    return MqttTopicResponseSchema(
        id=mqtt_topic.id,
        mqtt_client_id=mqtt_topic.mqtt_client_id,
        name=mqtt_topic.name,
        description=mqtt_topic.description,
        config=mqtt_topic.config,
        status=mqtt_topic.status,
        created_at=str(mqtt_topic.created_at),
        updated_at=str(mqtt_topic.updated_at),
        mqtt_client=MqttClientResponseSchema(
            id=mqtt_topic.mqtt_client.id,
            user_id=mqtt_topic.mqtt_client.user_id,
            name=mqtt_topic.mqtt_client.name,
            description=mqtt_topic.mqtt_client.description,
            username=mqtt_topic.mqtt_client.username,
            password=mqtt_topic.mqtt_client.password,
            config=mqtt_topic.mqtt_client.config,
            status=mqtt_topic.mqtt_client.status,
            created_at=str(mqtt_topic.mqtt_client.created_at),
            updated_at=str(mqtt_topic.mqtt_client.updated_at),
            user=UserResponseSchema(
                id=mqtt_topic.mqtt_client.user.id,
                email=mqtt_topic.mqtt_client.user.email,
                username=mqtt_topic.mqtt_client.user.username,
                fullname=mqtt_topic.mqtt_client.user.fullname,
                age=mqtt_topic.mqtt_client.user.age,
                gender=mqtt_topic.mqtt_client.user.gender,
                created_at=str(mqtt_topic.mqtt_client.user.created_at),
                updated_at=str(mqtt_topic.mqtt_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in mqtt_topic.mqtt_client.user.roles
                ]
            )
        )
    )

# Delete MQTT Topic
@router.delete("/mqtt-topics/{mqtt_topic_id}", response_model=MqttTopicResponseSchema)
def delete_mqtt_topic(mqtt_topic_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    mqtt_topic = MqttTopicService.delete_mqtt_topic(mqtt_topic_id, db)
    if not mqtt_topic:
        raise HTTPException(status_code=404, detail="MQTT Topic not found")
    return MqttTopicResponseSchema(
        id=mqtt_topic.id,
        mqtt_client_id=mqtt_topic.mqtt_client_id,
        name=mqtt_topic.name,
        description=mqtt_topic.description,
        config=mqtt_topic.config,
        status=mqtt_topic.status,
        created_at=str(mqtt_topic.created_at),
        updated_at=str(mqtt_topic.updated_at),
        mqtt_client=MqttClientResponseSchema(
            id=mqtt_topic.mqtt_client.id,
            user_id=mqtt_topic.mqtt_client.user_id,
            name=mqtt_topic.mqtt_client.name,
            description=mqtt_topic.mqtt_client.description,
            username=mqtt_topic.mqtt_client.username,
            password=mqtt_topic.mqtt_client.password,
            config=mqtt_topic.mqtt_client.config,
            status=mqtt_topic.mqtt_client.status,
            created_at=str(mqtt_topic.mqtt_client.created_at),
            updated_at=str(mqtt_topic.mqtt_client.updated_at),
            user=UserResponseSchema(
                id=mqtt_topic.mqtt_client.user.id,
                email=mqtt_topic.mqtt_client.user.email,
                username=mqtt_topic.mqtt_client.user.username,
                fullname=mqtt_topic.mqtt_client.user.fullname,
                age=mqtt_topic.mqtt_client.user.age,
                gender=mqtt_topic.mqtt_client.user.gender,
                created_at=str(mqtt_topic.mqtt_client.user.created_at),
                updated_at=str(mqtt_topic.mqtt_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in mqtt_topic.mqtt_client.user.roles
                ]
            )
        )
    )