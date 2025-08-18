# Intelligent Document Processing & Knowledge Base

A FastAPI backend boilerplate for document processing system with knowledge base management.

## Features

- **AI-Powered Analysis**: Basic structure for OpenAI integration
- **Data Management**: Core data models for document, knowledge, processing
- **JWT Authentication**: Basic security setup
- **Ocr Technology**: Foundation for ocr technology

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- OpenAI API key

### Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables**
```bash
cp env.example .env
```

Edit `.env` with your configuration:
```env
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=postgresql://user:password@localhost/intelligent_document_processing_&_knowledge_base_db
```

3. **Initialize database**
```bash
python -c "from app.database import init_db; init_db()"
```

4. **Run the application**
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application with endpoints
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas with validation
├── database.py          # Database configuration
├── auth.py              # JWT authentication
└── config.py            # Application settings
```

## API Endpoints

- `POST /auth/login` - Authenticate user
- `POST /ai/analyze` - Analyze data with AI
- `GET /health` - Health check

## Next Steps

This is a boilerplate. Implement the TODO sections in each endpoint to add:

- Business logic for data management
- AI integration for analysis
- Database operations
- Error handling
- Additional security features

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | JWT secret key | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `DATABASE_URL` | Database connection | Yes |
| `DEBUG` | Debug mode | No |
