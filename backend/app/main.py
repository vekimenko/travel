"""FastAPI application factory"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from alembic.config import Config
from alembic.command import upgrade
import os
import logging

logger = logging.getLogger(__name__)


def run_migrations():
    """Run Alembic migrations"""
    try:
        migrations_dir = os.path.join(os.path.dirname(__file__), "..", "migrations")
        alembic_cfg = Config(os.path.join(migrations_dir, "alembic.ini"))
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        upgrade(alembic_cfg, "head")
        logger.info("✅ Database migrations completed")
    except Exception as e:
        logger.error(f"⚠️  Migration error: {e}")
        raise


def create_app() -> FastAPI:
    """Create and configure FastAPI app"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version="0.1.0",
    )

    # Run migrations on startup
    run_migrations()

    # Add CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include routers (to be added later)
    # app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "ok", "environment": settings.ENVIRONMENT}

    return app


app = create_app()
