"""Tests for database models"""
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models import Article, Segment, Question, UserResponse
from app.repositories import (
    ArticleRepository,
    SegmentRepository,
    QuestionRepository,
    SessionRepository,
    UserResponseRepository,
)


def test_article_creation(db_session: Session):
    """Test creating an article"""
    repo = ArticleRepository(db_session)
    article_data = {
        "title": "Test Article",
        "content": "This is test content",
        "category": "Science",
        "difficulty_level": 3,
    }
    article = repo.create(article_data)

    assert article.id is not None
    assert article.title == "Test Article"
    assert article.category == "Science"

    # Verify it was saved
    fetched = repo.get(article.id)
    assert fetched is not None
    assert fetched.title == "Test Article"


def test_segment_creation(db_session: Session):
    """Test creating segments for an article"""
    article_repo = ArticleRepository(db_session)
    segment_repo = SegmentRepository(db_session)

    # Create article
    article = article_repo.create({
        "title": "Test Article",
        "content": "Content",
    })

    # Create segments
    segment1 = segment_repo.create({
        "article_id": article.id,
        "position": 0,
        "content": "First segment",
        "type": "introduction",
        "difficulty": 2,
    })

    segment2 = segment_repo.create({
        "article_id": article.id,
        "position": 1,
        "content": "Second segment",
        "type": "fact",
        "difficulty": 3,
    })

    # Fetch all segments
    segments = segment_repo.get_by_article(article.id)
    assert len(segments) == 2
    assert segments[0].position == 0
    assert segments[1].position == 1


def test_question_creation(db_session: Session):
    """Test creating a question for a segment"""
    article_repo = ArticleRepository(db_session)
    segment_repo = SegmentRepository(db_session)
    question_repo = QuestionRepository(db_session)

    # Create article and segment
    article = article_repo.create({"title": "Test", "content": "Content"})
    segment = segment_repo.create({
        "article_id": article.id,
        "position": 0,
        "content": "Test segment",
        "type": "fact",
    })

    # Create question
    question = question_repo.create({
        "segment_id": segment.id,
        "question_text": "What is the main idea?",
        "question_type": "predictive",
        "difficulty": 3,
        "hints": ["Think about...", "Consider..."],
        "acceptable_answers": ["Answer 1", "Answer 2"],
    })

    assert question.id is not None
    assert question.question_text == "What is the main idea?"
    assert len(question.hints) == 2

    # Fetch question
    fetched_question = question_repo.get_by_segment(segment.id)
    assert fetched_question is not None
    assert fetched_question.question_type == "predictive"


def test_session_creation(db_session: Session):
    """Test creating a session"""
    from app.models import Session as SessionModel
    from app.repositories import SessionRepository

    article_repo = ArticleRepository(db_session)
    session_repo = SessionRepository(db_session)

    # Create article
    article = article_repo.create({"title": "Test", "content": "Content"})

    # Create session
    session = session_repo.create({
        "article_id": article.id,
        "status": "active",
        "current_segment_index": 0,
        "total_segments": 5,
    })

    assert session.id is not None
    assert session.status == "active"
    assert session.current_segment_index == 0


def test_user_response_tracking(db_session: Session):
    """Test creating and tracking user responses"""
    article_repo = ArticleRepository(db_session)
    segment_repo = SegmentRepository(db_session)
    question_repo = QuestionRepository(db_session)
    session_repo = SessionRepository(db_session)
    response_repo = UserResponseRepository(db_session)

    # Create article with segment
    article = article_repo.create({"title": "Test", "content": "Content"})
    segment = segment_repo.create({
        "article_id": article.id,
        "position": 0,
        "content": "Test segment",
        "type": "fact",
    })
    question = question_repo.create({
        "segment_id": segment.id,
        "question_text": "What?",
        "question_type": "predictive",
    })

    # Create session
    session = session_repo.create({"article_id": article.id})

    # Create response
    response = response_repo.create({
        "session_id": session.id,
        "question_id": question.id,
        "segment_id": segment.id,
        "user_answer": "User's answer",
        "response_time_ms": 5000,
        "accuracy_score": 0.85,
        "accuracy_category": "good",
    })

    assert response.accuracy_score == 0.85
    assert response.accuracy_category == "good"

    # Fetch responses for session
    responses = response_repo.get_by_session(session.id)
    assert len(responses) == 1
    assert responses[0].user_answer == "User's answer"


def test_repository_get_all(db_session: Session):
    """Test getting all records"""
    repo = ArticleRepository(db_session)

    # Create multiple articles
    for i in range(5):
        repo.create({
            "title": f"Article {i}",
            "content": f"Content {i}",
        })

    # Get all
    articles = repo.get_all(skip=0, limit=10)
    assert len(articles) == 5

    # Get with pagination
    articles = repo.get_all(skip=2, limit=2)
    assert len(articles) == 2


if __name__ == "__main__":
    pytest.main([__file__])
