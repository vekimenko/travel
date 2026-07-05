# Feature: Question Generation Engine

## Overview
Automatically generate context-aware probing questions before each article segment to trigger predictive thinking and engagement.

## User Story
As a system, I need to generate meaningful probing questions for each segment so that readers can predict/project the content before it's revealed.

## Functional Requirements

### 2.1 Question Generation Strategies

**By Segment Type:**

| Segment Type | Question Strategy | Example |
|---|---|---|
| Introduction | Background knowledge | "What do you know about [topic]?" |
| Premise | Expectation setting | "Why do you think the author introduces [concept]?" |
| Fact | Prediction | "What specific information do you expect?" |
| Evidence | Application | "How would you support that claim?" |
| Conclusion | Synthesis | "What conclusion would you draw?" |
| Transition | Connection | "How does this relate to what we just discussed?" |

### 2.2 Question Types
- **Predictive**: "What comes next?" / "What might happen?"
- **Reflective**: "Why is this important?" / "What are implications?"
- **Definition**: "How would you explain [term]?"
- **Inference**: "What can we deduce from [context]?"
- **Application**: "How would you apply this?"

### 2.3 Question Diversity & Difficulty
- **Avoid repetition**: Cycle through question types
- **Difficulty levels** (1-5):
  - Level 1-2: Recall, basic understanding
  - Level 3: Application, inference
  - Level 4-5: Synthesis, evaluation
- **Adaptive difficulty**:
  - Ramp up through article
  - Adjust based on user performance
  - Context-aware complexity

### 2.4 Question Quality Standards
- **Open-ended**: Encourage thinking, not just yes/no
- **Contextual**: Reference prior segments when relevant
- **Accessible**: No jargon not yet introduced
- **Actionable**: Lead to concrete predictions
- **Multiple valid answers**: Allow diverse responses

## Technical Specifications

### Input Schema
```json
{
  "segment": {
    "id": "uuid",
    "content": "string",
    "type": "introduction|premise|fact|evidence|conclusion|transition",
    "difficulty": 1-5,
    "entities": ["entity1", "entity2"],
    "keywords": ["key1", "key2"],
    "context": {
      "previous_segments": ["segment_text_1", "segment_text_2"],
      "article_title": "string",
      "article_category": "string"
    }
  },
  "generation_params": {
    "strategy": "template|ai",
    "user_history": {
      "questions_answered": 10,
      "avg_accuracy": 0.72,
      "avg_response_difficulty": 2.5
    }
  }
}
```

### Output Schema
```json
{
  "question": {
    "id": "uuid",
    "segment_id": "uuid",
    "question_text": "string",
    "question_type": "predictive|reflective|definition|inference|application",
    "difficulty": 1-5,
    "context_teaser": "string (optional hint from next segment)",
    "acceptable_answers": [
      "answer_1",
      "answer_2 (alternative phrasing)"
    ],
    "hints": [
      "Think about...",
      "Consider..."
    ],
    "generated_by": "template|ai",
    "metadata": {
      "generated_at": "timestamp",
      "refinement_version": 1,
      "quality_score": 0.87
    }
  }
}
```

## Implementation Approaches

### Template-based (MVP)
- Rules and templates for each segment type
- Keyword insertion from extracted entities
- Variable difficulty via template selection
- **Pros**: Fast, deterministic, controllable
- **Cons**: Less variety, may feel repetitive

### AI-based (Phase 2)
- Use OpenAI/Claude API for generation
- Few-shot prompting with examples
- Fine-tuning on curated questions
- **Pros**: More natural, diverse, adaptive
- **Cons**: Slower, cost, external dependency

### Hybrid (Phase 3)
- Template-based for common cases
- AI for edge cases or low-confidence generations
- User feedback loop to improve templates

## Acceptance Criteria
- [ ] Generate ≥80% usable questions on test articles
- [ ] Question diversity: ≤20% exact template repeats
- [ ] Question-segment relevance: ≥0.85 semantic similarity
- [ ] Response time: <200ms per question (template), <2s (AI)
- [ ] Support all 6 segment types
- [ ] Difficulty distribution: reasonable spread across 1-5
- [ ] Validate against acceptability rubric

## Dependencies
- NLP libraries (spaCy, NLTK)
- OpenAI API (Phase 2+)
- Semantic similarity model (sentence-transformers)

## Success Metrics
- Question quality (manual review): ≥4/5
- User engagement (% questions answered): ≥75%
- Prediction accuracy: ≥60% user answers match segments
- Variety score: <15% template repetition
