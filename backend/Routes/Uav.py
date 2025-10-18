from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import get_db, UavModel, UserModel, MqttClientModel, StreamingClientModel, StationModel
from Schemas.Uav import UavCreateSchema, UavUpdateSchema, UavResponseSchema
from Schemas.MqttClient import MqttClientResponseSchema
from Schemas.StreamingClient import StreamingClientResponseSchema
from Schemas.Station import StationResponseSchema
from Schemas.User import UserResponseSchema
from Schemas.Role import RoleResponseSchema
from Services.Uav import UavService
from Security.jwt import get_current_user

router = APIRouter()

def is_admin(user: UserModel) -> bool:
    """Check if the user has an admin role."""
    return any(role.name.lower() == "admin" for role in user.roles)

@router.post("/uavs", response_model=UavResponseSchema)
def create_uav(
    uav: UavCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Validate ownership of mqtt_client_id, streaming_client_id, and station_id (if provided)
    if uav.mqtt_client_id is not None:
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == uav.mqtt_client_id).first()
        if not mqtt_client:
            raise HTTPException(status_code=404, detail="MQTT client not found")
        if not is_admin(current_user) and mqtt_client.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to use this MQTT client")
    
    if uav.streaming_client_id is not None:
        streaming_client = db.query(StreamingClientModel).filter(StreamingClientModel.id == uav.streaming_client_id).first()
        if not streaming_client:
            raise HTTPException(status_code=404, detail="Streaming client not found")
        if not is_admin(current_user) and streaming_client.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to use this streaming client")
    
    if uav.station_id is not None:
        station = db.query(StationModel).filter(StationModel.id == uav.station_id).first()
        if not station:
            raise HTTPException(status_code=404, detail="Station not found")
        # Assuming StationModel has a user_id field; adjust if it doesn't
        if hasattr(station, 'user_id') and not is_admin(current_user) and station.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to use this station")
    
    result = UavService.create_uav(uav, db)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    mqtt_client_response = None
    if result.mqtt_client:
        mqtt_client_response = MqttClientResponseSchema(
            id=result.mqtt_client.id,
            user_id=result.mqtt_client.user_id,
            name=result.mqtt_client.name,
            description=result.mqtt_client.description,
            username=result.mqtt_client.username,
            password=result.mqtt_client.password,
            config=result.mqtt_client.config,
            status=result.mqtt_client.status,
            created_at=str(result.mqtt_client.created_at),
            updated_at=str(result.mqtt_client.updated_at),
            user=UserResponseSchema(
                id=result.mqtt_client.user.id,
                email=result.mqtt_client.user.email,
                username=result.mqtt_client.user.username,
                fullname=result.mqtt_client.user.fullname,
                age=result.mqtt_client.user.age,
                gender=result.mqtt_client.user.gender,
                created_at=str(result.mqtt_client.user.created_at),
                updated_at=str(result.mqtt_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in result.mqtt_client.user.roles
                ]
            )
        )
    
    streaming_client_response = None
    if result.streaming_client:
        streaming_client_response = StreamingClientResponseSchema(
            id=result.streaming_client.id,
            user_id=result.streaming_client.user_id,
            name=result.streaming_client.name,
            description=result.streaming_client.description,
            username=result.streaming_client.username,
            password=result.streaming_client.password,
            config=result.streaming_client.config,
            status=result.streaming_client.status,
            validation_code=result.streaming_client.validation_code,
            created_at=str(result.streaming_client.created_at),
            updated_at=str(result.streaming_client.updated_at),
            user=UserResponseSchema(
                id=result.streaming_client.user.id,
                email=result.streaming_client.user.email,
                username=result.streaming_client.user.username,
                fullname=result.streaming_client.user.fullname,
                age=result.streaming_client.user.age,
                gender=result.streaming_client.user.gender,
                created_at=str(result.streaming_client.user.created_at),
                updated_at=str(result.streaming_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in result.streaming_client.user.roles
                ]
            )
        )
    
    station_response = None
    if result.station:
        station_response = StationResponseSchema(
            id=result.station.id,
            name=result.station.name,
            description=result.station.description,
            created_at=str(result.station.created_at),
            updated_at=str(result.station.updated_at),
            # Include lat and long only if they exist in StationModel
            lat=result.station.lat if hasattr(result.station, 'lat') else None,
            long=result.station.long if hasattr(result.station, 'long') else None
        )
    
    return UavResponseSchema(
        id=result.id,
        type=result.type,
        name=result.name,
        mqtt_client_id=result.mqtt_client_id,
        streaming_client_id=result.streaming_client_id,
        station_id=result.station_id,
        last_lat=result.last_lat,
        last_long=result.last_long,
        operation_data=result.operation_data,
        created_at=str(result.created_at),
        updated_at=str(result.updated_at),
        mqtt_client=mqtt_client_response,
        streaming_client=streaming_client_response,
        station=station_response
    )

@router.get("/uavs", response_model=list[UavResponseSchema])
def get_uavs(
    query: str = "",
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Admins see all UAVs; regular users see only UAVs linked to their streaming clients
    if is_admin(current_user):
        uavs = UavService.get_uavs(db, query)
    else:
        uavs = UavService.get_uavs_by_user(current_user.id, db, query)
    
    return [
        UavResponseSchema(
            id=u.id,
            type=u.type,
            name=u.name,
            mqtt_client_id=u.mqtt_client_id,
            streaming_client_id=u.streaming_client_id,
            station_id=u.station_id,
            last_lat=u.last_lat,
            last_long=u.last_long,
            operation_data=u.operation_data,
            created_at=str(u.created_at),
            updated_at=str(u.updated_at),
            mqtt_client=MqttClientResponseSchema(
                id=u.mqtt_client.id,
                user_id=u.mqtt_client.user_id,
                name=u.mqtt_client.name,
                description=u.mqtt_client.description,
                username=u.mqtt_client.username,
                password=u.mqtt_client.password,
                config=u.mqtt_client.config,
                status=u.mqtt_client.status,
                created_at=str(u.mqtt_client.created_at),
                updated_at=str(u.mqtt_client.updated_at),
                user=UserResponseSchema(
                    id=u.mqtt_client.user.id,
                    email=u.mqtt_client.user.email,
                    username=u.mqtt_client.user.username,
                    fullname=u.mqtt_client.user.fullname,
                    age=u.mqtt_client.user.age,
                    gender=u.mqtt_client.user.gender,
                    created_at=str(u.mqtt_client.user.created_at),
                    updated_at=str(u.mqtt_client.user.updated_at),
                    roles=[
                        RoleResponseSchema(
                            id=role.id,
                            name=role.name,
                            description=role.description,
                            created_at=str(role.created_at),
                            updated_at=str(role.updated_at)
                        ) for role in u.mqtt_client.user.roles
                    ]
                )
            ) if u.mqtt_client else None,
            streaming_client=StreamingClientResponseSchema(
                id=u.streaming_client.id,
                user_id=u.streaming_client.user_id,
                name=u.streaming_client.name,
                description=u.streaming_client.description,
                username=u.streaming_client.username,
                password=u.streaming_client.password,
                config=u.streaming_client.config,
                status=u.streaming_client.status,
                validation_code=u.streaming_client.validation_code,
                created_at=str(u.streaming_client.created_at),
                updated_at=str(u.streaming_client.updated_at),
                user=UserResponseSchema(
                    id=u.streaming_client.user.id,
                    email=u.streaming_client.user.email,
                    username=u.streaming_client.user.username,
                    fullname=u.streaming_client.user.fullname,
                    age=u.streaming_client.user.age,
                    gender=u.streaming_client.user.gender,
                    created_at=str(u.streaming_client.user.created_at),
                    updated_at=str(u.streaming_client.user.updated_at),
                    roles=[
                        RoleResponseSchema(
                            id=role.id,
                            name=role.name,
                            description=role.description,
                            created_at=str(role.created_at),
                            updated_at=str(role.updated_at)
                        ) for role in u.streaming_client.user.roles
                    ]
                )
            ) if u.streaming_client else None,
            station=StationResponseSchema(
                id=u.station.id,
                name=u.station.name,
                description=u.station.description,
                created_at=str(u.station.created_at),
                updated_at=str(u.station.updated_at),
                lat=u.station.lat if hasattr(u.station, 'lat') else None,
                long=u.station.long if hasattr(u.station, 'long') else None
            ) if u.station else None
        ) for u in uavs
    ]

@router.get("/uavs/{uav_id}", response_model=UavResponseSchema)
def get_uav(
    uav_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    uav = UavService.get_uav_by_id(uav_id, db)
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    # Regular users can only access UAVs linked to their streaming clients
    if not is_admin(current_user):
        if not uav.streaming_client:
            raise HTTPException(status_code=403, detail="Not authorized to access this UAV (no streaming client assigned)")
        if uav.streaming_client.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to access this UAV")
    
    mqtt_client_response = None
    if uav.mqtt_client:
        mqtt_client_response = MqttClientResponseSchema(
            id=uav.mqtt_client.id,
            user_id=uav.mqtt_client.user_id,
            name=uav.mqtt_client.name,
            description=uav.mqtt_client.description,
            username=uav.mqtt_client.username,
            password=uav.mqtt_client.password,
            config=uav.mqtt_client.config,
            status=uav.mqtt_client.status,
            created_at=str(uav.mqtt_client.created_at),
            updated_at=str(uav.mqtt_client.updated_at),
            user=UserResponseSchema(
                id=uav.mqtt_client.user.id,
                email=uav.mqtt_client.user.email,
                username=uav.mqtt_client.user.username,
                fullname=uav.mqtt_client.user.fullname,
                age=uav.mqtt_client.user.age,
                gender=uav.mqtt_client.user.gender,
                created_at=str(uav.mqtt_client.user.created_at),
                updated_at=str(uav.mqtt_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in uav.mqtt_client.user.roles
                ]
            )
        )
    
    streaming_client_response = None
    if uav.streaming_client:
        streaming_client_response = StreamingClientResponseSchema(
            id=uav.streaming_client.id,
            user_id=uav.streaming_client.user_id,
            name=uav.streaming_client.name,
            description=uav.streaming_client.description,
            username=uav.streaming_client.username,
            password=uav.streaming_client.password,
            config=uav.streaming_client.config,
            status=uav.streaming_client.status,
            validation_code=uav.streaming_client.validation_code,
            created_at=str(uav.streaming_client.created_at),
            updated_at=str(uav.streaming_client.updated_at),
            user=UserResponseSchema(
                id=uav.streaming_client.user.id,
                email=uav.streaming_client.user.email,
                username=uav.streaming_client.user.username,
                fullname=uav.streaming_client.user.fullname,
                age=uav.streaming_client.user.age,
                gender=uav.streaming_client.user.gender,
                created_at=str(uav.streaming_client.user.created_at),
                updated_at=str(uav.streaming_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in uav.streaming_client.user.roles
                ]
            )
        )
    
    station_response = None
    if uav.station:
        station_response = StationResponseSchema(
            id=uav.station.id,
            name=uav.station.name,
            description=uav.station.description,
            created_at=str(uav.station.created_at),
            updated_at=str(uav.station.updated_at),
            lat=uav.station.lat if hasattr(uav.station, 'lat') else None,
            long=uav.station.long if hasattr(uav.station, 'long') else None
        )
    
    return UavResponseSchema(
        id=uav.id,
        type=uav.type,
        name=uav.name,
        mqtt_client_id=uav.mqtt_client_id,
        streaming_client_id=uav.streaming_client_id,
        station_id=uav.station_id,
        last_lat=uav.last_lat,
        last_long=uav.last_long,
        operation_data=uav.operation_data,
        created_at=str(uav.created_at),
        updated_at=str(uav.updated_at),
        mqtt_client=mqtt_client_response,
        streaming_client=streaming_client_response,
        station=station_response
    )

@router.put("/uavs/{uav_id}", response_model=UavResponseSchema)
def update_uav(
    uav_id: int,
    uav_update: UavUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    uav = UavService.get_uav_by_id(uav_id, db)
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    # Regular users can only update UAVs linked to their streaming clients
    if not is_admin(current_user):
        if not uav.streaming_client:
            raise HTTPException(status_code=403, detail="Not authorized to update this UAV (no streaming client assigned)")
        if uav.streaming_client.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this UAV")
    
    # Validate ownership of mqtt_client_id, streaming_client_id, and station_id (if provided)
    update_data = {k: v for k, v in uav_update.dict(exclude_unset=True).items()}
    if "mqtt_client_id" in update_data and update_data["mqtt_client_id"] is not None:
        mqtt_client = db.query(MqttClientModel).filter(MqttClientModel.id == update_data["mqtt_client_id"]).first()
        if not mqtt_client:
            raise HTTPException(status_code=404, detail="MQTT client not found")
        if not is_admin(current_user) and mqtt_client.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to use this MQTT client")
    
    if "streaming_client_id" in update_data and update_data["streaming_client_id"] is not None:
        streaming_client = db.query(StreamingClientModel).filter(StreamingClientModel.id == update_data["streaming_client_id"]).first()
        if not streaming_client:
            raise HTTPException(status_code=404, detail="Streaming client not found")
        if not is_admin(current_user) and streaming_client.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to use this streaming client")
    
    if "station_id" in update_data and update_data["station_id"] is not None:
        station = db.query(StationModel).filter(StationModel.id == update_data["station_id"]).first()
        if not station:
            raise HTTPException(status_code=404, detail="Station not found")
        # Assuming StationModel has a user_id field; adjust if it doesn't
        if hasattr(station, 'user_id') and not is_admin(current_user) and station.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to use this station")
    
    uav = UavService.update_uav(uav_id, update_data, db)
    if isinstance(uav, dict) and "error" in uav:
        raise HTTPException(status_code=400, detail=uav["error"])
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    mqtt_client_response = None
    if uav.mqtt_client:
        mqtt_client_response = MqttClientResponseSchema(
            id=uav.mqtt_client.id,
            user_id=uav.mqtt_client.user_id,
            name=uav.mqtt_client.name,
            description=uav.mqtt_client.description,
            username=uav.mqtt_client.username,
            password=uav.mqtt_client.password,
            config=uav.mqtt_client.config,
            status=uav.mqtt_client.status,
            created_at=str(uav.mqtt_client.created_at),
            updated_at=str(uav.mqtt_client.updated_at),
            user=UserResponseSchema(
                id=uav.mqtt_client.user.id,
                email=uav.mqtt_client.user.email,
                username=uav.mqtt_client.user.username,
                fullname=uav.mqtt_client.user.fullname,
                age=uav.mqtt_client.user.age,
                gender=uav.mqtt_client.user.gender,
                created_at=str(uav.mqtt_client.user.created_at),
                updated_at=str(uav.mqtt_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in uav.mqtt_client.user.roles
                ]
            )
        )
    
    streaming_client_response = None
    if uav.streaming_client:
        streaming_client_response = StreamingClientResponseSchema(
            id=uav.streaming_client.id,
            user_id=uav.streaming_client.user_id,
            name=uav.streaming_client.name,
            description=uav.streaming_client.description,
            username=uav.streaming_client.username,
            password=uav.streaming_client.password,
            config=uav.streaming_client.config,
            status=uav.streaming_client.status,
            validation_code=uav.streaming_client.validation_code,
            created_at=str(uav.streaming_client.created_at),
            updated_at=str(uav.streaming_client.updated_at),
            user=UserResponseSchema(
                id=uav.streaming_client.user.id,
                email=uav.streaming_client.user.email,
                username=uav.streaming_client.user.username,
                fullname=uav.streaming_client.user.fullname,
                age=uav.streaming_client.user.age,
                gender=uav.streaming_client.user.gender,
                created_at=str(uav.streaming_client.user.created_at),
                updated_at=str(uav.streaming_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in uav.streaming_client.user.roles
                ]
            )
        )
    
    station_response = None
    if uav.station:
        station_response = StationResponseSchema(
            id=uav.station.id,
            name=uav.station.name,
            description=uav.station.description,
            created_at=str(uav.station.created_at),
            updated_at=str(uav.station.updated_at),
            lat=uav.station.lat if hasattr(uav.station, 'lat') else None,
            long=uav.station.long if hasattr(uav.station, 'long') else None
        )
    
    return UavResponseSchema(
        id=uav.id,
        type=uav.type,
        name=uav.name,
        mqtt_client_id=uav.mqtt_client_id,
        streaming_client_id=uav.streaming_client_id,
        station_id=uav.station_id,
        last_lat=uav.last_lat,
        last_long=uav.last_long,
        operation_data=uav.operation_data,
        created_at=str(uav.created_at),
        updated_at=str(uav.updated_at),
        mqtt_client=mqtt_client_response,
        streaming_client=streaming_client_response,
        station=station_response
    )

@router.delete("/uavs/{uav_id}", response_model=UavResponseSchema)
def delete_uav(
    uav_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    uav = UavService.get_uav_by_id(uav_id, db)
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
    
    # Regular users can only delete UAVs linked to their streaming clients
    if not is_admin(current_user):
        if not uav.streaming_client:
            raise HTTPException(status_code=403, detail="Not authorized to delete this UAV (no streaming client assigned)")
        if uav.streaming_client.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this UAV")
    
    # Build response before deletion
    mqtt_client_response = None
    if uav.mqtt_client:
        mqtt_client_response = MqttClientResponseSchema(
            id=uav.mqtt_client.id,
            user_id=uav.mqtt_client.user_id,
            name=uav.mqtt_client.name,
            description=uav.mqtt_client.description,
            username=uav.mqtt_client.username,
            password=uav.mqtt_client.password,
            config=uav.mqtt_client.config,
            status=uav.mqtt_client.status,
            created_at=str(uav.mqtt_client.created_at),
            updated_at=str(uav.mqtt_client.updated_at),
            user=UserResponseSchema(
                id=uav.mqtt_client.user.id,
                email=uav.mqtt_client.user.email,
                username=uav.mqtt_client.user.username,
                fullname=uav.mqtt_client.user.fullname,
                age=uav.mqtt_client.user.age,
                gender=uav.mqtt_client.user.gender,
                created_at=str(uav.mqtt_client.user.created_at),
                updated_at=str(uav.mqtt_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in uav.mqtt_client.user.roles
                ]
            )
        )
    
    streaming_client_response = None
    if uav.streaming_client:
        streaming_client_response = StreamingClientResponseSchema(
            id=uav.streaming_client.id,
            user_id=uav.streaming_client.user_id,
            name=uav.streaming_client.name,
            description=uav.streaming_client.description,
            username=uav.streaming_client.username,
            password=uav.streaming_client.password,
            config=uav.streaming_client.config,
            status=uav.streaming_client.status,
            validation_code=uav.streaming_client.validation_code,
            created_at=str(uav.streaming_client.created_at),
            updated_at=str(uav.streaming_client.updated_at),
            user=UserResponseSchema(
                id=uav.streaming_client.user.id,
                email=uav.streaming_client.user.email,
                username=uav.streaming_client.user.username,
                fullname=uav.streaming_client.user.fullname,
                age=uav.streaming_client.user.age,
                gender=uav.streaming_client.user.gender,
                created_at=str(uav.streaming_client.user.created_at),
                updated_at=str(uav.streaming_client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in uav.streaming_client.user.roles
                ]
            )
        )
    
    station_response = None
    if uav.station:
        station_response = StationResponseSchema(
            id=uav.station.id,
            name=uav.station.name,
            description=uav.station.description,
            created_at=str(uav.station.created_at),
            updated_at=str(uav.station.updated_at),
            lat=uav.station.lat if hasattr(uav.station, 'lat') else None,
            long=uav.station.long if hasattr(uav.station, 'long') else None
        )
    
    response = UavResponseSchema(
        id=uav.id,
        type=uav.type,
        name=uav.name,
        mqtt_client_id=uav.mqtt_client_id,
        streaming_client_id=uav.streaming_client_id,
        station_id=uav.station_id,
        last_lat=uav.last_lat,
        last_long=uav.last_long,
        operation_data=uav.operation_data,
        created_at=str(uav.created_at),
        updated_at=str(uav.updated_at),
        mqtt_client=mqtt_client_response,
        streaming_client=streaming_client_response,
        station=station_response
    )
    
    # Now delete the UAV
    UavService.delete_uav(uav_id, db)
    return response