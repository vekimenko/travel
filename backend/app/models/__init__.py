"""SQLAlchemy models for core entities"""
from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from sqlalchemy import (
    Column, String, Text, Integer, Float, DateTime,
    ForeignKey, JSON, Boolean, Index, CheckConstraint,
    func, UniqueConstraint, TypeDecorator, CHAR
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.db.base import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type using CHAR(32) for SQLite and UUID for PostgreSQL."""
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID())
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == 'postgresql':
            return str(value)
        if not isinstance(value, str):
            return value.hex
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        from uuid import UUID
        if isinstance(value, UUID):
            return value
        return UUID(value)


class Article(Base):
    """Article model"""
    __tablename__ = "articles"

    id = Column(GUID(), primary_key=True, default=uuid4)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), unique=True)
    source_url = Column(String(2048), nullable=True)
    source_format = Column(String(10), default="txt")  # txt, md, html
    category = Column(String(100), nullable=True)
    difficulty_level = Column(Integer, default=3)
    created_by = Column(GUID(), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    metadata_ = Column(JSON, default={})

    # Relationships
    segments = relationship("Segment", back_populates="article", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="article", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_articles_created_at", created_at),
        Index("ix_articles_category", category),
        Index("ix_articles_difficulty_level", difficulty_level),
        CheckConstraint("difficulty_level >= 1 AND difficulty_level <= 5"),
    )


class Segment(Base):
    """Article segment model"""
    __tablename__ = "segments"

    id = Column(GUID(), primary_key=True, default=uuid4)
    article_id = Column(GUID(), ForeignKey("articles.id"), nullable=False)
    position = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # introduction, premise, fact, evidence, conclusion, transition
    char_count = Column(Integer, default=0)
    difficulty = Column(Integer, default=3)
    entities = Column(JSON, default=[])
    keywords = Column(JSON, default=[])
    metadata_ = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    article = relationship("Article", back_populates="segments")
    questions = relationship("Question", back_populates="segment", cascade="all, delete-orphan")
    responses = relationship("UserResponse", back_populates="segment", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_segments_article_id", article_id),
        Index("ix_segments_position", position),
        Index("ix_segments_type", type),
        Index("ix_segments_difficulty", difficulty),
        UniqueConstraint("article_id", "position", name="uq_segment_position"),
        CheckConstraint("difficulty >= 1 AND difficulty <= 5"),
    )


class Question(Base):
    """Question model"""
    __tablename__ = "questions"

    id = Column(GUID(), primary_key=True, default=uuid4)
    segment_id = Column(GUID(), ForeignKey("segments.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # predictive, reflective, definition, inference, application
    difficulty = Column(Integer, default=3)
    acceptable_answers = Column(JSON, default=[])
    hints = Column(JSON, default=[])
    generated_by = Column(String(50), default="template")  # template, ai, manual
    quality_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    metadata_ = Column(JSON, default={})

    # Relationships
    segment = relationship("Segment", back_populates="questions")
    responses = relationship("UserResponse", back_populates="question", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_questions_segment_id", segment_id),
        Index("ix_questions_type", question_type),
        Index("ix_questions_difficulty", difficulty),
        CheckConstraint("difficulty >= 1 AND difficulty <= 5"),
    )


class User(Base):
    """User model (optional, for authentication)"""
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid4)
    username = Column(String(255), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=True)
    profile_data = Column(JSON, default={})
    preferences = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    sessions = relationship("Session", back_populates="user")

    __table_args__ = (
        Index("ix_users_email", email),
        Index("ix_users_username", username),
    )


class Session(Base):
    """User reading session model"""
    __tablename__ = "sessions"

    id = Column(GUID(), primary_key=True, default=uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=True)
    article_id = Column(GUID(), ForeignKey("articles.id"), nullable=False)
    started_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_accessed = Column(DateTime, server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="active")  # active, paused, completed, abandoned
    current_segment_index = Column(Integer, default=0)
    total_segments = Column(Integer, default=0)
    segments_completed = Column(Integer, default=0)
    segments_skipped = Column(Integer, default=0)
    questions_answered = Column(Integer, default=0)
    metadata_ = Column(JSON, default={})
    statistics = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")
    article = relationship("Article", back_populates="sessions")
    responses = relationship("UserResponse", back_populates="session", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_sessions_user_id", user_id),
        Index("ix_sessions_article_id", article_id),
        Index("ix_sessions_status", status),
        Index("ix_sessions_created_at", created_at),
    )


class UserResponse(Base):
    """User response to question model"""
    __tablename__ = "user_responses"

    id = Column(GUID(), primary_key=True, default=uuid4)
    session_id = Column(GUID(), ForeignKey("sessions.id"), nullable=False)
    question_id = Column(GUID(), ForeignKey("questions.id"), nullable=False)
    segment_id = Column(GUID(), ForeignKey("segments.id"), nullable=False)
    user_answer = Column(Text, nullable=False)
    answer_type = Column(String(50), default="free_text")  # free_text, multiple_choice, scale
    response_time_ms = Column(Integer, nullable=True)
    accuracy_score = Column(Float, nullable=True)
    accuracy_category = Column(String(50), nullable=True)  # exact, excellent, good, partial, off_track
    feedback = Column(Text, nullable=True)
    feedback_detail = Column(JSON, nullable=True)
    hint_used = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    session = relationship("Session", back_populates="responses")
    question = relationship("Question", back_populates="responses")
    segment = relationship("Segment", back_populates="responses")

    __table_args__ = (
        Index("ix_responses_session_id", session_id),
        Index("ix_responses_question_id", question_id),
        Index("ix_responses_segment_id", segment_id),
        Index("ix_responses_accuracy_category", accuracy_category),
        Index("ix_responses_created_at", created_at),
        CheckConstraint("accuracy_score >= 0 AND accuracy_score <= 1"),
    )


class AnalyticsEvent(Base):
    """Analytics event stream"""
    __tablename__ = "analytics_events"

    id = Column(GUID(), primary_key=True, default=uuid4)
    event_type = Column(String(50), nullable=False)
    session_id = Column(GUID(), nullable=True)
    user_id = Column(GUID(), nullable=True)
    article_id = Column(GUID(), nullable=True)
    segment_id = Column(GUID(), nullable=True)
    event_data = Column(JSON, default={})
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_analytics_timestamp", timestamp),
        Index("ix_analytics_session_id", session_id),
        Index("ix_analytics_event_type", event_type),
        Index("ix_analytics_user_id", user_id),
    )


class AnalyticsAggregation(Base):
    """Pre-computed analytics aggregations"""
    __tablename__ = "analytics_aggregations"

    id = Column(GUID(), primary_key=True, default=uuid4)
    aggregation_type = Column(String(50), nullable=False)  # session, daily, weekly, article, user
    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)
    article_id = Column(GUID(), nullable=True)
    user_id = Column(GUID(), nullable=True)
    metrics = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_aggregations_type", aggregation_type),
        Index("ix_aggregations_period", period_start, period_end),
        Index("ix_aggregations_article_id", article_id),
        Index("ix_aggregations_user_id", user_id),
    )
