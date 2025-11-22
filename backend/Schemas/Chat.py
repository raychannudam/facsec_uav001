from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ----------------- ChatMessage Schemas -----------------

class ChatMessageCreateSchema(BaseModel):
    """Schema for creating a new chat message."""
    user_prompt: str = Field(..., description="The user's prompt or question.")

class ChatMessageUpdateSchema(BaseModel):
    """Schema for updating an existing chat message."""
    user_prompt: Optional[str] = Field(None, description="The user's prompt or question.")
    response: Optional[str] = Field(None, description="The model's response to the user's prompt.")

class ChatMessageResponseSchema(BaseModel):
    """Schema for the response of a chat message."""
    id: int = Field(..., description="The unique ID of the chat message.")
    user_id: int = Field(..., description="The ID of the user who sent the message.")
    conversation_id: int = Field(..., description="The ID of the conversation this message belongs to.")
    user_prompt: str = Field(..., description="The user's prompt or question.")
    response: str = Field(..., description="The model's response to the user's prompt.")
    timestamp: datetime = Field(..., description="The timestamp when the message was created.")

    class Config:
        from_attributes = True

# ----------------- ChatConversation Schemas -----------------

class ChatConversationCreateSchema(BaseModel):
    """Schema for creating a new chat conversation."""
    name: Optional[str] = Field("New Conversation", description="The name of the conversation.")

class ChatConversationUpdateSchema(BaseModel):
    """Schema for updating an existing chat conversation."""
    name: Optional[str] = Field(None, description="The name of the conversation.")

class ChatConversationResponseSchema(BaseModel):
    """Schema for the response of a chat conversation."""
    id: int = Field(..., description="The unique ID of the conversation.")
    user_id: int = Field(..., description="The ID of the user who owns the conversation.")
    session_id: int = Field(..., description="The ID of the session this conversation belongs to.")
    name: str = Field(..., description="The name of the conversation.")
    created_at: datetime = Field(..., description="The timestamp when the conversation was created.")
    messages: List[ChatMessageResponseSchema] = Field([], description="A list of messages in this conversation.")

    class Config:
        from_attributes = True

# ----------------- ChatSession Schemas -----------------

class ChatSessionCreateSchema(BaseModel):
    """Schema for creating a new chat session."""
    pass

class ChatSessionUpdateSchema(BaseModel):
    """Schema for updating an existing chat session."""
    status: Optional[str] = Field(None, description="The status of the session (e.g., active, closed, expired).")
    ended_at: Optional[datetime] = Field(None, description="The timestamp when the session ended.")

class ChatSessionResponseSchema(BaseModel):
    """Schema for the response of a chat session."""
    id: int = Field(..., description="The unique ID of the session.")
    user_id: int = Field(..., description="The ID of the user who owns the session.")
    started_at: datetime = Field(..., description="The timestamp when the session started.")
    ended_at: Optional[datetime] = Field(None, description="The timestamp when the session ended.")
    status: str = Field(..., description="The current status of the session.")
    conversations: List[ChatConversationResponseSchema] = Field([], description="A list of conversations in this session.")

    class Config:
        from_attributes = True
