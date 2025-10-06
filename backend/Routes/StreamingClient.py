from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import get_db, StreamingClientModel
from Schemas.StreamingClient import StreamingClientCreateSchema, StreamingClientUpdateSchema, StreamingClientResponseSchema
from Services.StreamingClient import StreamingClientService
from Security.jwt import get_current_user
from Models import UserModel
from Schemas.Role import RoleResponseSchema
from Schemas import UserResponseSchema

router = APIRouter()

@router.post("/streaming-clients", response_model=StreamingClientResponseSchema)
def create_streaming_client(client: StreamingClientCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result = StreamingClientService.create_streaming_client(client, db, current_user)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    user = result.user
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    
    return StreamingClientResponseSchema(
        id=result.id,
        user_id=result.user_id,
        name=result.name,
        description=result.description,
        username=result.username,
        password=result.password,
        config=result.config,
        status=result.status,
        created_at=str(result.created_at),
        updated_at=str(result.updated_at),
        user=UserResponseSchema(
            id=user.id,
            email=user.email,
            username=user.username,
            fullname=user.fullname,
            age=user.age,
            gender=user.gender,
            roles=roles
        )
    )

@router.get("/streaming-clients", response_model=list[StreamingClientResponseSchema])
def get_streaming_clients(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    clients = StreamingClientService.get_streaming_clients(db)
    return [StreamingClientResponseSchema(
        id=c.id,
        user_id=c.user_id,
        name=c.name,
        description=c.description,
        username=c.username,
        password=c.password,
        config=c.config,
        status=c.status,
        created_at=str(c.created_at),
        updated_at=str(c.updated_at),
        user=UserResponseSchema(
            id=c.user.id,
            email=c.user.email,
            username=c.user.username,
            fullname=c.user.fullname,
            age=c.user.age,
            gender=c.user.gender,
            roles=[RoleResponseSchema(
                id=role.id,
                name=role.name,
                description=role.description,
                created_at=str(role.created_at),
                updated_at=str(role.updated_at)
            ) for role in c.user.roles]
        )
    ) for c in clients]

@router.get("/streaming-clients/{client_id}", response_model=StreamingClientResponseSchema)
def get_streaming_client(client_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    client = StreamingClientService.get_streaming_client_by_id(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    
    user = client.user
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    
    return StreamingClientResponseSchema(
        id=client.id,
        user_id=client.user_id,
        name=client.name,
        description=client.description,
        username=client.username,
        password=client.password,
        config=client.config,
        status=client.status,
        created_at=str(client.created_at),
        updated_at=str(client.updated_at),
        user=UserResponseSchema(
            id=user.id,
            email=user.email,
            username=user.username,
            fullname=user.fullname,
            age=user.age,
            gender=user.gender,
            roles=roles
        )
    )

@router.get("/streaming-clients/{client_id}/request-validation-code")
async def request_validation_code(client_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result = await StreamingClientService.request_validation_code(client_id, db)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to send validation code")
    return {"message": "Validation code sent to your email"}

@router.put("/streaming-clients/{client_id}/update-password")
def update_streaming_client_password(client_id: int, validation_code: str, new_password: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result = StreamingClientService.update_streaming_client_password(client_id, validation_code, new_password, db)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    if not result:
        raise HTTPException(status_code=404, detail="Streaming client not found or invalid validation code")
    
    user = result.user
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    
    return StreamingClientResponseSchema(
        id=result.id,
        user_id=result.user_id,
        name=result.name,
        description=result.description,
        username=result.username,
        password=result.password,
        config=result.config,
        status=result.status,
        created_at=str(result.created_at),
        updated_at=str(result.updated_at),
        user=UserResponseSchema(
            id=user.id,
            email=user.email,
            username=user.username,
            fullname=user.fullname,
            age=user.age,
            gender=user.gender,
            roles=roles
        )
    )

@router.put("/streaming-clients/{client_id}", response_model=StreamingClientResponseSchema)
def update_streaming_client(client_id: int, client_update: StreamingClientUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in client_update.dict().items() if v is not None}
    client = StreamingClientService.update_streaming_client(client_id, update_data, db)
    if isinstance(client, dict) and "error" in client:
        raise HTTPException(status_code=400, detail=client["error"])
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    
    user = client.user
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    
    return StreamingClientResponseSchema(
        id=client.id,
        user_id=client.user_id,
        name=client.name,
        description=client.description,
        username=client.username,
        password=client.password,
        config=client.config,
        status=client.status,
        created_at=str(client.created_at),
        updated_at=str(client.updated_at),
        user=UserResponseSchema(
            id=user.id,
            email=user.email,
            username=user.username,
            fullname=user.fullname,
            age=user.age,
            gender=user.gender,
            roles=roles
        )
    )

@router.delete("/streaming-clients/{client_id}", response_model=StreamingClientResponseSchema)
def delete_streaming_client(client_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    client = StreamingClientService.delete_streaming_client(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    
    user = client.user
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    
    return StreamingClientResponseSchema(
        id=client.id,
        user_id=client.user_id,
        name=client.name,
        description=client.description,
        username=client.username,
        password=client.password,
        config=client.config,
        status=client.status,
        created_at=str(client.created_at),
        updated_at=str(client.updated_at),
        user=UserResponseSchema(
            id=user.id,
            email=user.email,
            username=user.username,
            fullname=user.fullname,
            age=user.age,
            gender=user.gender,
            roles=roles
        )
    )

