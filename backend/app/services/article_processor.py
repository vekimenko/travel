"""Article processor - orchestrates ingestion and segmentation"""
import time
from typing import List, Dict, Any
from datetime import datetime
from uuid import UUID
from app.services.text_processor import TextProcessor
from app.services.nlp_service import NLPService
from app.models import Article, Segment
from app.repositories import ArticleRepository, SegmentRepository
from sqlalchemy.orm import Session


class ArticleProcessor:
    """Process and segment articles end-to-end"""

    def __init__(self, db_session: Session):
        self.db = db_session
        self.article_repo = ArticleRepository(db_session)
        self.segment_repo = SegmentRepository(db_session)

    def process_article(
        self,
        title: str,
        content: str,
        source_format: str = "txt",
        category: str = None,
        author: str = None,
        source_url: str = None,
        difficulty_override: int = None,
    ) -> Dict[str, Any]:
        """Process article end-to-end
        
        Returns: {
            'article': Article object,
            'segments': List[Segment objects],
            'metadata': processing metadata
        }
        """
        start_time = time.time()

        # Step 1: Clean text
        cleaned_content = TextProcessor.clean_text(content, source_format)
        if not cleaned_content:
            raise ValueError("Content is empty after cleaning")

        # Step 2: Extract metadata
        extracted_title = TextProcessor.extract_title(cleaned_content, title)
        reading_time = TextProcessor.estimate_reading_time(cleaned_content)
        content_hash = TextProcessor.calculate_content_hash(cleaned_content)

        # Step 3: Create article in database
        article_data = {
            "title": extracted_title,
            "content": cleaned_content,
            "category": category,
            "difficulty_level": difficulty_override or 3,
            "source_format": source_format,
            "source_url": source_url,
            "content_hash": content_hash,
            "metadata_": {
                "author": author,
                "reading_time_seconds": reading_time,
                "source_format": source_format,
            },
        }

        article = self.article_repo.create(article_data)
        self.db.commit()

        # Step 4: Segment the article
        segments_data = self._segment_article(cleaned_content, article.id)

        # Step 5: Create segments in database
        segments = []
        for idx, seg_data in enumerate(segments_data):
            seg_data["article_id"] = article.id
            seg_data["position"] = idx
            segment = self.segment_repo.create(seg_data)
            segments.append(segment)

        self.db.commit()

        # Calculate quality score
        quality_score = self._calculate_overall_quality(segments)

        processing_time = (time.time() - start_time) * 1000  # milliseconds

        return {
            "article": article,
            "segments": segments,
            "metadata": {
                "status": "success",
                "processing_time_ms": round(processing_time, 2),
                "total_segments": len(segments),
                "content_quality_score": quality_score,
                "reading_time_seconds": reading_time,
            },
        }

    def _segment_article(self, content: str, article_id: UUID) -> List[Dict[str, Any]]:
        """Segment article and enrich segments with metadata
        
        Returns: List of segment data dictionaries
        """
        # Use hybrid segmentation (paragraph + sentence-aware)
        raw_segments = TextProcessor.segment_into_chunks(
            content, method="hybrid"
        )

        if not raw_segments:
            raise ValueError("No segments could be created from content")

        segments_data = []

        for idx, segment_text in enumerate(raw_segments):
            # Classify segment
            segment_type = NLPService.classify_segment(
                segment_text, position=idx, total_segments=len(raw_segments)
            )

            # Extract entities and keywords
            entities = NLPService.extract_entities(segment_text)
            keywords = NLPService.extract_keywords(segment_text)

            # Estimate difficulty
            difficulty = NLPService.estimate_difficulty(
                segment_text, position=idx, total_segments=len(raw_segments)
            )

            # Get segment metadata
            seg_metadata = TextProcessor.get_segment_metadata(segment_text)

            segment_data = {
                "content": segment_text,
                "type": segment_type,
                "difficulty": difficulty,
                "entities": entities,
                "keywords": keywords,
                "metadata_": {
                    "char_count": seg_metadata["char_count"],
                    "word_count": seg_metadata["word_count"],
                    "sentence_count": seg_metadata["sentence_count"],
                    "contains_list": seg_metadata["contains_list"],
                    "contains_quote": seg_metadata["contains_quote"],
                    "segment_quality": round(
                        NLPService.calculate_content_quality(segment_text), 2
                    ),
                },
            }

            segments_data.append(segment_data)

        return segments_data

    def _calculate_overall_quality(self, segments: List[Segment]) -> float:
        """Calculate overall quality score for article"""
        if not segments:
            return 0.0

        quality_scores = []
        for segment in segments:
            if segment.metadata_ and "segment_quality" in segment.metadata_:
                quality_scores.append(segment.metadata_["segment_quality"])

        if not quality_scores:
            return 0.5

        avg_quality = sum(quality_scores) / len(quality_scores)
        return round(avg_quality, 2)

    def reprocess_article(self, article_id: UUID) -> Dict[str, Any]:
        """Reprocess an existing article
        
        Useful for algorithm improvements or manual corrections
        """
        article = self.article_repo.get(article_id)
        if not article:
            raise ValueError(f"Article {article_id} not found")

        # Delete existing segments
        existing_segments = self.db.query(Segment).filter(
            Segment.article_id == article_id
        ).all()
        for seg in existing_segments:
            self.db.delete(seg)
        self.db.commit()

        # Reprocess
        return self.process_article(
            title=article.title,
            content=article.content,
            source_format=article.source_format,
            category=article.category,
            author=article.metadata_.get("author") if article.metadata_ else None,
            source_url=article.source_url,
            difficulty_override=article.difficulty_level,
        )

    def get_article_summary(self, article_id: UUID) -> Dict[str, Any]:
        """Get summary of an article and its segments"""
        article = self.article_repo.get(article_id)
        if not article:
            raise ValueError(f"Article {article_id} not found")

        segments = self.db.query(Segment).filter(
            Segment.article_id == article_id
        ).all()

        segment_types = {}
        total_difficulty = 0

        for segment in segments:
            segment_types[segment.type] = segment_types.get(segment.type, 0) + 1
            total_difficulty += segment.difficulty

        avg_difficulty = (
            total_difficulty / len(segments) if segments else 0
        )

        return {
            "article_id": article_id,
            "title": article.title,
            "category": article.category,
            "total_segments": len(segments),
            "segment_types": dict(segment_types),
            "average_difficulty": round(avg_difficulty, 2),
            "total_words": sum(
                seg.metadata_.get("word_count", 0) if seg.metadata_ else 0
                for seg in segments
            ),
            "created_at": article.created_at,
        }
