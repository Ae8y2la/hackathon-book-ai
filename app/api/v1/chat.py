from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.database.postgres import get_db_session
from app.models.chat import ChatRequest, SelectedTextChatRequest, ChatResponse
from app.services.chat_service import chat_service
from app.utils.validators import validate_chat_message_length, validate_selected_text_length


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Chat endpoint for full-book RAG queries.
    """
    try:
        # Validate input
        if not validate_chat_message_length(request.message):
            raise HTTPException(status_code=400, detail="Message is too long or empty")

        # Process the chat request
        result = await chat_service.process_full_book_chat(
            db_session, request.message, request.session_id
        )

        return ChatResponse(
            response=result["response"],
            session_id=result["session_id"],
            citations=result["citations"]
        )
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.post("/chat/selection", response_model=ChatResponse)
async def chat_selection(
    request: SelectedTextChatRequest,
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Chat endpoint for selected-text RAG queries.
    """
    try:
        # Validate input
        if not validate_selected_text_length(request.selected_text):
            raise HTTPException(status_code=400, detail="Selected text is too long or empty")

        if not validate_chat_message_length(request.question):
            raise HTTPException(status_code=400, detail="Question is too long or empty")

        # Process the selected-text chat request
        result = await chat_service.process_selected_text_chat(
            db_session, request.selected_text, request.question, request.session_id
        )

        return ChatResponse(
            response=result["response"],
            session_id=result["session_id"],
            citations=result["citations"]
        )
    except Exception as e:
        logging.error(f"Error in selected-text chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Selected-text chat processing failed: {str(e)}")