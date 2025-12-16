from sqlalchemy import Column, Integer, String, Text, DateTime, UUID, ForeignKey, JSON, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB


Base = declarative_base()


class Document(Base):
    """
    Document entity representing a book content file.
    """
    __tablename__ = "documents"

    document_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_file = Column(String(500), nullable=False)  # Path to the source file in /docs directory
    title = Column(String(500))  # Title of the document
    content_hash = Column(String(64))  # SHA-256 hash of the content for change detection
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class DocumentChunk(Base):
    """
    DocumentChunk entity representing a chunk of document content.
    """
    __tablename__ = "document_chunks"

    chunk_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(PG_UUID(as_uuid=True), ForeignKey("documents.document_id"), nullable=False)
    chunk_index = Column(Integer)  # Sequential index of the chunk within the document
    content = Column(Text, nullable=False)  # The actual text content of the chunk
    embedding_id = Column(String(100))  # ID of the corresponding vector in Qdrant
    metadata = Column(JSONB)  # Additional metadata about the chunk (headers, section info, etc.)
    created_at = Column(DateTime, server_default=func.now())


class ChatSession(Base):
    """
    ChatSession entity representing a user's chat session.
    """
    __tablename__ = "chat_sessions"

    session_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True))  # Optional identifier for the user
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ChatMessage(Base):
    """
    ChatMessage entity representing a message in a chat session.
    """
    __tablename__ = "chat_messages"

    message_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("chat_sessions.session_id"), nullable=False)
    role = Column(String(10), CheckConstraint("role IN ('user', 'assistant')"), nullable=False)  # Role of the message sender
    content = Column(Text, nullable=False)  # The actual content of the message
    citations = Column(JSONB)  # List of citations used in the response
    created_at = Column(DateTime, server_default=func.now())