# RAG Chatbot Backend Deployment Guide

This guide provides instructions for deploying the RAG Chatbot backend to production.

## Prerequisites

- Python 3.11+
- OpenAI API key
- Qdrant Cloud account (Free Tier) or self-hosted Qdrant instance
- PostgreSQL database (Neon Serverless recommended)
- Access to the `/docs` directory with book content

## Deployment Options

### Option 1: Cloud Deployment (Recommended)

#### Deploy to Railway

1. **Prepare your Railway project**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login to Railway
   railway login
   ```

2. **Create a new Railway project**:
   ```bash
   railway init
   ```

3. **Set environment variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_api_key
   railway variables set QDRANT_URL=your_qdrant_cluster_url
   railway variables set QDRANT_API_KEY=your_qdrant_api_key
   railway variables set DATABASE_URL=your_postgres_connection_string
   railway variables set DOCS_DIR_PATH=/app/docs
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

#### Deploy to Render

1. **Create a Render Web Service**:
   - Go to https://render.com
   - Click "New +" and select "Web Service"
   - Connect to your GitHub repository
   - Set the following environment variables in the Render dashboard:
     - `OPENAI_API_KEY`
     - `QDRANT_URL`
     - `QDRANT_API_KEY`
     - `DATABASE_URL`

2. **Configuration**:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Deploy to Heroku

1. **Install Heroku CLI**:
   ```bash
   # Install Heroku CLI and login
   heroku login
   ```

2. **Create app and set config vars**:
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set QDRANT_URL=your_qdrant_cluster_url
   heroku config:set QDRANT_API_KEY=your_qdrant_api_key
   heroku config:set DATABASE_URL=your_postgres_connection_string
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```

### Option 2: Self-Hosting

#### Using Docker

1. **Create a Dockerfile**:
   ```Dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and run**:
   ```bash
   # Build the image
   docker build -t rag-chatbot-backend .

   # Run the container
   docker run -d \
     --name rag-chatbot \
     -p 8000:8000 \
     -e OPENAI_API_KEY=your_openai_api_key \
     -e QDRANT_URL=your_qdrant_cluster_url \
     -e QDRANT_API_KEY=your_qdrant_api_key \
     -e DATABASE_URL=your_postgres_connection_string \
     -e DOCS_DIR_PATH=/app/docs \
     -v /path/to/your/docs:/app/docs \
     rag-chatbot-backend
   ```

#### Using PM2 (Node.js process manager)

1. **Install PM2**:
   ```bash
   npm install -g pm2
   ```

2. **Create ecosystem.config.js**:
   ```javascript
   module.exports = {
     apps: [{
       name: 'rag-chatbot-backend',
       script: 'uvicorn',
       args: 'app.main:app --host 0.0.0.0 --port 8000',
       interpreter: 'python',
       env: {
         NODE_ENV: 'production',
         OPENAI_API_KEY: 'your_openai_api_key',
         QDRANT_URL: 'your_qdrant_cluster_url',
         QDRANT_API_KEY: 'your_qdrant_api_key',
         DATABASE_URL: 'your_postgres_connection_string',
         DOCS_DIR_PATH: './docs'
       }
     }]
   };
   ```

3. **Start the application**:
   ```bash
   pm2 start ecosystem.config.js
   ```

## Environment Configuration

Create a `.env.production` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_production_openai_api_key

# Qdrant Configuration
QDRANT_URL=your_production_qdrant_url
QDRANT_API_KEY=your_production_qdrant_api_key
QDRANT_COLLECTION_NAME=book_content_chunks

# Database Configuration
DATABASE_URL=your_production_postgres_url

# Application Configuration
APP_TITLE=RAG Chatbot for Docusaurus Book
APP_VERSION=1.0.0
DEBUG=False
DOCS_DIR_PATH=/app/docs
```

## Initial Setup

After deployment, you need to index your documentation:

1. **Upload your documentation** to the `/docs` directory accessible by the application

2. **Run the ingestion endpoint** to index all documents:
   ```bash
   curl -X POST "https://your-deployment-url/api/v1/ingest" \
     -H "Content-Type: application/json" \
     -d '{"force_reindex": true}'
   ```

## Production Considerations

### Security

- Use HTTPS in production
- Set `DEBUG=False` in production
- Use strong, unique API keys
- Implement rate limiting
- Validate and sanitize all inputs

### Performance

- Use a production ASGI server (like Uvicorn with Gunicorn)
- Implement caching where appropriate
- Monitor response times
- Optimize database queries

### Monitoring

- Set up logging to a centralized service
- Monitor API usage and performance
- Set up alerts for errors
- Track user engagement metrics

### Scaling

- Use connection pooling for database and vector store
- Consider horizontal scaling for high traffic
- Implement proper load balancing
- Use CDN for static assets if needed

## Health Checks

The application provides a health check endpoint:
- `GET /health` - Returns service status and connected services

## API Documentation

After deployment, API documentation is available at:
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify `DATABASE_URL` is correct
   - Check that the database is accessible
   - Ensure proper database permissions

2. **Qdrant Connection Issues**:
   - Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct
   - Check that the Qdrant service is running
   - Ensure proper network access

3. **OpenAI API Issues**:
   - Verify `OPENAI_API_KEY` is correct
   - Check API usage limits
   - Ensure proper billing setup

4. **Document Ingestion Issues**:
   - Verify the `/docs` directory exists and is accessible
   - Check that markdown files have proper format
   - Ensure sufficient memory for large documents

### Logging

Check application logs for detailed error information:
- For cloud deployments, check the platform's log interface
- For self-hosted, check the application logs
- Look for error messages with timestamps

## Rollback Procedure

To rollback to a previous version:
1. For cloud platforms, use the platform's deployment history
2. For Docker, redeploy a previous image tag
3. For manual deployments, revert to a previous commit and redeploy

## Maintenance

### Regular Tasks

1. **Monitor API usage** and performance metrics
2. **Update dependencies** regularly for security patches
3. **Backup database** and vector store regularly
4. **Review logs** for errors and performance issues
5. **Update documentation** as needed

### Updating Documentation

To re-index updated documentation:
```bash
curl -X POST "https://your-deployment-url/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": true}'
```

## Support

For deployment issues, check:
- Application logs for error details
- Platform-specific documentation
- The main README.md for configuration details
- Open an issue in the repository if you encounter bugs