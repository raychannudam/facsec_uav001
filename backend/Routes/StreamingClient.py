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
    return result

@router.get("/streaming-clients", response_model=list[StreamingClientResponseSchema])
def get_streaming_clients(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    clients = StreamingClientService.get_streaming_clients(db)
    return clients

@router.get("/streaming-clients/{client_id}", response_model=StreamingClientResponseSchema)
def get_streaming_client(client_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    client = StreamingClientService.get_streaming_client_by_id(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    return client

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
    return {"message": "Password updated successfully"}

@router.put("/streaming-clients/{client_id}", response_model=StreamingClientResponseSchema)
def update_streaming_client(client_id: int, client_update: StreamingClientUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in client_update.dict().items() if v is not None}
    client = StreamingClientService.update_streaming_client(client_id, update_data, db)
    if isinstance(client, dict) and "error" in client:
        raise HTTPException(status_code=400, detail=client["error"])
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    return client

@router.delete("/streaming-clients/{client_id}", response_model=StreamingClientResponseSchema)
def delete_streaming_client(client_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    client = StreamingClientService.delete_streaming_client(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Streaming client not found")
    return client

