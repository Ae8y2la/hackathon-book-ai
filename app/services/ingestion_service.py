import hashlib
import logging
from typing import List, Dict, Any
from uuid import UUID
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.document import Document, DocumentChunk, DocumentCreate, DocumentChunkCreate
from app.database.schemas import Document as DocumentDB, DocumentChunk as DocumentChunkDB
from app.utils.markdown_parser import parse_markdown_file, chunk_markdown_content, get_all_markdown_files
from app.vector_store.qdrant_client import qdrant_manager
from app.config.settings import settings
from qdrant_client.http import models


class IngestionService:
    """
    Service for handling document ingestion and indexing.
    """

    def __init__(self):
        self.openai_client = None

    async def initialize_openai_client(self):
        """
        Initialize the OpenAI client.
        """
        from openai import AsyncOpenAI
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text using OpenAI API.
        """
        if not self.openai_client:
            await self.initialize_openai_client()

        try:
            response = await self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response.data[0].embedding
        except Exception as e:
            logging.error(f"Error getting embedding: {e}")
            raise

    async def process_document(self, file_path: str, session: AsyncSession) -> Dict[str, Any]:
        """
        Process a single document: parse, chunk, create embeddings, and store.
        """
        # Parse the markdown file
        parsed_content = parse_markdown_file(file_path)

        # Calculate content hash
        content_hash = hashlib.sha256(parsed_content['content'].encode()).hexdigest()

        # Check if document already exists and hasn't changed
        existing_doc_query = select(DocumentDB).where(
            DocumentDB.source_file == file_path,
            DocumentDB.content_hash == content_hash
        )
        result = await session.execute(existing_doc_query)
        existing_doc = result.scalar_one_or_none()

        if existing_doc:
            logging.info(f"Document {file_path} already exists and is up-to-date")
            return {
                "document_id": existing_doc.document_id,
                "file_path": file_path,
                "title": existing_doc.title,
                "chunks_processed": 0,  # No new chunks needed
                "message": "Document already exists and is up-to-date"
            }

        # Create or update document record
        if existing_doc:
            # Update existing document
            existing_doc.title = parsed_content['title']
            existing_doc.content_hash = content_hash
            document_db = existing_doc
        else:
            # Create new document
            document_db = DocumentDB(
                source_file=file_path,
                title=parsed_content['title'],
                content_hash=content_hash
            )
            session.add(document_db)

        await session.flush()  # Get the document_id without committing

        # Chunk the content
        chunks = chunk_markdown_content(parsed_content['content'])

        # Prepare to store chunks in both vector store and database
        chunk_points = []
        chunk_records = []

        for i, chunk_text in enumerate(chunks):
            # Get embedding for the chunk
            embedding = await self.get_embedding(chunk_text)

            # Create Qdrant point
            chunk_id_str = f"{document_db.document_id}-{i}"
            point = models.PointStruct(
                id=chunk_id_str,
                vector=embedding,
                payload={
                    "document_id": str(document_db.document_id),
                    "source_file": file_path,
                    "chunk_index": i,
                    "title": parsed_content['title'],
                    "content": chunk_text,
                    "metadata": {
                        "headers": parsed_content['headers'],
                        "section": f"chunk_{i}"
                    }
                }
            )
            chunk_points.append(point)

            # Create database record
            chunk_record = DocumentChunkDB(
                document_id=document_db.document_id,
                chunk_index=i,
                content=chunk_text,
                embedding_id=chunk_id_str,
                metadata={
                    "headers": parsed_content['headers'],
                    "section": f"chunk_{i}"
                }
            )
            chunk_records.append(chunk_record)

        # Store chunks in database
        for chunk_record in chunk_records:
            session.add(chunk_record)

        # Store embeddings in Qdrant
        if chunk_points:
            await qdrant_manager.upsert_vectors(chunk_points)

        await session.commit()

        return {
            "document_id": document_db.document_id,
            "file_path": file_path,
            "title": parsed_content['title'],
            "chunks_processed": len(chunks),
            "message": f"Successfully processed {len(chunks)} chunks"
        }

    async def ingest_documents(self, force_reindex: bool = False) -> Dict[str, Any]:
        """
        Ingest all markdown documents from the docs directory.
        """
        try:
            # Get all markdown files
            md_files = get_all_markdown_files(settings.docs_dir_path)
            logging.info(f"Found {len(md_files)} markdown files to process")

            if not md_files:
                return {
                    "status": "success",
                    "processed_files": 0,
                    "indexed_chunks": 0,
                    "message": f"No markdown files found in {settings.docs_dir_path}"
                }

            # Initialize database session
            from app.database.postgres import AsyncSessionLocal
            async with AsyncSessionLocal() as session:
                processed_files = 0
                indexed_chunks = 0

                for file_path in md_files:
                    try:
                        result = await self.process_document(file_path, session)
                        processed_files += 1
                        indexed_chunks += result['chunks_processed']
                        logging.info(f"Processed {file_path}: {result['message']}")
                    except Exception as e:
                        logging.error(f"Error processing {file_path}: {e}")
                        continue

            return {
                "status": "success",
                "processed_files": processed_files,
                "indexed_chunks": indexed_chunks,
                "message": f"Successfully processed {processed_files} files and indexed {indexed_chunks} chunks"
            }
        except Exception as e:
            logging.error(f"Error during ingestion: {e}")
            return {
                "status": "error",
                "processed_files": 0,
                "indexed_chunks": 0,
                "message": f"Ingestion failed: {str(e)}"
            }

    async def delete_document(self, document_id: UUID):
        """
        Delete a document and all its chunks from both database and vector store.
        """
        from app.database.postgres import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            # Delete chunks from database
            chunk_query = select(DocumentChunkDB).where(
                DocumentChunkDB.document_id == document_id
            )
            chunk_result = await session.execute(chunk_query)
            chunks = chunk_result.scalars().all()

            # Delete document from database
            doc_query = select(DocumentDB).where(
                DocumentDB.document_id == document_id
            )
            doc_result = await session.execute(doc_query)
            document = doc_result.scalar_one_or_none()

            if document:
                await session.delete(document)
                await session.commit()

                # Delete vectors from Qdrant
                await qdrant_manager.delete_by_document_id(str(document_id))

                return {
                    "status": "success",
                    "message": f"Successfully deleted document {document_id} and its {len(chunks)} chunks"
                }

        return {
            "status": "error",
            "message": f"Document {document_id} not found"
        }


# Global instance
ingestion_service = IngestionService()