"""Pydantic schemas for API requests/responses"""
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


# Article Schemas
class ArticleBase(BaseModel):
    """Base article schema"""
    title: str
    content: str
    category: Optional[str] = None
    source_url: Optional[str] = None
    source_format: str = "txt"
    difficulty_level: int = 3


class ArticleCreate(ArticleBase):
    """Schema for creating article"""
    pass


class ArticleUpdate(BaseModel):
    """Schema for updating article"""
    title: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[int] = None


class ArticleResponse(ArticleBase):
    """Schema for article response"""
    id: UUID
    content_hash: Optional[str] = None
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Segment Schemas
class SegmentBase(BaseModel):
    """Base segment schema"""
    content: str
    type: str
    difficulty: int = 3
    entities: List[str] = []
    keywords: List[str] = []


class SegmentCreate(SegmentBase):
    """Schema for creating segment"""
    position: int
    article_id: UUID


class SegmentResponse(SegmentBase):
    """Schema for segment response"""
    id: UUID
    article_id: UUID
    position: int
    char_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# Question Schemas
class QuestionBase(BaseModel):
    """Base question schema"""
    question_text: str
    question_type: str
    difficulty: int = 3
    acceptable_answers: List[str] = []
    hints: List[str] = []
    generated_by: str = "template"


class QuestionCreate(QuestionBase):
    """Schema for creating question"""
    segment_id: UUID


class QuestionResponse(QuestionBase):
    """Schema for question response"""
    id: UUID
    segment_id: UUID
    quality_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Session Schemas
class SessionBase(BaseModel):
    """Base session schema"""
    article_id: UUID
    user_id: Optional[UUID] = None


class SessionCreate(SessionBase):
    """Schema for creating session"""
    pass


class SessionUpdate(BaseModel):
    """Schema for updating session"""
    current_segment_index: Optional[int] = None
    status: Optional[str] = None
    segments_completed: Optional[int] = None
    segments_skipped: Optional[int] = None
    questions_answered: Optional[int] = None


class SessionResponse(SessionBase):
    """Schema for session response"""
    id: UUID
    started_at: datetime
    last_accessed: datetime
    completed_at: Optional[datetime] = None
    status: str
    current_segment_index: int
    total_segments: int
    segments_completed: int
    segments_skipped: int
    questions_answered: int
    statistics: dict

    class Config:
        from_attributes = True


# User Response Schemas
class UserResponseBase(BaseModel):
    """Base user response schema"""
    user_answer: str
    answer_type: str = "free_text"
    response_time_ms: Optional[int] = None
    hint_used: bool = False


class UserResponseCreate(UserResponseBase):
    """Schema for creating user response"""
    session_id: UUID
    question_id: UUID
    segment_id: UUID


class UserResponseResponse(UserResponseBase):
    """Schema for user response response"""
    id: UUID
    session_id: UUID
    question_id: UUID
    segment_id: UUID
    accuracy_score: Optional[float] = None
    accuracy_category: Optional[str] = None
    feedback: Optional[str] = None
    feedback_detail: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Analytics Schemas
class AnalyticsEventCreate(BaseModel):
    """Schema for creating analytics event"""
    event_type: str
    session_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    article_id: Optional[UUID] = None
    segment_id: Optional[UUID] = None
    event_data: dict = {}


class AnalyticsEventResponse(AnalyticsEventCreate):
    """Schema for analytics event response"""
    id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True


# Bulk Operations
class ArticleWithSegments(ArticleResponse):
    """Article with all segments"""
    segments: List[SegmentResponse] = []


class SegmentWithQuestion(SegmentResponse):
    """Segment with associated question"""
    question: Optional[QuestionResponse] = None


class SessionWithResponses(SessionResponse):
    """Session with all responses"""
    responses: List[UserResponseResponse] = []
