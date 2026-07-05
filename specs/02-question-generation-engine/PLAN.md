# Question Generation Engine - Development Plan

## Phase 1: MVP (Template-based)

### Task 1: Template Library
- [ ] Create template database for each segment type
  - 5-10 templates per segment type
  - Parameterized for entity/keyword insertion
- [ ] Store templates in JSON or database
- [ ] Example templates:
  ```
  Introduction: "Based on the title [TITLE], what topics do you expect to be covered?"
  Premise: "Why might [ENTITY] be important in this context?"
  Fact: "What specific details do you predict about [KEYWORD]?"
  Conclusion: "What would be your main takeaway?"
  ```

### Task 2: Template Selection Engine
- [ ] Implement difficulty-aware template selection
- [ ] Add randomization to avoid repetition
- [ ] Track used templates per article to avoid immediate repeats
- [ ] Support template version control for refinement

### Task 3: Question Generation Service
- [ ] Create generate_question(segment, context) function
- [ ] Implement entity/keyword substitution
- [ ] Add acceptable answer extraction from segment text
- [ ] Implement hint generation (2-3 hints per question)

### Task 4: Quality Validation
- [ ] Length validation: 20-200 characters
- [ ] Relevance scoring using semantic similarity
- [ ] Fallback mechanism if generated question fails validation
- [ ] Logging and monitoring

### Task 5: API Endpoint
- [ ] POST /api/questions/generate
- [ ] Accept segment data + context
- [ ] Return generated question with metadata
- [ ] Error handling for edge cases

## Phase 2: AI-Enhanced

### Task 6: OpenAI/Claude Integration
- [ ] Set up API credentials and clients
- [ ] Create prompt engineering framework
- [ ] Implement few-shot examples for quality
- [ ] Add cost tracking and rate limiting

### Task 7: Question Quality Feedback Loop
- [ ] User satisfaction ratings per question
- [ ] Track which templates work best
- [ ] Collect data for AI fine-tuning
- [ ] Implement A/B testing framework

## Phase 3: Adaptive Generation

### Task 8: User-adaptive Difficulty
- [ ] Track user performance history
- [ ] Adjust future question difficulty based on accuracy
- [ ] Calibrate difficulty estimation model

## Testing Strategy
- Unit tests for template selection
- Integration tests with real articles
- Quality validation tests
- Performance benchmarking
- User acceptance testing on generated questions

## Estimated Effort
- **Phase 1 MVP**: 2-3 sprints
- **Phase 2 AI**: 2-3 sprints
- **Phase 3 Adaptive**: 1-2 sprints
