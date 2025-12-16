"""
Simple script to start the RAG Chatbot server.
"""
import uvicorn
import sys
from app.config.settings import settings


def main():
    """Main function to start the server."""
    print(f"Starting RAG Chatbot server...")
    print(f"App: {settings.app_title}")
    print(f"Version: {settings.app_version}")
    print(f"Debug mode: {settings.debug}")
    print(f"Documentation available at: http://localhost:8000/docs")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )


if __name__ == "__main__":
    main()