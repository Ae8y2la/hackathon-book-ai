# Data Model: RAG Chatbot for Docusaurus Book

## Document Entity
- **document_id**: UUID (primary key)
  - Unique identifier for each document
  - Generated automatically
- **source_file**: String (max 500 characters)
  - Path to the source file in /docs directory
  - Required field
- **title**: String (max 500 characters)
  - Title of the document
  - Extracted from markdown metadata or first heading
- **content_hash**: String (64 characters)
  - SHA-256 hash of the content
  - Used for change detection during reindexing
- **created_at**: DateTime
  - Timestamp when document was first indexed
- **updated_at**: DateTime
  - Timestamp when document was last updated

## DocumentChunk Entity
- **chunk_id**: UUID (primary key)
  - Unique identifier for each chunk
  - Generated automatically
- **document_id**: UUID (foreign key to Document)
  - References the parent document
  - Required field
- **chunk_index**: Integer
  - Sequential index of the chunk within the document
  - Used to maintain order
- **content**: Text
  - The actual text content of the chunk
  - Required field
- **embedding_id**: String (max 100 characters)
  - ID of the corresponding vector in Qdrant
  - Used to link database metadata with vector storage
- **metadata**: JSONB
  - Additional metadata about the chunk
  - Contains headers, section info, etc.
- **created_at**: DateTime
  - Timestamp when chunk was created

## ChatSession Entity
- **session_id**: UUID (primary key)
  - Unique identifier for each chat session
  - Generated automatically
- **user_id**: UUID (optional)
  - Optional identifier for the user
  - Used for tracking if needed
- **created_at**: DateTime
  - Timestamp when session was created
- **updated_at**: DateTime
  - Timestamp when session was last updated

## ChatMessage Entity
- **message_id**: UUID (primary key)
  - Unique identifier for each message
  - Generated automatically
- **session_id**: UUID (foreign key to ChatSession)
  - References the chat session this message belongs to
  - Required field
- **role**: String (enum: 'user', 'assistant')
  - Role of the message sender
  - Required field
- **content**: Text
  - The actual content of the message
  - Required field
- **citations**: JSONB
  - List of citations used in the response
  - Contains source file, title, and content snippet
- **created_at**: DateTime
  - Timestamp when message was created

## Relationships
- Document (1) → DocumentChunk (Many): One document can have many chunks
- ChatSession (1) → ChatMessage (Many): One session can have many messages

## Validation Rules
- Document.source_file must be a valid path in /docs directory
- DocumentChunk.content must not be empty
- ChatMessage.role must be either 'user' or 'assistant'
- DocumentChunk.document_id must reference an existing Document
- ChatMessage.session_id must reference an existing ChatSession

## Indexes
- Document.source_file: For efficient lookup by file path
- DocumentChunk.document_id: For efficient retrieval of chunks by document
- ChatSession.session_id: For efficient session lookup
- ChatMessage.session_id: For efficient message retrieval by session