from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import get_db, StreamingClientModel, UserModel
from Schemas.StreamingClient import StreamingClientCreateSchema, StreamingClientUpdateSchema, StreamingClientResponseSchema
from Schemas.User import UserResponseSchema
from Schemas.Role import RoleResponseSchema
from Services.StreamingClient import StreamingClientService
from Security.jwt import get_current_user

router = APIRouter()

def is_admin(user: UserModel) -> bool:
    """Check if the user has an admin role."""
    return any(role.name.lower() == "admin" for role in user.roles)

@router.post("/streaming-clients", response_model=StreamingClientResponseSchema)
def create_streaming_client(
    client: StreamingClientCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = StreamingClientService.create_streaming_client(client, db, current_user)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return StreamingClientResponseSchema(
        id=result.id,
        user_id=result.user_id,
        name=result.name,
        description=result.description,
        username=result.username,
        password=result.password,
        config=result.config,
        status=result.status,
        validation_code=result.validation_code,
        created_at=str(result.created_at),
        updated_at=str(result.updated_at),
        user=UserResponseSchema(
            id=result.user.id,
            email=result.user.email,
            username=result.user.username,
            fullname=result.user.fullname,
            age=result.user.age,
            gender=result.user.gender,
            created_at=str(result.user.created_at),
            updated_at=str(result.user.updated_at),
            roles=[
                RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in result.user.roles
            ]
        )
    )

@router.get("/streaming-clients", response_model=list[StreamingClientResponseSchema])
def get_streaming_clients(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Admins see all clients; regular users see only their own
    if is_admin(current_user):
        clients = StreamingClientService.get_streaming_clients(db)
    else:
        clients = StreamingClientService.get_streaming_clients_by_user(current_user.id, db)
    
    return [
        StreamingClientResponseSchema(
            id=client.id,
            user_id=client.user_id,
            name=client.name,
            description=client.description,
            username=client.username,
            password=client.password,
            config=client.config,
            status=client.status,
            validation_code=client.validation_code,
            created_at=str(client.created_at),
            updated_at=str(client.updated_at),
            user=UserResponseSchema(
                id=client.user.id,
                email=client.user.email,
                username=client.user.username,
                fullname=client.user.fullname,
                age=client.user.age,
                gender=client.user.gender,
                created_at=str(client.user.created_at),
                updated_at=str(client.user.updated_at),
                roles=[
                    RoleResponseSchema(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                        created_at=str(role.created_at),
                        updated_at=str(role.updated_at)
                    ) for role in client.user.roles
                ]
            )
        ) for client in clients
    ]

@router.get("/streaming-clients/{client_id}", response_model=StreamingClientResponseSchema)
def get_streaming_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    client = StreamingClientService.get_streaming_client_by_id(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    
    # Regular users can only access their own clients
    if not is_admin(current_user) and client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this streaming client")
    
    return StreamingClientResponseSchema(
        id=client.id,
        user_id=client.user_id,
        name=client.name,
        description=client.description,
        username=client.username,
        password=client.password,
        config=client.config,
        status=client.status,
        validation_code=client.validation_code,
        created_at=str(client.created_at),
        updated_at=str(client.updated_at),
        user=UserResponseSchema(
            id=client.user.id,
            email=client.user.email,
            username=client.user.username,
            fullname=client.user.fullname,
            age=client.user.age,
            gender=client.user.gender,
            created_at=str(client.user.created_at),
            updated_at=str(client.user.updated_at),
            roles=[
                RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in client.user.roles
            ]
        )
    )

@router.get("/streaming-clients/{client_id}/request-validation-code")
async def request_validation_code(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    client = StreamingClientService.get_streaming_client_by_id(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    
    # Regular users can only request validation codes for their own clients
    if not is_admin(current_user) and client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to request validation code for this streaming client")
    
    result = await StreamingClientService.request_validation_code(client_id, db)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to send validation code")
    return {"message": "Validation code sent to your email"}

@router.put("/streaming-clients/{client_id}/update-password")
def update_streaming_client_password(
    client_id: int,
    validation_code: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    client = StreamingClientService.get_streaming_client_by_id(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    
    # Regular users can only update passwords for their own clients
    if not is_admin(current_user) and client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update password for this streaming client")
    
    result = StreamingClientService.update_streaming_client_password(client_id, validation_code, new_password, db)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    if not result:
        raise HTTPException(status_code=400, detail="Invalid validation code")
    
    return StreamingClientResponseSchema(
        id=result.id,
        user_id=result.user_id,
        name=result.name,
        description=result.description,
        username=result.username,
        password=result.password,
        config=result.config,
        status=result.status,
        validation_code=result.validation_code,
        created_at=str(result.created_at),
        updated_at=str(result.updated_at),
        user=UserResponseSchema(
            id=result.user.id,
            email=result.user.email,
            username=result.user.username,
            fullname=result.user.fullname,
            age=result.user.age,
            gender=result.user.gender,
            created_at=str(result.user.created_at),
            updated_at=str(result.user.updated_at),
            roles=[
                RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in result.user.roles
            ]
        )
    )

@router.put("/streaming-clients/{client_id}", response_model=StreamingClientResponseSchema)
def update_streaming_client(
    client_id: int,
    client_update: StreamingClientUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    client = StreamingClientService.get_streaming_client_by_id(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    
    # Regular users can only update their own clients
    if not is_admin(current_user) and client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this streaming client")
    
    update_data = {k: v for k, v in client_update.dict(exclude_unset=True).items()}
    client = StreamingClientService.update_streaming_client(client_id, update_data, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    
    return StreamingClientResponseSchema(
        id=client.id,
        user_id=client.user_id,
        name=client.name,
        description=client.description,
        username=client.username,
        password=client.password,
        config=client.config,
        status=client.status,
        validation_code=client.validation_code,
        created_at=str(client.created_at),
        updated_at=str(client.updated_at),
        user=UserResponseSchema(
            id=client.user.id,
            email=client.user.email,
            username=client.user.username,
            fullname=client.user.fullname,
            age=client.user.age,
            gender=client.user.gender,
            created_at=str(client.user.created_at),
            updated_at=str(client.user.updated_at),
            roles=[
                RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in client.user.roles
            ]
        )
    )

@router.delete("/streaming-clients/{client_id}", response_model=StreamingClientResponseSchema)
def delete_streaming_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    client = StreamingClientService.get_streaming_client_by_id(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    
    # Regular users can only delete their own clients
    if not is_admin(current_user) and client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this streaming client")
    
    # Build response before deletion
    response = StreamingClientResponseSchema(
        id=client.id,
        user_id=client.user_id,
        name=client.name,
        description=client.description,
        username=client.username,
        password=client.password,
        config=client.config,
        status=client.status,
        validation_code=client.validation_code,
        created_at=str(client.created_at),
        updated_at=str(client.updated_at),
        user=UserResponseSchema(
            id=client.user.id,
            email=client.user.email,
            username=client.user.username,
            fullname=client.user.fullname,
            age=client.user.age,
            gender=client.user.gender,
            created_at=str(client.user.created_at),
            updated_at=str(client.user.updated_at),
            roles=[
                RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in client.user.roles
            ]
        )
    )
    
    # Now delete the client
    StreamingClientService.delete_streaming_client(client_id, db)
    return response