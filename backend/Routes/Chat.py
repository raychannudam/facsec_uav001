from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import json

from Models import get_db, UserModel
from Schemas import (
    ChatSessionResponseSchema,
    ChatConversationResponseSchema,
    ChatMessageResponseSchema,
    ChatMessageCreateSchema
)
from Services.Chat import ChatService
from typing import List
from Security.jwt import get_current_user, get_current_user_ws


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, conversation_id: int):
        await websocket.accept()
        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = []
        self.active_connections[conversation_id].append(websocket)

    def disconnect(self, websocket: WebSocket, conversation_id: int):
        if conversation_id in self.active_connections:
            self.active_connections[conversation_id].remove(websocket)

    async def broadcast(self, message: str, conversation_id: int):
        if conversation_id in self.active_connections:
            for connection in self.active_connections[conversation_id]:
                await connection.send_text(message)

manager = ConnectionManager()

@router.post("/sessions/", response_model=ChatSessionResponseSchema)
def create_chat_session(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    session = ChatService.create_chat_session(user_id=current_user.id, db=db)
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
def create_chat_conversation(session_id: int, name: str = "New Conversation", db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    conversation = ChatService.create_chat_conversation(session_id=session_id, user_id=current_user.id, name=name, db=db)
    if not conversation:
        raise HTTPException(status_code=400, detail="Unable to create conversation")
    return conversation

@router.get("/conversations/", response_model=List[ChatConversationResponseSchema])
def get_my_conversations(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    conversations = ChatService.get_conversations_by_user(current_user.id, db)
    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found for this user")
    return conversations

@router.get("/conversations/{conversation_id}", response_model=ChatConversationResponseSchema)
def get_chat_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = ChatService.get_chat_conversation(conversation_id, db)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.get("/conversations/{conversation_id}/messages/", response_model=List[ChatMessageResponseSchema])
def get_messages_in_conversation(conversation_id: int, db: Session = Depends(get_db)):
    messages = ChatService.get_messages_by_conversation(conversation_id, db)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this conversation")
    return messages


@router.post("/messages/", response_model=ChatMessageResponseSchema)
def create_chat_message(conversation_id: int, message: ChatMessageCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    chat_message = ChatService.create_chat_message(
        conversation_id=conversation_id,
        user_id=current_user.id,
        user_prompt=message.user_prompt,
        db=db
    )
    if not chat_message:
        raise HTTPException(status_code=400, detail="Unable to create message")
    return chat_message

@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_ws)):
    await manager.connect(websocket, conversation_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_prompt = message_data.get("user_prompt")

            if user_prompt is None:
                continue

            chat_message = ChatService.create_chat_message(
                conversation_id=conversation_id,
                user_id=current_user.id,
                user_prompt=user_prompt,
                db=db
            )

            if chat_message:
                response_message = ChatMessageResponseSchema.from_orm(chat_message).dict()
                await manager.broadcast(json.dumps(response_message, default=str), conversation_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, conversation_id)