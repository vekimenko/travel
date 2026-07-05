# Backend - Interactive Article Conversation System

## Overview

FastAPI backend for the Interactive Article Conversation System. Handles article ingestion, segment parsing, question generation, session management, response evaluation, and analytics.

## Project Structure

```
backend/
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/# API endpoints
│   ├── core/             # Configuration & utilities
│   ├── db/               # Database setup
│   └── main.py           # FastAPI app factory
├── migrations/           # Alembic migrations
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Poetry configuration
├── .env.example         # Environment variables template
└── main.py             # Entry point
```

## Setup

### 1. Install Dependencies

Using pip:
```bash
cd backend
pip install -r requirements.txt
```

Or using poetry:
```bash
poetry install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

### 3. Database Setup

**Option A: Using migrations (recommended)**
```bash
alembic upgrade head
```

**Option B: Auto-create tables (development only)**
Tables are created automatically when the app starts with `ENVIRONMENT=development`.

### 4. Download NLP Models

```bash
# SpaCy model for entity extraction
python -m spacy download en_core_web_sm

# Sentence transformer model for embeddings
# Downloaded automatically on first use
```

## Running the Server

```bash
# Development mode with auto-reload
python main.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/unit/test_models.py

# Run with verbose output
pytest -v
```

## Database

### Models

- **Article**: Parsed articles with metadata
- **Segment**: Content segments within articles
- **Question**: Questions for each segment
- **User**: User accounts (optional)
- **Session**: User reading sessions
- **UserResponse**: Captured user responses
- **AnalyticsEvent**: Event stream for analytics
- **AnalyticsAggregation**: Pre-computed statistics

### Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

## Services

### ArticleProcessor
- Parse articles in multiple formats (txt, md, html)
- Segment into logical chunks
- Extract entities and keywords
- Classify segment types

### QuestionGenerator
- Generate questions for segments
- Template-based and AI-powered strategies
- Difficulty adaptation
- Quality validation

### SessionManager
- Track user progress
- Auto-save sessions
- Calculate statistics
- Handle resumption

### ResponseEvaluator
- Validate user responses
- Score accuracy using semantic similarity
- Generate feedback
- Track engagement

### AnalyticsEngine
- Collect analytics events
- Aggregate metrics
- Generate reports
- Detect anomalies

## Configuration

Edit `app/core/config.py` or set environment variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/db

# API
API_V1_STR=/api/v1
PROJECT_NAME=Interactive Article System
SECRET_KEY=your-secret-key

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# External APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...

# Redis
REDIS_URL=redis://localhost:6379/0

# NLP
SPACY_MODEL=en_core_web_sm
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
```

## Development

### Code Quality

```bash
# Format code with black
black app/ tests/

# Check style with flake8
flake8 app/ tests/

# Type checking with mypy
mypy app/
```

### Git Hooks (optional)

Pre-commit hooks for code quality:
```bash
pip install pre-commit
pre-commit install
```

## Deployment

### Docker

Build Docker image:
```bash
docker build -t interactive-article-backend .
```

Run container:
```bash
docker run -p 8000:8000 --env-file .env interactive-article-backend
```

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set up proper CORS origins
- [ ] Enable HTTPS/SSL
- [ ] Set up logging and monitoring
- [ ] Configure database backups
- [ ] Set up error tracking (Sentry, etc.)

## Next Steps

1. **Implement Article Ingestion** (Feature 01)
   - Text parsing and segmentation
   - Entity extraction
   - Segment classification

2. **Implement Question Generation** (Feature 02)
   - Template library
   - Template selection engine
   - Question validation

3. **Implement Backend APIs** (Feature 07)
   - Article management endpoints
   - Session endpoints
   - Response evaluation endpoints

4. **Integrate with Frontend** (Feature 08)
   - Frontend API client setup
   - WebSocket for real-time updates
   - Error handling

## Troubleshooting

### Database connection error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify username/password

### NLP model not found
```bash
python -m spacy download en_core_web_sm
```

### Port already in use
```bash
# Change port in .env or use different port
uvicorn app.main:app --port 8001
```

### CORS errors
- Check `BACKEND_CORS_ORIGINS` in config
- Ensure frontend URL is included

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Support

For issues or questions, create an issue in the repository or contact the development team.
