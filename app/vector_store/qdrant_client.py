from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import logging
from uuid import UUID

from app.config.settings import settings


class QdrantManager:
    """
    Manager class for Qdrant vector store operations.
    """

    def __init__(self):
        """
        Initialize Qdrant client with configuration from settings.
        """
        self.client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=True
        )
        self.collection_name = settings.qdrant_collection_name

    async def create_collection(self):
        """
        Create the collection for book content chunks if it doesn't exist.
        Uses OpenAI ada-002 embeddings (1536 dimensions).
        """
        try:
            # Check if collection exists
            collections = await self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # OpenAI ada-002 embedding size
                        distance=models.Distance.COSINE
                    )
                )
                logging.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logging.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logging.error(f"Error creating Qdrant collection: {e}")
            raise

    async def upsert_vectors(self, points: List[models.PointStruct]):
        """
        Upsert vectors into the collection.
        """
        try:
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logging.info(f"Upserted {len(points)} vectors to {self.collection_name}")
        except Exception as e:
            logging.error(f"Error upserting vectors: {e}")
            raise

    async def search_vectors(self, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar vectors to the query vector.
        """
        try:
            results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'id': result.id,
                    'score': result.score,
                    'payload': result.payload,
                    'content': result.payload.get('content', ''),
                    'document_id': result.payload.get('document_id', ''),
                    'source_file': result.payload.get('source_file', ''),
                    'title': result.payload.get('title', ''),
                    'metadata': result.payload.get('metadata', {})
                })

            return formatted_results
        except Exception as e:
            logging.error(f"Error searching vectors: {e}")
            raise

    async def delete_by_document_id(self, document_id: str):
        """
        Delete all vectors associated with a specific document ID.
        """
        try:
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_id",
                            match=models.MatchValue(value=document_id)
                        )
                    ]
                )
            )
            logging.info(f"Deleted vectors for document_id: {document_id}")
        except Exception as e:
            logging.error(f"Error deleting vectors for document_id {document_id}: {e}")
            raise

    async def get_vector_count(self) -> int:
        """
        Get the total count of vectors in the collection.
        """
        try:
            count = await self.client.count(collection_name=self.collection_name)
            return count.count
        except Exception as e:
            logging.error(f"Error getting vector count: {e}")
            raise

    async def close(self):
        """
        Close the Qdrant client connection.
        """
        await self.client.aclose()


# Global instance
qdrant_manager = QdrantManager()