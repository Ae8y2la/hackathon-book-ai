from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime


class DocumentBase(BaseModel):
    """
    Base model for Document entity.
    """
    source_file: str
    title: Optional[str] = None
    content_hash: Optional[str] = None


class DocumentCreate(DocumentBase):
    """
    Model for creating a new Document.
    """
    pass


class DocumentUpdate(BaseModel):
    """
    Model for updating a Document.
    """
    title: Optional[str] = None


class Document(DocumentBase):
    """
    Model for Document entity with database fields.
    """
    document_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentChunkBase(BaseModel):
    """
    Base model for DocumentChunk entity.
    """
    document_id: UUID
    chunk_index: int
    content: str
    embedding_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentChunkCreate(DocumentChunkBase):
    """
    Model for creating a new DocumentChunk.
    """
    pass


class DocumentChunkUpdate(BaseModel):
    """
    Model for updating a DocumentChunk.
    """
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentChunk(DocumentChunkBase):
    """
    Model for DocumentChunk entity with database fields.
    """
    chunk_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentIngestionResponse(BaseModel):
    """
    Response model for document ingestion.
    """
    status: str
    processed_files: int
    indexed_chunks: int
    message: str