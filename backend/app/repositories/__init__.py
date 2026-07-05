"""Repositories for database access"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models import Article, Segment, Question, Session as SessionModel, UserResponse
from app.repositories.base import BaseRepository


class ArticleRepository(BaseRepository[Article]):
    """Repository for Article model"""

    def __init__(self, session: Session):
        super().__init__(session, Article)

    def get_by_title(self, title: str) -> Optional[Article]:
        """Get article by title"""
        return self.session.query(self.model).filter(self.model.title == title).first()

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Article]:
        """Get articles by category"""
        return (
            self.session.query(self.model)
            .filter(self.model.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_difficulty(self, difficulty: int, skip: int = 0, limit: int = 100) -> List[Article]:
        """Get articles by difficulty level"""
        return (
            self.session.query(self.model)
            .filter(self.model.difficulty_level == difficulty)
            .offset(skip)
            .limit(limit)
            .all()
        )


class SegmentRepository(BaseRepository[Segment]):
    """Repository for Segment model"""

    def __init__(self, session: Session):
        super().__init__(session, Segment)

    def get_by_article(self, article_id: UUID) -> List[Segment]:
        """Get all segments for an article ordered by position"""
        return (
            self.session.query(self.model)
            .filter(self.model.article_id == article_id)
            .order_by(self.model.position)
            .all()
        )

    def get_segment_at_position(self, article_id: UUID, position: int) -> Optional[Segment]:
        """Get segment at specific position"""
        return (
            self.session.query(self.model)
            .filter(self.model.article_id == article_id, self.model.position == position)
            .first()
        )

    def count_by_article(self, article_id: UUID) -> int:
        """Count segments in article"""
        return self.session.query(self.model).filter(self.model.article_id == article_id).count()


class QuestionRepository(BaseRepository[Question]):
    """Repository for Question model"""

    def __init__(self, session: Session):
        super().__init__(session, Question)

    def get_by_segment(self, segment_id: UUID) -> Optional[Question]:
        """Get question for a segment"""
        return self.session.query(self.model).filter(self.model.segment_id == segment_id).first()

    def get_by_type(self, question_type: str, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get questions by type"""
        return (
            self.session.query(self.model)
            .filter(self.model.question_type == question_type)
            .offset(skip)
            .limit(limit)
            .all()
        )


class SessionRepository(BaseRepository[SessionModel]):
    """Repository for Session model"""

    def __init__(self, session: Session):
        super().__init__(session, SessionModel)

    def get_by_user_article(self, user_id: Optional[UUID], article_id: UUID) -> Optional[SessionModel]:
        """Get session by user and article"""
        query = self.session.query(self.model).filter(self.model.article_id == article_id)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.first()

    def get_active_sessions(self, user_id: Optional[UUID] = None) -> List[SessionModel]:
        """Get active sessions"""
        query = self.session.query(self.model).filter(self.model.status == "active")
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.all()

    def get_user_sessions(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[SessionModel]:
        """Get all sessions for a user"""
        return (
            self.session.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


class UserResponseRepository(BaseRepository[UserResponse]):
    """Repository for UserResponse model"""

    def __init__(self, session: Session):
        super().__init__(session, UserResponse)

    def get_by_session(self, session_id: UUID) -> List[UserResponse]:
        """Get all responses in a session"""
        return (
            self.session.query(self.model)
            .filter(self.model.session_id == session_id)
            .order_by(self.model.created_at)
            .all()
        )

    def get_by_question(self, question_id: UUID) -> List[UserResponse]:
        """Get all responses to a question"""
        return self.session.query(self.model).filter(self.model.question_id == question_id).all()

    def get_average_accuracy(self, session_id: UUID) -> Optional[float]:
        """Get average accuracy for a session"""
        result = (
            self.session.query(self.model.accuracy_score)
            .filter(self.model.session_id == session_id, self.model.accuracy_score.isnot(None))
            .all()
        )
        if not result:
            return None
        scores = [r[0] for r in result if r[0] is not None]
        return sum(scores) / len(scores) if scores else None
