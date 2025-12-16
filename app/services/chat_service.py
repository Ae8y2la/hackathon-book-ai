import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.chat import ChatSession, ChatMessage, ChatSessionCreate, ChatMessageCreate
from app.database.schemas import ChatSession as ChatSessionDB, ChatMessage as ChatMessageDB
from app.services.rag_service import rag_service


class ChatService:
    """
    Service for handling chat session management and message storage.
    """

    async def create_session(self, session: AsyncSession, user_id: Optional[str] = None) -> ChatSession:
        """
        Create a new chat session.
        """
        session_db = ChatSessionDB(
            user_id=uuid.UUID(user_id) if user_id else None
        )
        session.add(session_db)
        await session.flush()
        await session.commit()

        # Refresh to get the created_at and updated_at values
        await session.refresh(session_db)

        return ChatSession.model_validate(session_db)

    async def get_or_create_session(self, session: AsyncSession, session_id: Optional[str] = None, user_id: Optional[str] = None) -> ChatSession:
        """
        Get an existing session or create a new one.
        """
        if session_id:
            # Try to get existing session
            stmt = select(ChatSessionDB).where(ChatSessionDB.session_id == uuid.UUID(session_id))
            result = await session.execute(stmt)
            existing_session = result.scalar_one_or_none()

            if existing_session:
                return ChatSession.model_validate(existing_session)

        # Create new session
        return await self.create_session(session, user_id)

    async def save_message(self, session: AsyncSession, chat_session: ChatSession, role: str, content: str, citations: Optional[List[Dict[str, Any]]] = None) -> ChatMessage:
        """
        Save a chat message to the database.
        """
        message_db = ChatMessageDB(
            session_id=chat_session.session_id,
            role=role,
            content=content,
            citations=citations
        )
        session.add(message_db)
        await session.flush()
        await session.commit()

        # Refresh to get the created_at value
        await session.refresh(message_db)

        return ChatMessage.model_validate(message_db)

    async def get_session_history(self, session: AsyncSession, session_id: str) -> List[ChatMessage]:
        """
        Get the chat history for a session.
        """
        stmt = select(ChatMessageDB).where(
            ChatMessageDB.session_id == uuid.UUID(session_id)
        ).order_by(ChatMessageDB.created_at)
        result = await session.execute(stmt)
        messages_db = result.scalars().all()

        return [ChatMessage.model_validate(msg) for msg in messages_db]

    async def process_full_book_chat(self, session: AsyncSession, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a full-book chat request.
        """
        # Get or create chat session
        chat_session = await self.get_or_create_session(session, session_id)

        # Save user message
        user_message = await self.save_message(
            session, chat_session, "user", message
        )

        # Process with RAG service
        rag_result = await rag_service.full_book_rag_query(message)

        # Save assistant message
        assistant_message = await self.save_message(
            session, chat_session, "assistant", rag_result["response"], rag_result["citations"]
        )

        return {
            "response": rag_result["response"],
            "session_id": str(chat_session.session_id),
            "citations": rag_result["citations"]
        }

    async def process_selected_text_chat(self, session: AsyncSession, selected_text: str, question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a selected-text chat request.
        """
        # Get or create chat session
        chat_session = await self.get_or_create_session(session, session_id)

        # Save user message (we'll save the selected text and question as separate messages or as a combined message)
        user_message_content = f"Selected text: {selected_text}\nQuestion: {question}"
        user_message = await self.save_message(
            session, chat_session, "user", user_message_content
        )

        # Process with RAG service
        rag_result = await rag_service.selected_text_rag_query(selected_text, question)

        # Save assistant message
        assistant_message = await self.save_message(
            session, chat_session, "assistant", rag_result["response"], rag_result["citations"]
        )

        return {
            "response": rag_result["response"],
            "session_id": str(chat_session.session_id),
            "citations": rag_result["citations"]
        }


# Global instance
chat_service = ChatService()