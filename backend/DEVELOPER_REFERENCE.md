# Developer Quick Reference - Backend Database Layer

## Quick Start (5 minutes)

```bash
# 1. Navigate to backend
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 4. Run migrations
alembic upgrade head

# 5. Start the server
python main.py
```

Server runs at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

---

## Database Tables Reference

### Core Tables

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| articles | Parsed articles | title, content, category, difficulty_level |
| segments | Content chunks | content, type, article_id, position |
| questions | Questions for segments | question_text, type, difficulty |
| sessions | User sessions | user_id, article_id, status, current_segment_index |
| user_responses | User answers | user_answer, accuracy_score, session_id |

### Support Tables

| Table | Purpose |
|-------|---------|
| users | User accounts (optional) |
| analytics_events | Event stream |
| analytics_aggregations | Computed statistics |

---

## Repository Methods Cheat Sheet

### ArticleRepository
```python
repo = ArticleRepository(session)
article = repo.create({"title": "...", "content": "..."})
article = repo.get(article_id)
articles = repo.get_by_category("Science")
articles = repo.get_by_difficulty(3)
```

### SegmentRepository
```python
repo = SegmentRepository(session)
segments = repo.get_by_article(article_id)
segment = repo.get_segment_at_position(article_id, position=0)
count = repo.count_by_article(article_id)
```

### QuestionRepository
```python
repo = QuestionRepository(session)
question = repo.get_by_segment(segment_id)
questions = repo.get_by_type("predictive")
```

### SessionRepository
```python
repo = SessionRepository(session)
session = repo.get_by_user_article(user_id, article_id)
sessions = repo.get_active_sessions(user_id)
sessions = repo.get_user_sessions(user_id, skip=0, limit=10)
```

### UserResponseRepository
```python
repo = UserResponseRepository(session)
responses = repo.get_by_session(session_id)
responses = repo.get_by_question(question_id)
avg_accuracy = repo.get_average_accuracy(session_id)
```

---

## Common Tasks

### Create an Article with Segments

```python
from app.repositories import ArticleRepository, SegmentRepository
from app.db.base import SessionLocal

db = SessionLocal()

# Create article
article_repo = ArticleRepository(db)
article = article_repo.create({
    "title": "Climate Change",
    "content": "...",
    "category": "Science",
    "difficulty_level": 3
})

# Create segments
segment_repo = SegmentRepository(db)
segment = segment_repo.create({
    "article_id": article.id,
    "position": 0,
    "content": "First paragraph...",
    "type": "introduction",
    "difficulty": 2,
    "keywords": ["climate", "change"]
})
```

### Create a Session and Track Response

```python
from app.models import Session as SessionModel, UserResponse
from app.repositories import SessionRepository, UserResponseRepository

session_repo = SessionRepository(db)
response_repo = UserResponseRepository(db)

# Create session
session = session_repo.create({
    "user_id": user_id,
    "article_id": article_id,
    "total_segments": 10
})

# Create response
response = response_repo.create({
    "session_id": session.id,
    "question_id": question_id,
    "segment_id": segment_id,
    "user_answer": "User's prediction",
    "accuracy_score": 0.85,
    "accuracy_category": "good",
    "response_time_ms": 5000
})
```

### Query Recent Articles

```python
article_repo = ArticleRepository(db)

# Get by category
science_articles = article_repo.get_by_category(
    "Science", skip=0, limit=10
)

# Get by difficulty
advanced_articles = article_repo.get_by_difficulty(
    5, skip=0, limit=10
)

# Get all with pagination
all_articles = article_repo.get_all(skip=0, limit=20)
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/unit/test_models.py

# Run specific test
pytest tests/unit/test_models.py::test_article_creation

# Verbose output
pytest -v

# Show print statements
pytest -s
```

---

## Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply one migration
alembic upgrade +1

# Rollback one migration
alembic downgrade -1

# Rollback all
alembic downgrade base

# Create new migration
alembic revision --autogenerate -m "Add column X to table Y"

# Show migration history
alembic history

# Current revision
alembic current
```

---

## Code Quality

```bash
# Format code
black app/ tests/

# Check style
flake8 app/ tests/

# Type checking
mypy app/

# All checks together
black app/ && flake8 app/ && mypy app/
```

---

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
ENVIRONMENT=development
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME=Interactive Article System
SECRET_KEY=your-secret-key
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

---

## API Response Schemas

### Article Response
```json
{
  "id": "uuid",
  "title": "string",
  "content": "string",
  "category": "string",
  "difficulty_level": 3,
  "created_at": "2026-07-04T23:13:30",
  "updated_at": "2026-07-04T23:13:30"
}
```

### Segment Response
```json
{
  "id": "uuid",
  "article_id": "uuid",
  "position": 0,
  "content": "string",
  "type": "introduction|premise|fact|evidence|conclusion",
  "difficulty": 3,
  "entities": ["entity1", "entity2"],
  "keywords": ["keyword1", "keyword2"],
  "created_at": "2026-07-04T23:13:30"
}
```

### Session Response
```json
{
  "id": "uuid",
  "user_id": "uuid|null",
  "article_id": "uuid",
  "status": "active|paused|completed",
  "current_segment_index": 5,
  "total_segments": 10,
  "segments_completed": 5,
  "statistics": {
    "accuracy_score": 0.75,
    "avg_response_time_ms": 5000
  },
  "started_at": "2026-07-04T23:13:30",
  "last_accessed": "2026-07-04T23:30:00"
}
```

### UserResponse Response
```json
{
  "id": "uuid",
  "session_id": "uuid",
  "question_id": "uuid",
  "segment_id": "uuid",
  "user_answer": "string",
  "accuracy_score": 0.85,
  "accuracy_category": "good|excellent|partial|exact|off_track",
  "feedback": "Great prediction!",
  "response_time_ms": 5000,
  "hint_used": false,
  "created_at": "2026-07-04T23:13:30"
}
```

---

## Troubleshooting

### Database Connection Error
```
ERROR: could not connect to server
```
**Solution**: Check DATABASE_URL in .env, ensure PostgreSQL is running

### Migration Error
```
ERROR: relation "articles" already exists
```
**Solution**: Check current migration status: `alembic current`

### Import Error
```
ModuleNotFoundError: No module named 'app'
```
**Solution**: Make sure you're in the `backend` directory: `cd backend`

### Test Database Error
```
sqlite3.OperationalError: attempt to write a readonly database
```
**Solution**: Tests use in-memory SQLite, should not persist

---

## File Organization for New Features

When adding a new repository, follow this pattern:

```python
# 1. Add to app/models/__init__.py
class MyEntity(Base):
    __tablename__ = "my_entities"
    # ... model definition

# 2. Create repository in app/repositories/__init__.py
class MyEntityRepository(BaseRepository[MyEntity]):
    def __init__(self, session: Session):
        super().__init__(session, MyEntity)
    
    # ... custom query methods

# 3. Create schema in app/schemas/__init__.py
class MyEntityResponse(BaseModel):
    # ... schema fields

# 4. Create migration in migrations/versions/
# Describe your schema changes

# 5. Add tests in tests/unit/test_*.py
def test_my_entity_creation(db_session):
    # ... test implementation
```

---

## Next: Feature 01 - Article Ingestion

**What you'll need:**
- ArticleRepository ✅ (ready)
- SegmentRepository ✅ (ready)
- Article/Segment models ✅ (ready)

**What you'll build:**
- ArticleProcessor service
- Text parsing logic
- Segmentation algorithm
- Entity extraction
- Segment classification

---

**Last Updated**: 2026-07-04
**Backend Status**: Production Ready ✅
