# Feature: User Response Handling & Evaluation

## Overview
Process user responses, score accuracy, generate feedback, and correlate predictions with revealed content.

## User Story
As a system, I need to evaluate user responses against the actual segment content so that I can provide meaningful feedback and track prediction accuracy.

## Functional Requirements

### 5.1 Response Validation
- **Input validation**:
  - Check minimum length (2 characters)
  - Check maximum length (5000 characters)
  - Trim whitespace
  - Normalize text (lowercase for comparison)
  - Detect spam/gibberish patterns
- **Rejection handling**:
  - User-friendly error messages
  - Allow correction attempts
  - Track invalid submission count

### 5.2 Accuracy Scoring
- **Scoring Methodology**:
  - Exact match: 1.0 (perfect)
  - Semantic similarity: 0.0-0.99
  - Keyword overlap: Partial score
  - Concept alignment: Bonus score
- **Scoring Engine**:
  - Use sentence-transformers for embeddings
  - Calculate cosine similarity
  - Combine multiple signals (keyword match + semantic)
  - Threshold-based categorization: Exact/Partial/Close/Off

### 5.3 Accuracy Categories
| Score | Category | Feedback |
|-------|----------|----------|
| ≥0.95 | Exact | "Perfect prediction!" |
| 0.80-0.94 | Excellent | "Great intuition!" |
| 0.60-0.79 | Good | "Similar thinking!" |
| 0.40-0.59 | Partial | "Good attempt!" |
| <0.40 | Off-track | "Interesting angle..." |

### 5.4 Key Points Extraction
- Extract main concepts from user response
- Extract main concepts from actual segment
- Calculate overlap
- Identify relevant but different angles
- Display comparison visually

### 5.5 Feedback Generation
- **Components**:
  - Accuracy assessment (category + emoji)
  - Encouraging message (positive framing)
  - Key insights (what user got right)
  - Clarification (what was actually said)
  - Connection (how it relates to context)
- **Tone**: Encouraging, non-judgmental, educational

### 5.6 Response Storage
- Store all responses with full context
- Preserve user input (original + normalized)
- Store accuracy score and category
- Record feedback shown
- Enable response review/history

### 5.7 Hint Correlation
- Track if hint was used before response
- Adjust accuracy scoring if hint used (mark with flag)
- Analyze hint effectiveness
- Determine which hints helped

## Technical Specifications

### Request Schema
```json
{
  "session_id": "uuid",
  "question_id": "uuid",
  "segment_id": "uuid",
  "user_response": "string",
  "response_time_ms": 8500,
  "input_type": "free_text|multiple_choice|scale",
  "hint_used": false,
  "timestamp": "timestamp"
}
```

### Scoring Output Schema
```json
{
  "response_id": "uuid",
  "raw_response": "string",
  "normalized_response": "string",
  "accuracy_score": 0.72,
  "accuracy_category": "good|excellent|partial|off_track",
  "scoring_details": {
    "semantic_similarity": 0.75,
    "keyword_overlap": 0.80,
    "concept_alignment": 0.65,
    "signals_used": ["semantic", "keyword", "concept"]
  },
  "key_points": {
    "user_concepts": ["concept1", "concept2"],
    "actual_concepts": ["concept1", "concept3", "concept4"],
    "overlap": ["concept1"],
    "missed": ["concept3", "concept4"],
    "extra": ["concept2"]
  },
  "feedback": {
    "accuracy_message": "Good intuition!",
    "encouragement": "You identified the main point correctly.",
    "clarification": "The segment actually emphasized...",
    "connection": "This builds on what we discussed about..."
  },
  "metadata": {
    "hint_used": false,
    "response_length": 42,
    "processing_time_ms": 350,
    "model_version": "v1.2",
    "confidence": 0.85
  }
}
```

## Acceptance Criteria
- [ ] Response validation catches 100% of spam/empty inputs
- [ ] Accuracy scoring ≥85% agreement with manual review
- [ ] Scoring completes in <500ms
- [ ] Feedback messages personalized and encouraging
- [ ] Key points extracted correctly ≥80% of time
- [ ] Hint correlation tracked accurately
- [ ] Response storage includes all metadata
- [ ] Scoring handles edge cases (very short/long responses)

## Dependencies
- sentence-transformers library (embeddings)
- spaCy (NLP, keyword extraction)
- Semantic similarity backend (on-device or API)
- Response database

## Success Metrics
- Scoring accuracy: ≥85% user agreement
- Processing speed: <500ms per response
- False positive rate: <5% (spam detection)
- User satisfaction with feedback: ≥4/5
