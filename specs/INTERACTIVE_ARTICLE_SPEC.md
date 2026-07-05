# Interactive Article Conversation System - Specification

## 1. Problem Statement
Convert static articles into interactive learning experiences by:
- Segmenting articles into logical chunks (sentences, facts, premises, conclusions)
- Generating contextual probing questions **before** each segment
- Enabling readers to predict/project content before revealing it
- Facilitating active thinking and retention

---

## 2. Core Features

### 2.1 Article Ingestion & Parsing
- **Input**: Plain text articles (can extend to Markdown, HTML)
- **Output**: Structured content segments with metadata
- **Segmentation Logic**:
  - Identify logical boundaries (not just sentence-splitting)
  - Classify segments: Introduction, Premise, Fact, Conclusion, Transition, Evidence
  - Preserve context and relationships between segments

### 2.2 Question Generation
- **Types of Questions**:
  - **Predictive**: "What do you think comes next?" / "What might the author suggest?"
  - **Premise-building**: "Based on [context], what would you expect?"
  - **Reflective**: "Why might this be important?" / "What are the implications?"
  - **Definition-checking**: "How would you explain [concept]?"
  
- **Question Characteristics**:
  - Open-ended (encourage thinking, not just yes/no)
  - Difficulty levels: Simple recall → inference → synthesis
  - Adaptive based on segment type
  - Multiple acceptable answers

### 2.3 Interactive Conversation Flow
- Display question to user
- Capture user response (free text, multiple choice, or rating)
- Reveal actual segment after response (or optional time delay)
- Show how user's prediction relates to actual content
- Progress to next segment

### 2.4 User Engagement & Analytics
- Track prediction accuracy (% correct/partial/off)
- Measure response time
- Engagement metrics (completions, dropoff points)
- Optional: Difficulty adjustment based on performance

---

## 3. Architecture

### 3.1 System Components

\\\
┌─────────────────────────────────────────────────────────────┐
│                    User Interface                            │
│  (Web/Mobile: Question Display → User Input → Content Reveal)│
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Session Manager                                 │
│  (State tracking, progress, analytics)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│          Content & Question Engine                           │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐        │
│  │ Segment      │  │ Question    │  │ Difficulty  │        │
│  │ Parser       │  │ Generator   │  │ Adjuster    │        │
│  └──────────────┘  └─────────────┘  └──────────────┘        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Data Layer                                      │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐        │
│  │ Articles     │  │ Sessions    │  │ Annotations  │        │
│  │ (parsed)     │  │ (progress)  │  │ (metadata)   │        │
│  └──────────────┘  └─────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────┘
\\\

### 3.2 Key Services
1. **ArticleProcessor**: Parse → Segment → Enrich
2. **QuestionGenerator**: Create contextual questions
3. **SessionManager**: Track user progress, responses, state
4. **AnalyticsEngine**: Compute engagement metrics
5. **Recommender** (optional): Suggest questions based on user profile

---

## 4. Data Models

### 4.1 Article
\\\
{
  id: UUID,
  title: string,
  content: string (raw),
  source_url: string (optional),
  metadata: {
    author: string,
    category: string,
    difficulty_level: "beginner" | "intermediate" | "advanced",
    estimated_reading_time: number (minutes)
  },
  created_at: timestamp,
  updated_at: timestamp
}
\\\

### 4.2 Segment
\\\
{
  id: UUID,
  article_id: UUID,
  position: number (order in article),
  content: string,
  type: "introduction" | "premise" | "fact" | "evidence" | "conclusion" | "transition",
  context: {
    previous_segment_id: UUID (optional),
    related_concepts: string[],
    difficulty: 1-5
  },
  metadata: {
    character_count: number,
    key_entities: string[],
    keywords: string[]
  }
}
\\\

### 4.3 Question
\\\
{
  id: UUID,
  segment_id: UUID,
  question_text: string,
  question_type: "predictive" | "reflective" | "definition" | "inference",
  question_subtype: string (e.g., "what_happens_next", "why_important"),
  difficulty: 1-5,
  context_snippet: string (teaser from context),
  acceptable_answers: string[] (for comparison/validation),
  hints: string[] (optional, revealed on request),
  generated_by: "ai" | "manual",
  metadata: {
    created_at: timestamp,
    refinement_version: number
  }
}
\\\

### 4.4 UserResponse
\\\
{
  id: UUID,
  session_id: UUID,
  question_id: UUID,
  segment_id: UUID,
  user_answer: string,
  answer_type: "free_text" | "multiple_choice" | "rating",
  response_time_ms: number,
  revealed_answer: string,
  accuracy_score: 0-1 (calculated),
  feedback: string (e.g., "Good prediction!" | "Slightly different angle"),
  created_at: timestamp
}
\\\

### 4.5 Session
\\\
{
  id: UUID,
  user_id: UUID (or anonymous),
  article_id: UUID,
  started_at: timestamp,
  last_accessed: timestamp,
  completed_at: timestamp (null if ongoing),
  current_segment_index: number,
  total_segments: number,
  statistics: {
    accuracy_score: 0-1 (average),
    avg_response_time_ms: number,
    segments_completed: number,
    segments_skipped: number,
    questions_answered: number
  },
  metadata: {
    device: string,
    language: string,
    theme: "light" | "dark"
  }
}
\\\

---

## 5. User Flows

### 5.1 Read Article Flow
\\\
1. User selects/uploads article
   ↓
2. System parses & segments article (async)
   ↓
3. Display article info + start CTA
   ↓
4. Loop until completion:
   a. Generate & display question for next segment
   b. User submits response (or requests hint)
   c. Reveal segment + feedback
   d. Track response metrics
   e. Move to next segment or offer: Continue | Restart | Exit
   ↓
5. Show completion summary & analytics
\\\

### 5.2 Question Lifecycle
\\\
Question generated
   ↓ (user views)
Question displayed
   ↓ (user thinks)
User responds
   ↓ (system evaluates)
Feedback provided
   ↓ (context reveal)
Segment displayed
   ↓ (comparison shown)
Analytics recorded
\\\

---

## 6. Question Generation Strategy

### 6.1 Triggers for Question Generation
- **Before Introduction**: "What do you know about [topic]?"
- **Before Premise**: "Why do you think the author mentions [related concept]?"
- **Before Fact**: "What would you expect to find here?"
- **Before Evidence**: "How might you support that claim?"
- **Before Conclusion**: "What conclusion would you draw?"

### 6.2 Question Diversity
- Vary question types to avoid repetition
- Cycle: Predictive → Reflective → Definition → Inference
- Adjust difficulty based on:
  - Segment complexity
  - User performance history
  - Position in article (ramp-up)

### 6.3 Implementation Options
- **AI-based** (OpenAI/Claude API): Generate contextually aware questions
- **Template-based**: Rules + templates for each segment type
- **Hybrid**: Templates + AI refinement
- **Manual curation**: Editors write questions (for premium articles)

---

## 7. Technical Requirements

### 7.1 Backend
- **Language**: Python / Node.js / Go (suggest Python for NLP flexibility)
- **APIs**:
  - POST /api/articles (upload article)
  - GET /api/articles/{id} (retrieve article with segments)
  - GET /api/questions/{segment_id} (get question for segment)
  - POST /api/responses (submit user response)
  - GET /api/sessions/{id}/analytics (fetch user stats)
  
### 7.2 Frontend
- **Framework**: React / Vue / Svelte
- **Key Views**:
  - Article selection/upload
  - Question + response interface
  - Content reveal + comparison
  - Session analytics/dashboard
  
### 7.3 NLP Processing
- Sentence tokenization & segmentation
- Named entity recognition (identify concepts)
- Abstractive summarization (extract key ideas)
- Semantic similarity (compare user answer vs expected)

### 7.4 Database
- PostgreSQL (relational) or MongoDB (document-based)
- Indexes: article_id, session_id, user_id, segment_id
- Cache layer: Redis (for question caching)

---

## 8. Success Metrics & Acceptance Criteria

### 8.1 Functional Requirements
- [ ] Parse arbitrary articles into segments
- [ ] Generate context-aware questions for ≥80% of segments
- [ ] Track user responses accurately
- [ ] Calculate accuracy scores (user prediction vs actual)
- [ ] Display progression through article
- [ ] Export session analytics

### 8.2 Quality Metrics
- **Question Quality**: User satisfaction ≥4/5, answer relevance ≥0.75
- **Accuracy Detection**: 85%+ correct matching of user answers
- **Performance**: <500ms for question generation, <100ms UI interactions
- **Engagement**: ≥70% article completion rate

### 8.3 UX Requirements
- Intuitive question/response/reveal flow
- Mobile-responsive design
- Dark mode support
- Accessibility (WCAG 2.1 AA)
- <2 second load times for each segment transition

---

## 9. Phases & Development Roadmap

### Phase 1: MVP (Core Flow)
- [ ] Article ingestion & basic segmentation
- [ ] Template-based question generation
- [ ] Simple session tracking
- [ ] Web UI for QA flow
- [ ] Analytics dashboard (basic)

### Phase 2: Enhancement
- [ ] AI-powered question generation
- [ ] User accounts & session history
- [ ] Difficulty adaptation
- [ ] Answer comparison scoring

### Phase 3: Scale & Polish
- [ ] Mobile app
- [ ] Bulk article upload
- [ ] Advanced analytics
- [ ] Social features (share sessions, leaderboards)
- [ ] Multi-language support

---

## 10. Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Poor segmentation | Confusing questions | Test on diverse articles, manual validation |
| Low question quality | Low engagement | Combine AI + curation, user feedback loop |
| Slow performance | User frustration | Cache aggressively, async processing |
| Answer matching complexity | Inaccurate scoring | Use semantic similarity, allow manual adjustments |
| Scalability | System bottleneck | Async jobs, database optimization, CDN |

---

## 11. Example Workflow

**Article:** "Climate change is accelerating. Scientists observe..." 

**Segment 1 (Intro):**
- Question: "What factors do you think contribute to climate change?"
- User: "CO2 emissions and deforestation"
- Reveal: "Climate change is accelerating." (partial match ✓)

**Segment 2 (Fact):**
- Question: "How do you think scientists measure this acceleration?"
- User: "Temperature records over time?"
- Reveal: "Scientists observe temperature records and ice core data..." (good prediction ✓)

**Segment 3 (Conclusion):**
- Question: "What action might experts recommend?"
- User: "Reduce emissions?"
- Reveal: "We must transition to renewable energy..." (partially aligned ✓)

---

## Notes for Implementation
- Start with template-based questions (faster MVP)
- Plan for AI integration in Phase 2
- Use LLM APIs for semantic similarity scoring
- Consider Retrieval-Augmented Generation (RAG) for better context
