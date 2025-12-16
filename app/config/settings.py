from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    app_title: str = "RAG Chatbot for Docusaurus Book"
    app_version: str = "1.0.0"
    debug: bool = False

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "book_content_chunks")

    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/rag_chatbot")

    # Application Configuration
    docs_dir_path: str = os.getenv("DOCS_DIR_PATH", "./docs")

    class Config:
        env_file = ".env"


# Create settings instance
settings = Settings()