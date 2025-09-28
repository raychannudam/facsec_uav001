from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import MqttClientModel, get_db
from Schemas.MqttClient import MqttClientCreateSchema, MqttClientUpdateSchema, MqttClientResponseSchema
from Schemas.User import UserResponseSchema
from Schemas.Role import RoleResponseSchema
from Services.MqttClient import MqttClientService
from Security.jwt import get_current_user
from Models import UserModel

router = APIRouter()

# Create MQTT Client
@router.post("/mqtt-clients", response_model=MqttClientResponseSchema)
def create_mqtt_client(mqtt_client: MqttClientCreateSchema, db: Session = Depends(get_db)):
    new_mqtt_client = MqttClientService.create_mqtt_client(mqtt_client, db)
    return MqttClientResponseSchema(
        id=new_mqtt_client.id,
        user_id=new_mqtt_client.user_id,
        name=new_mqtt_client.name,
        description=new_mqtt_client.description,
        username=new_mqtt_client.username,
        password=new_mqtt_client.password,
        config=new_mqtt_client.config,
        status=new_mqtt_client.status,
        created_at=str(new_mqtt_client.created_at),
        updated_at=str(new_mqtt_client.updated_at),
        user=UserResponseSchema(
            id=new_mqtt_client.user.id,
            email=new_mqtt_client.user.email,
            username=new_mqtt_client.user.username,
            fullname=new_mqtt_client.user.fullname,
            age=new_mqtt_client.user.age,
            gender=new_mqtt_client.user.gender,
            created_at=str(new_mqtt_client.user.created_at),
            updated_at=str(new_mqtt_client.user.updated_at),
            roles=[
                RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in new_mqtt_client.user.roles
            ]
        )
    )

# Get all MQTT Clients
@router.get("/mqtt-clients", response_model=list[MqttClientResponseSchema])
def get_mqtt_clients(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    mqtt_clients = MqttClientService.get_mqtt_clients(db)
    return [
        MqttClientResponseSchema(
            id=m.id,
            user_id=m.user_id,
            name=m.name,
            description=m.description,
            username=m.username,
            password=m.password,
            config=m.config,
            status=m.status,
            created_at=str(m.created_at),
            updated_at=str(m.updated_at),
            user=UserResponseSchema(
                id=m.user.id,
                email=m.user.email,
                username=m.user.username,
                fullname=m.user.fullname,
                age=m.user.age,
                gender=m.user.gender,
                created_at=str(m.user.created_at),
                updated_at=str(m.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in m.user.roles
                ]
            )
        ) for m in mqtt_clients
    ]

# Get MQTT Client by ID
@router.get("/mqtt-clients/{mqtt_client_id}", response_model=MqttClientResponseSchema)
def get_mqtt_client(mqtt_client_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    mqtt_client = MqttClientService.get_mqtt_client_by_id(mqtt_client_id, db)
    if not mqtt_client:
        raise HTTPException(status_code=404, detail="MQTT Client not found")
    return MqttClientResponseSchema(
        id=mqtt_client.id,
        user_id=mqtt_client.user_id,
        name=mqtt_client.name,
        description=mqtt_client.description,
        username=mqtt_client.username,
        password=mqtt_client.password,
        config=mqtt_client.config,
        status=mqtt_client.status,
        created_at=str(mqtt_client.created_at),
        updated_at=str(mqtt_client.updated_at),
        user=UserResponseSchema(
            id=mqtt_client.user.id,
            email=mqtt_client.user.email,
            username=mqtt_client.user.username,
            fullname=mqtt_client.user.fullname,
            age=mqtt_client.user.age,
            gender=mqtt_client.user.gender,
            created_at=str(mqtt_client.user.created_at),
            updated_at=str(mqtt_client.user.updated_at),
            roles=[
                RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in mqtt_client.user.roles
            ]
        )
    )

# Update MQTT Client
@router.put("/mqtt-clients/{mqtt_client_id}", response_model=MqttClientResponseSchema)
def update_mqtt_client(mqtt_client_id: int, mqtt_client_update: MqttClientUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in mqtt_client_update.dict(exclude_unset=True).items()}
    mqtt_client = MqttClientService.update_mqtt_client(mqtt_client_id, update_data, db)
    if not mqtt_client:
        raise HTTPException(status_code=404, detail="MQTT Client not found")
    return MqttClientResponseSchema(
        id=mqtt_client.id,
        user_id=mqtt_client.user_id,
        name=mqtt_client.name,
        description=mqtt_client.description,
        username=mqtt_client.username,
        password=mqtt_client.password,
        config=mqtt_client.config,
        status=mqtt_client.status,
        created_at=str(mqtt_client.created_at),
        updated_at=str(mqtt_client.updated_at),
        user=UserResponseSchema(
            id=mqtt_client.user.id,
            email=mqtt_client.user.email,
            username=mqtt_client.user.username,
            fullname=mqtt_client.user.fullname,
            age=mqtt_client.user.age,
            gender=mqtt_client.user.gender,
            created_at=str(mqtt_client.user.created_at),
            updated_at=str(mqtt_client.user.updated_at),
            roles=[
                RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in mqtt_client.user.roles
            ]
        )
    )

# Delete MQTT Client
@router.delete("/mqtt-clients/{mqtt_client_id}", response_model=MqttClientResponseSchema)
def delete_mqtt_client(mqtt_client_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    mqtt_client = MqttClientService.delete_mqtt_client(mqtt_client_id, db)
    if not mqtt_client:
        raise HTTPException(status_code=404, detail="MQTT Client not found")
    return MqttClientResponseSchema(
        id=mqtt_client.id,
        user_id=mqtt_client.user_id,
        name=mqtt_client.name,
        description=mqtt_client.description,
        username=mqtt_client.username,
        password=mqtt_client.password,
        config=mqtt_client.config,
        status=mqtt_client.status,
        created_at=str(mqtt_client.created_at),
        updated_at=str(mqtt_client.updated_at),
        user=UserResponseSchema(
            id=mqtt_client.user.id,
            email=mqtt_client.user.email,
            username=mqtt_client.user.username,
            fullname=mqtt_client.user.fullname,
            age=mqtt_client.user.age,
            gender=mqtt_client.user.gender,
            created_at=str(mqtt_client.user.created_at),
            updated_at=str(mqtt_client.user.updated_at),
            roles=[
                RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in mqtt_client.user.roles
            ]
        )
    )