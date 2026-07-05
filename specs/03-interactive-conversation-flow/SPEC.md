# Feature: Interactive Conversation Flow

## Overview
Orchestrate the core interactive experience: question display → user input → content reveal → feedback → next segment progression.

## User Story
As a reader, I want to engage in an interactive conversation where I predict content before it's revealed, so that I can actively think through the material and improve retention.

## Functional Requirements

### 3.1 Conversation State Machine
```
States:
  STARTING → QUESTION_READY → AWAITING_RESPONSE → RESPONSE_RECEIVED 
    → REVEALING_CONTENT → CONTENT_REVEALED → FEEDBACK_SHOWN → [NEXT_SEGMENT or END]
```

### 3.2 Question Display Phase
- Display question prominently
- Show difficulty indicator (1-5 stars)
- Show "Hint" button (reveal hint on click)
- Show response input area
- Display progress indicator (segment X of Y)
- Optional: Show time elapsed

### 3.3 User Input Handling
- **Input Types** (configurable per question):
  - Free text (textarea)
  - Multiple choice (radio buttons)
  - Scale rating (1-5 Likert)
- **Constraints**:
  - Min text length: 2 characters
  - Max text length: 5000 characters
  - Timeout (optional): 15-300 seconds
- **Validation**:
  - Trim whitespace
  - Normalize text
  - Check for empty submissions

### 3.4 Content Reveal Phase
- **Reveal Strategy**:
  - Immediate: Show segment after response
  - Delayed: 2-5 second delay for reflection
  - Progressive: Reveal sentence by sentence
- **Display**:
  - Highlight predicted content vs actual content
  - Show segment in original formatting
  - Context: 1-2 sentences before/after for continuity

### 3.5 Feedback Phase
- **Accuracy Assessment**:
  - Exact match: "Perfect prediction!"
  - Partial match (≥60% semantic similarity): "Great intuition!"
  - Close concept: "Similar thinking, different angle"
  - Off-track: "Interesting thought, let's see what was actually said"
- **Feedback Display**:
  - Short feedback message (1-2 sentences)
  - Comparison of user answer vs actual content
  - Explanation of key differences (if applicable)
  - Encouragement emoji/icons

### 3.6 Progression Controls
After feedback, user can:
- **Continue**: Next segment (enabled by default)
- **Review**: Re-read current segment
- **Pause**: Save progress and exit
- **Skip**: Skip to next segment (tracked)
- **Restart**: Start article over

### 3.7 Session Persistence
- Auto-save session state (position, responses, time)
- Resume session from last position
- Allow offline mode (local storage sync)
- Support tabbed browsing (prevent duplicate progress)

## Technical Specifications

### Conversation Flow Schema
```json
{
  "session_state": {
    "session_id": "uuid",
    "article_id": "uuid",
    "current_segment_index": 5,
    "total_segments": 20,
    "current_phase": "QUESTION_READY|AWAITING_RESPONSE|...",
    "timestamp": "ISO-8601",
    "client_state": "in_progress|paused|completed"
  },
  "question_context": {
    "question_id": "uuid",
    "segment_id": "uuid",
    "question_text": "string",
    "difficulty": 3,
    "input_type": "free_text|multiple_choice|scale",
    "reveal_strategy": "immediate|delayed",
    "hints": ["hint1", "hint2"]
  },
  "user_interaction": {
    "response_id": "uuid",
    "user_answer": "string",
    "response_time_ms": 8500,
    "input_method": "keyboard|voice|selection",
    "hint_used": false,
    "submitted_at": "timestamp"
  },
  "feedback": {
    "accuracy_score": 0.75,
    "feedback_message": "string",
    "revealed_segment": "string",
    "comparison": {
      "user_key_points": ["point1", "point2"],
      "actual_key_points": ["point1", "point3"],
      "overlap": ["point1"]
    }
  }
}
```

### Event Stream
```json
{
  "events": [
    {"type": "session_started", "timestamp": "...", "session_id": "..."},
    {"type": "question_displayed", "timestamp": "...", "question_id": "..."},
    {"type": "hint_requested", "timestamp": "...", "hint_index": 0},
    {"type": "response_submitted", "timestamp": "...", "response": "...", "response_time_ms": 8500},
    {"type": "content_revealed", "timestamp": "...", "segment_id": "..."},
    {"type": "feedback_shown", "timestamp": "...", "accuracy_score": 0.75},
    {"type": "next_segment_selected", "timestamp": "..."},
    {"type": "session_paused", "timestamp": "..."},
    {"type": "session_completed", "timestamp": "...", "total_time_ms": 450000}
  ]
}
```

## Acceptance Criteria
- [ ] Smooth state transitions between all phases
- [ ] User input validated before processing
- [ ] Responses saved within 100ms
- [ ] Accuracy scoring ≥85% accurate
- [ ] Feedback messages personalized and encouraging
- [ ] Session resumption works across browser sessions
- [ ] Progress not lost on page refresh
- [ ] Mobile-friendly flow (touch-optimized inputs)
- [ ] Accessibility: Keyboard-navigable, screen-reader compatible

## Dependencies
- Frontend framework (React/Vue/Svelte)
- State management (Redux/Vuex/Zustand)
- Real-time synchronization (WebSocket or polling)
- Local storage API

## Success Metrics
- Session completion rate: ≥70%
- Average time per segment: 30-120 seconds
- User satisfaction: ≥4/5
- Mobile usability: ≥4/5
- Zero progress loss: 100% recovery rate
