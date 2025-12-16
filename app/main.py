from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import asyncio
from typing import Dict, Any

from app.config.settings import settings
from app.api.v1 import chat, ingestion
from app.vector_store.qdrant_client import qdrant_manager
from app.database.postgres import init_db


# Set up logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application startup and shutdown events.
    """
    # Startup
    logging.info("Starting up the RAG Chatbot application...")

    try:
        # Initialize database
        await init_db()
        logging.info("Database initialized successfully")

        # Initialize Qdrant collection
        await qdrant_manager.create_collection()
        logging.info("Qdrant collection created/verified successfully")

        logging.info("RAG Chatbot application started successfully")
    except Exception as e:
        logging.error(f"Error during application startup: {e}")
        raise

    yield

    # Shutdown
    try:
        await qdrant_manager.close()
        logging.info("Qdrant client closed successfully")
        logging.info("RAG Chatbot application shut down successfully")
    except Exception as e:
        logging.error(f"Error during application shutdown: {e}")


# Create FastAPI app instance
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="RAG Chatbot for Docusaurus Book - Backend API",
    lifespan=lifespan,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["http://localhost:3000"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(ingestion.router, prefix="/api/v1", tags=["ingestion"])


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify service status.
    """
    # Check services connectivity
    services_status: Dict[str, str] = {
        "database": "connected",  # This would be checked in a real implementation
        "vector_store": "connected",  # This would be checked in a real implementation
        "openai_api": "reachable"  # This would be checked in a real implementation
    }

    return {
        "status": "healthy",
        "timestamp": "2025-12-16T10:00:00Z",
        "services": services_status
    }


@app.get("/")
async def root():
    """
    Root endpoint for basic service information.
    """
    return {
        "message": "RAG Chatbot for Docusaurus Book API",
        "version": settings.app_version,
        "docs": "/docs",
        "endpoints": {
            "ingestion": "/api/v1/ingest",
            "chat": "/api/v1/chat",
            "selected_text_chat": "/api/v1/chat/selection",
            "health": "/health"
        }
    }