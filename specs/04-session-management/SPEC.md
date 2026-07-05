# Feature: Session Management

## Overview
Track user progress through articles, manage session state, and enable resumption across devices and sessions.

## User Story
As a user, I want my progress to be saved automatically so that I can resume reading an article where I left off without losing any responses or progress.

## Functional Requirements

### 4.1 Session Lifecycle
- **Create**: New session on article start
- **Active**: User is reading/responding
- **Paused**: User leaves (auto-save)
- **Resumed**: User returns to continue
- **Completed**: Article finished
- **Abandoned**: No activity for 30+ days (archive)

### 4.2 Session Initialization
- Create session on article access
- Link session to user (or anonymous ID)
- Set initial state: segment 0, no responses
- Record start time and device info
- Generate session ID (UUID)

### 4.3 Progress Tracking
For each session, track:
- **Current segment**: Index in article
- **Responses**: All user answers with timestamps
- **Time spent**: Per segment and total
- **Hints used**: Which hints accessed
- **Pauses/Resumes**: Session interruptions
- **Metadata**: Device, location (if available), language

### 4.4 Auto-save Mechanism
- Save every state change (debounced, max 5s intervals)
- Save on page unload/close
- Save on pause action
- Local caching first, then sync to server
- Retry logic for failed saves

### 4.5 Resume Session
- Detect existing session on return
- Restore to exact position
- Re-validate saved state
- Offer: Continue from where you left off / Restart / Switch article
- Merge offline changes with server state

### 4.6 Multi-device Sync
- Same user across devices: sync progress
- Conflict resolution: Most recent version wins
- Local offline capability (sync on reconnect)
- Cross-tab synchronization (broadcast channels)

### 4.7 Session Analytics
Calculate and store:
- **Duration**: Total time spent
- **Engagement**: % segments completed
- **Accuracy**: Average prediction accuracy
- **Pace**: Average time per segment
- **Completion status**: Complete / Partial / Abandoned

### 4.8 Session Privacy & Cleanup
- Session retention: 90 days (user configurable)
- Anonymous sessions: Cleared after 30 days inactivity
- GDPR compliance: Easy deletion option
- No PII storage in responses

## Technical Specifications

### Session Schema
```json
{
  "id": "uuid",
  "user_id": "uuid|null (anonymous)",
  "article_id": "uuid",
  "started_at": "timestamp",
  "last_accessed": "timestamp",
  "completed_at": "timestamp|null",
  "status": "active|paused|completed|abandoned",
  "current_segment_index": 5,
  "total_segments": 20,
  "segments_completed": 5,
  "segments_skipped": 0,
  "questions_answered": 5,
  "metadata": {
    "device": "web|mobile|tablet",
    "user_agent": "string",
    "language": "en",
    "theme": "light|dark",
    "offline_edits": 0
  },
  "statistics": {
    "total_duration_ms": 450000,
    "avg_segment_duration_ms": 90000,
    "accuracy_score": 0.72,
    "engagement_rate": 0.85,
    "hints_used": 2,
    "times_paused": 3
  },
  "sync_state": {
    "last_sync": "timestamp",
    "pending_changes": false,
    "version": 3
  }
}
```

### Session Response Log
```json
{
  "responses": [
    {
      "response_id": "uuid",
      "segment_index": 0,
      "question_id": "uuid",
      "user_answer": "string",
      "accuracy_score": 0.85,
      "response_time_ms": 12500,
      "timestamp": "timestamp",
      "hint_used": false,
      "synced": true
    }
  ]
}
```

## Acceptance Criteria
- [ ] Session created on first article access
- [ ] Progress saved within 5s of state change
- [ ] Session resumed within 100ms
- [ ] Accuracy calculation ≥95% correct
- [ ] Multi-device sync within 10s
- [ ] Offline changes merge correctly (0 loss)
- [ ] Session cleanup: automatic after retention period
- [ ] Cross-tab sync prevents duplicates
- [ ] Mobile app sync works without errors

## Dependencies
- Database (PostgreSQL/MongoDB)
- Backend API
- Redux/Zustand (frontend state management)
- IndexedDB (offline storage)
- Service Worker (background sync)

## Success Metrics
- Session persistence: 100% recovery rate
- Resume time: <500ms
- Sync accuracy: 100%
- User retention (week 1→2): ≥60%
- Completion rate: ≥70% of started articles
