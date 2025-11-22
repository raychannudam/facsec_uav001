from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Models import get_db, ChatSessionModel, ChatConversationModel, ChatMessageModel
from Schemas import (
    ChatSessionResponseSchema,
    ChatConversationResponseSchema,
    ChatMessageResponseSchema,
    ChatMessageCreateSchema
)
from Services.Chat import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("/sessions/", response_model=ChatSessionResponseSchema)
def create_chat_session(user_id: int, db: Session = Depends(get_db)):
    session = ChatService.create_chat_session(user_id=user_id, db=db)
    if not session:
        raise HTTPException(status_code=400, detail="Unable to create chat session")
    return session

@router.get("/sessions/{session_id}", response_model=ChatSessionResponseSchema)
def get_chat_session(session_id: int, db: Session = Depends(get_db)):
    session = ChatService.get_chat_session(session_id, db)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/conversations/", response_model=ChatConversationResponseSchema)
def create_chat_conversation(session_id: int, user_id: int, name: str = "New Conversation", db: Session = Depends(get_db)):
    conversation = ChatService.create_chat_conversation(session_id=session_id, user_id=user_id, name=name, db=db)
    if not conversation:
        raise HTTPException(status_code=400, detail="Unable to create conversation")
    return conversation

@router.get("/conversations/{conversation_id}", response_model=ChatConversationResponseSchema)
def get_chat_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = ChatService.get_chat_conversation(conversation_id, db)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/messages/", response_model=ChatMessageResponseSchema)
def create_chat_message(conversation_id: int, user_id: int, message: ChatMessageCreateSchema, db: Session = Depends(get_db)):
    chat_message = ChatService.create_chat_message(
        conversation_id=conversation_id,
        user_id=user_id,
        user_prompt=message.user_prompt,
        db=db
    )
    if not chat_message:
        raise HTTPException(status_code=400, detail="Unable to create message")
    return chat_message
