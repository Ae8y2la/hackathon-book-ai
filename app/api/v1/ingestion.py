from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres import get_db_session
from app.models.document import DocumentIngestionResponse
from app.services.ingestion_service import ingestion_service
from app.config.settings import settings


router = APIRouter()


@router.post("/ingest", response_model=DocumentIngestionResponse)
async def ingest_documents(
    force_reindex: bool = False,
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Ingest all markdown documents from the /docs directory.
    """
    try:
        result = await ingestion_service.ingest_documents(force_reindex=force_reindex)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        return DocumentIngestionResponse(
            status=result["status"],
            processed_files=result["processed_files"],
            indexed_chunks=result["indexed_chunks"],
            message=result["message"]
        )
    except Exception as e:
        logging.error(f"Error during ingestion: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")