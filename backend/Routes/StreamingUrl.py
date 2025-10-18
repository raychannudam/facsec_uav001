from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import get_db, StreamingUrlModel, StreamingClientModel, UserModel
from Schemas.StreamingUrl import StreamingUrlCreateSchema, StreamingUrlUpdateSchema, StreamingUrlResponseSchema
from Schemas.StreamingClient import StreamingClientResponseSchema
from Schemas.User import UserResponseSchema
from Schemas.Role import RoleResponseSchema
from Services.StreamingUrl import StreamingUrlService
from Security.jwt import get_current_user

router = APIRouter()

def is_admin(user: UserModel) -> bool:
    """Check if the user has an admin role."""
    return any(role.name.lower() == "admin" for role in user.roles)

@router.post("/streaming-urls", response_model=StreamingUrlResponseSchema)
def create_streaming_url(
    url: StreamingUrlCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if the streaming client belongs to the user (unless admin)
    streaming_client = db.query(StreamingClientModel).filter(StreamingClientModel.id == url.streaming_client_id).first()
    if not streaming_client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    if not is_admin(current_user) and streaming_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create streaming URL for this streaming client")
    
    result = StreamingUrlService.create_streaming_url(url, db)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    streaming_client = result.streaming_client
    user = streaming_client.user
    roles = [
        RoleResponseSchema(
            id=role.id,
            name=role.name,
            description=role.description,
            created_at=str(role.created_at),
            updated_at=str(role.updated_at)
        ) for role in user.roles
    ]
    
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
            validation_code=streaming_client.validation_code,
            created_at=str(streaming_client.created_at),
            updated_at=str(streaming_client.updated_at),
            user=UserResponseSchema(
                id=user.id,
                email=user.email,
                username=user.username,
                fullname=user.fullname,
                age=user.age,
                gender=user.gender,
                created_at=str(user.created_at),
                updated_at=str(user.updated_at),
                roles=roles
            )
        )
    )

@router.get("/streaming-urls/{streaming_client_id}", response_model=list[StreamingUrlResponseSchema])
def get_streaming_urls(
    streaming_client_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if the streaming client exists and belongs to the user (unless admin)
    streaming_client = db.query(StreamingClientModel).filter(StreamingClientModel.id == streaming_client_id).first()
    if not streaming_client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    if not is_admin(current_user) and streaming_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access streaming URLs for this streaming client")
    
    urls = StreamingUrlService.get_streaming_urls(streaming_client_id, db)
    return [
        StreamingUrlResponseSchema(
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
            )
        ) for u in urls
    ]

@router.get("/streaming-urls/single/{url_id}", response_model=StreamingUrlResponseSchema)
def get_streaming_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    url = StreamingUrlService.get_streaming_url_by_id(url_id, db)
    if not url:
        raise HTTPException(status_code=404, detail="Streaming URL not found")
    
    # Check if the streaming client belongs to the user (unless admin)
    streaming_client = url.streaming_client
    if not is_admin(current_user) and streaming_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this streaming URL")
    
    user = streaming_client.user
    roles = [
        RoleResponseSchema(
            id=role.id,
            name=role.name,
            description=role.description,
            created_at=str(role.created_at),
            updated_at=str(role.updated_at)
        ) for role in user.roles
    ]
    
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
            validation_code=streaming_client.validation_code,
            created_at=str(streaming_client.created_at),
            updated_at=str(streaming_client.updated_at),
            user=UserResponseSchema(
                id=user.id,
                email=user.email,
                username=user.username,
                fullname=user.fullname,
                age=user.age,
                gender=user.gender,
                created_at=str(user.created_at),
                updated_at=str(user.updated_at),
                roles=roles
            )
        )
    )

@router.put("/streaming-urls/{url_id}", response_model=StreamingUrlResponseSchema)
def update_streaming_url(
    url_id: int,
    url_update: StreamingUrlUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    url = StreamingUrlService.get_streaming_url_by_id(url_id, db)
    if not url:
        raise HTTPException(status_code=404, detail="Streaming URL not found")
    
    # Check if the streaming client belongs to the user (unless admin)
    streaming_client = url.streaming_client
    if not is_admin(current_user) and streaming_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this streaming URL")
    
    # Check if the new streaming_client_id (if provided) belongs to the user (unless admin)
    update_data = {k: v for k, v in url_update.dict(exclude_unset=True).items()}
    if "streaming_client_id" in update_data and update_data["streaming_client_id"] != url.streaming_client_id:
        new_streaming_client = db.query(StreamingClientModel).filter(
            StreamingClientModel.id == update_data["streaming_client_id"]
        ).first()
        if not new_streaming_client:
            raise HTTPException(status_code=404, detail="New streaming client not found")
        if not is_admin(current_user) and new_streaming_client.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to assign streaming URL to this streaming client")
    
    url = StreamingUrlService.update_streaming_url(url_id, update_data, db)
    if isinstance(url, dict) and "error" in url:
        raise HTTPException(status_code=400, detail=url["error"])
    if not url:
        raise HTTPException(status_code=404, detail="Streaming URL not found")
    
    streaming_client = url.streaming_client
    user = streaming_client.user
    roles = [
        RoleResponseSchema(
            id=role.id,
            name=role.name,
            description=role.description,
            created_at=str(role.created_at),
            updated_at=str(role.updated_at)
        ) for role in user.roles
    ]
    
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
            validation_code=streaming_client.validation_code,
            created_at=str(streaming_client.created_at),
            updated_at=str(streaming_client.updated_at),
            user=UserResponseSchema(
                id=user.id,
                email=user.email,
                username=user.username,
                fullname=user.fullname,
                age=user.age,
                gender=user.gender,
                created_at=str(user.created_at),
                updated_at=str(user.updated_at),
                roles=roles
            )
        )
    )

@router.delete("/streaming-urls/{url_id}", response_model=StreamingUrlResponseSchema)
def delete_streaming_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    url = StreamingUrlService.get_streaming_url_by_id(url_id, db)
    if not url:
        raise HTTPException(status_code=404, detail="Streaming URL not found")
    
    # Check if the streaming client belongs to the user (unless admin)
    streaming_client = url.streaming_client
    if not is_admin(current_user) and streaming_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this streaming URL")
    
    # Build response before deletion
    user = streaming_client.user
    roles = [
        RoleResponseSchema(
            id=role.id,
            name=role.name,
            description=role.description,
            created_at=str(role.created_at),
            updated_at=str(role.updated_at)
        ) for role in user.roles
    ]
    
    response = StreamingUrlResponseSchema(
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
            validation_code=streaming_client.validation_code,
            created_at=str(streaming_client.created_at),
            updated_at=str(streaming_client.updated_at),
            user=UserResponseSchema(
                id=user.id,
                email=user.email,
                username=user.username,
                fullname=user.fullname,
                age=user.age,
                gender=user.gender,
                created_at=str(user.created_at),
                updated_at=str(user.updated_at),
                roles=roles
            )
        )
    )
    
    # Now delete the URL
    StreamingUrlService.delete_streaming_url(url_id, db)
    return response