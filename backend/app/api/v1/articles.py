"""Article ingestion API endpoints"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.article_processor import ArticleProcessor
from app.schemas import ArticleCreate, ArticleResponse, SegmentResponse
from pydantic import BaseModel


# Response schemas
class SegmentDetailResponse(BaseModel):
    """Detailed segment response"""
    id: UUID
    position: int
    content: str
    type: str
    difficulty: int
    entities: list
    keywords: list
    char_count: int

    class Config:
        from_attributes = True


class ArticleProcessingResponse(BaseModel):
    """Response from article processing"""
    article: ArticleResponse
    segments: list[SegmentDetailResponse]
    metadata: dict

    class Config:
        from_attributes = True


class ArticleSummaryResponse(BaseModel):
    """Summary of article with statistics"""
    article_id: UUID
    title: str
    category: Optional[str]
    total_segments: int
    segment_types: dict
    average_difficulty: float
    total_words: int


# Create router
router = APIRouter(prefix="/api/v1/articles", tags=["articles"])


@router.post("/ingest", response_model=ArticleProcessingResponse)
async def ingest_article(
    title: str = Form(None),
    content: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    source_url: Optional[str] = Form(None),
    source_format: str = Form("txt"),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """Ingest and process an article
    
    Accepts either:
    - Raw text via 'content' form field
    - File upload via 'file' parameter
    
    Returns segmented article with metadata
    """
    try:
        # Get content from form or file
        if file:
            if file.size and file.size > 10 * 1024 * 1024:  # 10MB limit
                raise HTTPException(status_code=413, detail="File too large (max 10MB)")

            content = (await file.read()).decode("utf-8", errors="ignore")
            source_format = file.filename.split(".")[-1] if file.filename else "txt"
        elif not content:
            raise HTTPException(status_code=400, detail="Content or file required")

        # Auto-detect format from file extension if not specified
        if file and source_format == "txt":
            ext = file.filename.split(".")[-1].lower() if file.filename else "txt"
            if ext in ["md", "html"]:
                source_format = ext

        # Validate content
        if not content or not content.strip():
            raise HTTPException(status_code=400, detail="Content is empty")

        # Process article
        processor = ArticleProcessor(db)
        result = processor.process_article(
            title=title,
            content=content,
            source_format=source_format,
            category=category,
            author=author,
            source_url=source_url,
        )

        # Build response
        return ArticleProcessingResponse(
            article=ArticleResponse.from_attributes(result["article"]),
            segments=[
                SegmentDetailResponse(
                    id=seg.id,
                    position=seg.position,
                    content=seg.content,
                    type=seg.type,
                    difficulty=seg.difficulty,
                    entities=seg.entities or [],
                    keywords=seg.keywords or [],
                    char_count=len(seg.content),
                )
                for seg in result["segments"]
            ],
            metadata=result["metadata"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/ingest-text", response_model=ArticleProcessingResponse)
async def ingest_text(
    article: ArticleCreate,
    db: Session = Depends(get_db),
):
    """Ingest article from JSON body
    
    Simpler endpoint for text-based ingestion
    """
    try:
        processor = ArticleProcessor(db)
        result = processor.process_article(
            title=article.title,
            content=article.content,
            source_format=getattr(article, "source_format", "txt"),
            category=getattr(article, "category", None),
        )

        return ArticleProcessingResponse(
            article=ArticleResponse.from_attributes(result["article"]),
            segments=[
                SegmentDetailResponse(
                    id=seg.id,
                    position=seg.position,
                    content=seg.content,
                    type=seg.type,
                    difficulty=seg.difficulty,
                    entities=seg.entities or [],
                    keywords=seg.keywords or [],
                    char_count=len(seg.content),
                )
                for seg in result["segments"]
            ],
            metadata=result["metadata"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.get("/{article_id}/summary", response_model=ArticleSummaryResponse)
async def get_article_summary(
    article_id: UUID,
    db: Session = Depends(get_db),
):
    """Get summary statistics for an article"""
    try:
        processor = ArticleProcessor(db)
        summary = processor.get_article_summary(article_id)
        return ArticleSummaryResponse(**summary)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/{article_id}/reprocess")
async def reprocess_article(
    article_id: UUID,
    db: Session = Depends(get_db),
):
    """Reprocess an existing article with latest algorithm
    
    Deletes old segments and creates new ones
    """
    try:
        processor = ArticleProcessor(db)
        result = processor.reprocess_article(article_id)

        return ArticleProcessingResponse(
            article=ArticleResponse.from_attributes(result["article"]),
            segments=[
                SegmentDetailResponse(
                    id=seg.id,
                    position=seg.position,
                    content=seg.content,
                    type=seg.type,
                    difficulty=seg.difficulty,
                    entities=seg.entities or [],
                    keywords=seg.keywords or [],
                    char_count=len(seg.content),
                )
                for seg in result["segments"]
            ],
            metadata=result["metadata"],
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
