"""v1 API endpoints"""
from fastapi import APIRouter
from app.api.v1.articles import router as articles_router

api_router = APIRouter()
api_router.include_router(articles_router)

__all__ = ["api_router"]
