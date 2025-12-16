from typing import Optional
import re
from pydantic import BaseModel, field_validator, ValidationError
from app.models.chat import ChatRequest, SelectedTextChatRequest


def validate_file_path(file_path: str, base_path: str = "./docs") -> bool:
    """
    Validate that a file path is within the allowed directory.
    """
    try:
        # Resolve the path to prevent directory traversal
        resolved_path = (Path(base_path) / file_path).resolve()
        base_path_resolved = Path(base_path).resolve()

        # Check if the resolved path is within the base path
        resolved_path.relative_to(base_path_resolved)
        return True
    except ValueError:
        # Path is outside the base directory
        return False
    except Exception:
        # Other error occurred
        return False
    from pathlib import Path


def validate_document_content(content: str, max_length: int = 100000) -> bool:
    """
    Validate document content length and format.
    """
    if not content:
        return False

    if len(content) > max_length:
        return False

    # Check for basic text content (not binary)
    try:
        content.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False


def validate_selected_text_length(text: str, max_length: int = 5000) -> bool:
    """
    Validate selected text length for selected-text RAG mode.
    """
    if not text or len(text.strip()) == 0:
        return False

    if len(text) > max_length:
        return False

    return True


def validate_selected_text_citations(selected_text: str, response: str) -> bool:
    """
    Validate that the response is based on the selected text.
    This is a simplified validation - in production, you might want more sophisticated checks.
    """
    # For now, just return True
    # In a more sophisticated implementation, you could check if key phrases
    # in the response appear in the selected text
    return True


def validate_chat_message_length(message: str, max_length: int = 1000) -> bool:
    """
    Validate chat message length.
    """
    if not message or len(message.strip()) == 0:
        return False

    if len(message) > max_length:
        return False

    return True


def validate_session_id(session_id: Optional[str]) -> bool:
    """
    Validate session ID format (UUID-like string).
    """
    if not session_id:
        return True  # Session ID is optional

    # Basic UUID format validation (simplified)
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    return bool(uuid_pattern.match(session_id))