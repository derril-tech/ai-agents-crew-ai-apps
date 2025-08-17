# Creative AI & Content Generation Boilerplate

## Overview
This boilerplate provides a foundation for creative AI applications including video generation, image creation, content writing, and multimedia processing. It's designed for 7 projects covering various creative AI use cases.

## 🎯 Target Projects
- AI-Powered Video Content Generator
- AI Image Generation & Editing Platform
- Creative Writing Assistant & Story Generator
- Social Media Content Creator
- Podcast & Audio Content Generator
- Marketing Copy & Ad Generator
- Creative Portfolio Builder

## 🏗️ Architecture

```
04_creative_ai_content_gen/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── project.py         # Creative project model
│   │   ├── asset.py           # Media asset model
│   │   ├── generation.py      # Generation job model
│   │   └── user.py           # User model
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── generation.py
│   │   └── response.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── video_service.py
│   │   ├── image_service.py
│   │   ├── audio_service.py
│   │   ├── text_service.py
│   │   └── generation_service.py
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── projects.py
│   │   ├── video.py
│   │   ├── image.py
│   │   ├── audio.py
│   │   └── text.py
│   ├── workers/               # Background workers
│   │   ├── __init__.py
│   │   ├── video_worker.py
│   │   ├── image_worker.py
│   │   └── audio_worker.py
│   └── utils/                 # Utilities
│       ├── __init__.py
│       ├── media_processor.py
│       ├── prompt_builder.py
│       ├── file_handler.py
│       └── quality_checker.py
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

# Start background workers
celery -A app.workers.celery_app worker --loglevel=info
```

## 🔧 Core Features

### Video Generation
- **Text-to-Video**: OpenAI Sora, Runway ML, Pika Labs
- **Video Editing**: FFmpeg integration, transitions, effects
- **Subtitle Generation**: Automatic caption creation
- **Video Enhancement**: Upscaling, color correction
- **Batch Processing**: Multiple video generation

### Image Generation
- **Text-to-Image**: DALL-E, Midjourney, Stable Diffusion
- **Image Editing**: Inpainting, outpainting, style transfer
- **Image Enhancement**: Upscaling, denoising, color correction
- **Batch Generation**: Multiple variations
- **Style Transfer**: Apply artistic styles

### Audio Generation
- **Text-to-Speech**: ElevenLabs, OpenAI TTS, Coqui TTS
- **Voice Cloning**: Custom voice training
- **Audio Editing**: Noise reduction, effects, mixing
- **Music Generation**: AI music composition
- **Podcast Generation**: Full episode creation

### Content Writing
- **Copywriting**: Marketing copy, ads, social media
- **Story Generation**: Creative writing, narratives
- **Content Planning**: Editorial calendars, topics
- **SEO Optimization**: Keyword integration
- **Tone Adaptation**: Formal, casual, professional

### API Endpoints
```
POST   /api/projects/              # Create project
GET    /api/projects/              # List projects
GET    /api/projects/{id}          # Get project
PUT    /api/projects/{id}          # Update project
DELETE /api/projects/{id}          # Delete project

POST   /api/video/generate         # Generate video
GET    /api/video/{id}/status      # Check status
GET    /api/video/{id}/download    # Download video

POST   /api/image/generate         # Generate image
GET    /api/image/{id}/status      # Check status
GET    /api/image/{id}/download    # Download image

POST   /api/audio/generate         # Generate audio
GET    /api/audio/{id}/status      # Check status
GET    /api/audio/{id}/download    # Download audio

POST   /api/text/generate          # Generate text
GET    /api/text/history           # Text history
```

## 📊 Database Schema

### Projects Table
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    project_type VARCHAR(50), -- video, image, audio, text
    status VARCHAR(50), -- draft, processing, completed, failed
    settings JSONB, -- generation parameters
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Assets Table
```sql
CREATE TABLE assets (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    asset_type VARCHAR(50), -- video, image, audio, text
    file_path VARCHAR(500),
    file_size INTEGER,
    duration INTEGER, -- for video/audio
    dimensions VARCHAR(50), -- for images
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Generation Jobs Table
```sql
CREATE TABLE generation_jobs (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    job_type VARCHAR(50), -- video, image, audio, text
    status VARCHAR(50), -- queued, processing, completed, failed
    progress INTEGER DEFAULT 0, -- 0-100
    result_url VARCHAR(500),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

## 🔑 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/creative_ai_db

# AI APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
ELEVENLABS_API_KEY=your_elevenlabs_key
REPLICATE_API_KEY=your_replicate_key
RUNWAY_API_KEY=your_runway_key

# Video APIs
PIKA_API_KEY=your_pika_key
STABILITY_API_KEY=your_stability_key

# Image APIs
MIDJOURNEY_API_KEY=your_midjourney_key
DALLE_API_KEY=your_openai_key

# Storage
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket_name
AWS_REGION=us-west-2

# Redis (for Celery)
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=524288000  # 500MB
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_video_service.py

# Test background workers
celery -A app.workers.celery_app worker --loglevel=info &
pytest tests/test_workers.py
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Scale workers
docker-compose up --scale worker=3
```

## 📈 Performance Optimization

### Caching Strategy
- **Redis**: Job queue, result caching, session storage
- **CDN**: Static asset delivery
- **File Cache**: Frequently accessed media files

### Scaling Considerations
- **Horizontal Scaling**: Multiple API instances
- **Worker Scaling**: Multiple Celery workers
- **Database Sharding**: By user or project type
- **Load Balancing**: Nginx or cloud load balancer

## 🔒 Security Features

- **Authentication**: JWT-based auth
- **Authorization**: Role-based access control
- **File Validation**: Type and size checking
- **Rate Limiting**: API request throttling
- **Content Filtering**: NSFW detection
- **Watermarking**: Automatic content protection

## 📚 Integration Examples

### Frontend Integration
```javascript
// Create video generation project
const project = await fetch('/api/projects/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        title: 'My Video Project',
        project_type: 'video',
        settings: {
            prompt: 'A beautiful sunset over mountains',
            duration: 10,
            style: 'cinematic'
        }
    })
});

// Generate video
const generation = await fetch('/api/video/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        project_id: project.id,
        prompt: 'A beautiful sunset over mountains',
        duration: 10
    })
});

// Check status
const status = await fetch(`/api/video/${generation.id}/status`);
```

### External API Integration
```python
# OpenAI Video Generation
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.videos.generate(
    model="sora",
    prompt="A beautiful sunset over mountains",
    duration=10
)

# ElevenLabs Audio Generation
import elevenlabs
elevenlabs.set_api_key(os.getenv("ELEVENLABS_API_KEY"))
audio = elevenlabs.generate(
    text="Hello, this is a test audio generation",
    voice="Josh"
)

# Replicate Image Generation
import replicate
output = replicate.run(
    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    input={"prompt": "A beautiful landscape painting"}
)
```

## 🚀 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Redis server running
- [ ] Celery workers started
- [ ] File storage configured
- [ ] SSL certificates installed
- [ ] Monitoring and logging setup
- [ ] Backup strategy implemented
- [ ] Performance testing completed
- [ ] Content filtering enabled

## 📞 Support

For issues and questions:
1. Check the logs: `docker-compose logs`
2. Verify environment variables
3. Test API key permissions
4. Check worker status: `celery -A app.workers.celery_app inspect active`

## 🔄 Updates and Maintenance

- **Regular Updates**: Keep dependencies current
- **Security Patches**: Monitor for vulnerabilities
- **Performance Monitoring**: Track generation times
- **Backup Strategy**: Regular database backups
- **Scaling**: Monitor resource usage
- **Content Moderation**: Regular filter updates

