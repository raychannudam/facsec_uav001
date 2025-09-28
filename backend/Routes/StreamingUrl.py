from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import get_db, StreamingUrlModel, StreamingClientModel
from Schemas.StreamingUrl import StreamingUrlCreateSchema, StreamingUrlUpdateSchema, StreamingUrlResponseSchema
from Services.StreamingUrl import StreamingUrlService
from Security.jwt import get_current_user
from Models import UserModel
from Schemas import UserResponseSchema, RoleResponseSchema
from Schemas.StreamingClient import StreamingClientResponseSchema

router = APIRouter()

@router.post("/streaming-urls", response_model=StreamingUrlResponseSchema)
def create_streaming_url(url: StreamingUrlCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result = StreamingUrlService.create_streaming_url(url, db)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    streaming_client = result.streaming_client
    user = streaming_client.user
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    
    return StreamingUrlResponseSchema(
        id=result.id,
        streaming_client_id=result.streaming_client_id,
        name=result.name,
        description=result.description,
        config=result.config,
        status=result.status,
        created_at=str(result.created_at),
        updated_at=str(result.updated_at),
        streaming_client=StreamingClientResponseSchema(
            id=streaming_client.id,
            user_id=streaming_client.user_id,
            name=streaming_client.name,
            description=streaming_client.description,
            username=streaming_client.username,
            password=streaming_client.password,
            config=streaming_client.config,
            status=streaming_client.status,
            created_at=str(streaming_client.created_at),
            updated_at=str(streaming_client.updated_at),
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
    )

@router.get("/streaming-urls", response_model=list[StreamingUrlResponseSchema])
def get_streaming_urls(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    urls = StreamingUrlService.get_streaming_urls(db)
    return [StreamingUrlResponseSchema(
        id=u.id,
        streaming_client_id=u.streaming_client_id,
        name=u.name,
        description=u.description,
        config=u.config,
        status=u.status,
        created_at=str(u.created_at),
        updated_at=str(u.updated_at),
        streaming_client=StreamingClientResponseSchema(
            id=u.streaming_client.id,
            user_id=u.streaming_client.user_id,
            name=u.streaming_client.name,
            description=u.streaming_client.description,
            username=u.streaming_client.username,
            password=u.streaming_client.password,
            config=u.streaming_client.config,
            status=u.streaming_client.status,
            created_at=str(u.streaming_client.created_at),
            updated_at=str(u.streaming_client.updated_at),
            user=UserResponseSchema(
                id=u.streaming_client.user.id,
                email=u.streaming_client.user.email,
                username=u.streaming_client.user.username,
                fullname=u.streaming_client.user.fullname,
                age=u.streaming_client.user.age,
                gender=u.streaming_client.user.gender,
                roles=[RoleResponseSchema(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    created_at=str(role.created_at),
                    updated_at=str(role.updated_at)
                ) for role in u.streaming_client.user.roles]
            )
        )
    ) for u in urls]

@router.get("/streaming-urls/{url_id}", response_model=StreamingUrlResponseSchema)
def get_streaming_url(url_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    url = StreamingUrlService.get_streaming_url_by_id(url_id, db)
    if not url:
        raise HTTPException(status_code=404, detail="Streaming URL not found")
    
    streaming_client = url.streaming_client
    user = streaming_client.user
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    
    return StreamingUrlResponseSchema(
        id=url.id,
        streaming_client_id=url.streaming_client_id,
        name=url.name,
        description=url.description,
        config=url.config,
        status=url.status,
        created_at=str(url.created_at),
        updated_at=str(url.updated_at),
        streaming_client=StreamingClientResponseSchema(
            id=streaming_client.id,
            user_id=streaming_client.user_id,
            name=streaming_client.name,
            description=streaming_client.description,
            username=streaming_client.username,
            password=streaming_client.password,
            config=streaming_client.config,
            status=streaming_client.status,
            created_at=str(streaming_client.created_at),
            updated_at=str(streaming_client.updated_at),
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
    )

@router.put("/streaming-urls/{url_id}", response_model=StreamingUrlResponseSchema)
def update_streaming_url(url_id: int, url_update: StreamingUrlUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in url_update.dict().items() if v is not None}
    url = StreamingUrlService.update_streaming_url(url_id, update_data, db)
    if isinstance(url, dict) and "error" in url:
        raise HTTPException(status_code=400, detail=url["error"])
    if not url:
        raise HTTPException(status_code=404, detail="Streaming URL not found")
    
    streaming_client = url.streaming_client
    user = streaming_client.user
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    
    return StreamingUrlResponseSchema(
        id=url.id,
        streaming_client_id=url.streaming_client_id,
        name=url.name,
        description=url.description,
        config=url.config,
        status=url.status,
        created_at=str(url.created_at),
        updated_at=str(url.updated_at),
        streaming_client=StreamingClientResponseSchema(
            id=streaming_client.id,
            user_id=streaming_client.user_id,
            name=streaming_client.name,
            description=streaming_client.description,
            username=streaming_client.username,
            password=streaming_client.password,
            config=streaming_client.config,
            status=streaming_client.status,
            created_at=str(streaming_client.created_at),
            updated_at=str(streaming_client.updated_at),
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
    )

@router.delete("/streaming-urls/{url_id}", response_model=StreamingUrlResponseSchema)
def delete_streaming_url(url_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    url = StreamingUrlService.delete_streaming_url(url_id, db)
    if not url:
        raise HTTPException(status_code=404, detail="Streaming URL not found")
    
    streaming_client = url.streaming_client
    user = streaming_client.user
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    
    return StreamingUrlResponseSchema(
        id=url.id,
        streaming_client_id=url.streaming_client_id,
        name=url.name,
        description=url.description,
        config=url.config,
        status=url.status,
        created_at=str(url.created_at),
        updated_at=str(url.updated_at),
        streaming_client=StreamingClientResponseSchema(
            id=streaming_client.id,
            user_id=streaming_client.user_id,
            name=streaming_client.name,
            description=streaming_client.description,
            username=streaming_client.username,
            password=streaming_client.password,
            config=streaming_client.config,
            status=streaming_client.status,
            created_at=str(streaming_client.created_at),
            updated_at=str(streaming_client.updated_at),
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
    )