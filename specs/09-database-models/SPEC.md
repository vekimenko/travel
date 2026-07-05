# Feature: Database Models & Persistence Layer

## Overview
Design and implement data models for articles, segments, questions, sessions, responses, and analytics in a relational database.

## User Story
As a developer, I need well-designed database schemas and efficient queries so that the application can reliably store and retrieve data at scale.

## Functional Requirements

### 9.1 Core Models

#### Article
Store parsed articles with metadata
```sql
CREATE TABLE articles (
  id UUID PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  content TEXT NOT NULL,
  content_hash VARCHAR(64),
  source_url VARCHAR(2048),
  source_format VARCHAR(10),
  category VARCHAR(100),
  difficulty_level INTEGER (1-5),
  created_by UUID,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP,
  metadata JSON,
  INDEXES: created_at, category, difficulty_level, created_by
);
```

#### Segment
Article segments with type and context
```sql
CREATE TABLE segments (
  id UUID PRIMARY KEY,
  article_id UUID NOT NULL (FK),
  position INTEGER NOT NULL,
  content TEXT NOT NULL,
  type VARCHAR(50),
  character_count INTEGER,
  difficulty INTEGER (1-5),
  entities TEXT[] (JSON array),
  keywords TEXT[] (JSON array),
  metadata JSON,
  created_at TIMESTAMP,
  INDEXES: article_id, position, type, difficulty
);
```

#### Question
Generated questions for segments
```sql
CREATE TABLE questions (
  id UUID PRIMARY KEY,
  segment_id UUID NOT NULL (FK),
  question_text TEXT NOT NULL,
  question_type VARCHAR(50),
  difficulty INTEGER (1-5),
  acceptable_answers TEXT[] (JSON array),
  hints TEXT[] (JSON array),
  generated_by VARCHAR(50),
  quality_score DECIMAL,
  created_at TIMESTAMP,
  metadata JSON,
  INDEXES: segment_id, difficulty, question_type
);
```

#### Session
User reading sessions
```sql
CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  user_id UUID,
  article_id UUID NOT NULL (FK),
  started_at TIMESTAMP NOT NULL,
  last_accessed TIMESTAMP,
  completed_at TIMESTAMP,
  status VARCHAR(50),
  current_segment_index INTEGER DEFAULT 0,
  total_segments INTEGER,
  segments_completed INTEGER DEFAULT 0,
  segments_skipped INTEGER DEFAULT 0,
  questions_answered INTEGER DEFAULT 0,
  metadata JSON,
  statistics JSON,
  created_at TIMESTAMP,
  INDEXES: user_id, article_id, status, created_at
);
```

#### UserResponse
Captured user responses to questions
```sql
CREATE TABLE user_responses (
  id UUID PRIMARY KEY,
  session_id UUID NOT NULL (FK),
  question_id UUID NOT NULL (FK),
  segment_id UUID NOT NULL (FK),
  user_answer TEXT NOT NULL,
  answer_type VARCHAR(50),
  response_time_ms INTEGER,
  accuracy_score DECIMAL,
  accuracy_category VARCHAR(50),
  feedback TEXT,
  feedback_detail JSON,
  hint_used BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP,
  INDEXES: session_id, question_id, segment_id, accuracy_category
);
```

#### User (optional, for authentication)
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(255) UNIQUE,
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255),
  profile_data JSON,
  preferences JSON,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP,
  INDEXES: email, username
);
```

#### Analytics Events
Real-time event stream
```sql
CREATE TABLE analytics_events (
  id UUID PRIMARY KEY,
  event_type VARCHAR(50) NOT NULL,
  session_id UUID,
  user_id UUID,
  article_id UUID,
  segment_id UUID,
  event_data JSON,
  timestamp TIMESTAMP NOT NULL,
  INDEXES: timestamp, session_id, event_type, user_id
  PARTITION BY date(timestamp)
);
```

#### Aggregated Analytics
Pre-computed statistics
```sql
CREATE TABLE analytics_aggregations (
  id UUID PRIMARY KEY,
  aggregation_type VARCHAR(50),
  period_start TIMESTAMP,
  period_end TIMESTAMP,
  article_id UUID,
  user_id UUID,
  metrics JSON,
  created_at TIMESTAMP,
  INDEXES: aggregation_type, period_start, article_id, user_id
);
```

### 9.2 Relationships
- Article (1) ← → (M) Segments
- Segment (1) ← → (M) Questions
- Session (M) → (1) Article
- Session (1) ← → (M) UserResponses
- UserResponse (M) → (1) Question
- Session (M) → (1) User (optional)
- Analytics Events → Sessions/Users/Articles

### 9.3 Query Patterns

#### Performance-critical Queries
- Get segments for article (with pagination)
- Get question for segment
- Get session with all responses
- Aggregate analytics by time period
- Search articles by text/category

#### Optimization Strategies
- Indexes on foreign keys
- Time-series partitioning for events table
- Materialized views for aggregations
- Caching frequently accessed data
- Archive old analytics events

### 9.4 Database Choice
**PostgreSQL Recommended**:
- JSON support for flexible schemas
- Full-text search capabilities
- Partitioning for large tables
- LISTEN/NOTIFY for real-time updates
- Mature transaction support
- Cost-effective

**Alternative: MongoDB**:
- Flexible document schema
- Horizontal scaling
- Good for time-series data
- Easier for rapid iteration

### 9.5 Data Integrity
- Foreign key constraints
- Check constraints (difficulty 1-5, status in enum)
- Not null constraints where required
- Unique constraints (user email, article hash)
- Transaction support for critical operations

### 9.6 Backup & Recovery
- Daily automated backups
- Point-in-time recovery capability
- Backup encryption
- Cross-region replication (optional)
- Disaster recovery plan

### 9.7 Data Privacy & Compliance
- Encryption at rest (optional)
- Encryption in transit (TLS)
- No PII in analytics events
- GDPR deletion capability
- Audit logging for sensitive data

## Technical Specifications

### Database Configuration
- **Engine**: PostgreSQL 14+
- **Connection Pooling**: PgBouncer or application-level
- **Backup**: pg_dump + cloud storage
- **Monitoring**: CloudWatch / DataDog / Prometheus
- **Replication**: Streaming replication for HA

### Migrations
- Version control for schema changes
- Forward & backward compatible migrations
- Testing before production deployment
- Rollback capability

### ORM/Query Layer
- **SQLAlchemy** (Python) or **Prisma** (Node.js)
- Query builders for type safety
- Relationship management
- Migration tools

## Acceptance Criteria
- [ ] All required tables created with proper schema
- [ ] Foreign key relationships enforced
- [ ] Indexes present on all query columns
- [ ] Query response times <100ms for 95% of reads
- [ ] Data consistency verified
- [ ] Backup/restore working correctly
- [ ] GDPR compliance verified
- [ ] No N+1 query problems

## Dependencies
- PostgreSQL database
- Migration tool (Alembic, Flyway, or Prisma Migrate)
- ORM library (SQLAlchemy, Prisma, etc.)
- Monitoring tools

## Success Metrics
- Query performance: p95 <100ms
- Data consistency: 100% integrity
- Backup success rate: 100%
- GDPR compliance: Verified
- Scalability: Supports 1M sessions
