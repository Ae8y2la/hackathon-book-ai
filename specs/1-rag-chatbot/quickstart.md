# Quickstart Guide: RAG Chatbot for Docusaurus Book

## Prerequisites
- Python 3.11+
- Access to OpenAI API key
- Qdrant Cloud account (Free Tier)
- Neon Serverless Postgres account

## Setup

### 1. Environment Configuration
```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-name>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-dotenv openai qdrant-client psycopg2-binary markdown mistune
```

### 2. Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_postgres_connection_string
```

### 3. Initialize the Application
```bash
# Start the FastAPI application
uvicorn app.main:app --reload --port 8000
```

## API Usage

### 1. Ingest Book Content
Index all markdown files from the `/docs` directory:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": false}'
```

### 2. Full-book Chat
Ask questions about the entire book content:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the key concepts in chapter 3?",
    "session_id": "optional-session-id"
  }'
```

### 3. Selected-text Chat
Ask questions based only on provided text:
```bash
curl -X POST "http://localhost:8000/chat/selection" \
  -H "Content-Type: application/json" \
  -d '{
    "selected_text": "The fundamental concept of Retrieval-Augmented Generation...",
    "question": "Can you explain this in simpler terms?",
    "session_id": "optional-session-id"
  }'
```

### 4. Health Check
Verify service status:
```bash
curl -X GET "http://localhost:8000/health"
```

## Integration with Docusaurus
To integrate with your existing Docusaurus site:

1. Deploy the FastAPI backend separately or as a service
2. Configure CORS in the FastAPI app to allow requests from your Docusaurus domain
3. Create frontend components that call the API endpoints
4. Handle responses and citations appropriately in the UI

## Example Frontend Integration
```javascript
// Example of how to call the chat endpoint from a frontend
async function askQuestion(message, sessionId = null) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      session_id: sessionId
    })
  });

  const data = await response.json();
  return data;
}
```

## Development
- The application uses async processing throughout for better performance
- All endpoints return JSON responses
- Error handling is implemented for all API calls
- Logging is configured for debugging and monitoring