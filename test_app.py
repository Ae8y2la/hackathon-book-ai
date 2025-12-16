"""
Simple test to verify that the RAG Chatbot application can be imported and initialized.
"""
import asyncio
from app.main import app
from app.services.ingestion_service import ingestion_service
from app.services.rag_service import rag_service
from app.services.chat_service import chat_service

def test_app_imports():
    """Test that all main components can be imported without error."""
    assert app is not None
    assert ingestion_service is not None
    assert rag_service is not None
    assert chat_service is not None
    print("✓ All main components imported successfully")

def test_services_initialized():
    """Test that services are properly initialized."""
    # Check that services have the expected methods
    assert hasattr(ingestion_service, 'ingest_documents')
    assert hasattr(rag_service, 'full_book_rag_query')
    assert hasattr(chat_service, 'process_full_book_chat')
    print("✓ All services have expected methods")

if __name__ == "__main__":
    test_app_imports()
    test_services_initialized()
    print("\n✓ All basic tests passed! The RAG Chatbot backend is ready.")