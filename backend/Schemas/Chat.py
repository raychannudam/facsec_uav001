from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessageSchema(BaseModel):
    role: str
    message: str
    created_at: Optional[datetime]

class ChatSessionCreateSchema(BaseModel):
    session_name: Optional[str]

class ChatSessionResponseSchema(BaseModel):
    id: int
    user_id: int
    session_name: Optional[str]
    messages: List[ChatMessageSchema]

    class Config:
        orm_mode = True