# RAG & Document Processing Boilerplate

## Overview
This boilerplate provides a foundation for RAG (Retrieval-Augmented Generation) applications and document processing systems. It's designed for 8 projects including document analysis, knowledge bases, and semantic search applications.

## 🎯 Target Projects
- Intelligent Document Processing & Knowledge Base
- AI-Powered Resume Parser & Job Matcher  
- AI-Powered Legal Document Analysis & Contract Negotiation
- Research Assistant with Document Q&A
- PDF Analysis & Summarization Tool
- Document Classification & Organization
- Multi-format Document Processor
- Knowledge Base with Vector Search

## 🏗️ Architecture

```
03_rag_document_processing/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── document.py        # Document model
│   │   ├── embedding.py       # Embedding model
│   │   └── user.py           # User model
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── document.py
│   │   └── response.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── vector_store.py
│   │   └── rag_service.py
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── documents.py
│   │   ├── search.py
│   │   └── chat.py
│   └── utils/                 # Utilities
│       ├── __init__.py
│       ├── file_processor.py
│       ├── text_extractor.py
│       └── chunking.py
├── tests/                     # Test suite
├── alembic/                   # Database migrations
├── requirements.txt           # Dependencies
├── .env.example              # Environment variables
├── docker-compose.yml        # Docker setup
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 2. Database Setup
```bash
# Initialize database
alembic upgrade head

# Create initial data
python -m app.scripts.seed_data
```

### 3. Run Application
```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔧 Core Features

### Document Processing
- **Multi-format Support**: PDF, DOCX, TXT, HTML, Markdown
- **Text Extraction**: OCR for images, table extraction
- **Chunking**: Intelligent text splitting for RAG
- **Metadata Extraction**: Author, date, title, etc.

### Vector Database Integration
- **Pinecone**: Cloud vector database
- **Weaviate**: Self-hosted option
- **Chroma**: Local development
- **Qdrant**: High-performance option

### RAG Pipeline
- **Embedding Generation**: OpenAI, Cohere, local models
- **Retrieval**: Semantic search with filters
- **Generation**: LLM integration with context
- **Caching**: Redis for performance

### API Endpoints
```
POST   /api/documents/upload     # Upload document
GET    /api/documents/           # List documents
GET    /api/documents/{id}       # Get document
DELETE /api/documents/{id}       # Delete document
POST   /api/search/              # Semantic search
POST   /api/chat/                # RAG chat
GET    /api/chat/history         # Chat history
```

## 📊 Database Schema

### Documents Table
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    file_path VARCHAR(500),
    file_type VARCHAR(50),
    file_size INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Embeddings Table
```sql
CREATE TABLE embeddings (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id),
    chunk_index INTEGER,
    chunk_text TEXT,
    embedding_vector VECTOR(1536),  -- OpenAI dimensions
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🔑 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/rag_db

# Vector Database
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=documents

# LLM APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
COHERE_API_KEY=your_cohere_key

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# Security
SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_document_service.py
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📈 Performance Optimization

### Caching Strategy
- **Redis**: Session storage, API response caching
- **Vector Cache**: Embedding similarity cache
- **Document Cache**: Frequently accessed documents

### Scaling Considerations
- **Horizontal Scaling**: Multiple API instances
- **Database Sharding**: By user or document type
- **CDN**: Static file delivery
- **Load Balancing**: Nginx or cloud load balancer

## 🔒 Security Features

- **Authentication**: JWT-based auth
- **Authorization**: Role-based access control
- **File Validation**: Type and size checking
- **Rate Limiting**: API request throttling
- **Input Sanitization**: XSS and injection prevention

## 📚 Integration Examples

### Frontend Integration
```javascript
// Upload document
const formData = new FormData();
formData.append('file', file);
const response = await fetch('/api/documents/upload', {
    method: 'POST',
    body: formData
});

// Search documents
const searchResponse = await fetch('/api/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: 'search term' })
});

// Chat with documents
const chatResponse = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'user question' })
});
```

### External API Integration
```python
# OpenAI Embeddings
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.embeddings.create(
    input="text to embed",
    model="text-embedding-3-small"
)

# Pinecone Vector Store
import pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
index = pinecone.Index("documents")
index.upsert(vectors=[{"id": "vec1", "values": embedding}])
```

## 🚀 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Vector database index created
- [ ] File storage directory exists
- [ ] SSL certificates installed
- [ ] Monitoring and logging setup
- [ ] Backup strategy implemented
- [ ] Performance testing completed

## 📞 Support

For issues and questions:
1. Check the logs: `docker-compose logs`
2. Verify environment variables
3. Test database connectivity
4. Check API key permissions

## 🔄 Updates and Maintenance

- **Regular Updates**: Keep dependencies current
- **Security Patches**: Monitor for vulnerabilities
- **Performance Monitoring**: Track response times
- **Backup Strategy**: Regular database backups
- **Scaling**: Monitor resource usage



