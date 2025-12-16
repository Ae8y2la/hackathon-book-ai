import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
import asyncio

from app.config.settings import settings
from app.vector_store.qdrant_client import qdrant_manager
from app.models.chat import Citation


class RAGService:
    """
    Service for handling RAG (Retrieval-Augmented Generation) functionality.
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

    async def retrieve_relevant_chunks(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant document chunks based on the query.
        """
        try:
            query_embedding = await self.get_embedding(query)
            results = await qdrant_manager.search_vectors(
                query_vector=query_embedding,
                limit=limit
            )
            return results
        except Exception as e:
            logging.error(f"Error retrieving relevant chunks: {e}")
            raise

    async def construct_context(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Construct context from retrieved chunks for the LLM.
        """
        context_parts = []
        for chunk in retrieved_chunks:
            content = chunk.get('content', '')
            source_file = chunk.get('source_file', 'Unknown')
            title = chunk.get('title', 'Untitled')

            context_parts.append(
                f"Source: {source_file} | Title: {title}\n"
                f"Content: {content}\n"
                f"---\n"
            )

        return "\n".join(context_parts)

    async def generate_response(self, query: str, context: str) -> str:
        """
        Generate response using OpenAI API with the provided context.
        """
        if not self.openai_client:
            await self.initialize_openai_client()

        try:
            system_message = (
                "You are an AI assistant that answers questions based only on the provided context. "
                "Do not use any external knowledge. If the answer is not in the provided context, "
                "say 'I cannot answer this question based on the provided book content.'"
            )

            user_message = f"Context:\n{context}\n\nQuestion: {query}"

            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.3
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            raise

    async def generate_response_with_selected_text(self, selected_text: str, question: str) -> str:
        """
        Generate response using OpenAI API with the selected text as context.
        """
        if not self.openai_client:
            await self.initialize_openai_client()

        try:
            system_message = (
                "You are an AI assistant that answers questions based only on the provided selected text. "
                "Do not use any external knowledge. If the answer is not in the provided text, "
                "say 'I cannot answer this question based on the provided text.'"
            )

            user_message = f"Selected text:\n{selected_text}\n\nQuestion: {question}"

            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.3
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"Error generating response with selected text: {e}")
            raise

    async def create_citations(self, retrieved_chunks: List[Dict[str, Any]]) -> List[Citation]:
        """
        Create citation objects from retrieved chunks with detailed information.
        """
        citations = []
        for chunk in retrieved_chunks:
            # Create a more detailed content snippet with context
            content = chunk.get('content', '')
            if len(content) > 200:
                # Try to break at sentence boundary
                snippet = content[:200]
                last_period = snippet.rfind('.')
                if last_period != -1 and last_period > 100:  # Don't cut too early
                    snippet = snippet[:last_period + 1]
                else:
                    snippet = snippet + "..."
            else:
                snippet = content

            citation = Citation(
                source_file=chunk.get('source_file', 'Unknown'),
                title=chunk.get('title', 'Untitled'),
                content_snippet=snippet
            )
            citations.append(citation)

        return citations

    async def full_book_rag_query(self, query: str) -> Dict[str, Any]:
        """
        Perform a full-book RAG query.
        """
        try:
            # Retrieve relevant chunks
            retrieved_chunks = await self.retrieve_relevant_chunks(query)

            # Construct context
            context = await self.construct_context(retrieved_chunks)

            # Generate response
            response = await self.generate_response(query, context)

            # Create citations
            citations = await self.create_citations(retrieved_chunks)

            return {
                "response": response,
                "citations": [c.dict() for c in citations],
                "retrieved_chunks_count": len(retrieved_chunks)
            }
        except Exception as e:
            logging.error(f"Error in full-book RAG query: {e}")
            raise

    async def selected_text_rag_query(self, selected_text: str, question: str) -> Dict[str, Any]:
        """
        Perform a selected-text RAG query.
        """
        try:
            # Generate response using selected text as context
            response = await self.generate_response_with_selected_text(selected_text, question)

            # Create citation for the selected text
            citation = Citation(
                source_file="user_provided_text",
                title="Selected Text",
                content_snippet=selected_text[:200] + "..." if len(selected_text) > 200 else selected_text
            )

            return {
                "response": response,
                "citations": [citation.dict()]
            }
        except Exception as e:
            logging.error(f"Error in selected-text RAG query: {e}")
            raise

    async def validate_grounding(self, response: str, context: str) -> bool:
        """
        Validate that the response is grounded in the provided context.
        This is a simplified check - in production, you might want more sophisticated validation.
        """
        # For now, we'll just return True
        # In a more sophisticated implementation, you could check if key phrases
        # in the response appear in the context
        return True


# Global instance
rag_service = RAGService()