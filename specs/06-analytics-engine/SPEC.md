# Feature: Analytics Engine

## Overview
Collect, analyze, and visualize user engagement and learning metrics across articles and sessions.

## User Story
As an admin, I want to understand how users engage with articles so that I can measure effectiveness and improve the platform.

## Functional Requirements

### 6.1 Metrics Collection
- **Per Session**:
  - Total duration
  - Segments completed / skipped / abandoned
  - Accuracy score (average)
  - Engagement rate (% completion)
  - Questions answered
  - Hints used
  - Times paused
  
- **Per User** (aggregate):
  - Articles read
  - Total time invested
  - Average accuracy across articles
  - Engagement trend (improving/stable/declining)
  - Preferred categories
  - Learning velocity
  
- **Per Article**:
  - Views / starts / completions
  - Completion rate (%)
  - Average accuracy
  - Dropoff points (where users quit)
  - Most skipped segments
  - Most common misconceptions

### 6.2 Engagement Metrics
| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| Completion Rate | Completed Sessions / Total Sessions | % of articles finished |
| Engagement Score | (Responses + Time) / Max | Overall activity level |
| Accuracy Score | Avg(Response Scores) | Prediction quality |
| Pace | Avg Time per Segment | Learning speed |
| Consistency | Std Dev of Accuracy | Prediction stability |

### 6.3 Learner Profiles
Identify user types:
- **Power Readers**: High completion, high accuracy
- **Explorers**: High completion, variable accuracy
- **Perfectionists**: Lower pace, high accuracy, frequent hints
- **Casual**: Low completion, variable engagement
- **Skimmers**: High completion, low accuracy

### 6.4 Real-time Dashboard
- Active sessions count
- Current engagement metrics
- Popular articles
- Trending topics
- Performance anomalies

### 6.5 Reporting
- **Daily Report**: Sessions, completions, engagement
- **Weekly Report**: Trends, top articles, user insights
- **Custom Reports**: Segment data by date range, category, user cohort

### 6.6 Anomaly Detection
- Unusual accuracy scores (too high/low)
- Engagement spikes/drops
- Content quality issues
- User behavior changes

### 6.7 Data Privacy
- Anonymize analytics (no PII in reports)
- Aggregate data before analysis
- Allow users to opt-out of analytics
- Comply with data retention policies

## Technical Specifications

### Analytics Event Schema
```json
{
  "event_type": "session_start|response_submitted|content_revealed|session_complete",
  "timestamp": "timestamp",
  "session_id": "uuid",
  "user_id": "uuid|null",
  "article_id": "uuid",
  "segment_index": 5,
  "question_id": "uuid",
  "user_response": "string|null",
  "accuracy_score": 0.72,
  "response_time_ms": 8500,
  "event_metadata": {
    "device": "web|mobile",
    "browser": "string",
    "language": "en"
  }
}
```

### Analytics Aggregation Schema
```json
{
  "aggregation_id": "uuid",
  "aggregation_type": "session|daily|weekly",
  "period": {
    "start": "timestamp",
    "end": "timestamp"
  },
  "metrics": {
    "total_sessions": 150,
    "completed_sessions": 105,
    "abandoned_sessions": 45,
    "avg_accuracy": 0.72,
    "avg_duration_ms": 450000,
    "total_responses": 2250,
    "hints_used": 180
  },
  "breakdown": {
    "by_category": { "category1": {...}, "category2": {...} },
    "by_article": { "article_id": {...} },
    "by_difficulty": { "1": {...}, "2": {...}, "3": {...} }
  }
}
```

### Dashboard Schema
```json
{
  "dashboard": {
    "kpis": {
      "active_sessions": 42,
      "completion_rate_today": 0.71,
      "avg_accuracy_today": 0.68,
      "articles_in_progress": 156
    },
    "charts": {
      "accuracy_distribution": { "bins": [...], "counts": [...] },
      "completion_timeline": { "dates": [...], "completions": [...] },
      "engagement_by_category": { "category": {...} }
    },
    "insights": [
      "Completion rate up 5% week-over-week",
      "Science category has lowest completion rate (45%)",
      "Average response time increasing (slower engagement)"
    ]
  }
}
```

## Acceptance Criteria
- [ ] Collect all required metrics accurately
- [ ] Dashboard updates in real-time (≤5s latency)
- [ ] Report generation <30s for large datasets
- [ ] Metrics visible within 5 minutes of session start
- [ ] 100% data privacy compliance
- [ ] Anomaly detection catches >90% real issues
- [ ] No performance impact on main application
- [ ] Analytics API returns <1s responses

## Dependencies
- Data warehouse (BigQuery, Redshift, or PostgreSQL)
- Analytics frontend (Grafana, Metabase, custom)
- Event streaming (Kafka or simple queue)
- Aggregation jobs (Apache Spark or Python jobs)

## Success Metrics
- Insight quality: Actionable recommendations ≥3/report
- Dashboard usability: Admin satisfaction ≥4/5
- Reporting accuracy: ≥99% metric accuracy
- System performance: No latency impact on app
