# Implementation Plan: RAG Chatbot for Docusaurus Book

**Feature**: 1-rag-chatbot
**Created**: 2025-12-16
**Status**: Draft
**Author**: Claude

## Technical Context

### Architecture Overview
The RAG chatbot backend will be built using FastAPI with async capabilities to handle concurrent user requests. The system will index book content from the /docs directory and store embeddings in Qdrant for semantic search. Metadata will be stored in Neon Postgres, and the system will provide two query modes: full-book search and selected-text search.

### Core Components
- **Ingestion Pipeline**: Processes Markdown files from /docs directory
- **Vector Store**: Qdrant collection for semantic search
- **Metadata Store**: Neon Postgres for document metadata
- **API Layer**: FastAPI endpoints for ingestion and chat functionality
- **RAG Service**: Core logic for retrieval and generation

### Dependencies
- Python 3.11+
- FastAPI
- OpenAI SDK
- Qdrant
- Postgres/Neon
- Markdown processing libraries

### Integration Points
- Existing Docusaurus site (backend integration)
- /docs directory for content ingestion
- OpenAI API for generation

## Constitution Check

### Grounded Answers
- Implementation must ensure responses are strictly from indexed book content
- No external knowledge sources allowed
- System must reject queries requiring external information

### Retrieval Accuracy
- Semantic search must provide accurate document retrieval
- All responses must include proper source citations
- Citation system must link to specific document sections

### Student Clarity
- Responses must be clear and well-structured
- Technical precision maintained while avoiding unnecessary jargon
- User-friendly error messages

### Reproducible Ingestion
- Ingestion pipeline must be deterministic
- Indexing process must be repeatable
- Version control for indexing process

### Backend Engineering Rigor
- Async processing throughout
- Proper error handling and logging
- Production-ready code quality
- Clean integration with existing Docusaurus infrastructure

## Gates

### Gate 1: Architecture Compliance
✅ Architecture supports all required features (full-book RAG, selected-text RAG, citations)

### Gate 2: Constitution Alignment
✅ All constitution principles addressed in design

### Gate 3: Technical Feasibility
✅ Technology stack supports requirements

## Phase 0: Research & Unknowns Resolution

### Research Tasks

#### 1. RAG Architecture Patterns
**Decision**: Implement a standard RAG architecture with document chunking, embedding, and retrieval-augmented generation
**Rationale**: Proven pattern for document-based question answering systems
**Alternatives considered**: Simple keyword search, full-text search engines

#### 2. Document Chunking Strategy
**Decision**: Use semantic chunking with overlap to preserve context while enabling precise citations
**Rationale**: Better retrieval quality than fixed-size chunking for book content
**Alternatives considered**: Fixed-size chunks, paragraph-based chunks

#### 3. Vector Database Selection
**Decision**: Qdrant for vector storage with Neon Postgres for metadata
**Rationale**: Qdrant provides efficient similarity search with good Python integration; Postgres handles structured metadata
**Alternatives considered**: Pinecone, Weaviate, Chroma

#### 4. Markdown Processing
**Decision**: Use markdown and mistune libraries to extract content while preserving structure
**Rationale**: Standard libraries with good performance and compatibility
**Alternatives considered**: BeautifulSoup for HTML conversion, custom parsers

## Phase 1: Data Model & API Contracts

### Data Model (data-model.md)

#### Document Entity
- **document_id**: UUID (primary key)
- **source_file**: String (path in /docs)
- **title**: String (document title)
- **content_hash**: String (for change detection)
- **created_at**: DateTime
- **updated_at**: DateTime

#### DocumentChunk Entity
- **chunk_id**: UUID (primary key)
- **document_id**: UUID (foreign key to Document)
- **chunk_index**: Integer (order in document)
- **content**: Text (the chunk text)
- **embedding_id**: String (Qdrant point ID)
- **metadata**: JSON (source location, headers, etc.)
- **created_at**: DateTime

#### ChatSession Entity
- **session_id**: UUID (primary key)
- **user_id**: UUID (optional, for tracking)
- **created_at**: DateTime
- **updated_at**: DateTime

#### ChatMessage Entity
- **message_id**: UUID (primary key)
- **session_id**: UUID (foreign key to ChatSession)
- **role**: String (user/assistant)
- **content**: Text
- **citations**: JSON (references to document chunks)
- **created_at**: DateTime

### API Contracts

#### Ingestion Endpoint: POST /ingest
```
Request:
{
  "force_reindex": boolean (optional, default false)
}

Response:
{
  "status": "success" | "error",
  "processed_files": integer,
  "indexed_chunks": integer,
  "message": string
}
```

#### Full-book Chat Endpoint: POST /chat
```
Request:
{
  "message": string,
  "session_id": string (optional)
}

Response:
{
  "response": string,
  "session_id": string,
  "citations": [
    {
      "source_file": string,
      "title": string,
      "content_snippet": string
    }
  ]
}
```

#### Selected-text Chat Endpoint: POST /chat/selection
```
Request:
{
  "selected_text": string,
  "question": string,
  "session_id": string (optional)
}

Response:
{
  "response": string,
  "session_id": string,
  "citations": [
    {
      "source_file": string,
      "title": string,
      "content_snippet": string
    }
  ]
}
```

#### Health Check Endpoint: GET /health
```
Response:
{
  "status": "healthy",
  "timestamp": string,
  "services": {
    "database": "connected",
    "vector_store": "connected",
    "openai_api": "reachable"
  }
}
```

## Phase 2: Implementation Architecture

### Backend Architecture Overview
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Docusaurus    │    │   FastAPI App    │    │   External      │
│    Frontend     │◄──►│   (Backend)      │◄──►│   Services      │
└─────────────────┘    │                  │    │                 │
                       │  ┌─────────────┐  │    │  ┌──────────┐   │
                       │  │  API Layer  │  │    │  │ OpenAI   │   │
                       │  └─────────────┘  │    │  │ API      │   │
                       │         │         │    │  └──────────┘   │
                       │  ┌─────────────┐  │    │  ┌──────────┐   │
                       │  │ RAG Service │  │    │  │ Qdrant   │   │
                       │  └─────────────┘  │    │  │ Vector   │   │
                       │         │         │    │  │ Store    │   │
                       │  ┌─────────────┐  │    │  └──────────┘   │
                       │  │ Data Layer  │  │    │  ┌──────────┐   │
                       │  └─────────────┘  │    │  │ Neon     │   │
                       └──────────────────┘    │  │ Postgres │   │
                                               │  └──────────┘   │
                                               └─────────────────┘
```

### FastAPI App Structure
```
app/
├── main.py                 # Application entry point
├── config/                 # Configuration settings
│   └── settings.py
├── api/                    # API routes
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── chat.py         # Chat endpoints
│   │   └── ingestion.py    # Ingestion endpoints
├── services/               # Business logic
│   ├── __init__.py
│   ├── rag_service.py      # Core RAG functionality
│   ├── ingestion_service.py # Document processing
│   └── chat_service.py     # Chat session management
├── models/                 # Data models
│   ├── __init__.py
│   ├── document.py         # Document entities
│   └── chat.py             # Chat entities
├── database/               # Database operations
│   ├── __init__.py
│   ├── postgres.py         # Postgres connections
│   └── schemas.py          # Database schemas
├── vector_store/           # Vector store operations
│   ├── __init__.py
│   └── qdrant_client.py    # Qdrant operations
└── utils/                  # Utility functions
    ├── __init__.py
    ├── markdown_parser.py  # Markdown processing
    └── validators.py       # Input validation
```

### Markdown Ingestion Pipeline
1. **Discovery**: Scan /docs directory for .md files
2. **Parsing**: Extract content while preserving structure and metadata
3. **Chunking**: Split documents into semantic chunks with overlap
4. **Embedding**: Generate embeddings for each chunk
5. **Storage**: Store embeddings in Qdrant, metadata in Postgres
6. **Indexing**: Create searchable index with document relationships

### Qdrant Collection Design
- **Collection Name**: `book_content_chunks`
- **Vector Size**: 1536 (OpenAI ada-002 embeddings)
- **Payload Schema**:
  ```json
  {
    "document_id": "string",
    "source_file": "string",
    "chunk_index": "integer",
    "title": "string",
    "content": "string",
    "metadata": {
      "headers": ["string"],
      "section": "string"
    }
  }
  ```

### Neon Postgres Schema
```sql
-- Documents table
CREATE TABLE documents (
    document_id UUID PRIMARY KEY,
    source_file VARCHAR(500) NOT NULL,
    title VARCHAR(500),
    content_hash VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document chunks table
CREATE TABLE document_chunks (
    chunk_id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(document_id),
    chunk_index INTEGER,
    content TEXT,
    embedding_id VARCHAR(100), -- Qdrant point ID
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat sessions table
CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY,
    user_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages table
CREATE TABLE chat_messages (
    message_id UUID PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id),
    role VARCHAR(10) CHECK (role IN ('user', 'assistant')),
    content TEXT,
    citations JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints Implementation

#### 1. Ingestion Endpoint (`/ingest`)
- Discovers all .md files in /docs directory
- Processes each file to extract content and metadata
- Chunks documents semantically
- Generates embeddings for each chunk
- Stores embeddings in Qdrant with document_id reference
- Stores metadata in Postgres
- Returns processing statistics

#### 2. Full-book Chat Endpoint (`/chat`)
- Accepts user message and optional session_id
- Generates embeddings for user query
- Searches Qdrant for relevant document chunks
- Constructs context from retrieved chunks
- Sends context + query to OpenAI API
- Formats response with citations
- Stores conversation in database
- Returns response with session_id and citations

#### 3. Selected-text Chat Endpoint (`/chat/selection`)
- Accepts selected text and question
- Uses provided text as context (no vector search)
- Sends selected text + question to OpenAI API
- Returns response with citation to the provided text
- Stores conversation in database

#### 4. Health Check Endpoint (`/health`)
- Checks connectivity to Postgres
- Checks connectivity to Qdrant
- Checks connectivity to OpenAI API
- Returns overall health status

## Phase 3: Implementation Approach

### Implementation Order
1. **Setup & Configuration**: Environment, dependencies, basic FastAPI structure
2. **Database Layer**: Postgres schemas and connection setup
3. **Vector Store**: Qdrant collection setup and client
4. **Data Models**: Pydantic models and database models
5. **Ingestion Pipeline**: Markdown processing and indexing
6. **RAG Service**: Core retrieval and generation logic
7. **API Endpoints**: Chat and ingestion endpoints
8. **Testing**: Unit and integration tests
9. **Documentation**: API docs and deployment guide

### Risk Mitigation
- **Large Document Processing**: Implement chunking with overlap to handle long documents
- **API Rate Limits**: Implement caching and rate limiting
- **Data Consistency**: Use transactions for related operations
- **Performance**: Async processing throughout, connection pooling

## Compliance Verification

### Constitution Alignment Check
✅ Grounded Answers: System only responds with content from indexed documents
✅ Retrieval Accuracy: Proper citation system implemented
✅ Student Clarity: Responses structured for educational use
✅ Reproducible Ingestion: Deterministic indexing process
✅ Backend Engineering Rigor: Async, error handling, production practices

### Success Criteria Mapping
- **SC-001**: 3-second response time through async processing and optimized retrieval
- **SC-002**: 95% citation accuracy via mandatory citation system
- **SC-003**: 90% relevant answers through proper grounding enforcement
- **SC-004**: Both query modes supported as separate endpoints
- **SC-005**: Service availability through proper error handling and monitoring

## Next Steps
1. Implement Phase 1 deliverables (data model, contracts)
2. Begin Phase 2 implementation following architecture
3. Create detailed task breakdown for development
4. Set up development environment and dependencies