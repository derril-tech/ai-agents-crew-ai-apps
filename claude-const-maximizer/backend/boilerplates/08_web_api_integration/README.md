# Web & API Integration Boilerplate

## Overview
This boilerplate provides a foundation for web scraping, API integration, data aggregation, and web automation applications. It's designed for 3 projects covering various web integration use cases.

## 🎯 Target Projects
- Web Scraping & Data Aggregation Platform
- API Integration & Workflow Automation
- Real-time Data Monitoring & Alerting System

## 🏗️ Architecture

```
08_web_api_integration/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── integration.py     # API integration model
│   │   ├── scraping_job.py    # Web scraping job model
│   │   ├── data_source.py     # Data source model
│   │   ├── workflow.py        # Workflow automation model
│   │   ├── alert.py           # Alert model
│   │   └── user.py           # User model
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── integration.py
│   │   ├── scraping.py
│   │   ├── workflow.py
│   │   ├── alert.py
│   │   └── response.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── web_scraping_service.py
│   │   ├── api_integration_service.py
│   │   ├── data_aggregation_service.py
│   │   ├── workflow_service.py
│   │   ├── monitoring_service.py
│   │   └── alert_service.py
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── integrations.py
│   │   ├── scraping.py
│   │   ├── workflows.py
│   │   ├── monitoring.py
│   │   ├── alerts.py
│   │   └── data.py
│   ├── workers/               # Background workers
│   │   ├── __init__.py
│   │   ├── scraper_worker.py
│   │   ├── api_worker.py
│   │   ├── data_processor.py
│   │   └── alert_worker.py
│   ├── scrapers/              # Web scraping engines
│   │   ├── __init__.py
│   │   ├── base_scraper.py
│   │   ├── selenium_scraper.py
│   │   ├── requests_scraper.py
│   │   ├── playwright_scraper.py
│   │   └── custom_scrapers/
│   ├── integrations/          # API integrations
│   │   ├── __init__.py
│   │   ├── base_integration.py
│   │   ├── rest_integration.py
│   │   ├── graphql_integration.py
│   │   ├── webhook_integration.py
│   │   └── custom_integrations/
│   └── utils/                 # Utilities
│       ├── __init__.py
│       ├── http_client.py
│       ├── data_parser.py
│       ├── rate_limiter.py
│       ├── proxy_manager.py
│       └── data_validator.py
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
# Edit .env with your API keys and integration settings
```

### 2. Database Setup
```bash
# Initialize database
alembic upgrade head

# Create initial data
python -m app.scripts.seed_data

# Set up demo integrations
python -m app.scripts.setup_demo_integrations
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

### Web Scraping
- **Multi-Engine Support**: Selenium, Playwright, Requests, Scrapy
- **Dynamic Content**: JavaScript rendering and interaction
- **Rate Limiting**: Intelligent request throttling
- **Proxy Management**: Rotating proxy support
- **Data Extraction**: Structured data parsing and validation
- **Anti-Detection**: Browser fingerprinting and evasion

### API Integration
- **REST APIs**: Standard REST API integration
- **GraphQL**: GraphQL query and mutation support
- **Webhooks**: Real-time webhook processing
- **Authentication**: OAuth, API keys, JWT support
- **Rate Limiting**: API rate limit management
- **Error Handling**: Robust error handling and retry logic

### Data Aggregation
- **Multi-Source**: Combine data from multiple sources
- **Data Transformation**: ETL pipeline for data processing
- **Data Validation**: Schema validation and data quality checks
- **Data Storage**: Structured storage with indexing
- **Data Export**: Multiple export formats (JSON, CSV, Excel)
- **Real-time Processing**: Stream processing capabilities

### Workflow Automation
- **Visual Workflows**: Drag-and-drop workflow builder
- **Conditional Logic**: If-then-else workflow conditions
- **Scheduling**: Cron-based and event-driven scheduling
- **Error Recovery**: Automatic retry and error handling
- **Monitoring**: Real-time workflow monitoring
- **Versioning**: Workflow version control

### Real-time Monitoring
- **Data Monitoring**: Real-time data change detection
- **Performance Monitoring**: API response time tracking
- **Availability Monitoring**: Uptime and health checks
- **Threshold Alerts**: Configurable alert thresholds
- **Trend Analysis**: Historical data analysis
- **Dashboard**: Real-time monitoring dashboard

### Alert System
- **Multi-Channel**: Email, SMS, Slack, Discord, webhook alerts
- **Escalation**: Alert escalation rules
- **Templates**: Customizable alert templates
- **Grouping**: Alert grouping and deduplication
- **Acknowledgment**: Alert acknowledgment system
- **History**: Complete alert history tracking

### API Endpoints
```
POST   /api/integrations/          # Create integration
GET    /api/integrations/          # List integrations
GET    /api/integrations/{id}      # Get integration details
PUT    /api/integrations/{id}      # Update integration
DELETE /api/integrations/{id}      # Delete integration

POST   /api/scraping/jobs          # Create scraping job
GET    /api/scraping/jobs          # List scraping jobs
GET    /api/scraping/jobs/{id}     # Get job details
PUT    /api/scraping/jobs/{id}     # Update job
DELETE /api/scraping/jobs/{id}     # Delete job

POST   /api/workflows/             # Create workflow
GET    /api/workflows/             # List workflows
GET    /api/workflows/{id}         # Get workflow details
PUT    /api/workflows/{id}         # Update workflow
POST   /api/workflows/{id}/run     # Run workflow

GET    /api/monitoring/status      # Get monitoring status
GET    /api/monitoring/metrics     # Get monitoring metrics
POST   /api/monitoring/check       # Run health check

POST   /api/alerts/                # Create alert
GET    /api/alerts/                # List alerts
GET    /api/alerts/{id}            # Get alert details
PUT    /api/alerts/{id}/acknowledge # Acknowledge alert

GET    /api/data/                  # Get aggregated data
POST   /api/data/export            # Export data
GET    /api/data/sources           # List data sources
```

## 📊 Database Schema

### Integrations Table
```sql
CREATE TABLE integrations (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50), -- rest, graphql, webhook, scraping
    config JSONB NOT NULL,
    authentication JSONB,
    rate_limits JSONB,
    status VARCHAR(50) DEFAULT 'active',
    last_sync_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);
```

### Scraping Jobs Table
```sql
CREATE TABLE scraping_jobs (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(500),
    scraper_type VARCHAR(50), -- selenium, playwright, requests
    selectors JSONB,
    data_schema JSONB,
    schedule VARCHAR(100), -- cron expression
    status VARCHAR(50) DEFAULT 'pending',
    last_run_at TIMESTAMP,
    next_run_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);
```

### Data Sources Table
```sql
CREATE TABLE data_sources (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50), -- api, scraping, webhook
    source_url VARCHAR(500),
    data_format VARCHAR(50), -- json, xml, csv, html
    schema JSONB,
    refresh_interval INTEGER, -- seconds
    last_refresh_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Workflows Table
```sql
CREATE TABLE workflows (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    steps JSONB NOT NULL,
    triggers JSONB,
    schedule VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active',
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);
```

### Alerts Table
```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    alert_type VARCHAR(50), -- threshold, anomaly, availability
    conditions JSONB NOT NULL,
    channels JSONB, -- email, sms, slack, webhook
    status VARCHAR(50) DEFAULT 'active',
    last_triggered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);
```

### Monitoring Data Table
```sql
CREATE TABLE monitoring_data (
    id UUID PRIMARY KEY,
    source_id UUID REFERENCES data_sources(id),
    metric_name VARCHAR(100),
    metric_value DECIMAL(15,2),
    timestamp TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);
```

## 🔑 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/webapi_db

# Web Scraping
SELENIUM_DRIVER_PATH=/path/to/chromedriver
PLAYWRIGHT_BROWSER_PATH=/path/to/browser
SCRAPY_SETTINGS_MODULE=app.scrapers.settings

# Proxy Configuration
PROXY_LIST_URL=your_proxy_list_url
PROXY_USERNAME=your_proxy_username
PROXY_PASSWORD=your_proxy_password

# API Integration
API_RATE_LIMIT_DEFAULT=100
API_RATE_LIMIT_WINDOW=3600
API_TIMEOUT_DEFAULT=30

# External APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token

# Email and Notifications
SMTP_HOST=your_smtp_host
SMTP_PORT=587
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
SLACK_WEBHOOK_URL=your_slack_webhook
DISCORD_WEBHOOK_URL=your_discord_webhook

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
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Monitoring
MONITORING_INTERVAL=300  # 5 minutes
ALERT_COOLDOWN=3600      # 1 hour
MAX_RETRY_ATTEMPTS=3
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_web_scraping_service.py

# Test API integrations
pytest tests/test_api_integration_service.py

# Test monitoring
pytest tests/test_monitoring_service.py
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
- **Redis**: API responses, scraping results, workflow state
- **CDN**: Static assets and cached data
- **Database Cache**: Frequently accessed integration data

### Scaling Considerations
- **Horizontal Scaling**: Multiple API instances
- **Worker Scaling**: Multiple Celery workers for scraping
- **Database Sharding**: By integration type or region
- **Load Balancing**: Nginx or cloud load balancer

## 🔒 Security Features

- **Authentication**: JWT-based auth with role-based access
- **API Security**: Rate limiting and input validation
- **Data Encryption**: Sensitive integration data
- **Proxy Security**: Secure proxy management
- **Audit Logging**: Complete integration and scraping tracking
- **Access Control**: Integration-level permissions

## 📚 Integration Examples

### Frontend Integration
```javascript
// Create scraping job
const job = await fetch('/api/scraping/jobs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'News Scraper',
        url: 'https://news.example.com',
        scraper_type: 'playwright',
        selectors: {
            title: '.article-title',
            content: '.article-content',
            date: '.article-date'
        },
        schedule: '0 */6 * * *' // Every 6 hours
    })
});

// Create workflow
const workflow = await fetch('/api/workflows/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'Data Pipeline',
        steps: [
            {
                type: 'scrape',
                job_id: job.id
            },
            {
                type: 'transform',
                operation: 'clean_data'
            },
            {
                type: 'store',
                destination: 'database'
            }
        ],
        triggers: ['schedule', 'webhook']
    })
});

// Set up monitoring
const monitoring = await fetch('/api/monitoring/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        source_id: source.id,
        metrics: ['response_time', 'availability', 'data_quality']
    })
});
```

### External API Integration
```python
# REST API Integration
import requests
response = requests.get(
    'https://api.example.com/data',
    headers={'Authorization': f'Bearer {api_key}'},
    timeout=30
)

# GraphQL Integration
import gql
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(url='https://api.example.com/graphql')
client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
    query GetData($id: ID!) {
        data(id: $id) {
            id
            name
            value
        }
    }
""")

result = client.execute(query, variable_values={'id': '123'})

# Webhook Processing
from flask import Flask, request
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Process webhook data
    process_webhook_data(data)
    return {'status': 'success'}, 200
```

## 🚀 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Proxy configuration set up
- [ ] SSL certificates installed
- [ ] Monitoring and logging setup
- [ ] Backup strategy implemented
- [ ] Performance testing completed
- [ ] Security audit completed
- [ ] Rate limiting configured
- [ ] Alert system tested

## 📞 Support

For issues and questions:
1. Check the logs: `docker-compose logs`
2. Verify API key permissions
3. Test proxy connections
4. Check worker status: `celery -A app.workers.celery_app inspect active`

## 🔄 Updates and Maintenance

- **Regular Updates**: Keep dependencies current
- **Security Patches**: Monitor for vulnerabilities
- **Proxy Updates**: Keep proxy lists updated
- **Performance Monitoring**: Track scraping performance
- **Backup Strategy**: Regular database backups
- **Scaling**: Monitor resource usage

