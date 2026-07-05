"""Initial migration - create core tables

Revision ID: 001_initial
Revises:
Create Date: 2026-07-04 23:13:30.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("username", sa.String(255), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("password_hash", sa.String(255), nullable=True),
        sa.Column("profile_data", sa.JSON(), nullable=True),
        sa.Column("preferences", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("username", name="uq_users_username"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=False)

    # Create articles table
    op.create_table(
        "articles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=True),
        sa.Column("source_url", sa.String(2048), nullable=True),
        sa.Column("source_format", sa.String(10), nullable=True),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("difficulty_level", sa.Integer(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("metadata_", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("content_hash", name="uq_articles_content_hash"),
        sa.CheckConstraint("difficulty_level >= 1 AND difficulty_level <= 5"),
    )
    op.create_index("ix_articles_created_at", "articles", ["created_at"], unique=False)
    op.create_index("ix_articles_category", "articles", ["category"], unique=False)
    op.create_index("ix_articles_difficulty_level", "articles", ["difficulty_level"], unique=False)

    # Create segments table
    op.create_table(
        "segments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("article_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("char_count", sa.Integer(), nullable=True),
        sa.Column("difficulty", sa.Integer(), nullable=True),
        sa.Column("entities", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("keywords", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("metadata_", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"], ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("article_id", "position", name="uq_segment_position"),
        sa.CheckConstraint("difficulty >= 1 AND difficulty <= 5"),
    )
    op.create_index("ix_segments_article_id", "segments", ["article_id"], unique=False)
    op.create_index("ix_segments_position", "segments", ["position"], unique=False)
    op.create_index("ix_segments_type", "segments", ["type"], unique=False)
    op.create_index("ix_segments_difficulty", "segments", ["difficulty"], unique=False)

    # Create questions table
    op.create_table(
        "questions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("segment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("question_type", sa.String(50), nullable=False),
        sa.Column("difficulty", sa.Integer(), nullable=True),
        sa.Column("acceptable_answers", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("hints", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("generated_by", sa.String(50), nullable=True),
        sa.Column("quality_score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("metadata_", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["segment_id"], ["segments.id"], ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("difficulty >= 1 AND difficulty <= 5"),
    )
    op.create_index("ix_questions_segment_id", "questions", ["segment_id"], unique=False)
    op.create_index("ix_questions_type", "questions", ["question_type"], unique=False)
    op.create_index("ix_questions_difficulty", "questions", ["difficulty"], unique=False)

    # Create sessions table
    op.create_table(
        "sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("article_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("started_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("last_accessed", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("current_segment_index", sa.Integer(), nullable=True),
        sa.Column("total_segments", sa.Integer(), nullable=True),
        sa.Column("segments_completed", sa.Integer(), nullable=True),
        sa.Column("segments_skipped", sa.Integer(), nullable=True),
        sa.Column("questions_answered", sa.Integer(), nullable=True),
        sa.Column("metadata_", sa.JSON(), nullable=True),
        sa.Column("statistics", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"], ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"], unique=False)
    op.create_index("ix_sessions_article_id", "sessions", ["article_id"], unique=False)
    op.create_index("ix_sessions_status", "sessions", ["status"], unique=False)
    op.create_index("ix_sessions_created_at", "sessions", ["created_at"], unique=False)

    # Create user_responses table
    op.create_table(
        "user_responses",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("question_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("segment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_answer", sa.Text(), nullable=False),
        sa.Column("answer_type", sa.String(50), nullable=True),
        sa.Column("response_time_ms", sa.Integer(), nullable=True),
        sa.Column("accuracy_score", sa.Float(), nullable=True),
        sa.Column("accuracy_category", sa.String(50), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("feedback_detail", sa.JSON(), nullable=True),
        sa.Column("hint_used", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ),
        sa.ForeignKeyConstraint(["segment_id"], ["segments.id"], ),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("accuracy_score >= 0 AND accuracy_score <= 1"),
    )
    op.create_index("ix_responses_session_id", "user_responses", ["session_id"], unique=False)
    op.create_index("ix_responses_question_id", "user_responses", ["question_id"], unique=False)
    op.create_index("ix_responses_segment_id", "user_responses", ["segment_id"], unique=False)
    op.create_index("ix_responses_accuracy_category", "user_responses", ["accuracy_category"], unique=False)
    op.create_index("ix_responses_created_at", "user_responses", ["created_at"], unique=False)

    # Create analytics_events table
    op.create_table(
        "analytics_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("article_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("segment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("event_data", sa.JSON(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analytics_timestamp", "analytics_events", ["timestamp"], unique=False)
    op.create_index("ix_analytics_session_id", "analytics_events", ["session_id"], unique=False)
    op.create_index("ix_analytics_event_type", "analytics_events", ["event_type"], unique=False)
    op.create_index("ix_analytics_user_id", "analytics_events", ["user_id"], unique=False)

    # Create analytics_aggregations table
    op.create_table(
        "analytics_aggregations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("aggregation_type", sa.String(50), nullable=False),
        sa.Column("period_start", sa.DateTime(), nullable=True),
        sa.Column("period_end", sa.DateTime(), nullable=True),
        sa.Column("article_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("metrics", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_aggregations_type", "analytics_aggregations", ["aggregation_type"], unique=False)
    op.create_index("ix_aggregations_period", "analytics_aggregations", ["period_start", "period_end"], unique=False)
    op.create_index("ix_aggregations_article_id", "analytics_aggregations", ["article_id"], unique=False)
    op.create_index("ix_aggregations_user_id", "analytics_aggregations", ["user_id"], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_index("ix_aggregations_user_id", table_name="analytics_aggregations")
    op.drop_index("ix_aggregations_article_id", table_name="analytics_aggregations")
    op.drop_index("ix_aggregations_period", table_name="analytics_aggregations")
    op.drop_index("ix_aggregations_type", table_name="analytics_aggregations")
    op.drop_table("analytics_aggregations")

    op.drop_index("ix_analytics_user_id", table_name="analytics_events")
    op.drop_index("ix_analytics_event_type", table_name="analytics_events")
    op.drop_index("ix_analytics_session_id", table_name="analytics_events")
    op.drop_index("ix_analytics_timestamp", table_name="analytics_events")
    op.drop_table("analytics_events")

    op.drop_index("ix_responses_created_at", table_name="user_responses")
    op.drop_index("ix_responses_accuracy_category", table_name="user_responses")
    op.drop_index("ix_responses_segment_id", table_name="user_responses")
    op.drop_index("ix_responses_question_id", table_name="user_responses")
    op.drop_index("ix_responses_session_id", table_name="user_responses")
    op.drop_table("user_responses")

    op.drop_index("ix_sessions_created_at", table_name="sessions")
    op.drop_index("ix_sessions_status", table_name="sessions")
    op.drop_index("ix_sessions_article_id", table_name="sessions")
    op.drop_index("ix_sessions_user_id", table_name="sessions")
    op.drop_table("sessions")

    op.drop_index("ix_questions_difficulty", table_name="questions")
    op.drop_index("ix_questions_type", table_name="questions")
    op.drop_index("ix_questions_segment_id", table_name="questions")
    op.drop_table("questions")

    op.drop_index("ix_segments_difficulty", table_name="segments")
    op.drop_index("ix_segments_type", table_name="segments")
    op.drop_index("ix_segments_position", table_name="segments")
    op.drop_index("ix_segments_article_id", table_name="segments")
    op.drop_table("segments")

    op.drop_index("ix_articles_difficulty_level", table_name="articles")
    op.drop_index("ix_articles_category", table_name="articles")
    op.drop_index("ix_articles_created_at", table_name="articles")
    op.drop_table("articles")

    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
