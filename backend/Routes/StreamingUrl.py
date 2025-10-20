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
    
    return result

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
    return urls

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
    
    return url

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
    
    return url

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
    
    # Now delete the URL
    StreamingUrlService.delete_streaming_url(url_id, db, current_user)
    return url