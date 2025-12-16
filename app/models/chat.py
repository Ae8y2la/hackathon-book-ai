from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime


class ChatSessionBase(BaseModel):
    """
    Base model for ChatSession entity.
    """
    user_id: Optional[UUID] = None


class ChatSessionCreate(ChatSessionBase):
    """
    Model for creating a new ChatSession.
    """
    pass


class ChatSession(ChatSessionBase):
    """
    Model for ChatSession entity with database fields.
    """
    session_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageBase(BaseModel):
    """
    Base model for ChatMessage entity.
    """
    session_id: UUID
    role: str  # 'user' or 'assistant'
    content: str
    citations: Optional[List[Dict[str, Any]]] = None


class ChatMessageCreate(ChatMessageBase):
    """
    Model for creating a new ChatMessage.
    """
    pass


class ChatMessage(ChatMessageBase):
    """
    Model for ChatMessage entity with database fields.
    """
    message_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    """
    message: str
    session_id: Optional[str] = None


class SelectedTextChatRequest(BaseModel):
    """
    Request model for selected-text chat endpoint.
    """
    selected_text: str
    question: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Response model for chat endpoints.
    """
    response: str
    session_id: str
    citations: List[Dict[str, str]]


class Citation(BaseModel):
    """
    Model for citation information.
    """
    source_file: str
    title: str
    content_snippet: str