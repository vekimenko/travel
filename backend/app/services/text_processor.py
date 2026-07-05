"""Text cleaning and preprocessing service"""
import re
from typing import List, Tuple
import html


class TextProcessor:
    """Handles text cleaning and preprocessing"""

    MIN_SEGMENT_LENGTH = 20
    MAX_SEGMENT_LENGTH = 500
    MIN_SENTENCE_LENGTH = 10

    @staticmethod
    def clean_text(text: str, source_format: str = "txt") -> str:
        """Clean and normalize text content"""
        if not text:
            return ""

        # Handle HTML tags
        if source_format == "html" or "<" in text and ">" in text:
            text = html.unescape(text)
            text = re.sub(r"<[^>]+>", " ", text)

        # Normalize whitespace
        text = re.sub(r"\r\n", "\n", text)  # Windows to Unix line endings
        text = re.sub(r"\n\s*\n", "\n\n", text)  # Multiple blank lines to double
        text = re.sub(r"[ \t]+", " ", text)  # Multiple spaces/tabs to single
        text = text.strip()

        return text

    @staticmethod
    def extract_title(text: str, provided_title: str = None) -> str:
        """Extract title from text or use provided"""
        if provided_title:
            return provided_title.strip()

        # Try first non-empty line as title
        lines = text.split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped and len(stripped) < 200:
                return stripped
        return "Untitled Article"

    @staticmethod
    def split_into_paragraphs(text: str) -> List[str]:
        """Split text into paragraphs"""
        paragraphs = text.split("\n\n")
        return [p.strip() for p in paragraphs if p.strip()]

    @staticmethod
    def split_sentences(text: str) -> List[str]:
        """Split text into sentences with basic regex"""
        # Handle common abbreviations
        text = re.sub(r"(?<=[A-Z])\.", "", text)  # Dr., Mr., etc.
        text = re.sub(r"(?<=\d)\.", "", text)  # Numbers like 3.14

        # Split on sentence boundaries
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def merge_short_paragraphs(paragraphs: List[str], min_length: int = 20) -> List[str]:
        """Merge paragraphs that are too short with adjacent ones"""
        if not paragraphs:
            return []

        merged = []
        current = ""

        for para in paragraphs:
            if current and len(current) < min_length:
                current += " " + para
            else:
                if current:
                    merged.append(current)
                current = para

        if current:
            merged.append(current)

        return merged

    @staticmethod
    def segment_into_chunks(
        text: str,
        min_length: int = None,
        max_length: int = None,
        method: str = "paragraph",
    ) -> List[str]:
        """Segment text into chunks of appropriate size
        
        Methods:
        - 'paragraph': Use natural paragraph breaks
        - 'hybrid': Use paragraphs but split long ones by sentences
        """
        min_length = min_length or TextProcessor.MIN_SEGMENT_LENGTH
        max_length = max_length or TextProcessor.MAX_SEGMENT_LENGTH

        if method == "paragraph":
            paragraphs = TextProcessor.split_into_paragraphs(text)
            paragraphs = TextProcessor.merge_short_paragraphs(
                paragraphs, min_length
            )
            return paragraphs

        elif method == "hybrid":
            paragraphs = TextProcessor.split_into_paragraphs(text)
            segments = []

            for para in paragraphs:
                if len(para) <= max_length:
                    if len(para) >= min_length:
                        segments.append(para)
                else:
                    # Split long paragraph by sentences
                    sentences = TextProcessor.split_sentences(para)
                    current_segment = ""

                    for sent in sentences:
                        if len(current_segment) + len(sent) + 1 <= max_length:
                            current_segment += (" " if current_segment else "") + sent
                        else:
                            if len(current_segment) >= min_length:
                                segments.append(current_segment)
                            current_segment = sent

                    if len(current_segment) >= min_length:
                        segments.append(current_segment)

            return segments

        return []

    @staticmethod
    def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
        """Estimate reading time in seconds"""
        word_count = len(text.split())
        return max(1, (word_count // words_per_minute) * 60)

    @staticmethod
    def calculate_content_hash(text: str) -> str:
        """Generate hash of content for deduplication"""
        import hashlib

        normalized = " ".join(text.split()).lower()
        return hashlib.sha256(normalized.encode()).hexdigest()

    @staticmethod
    def detect_list_items(text: str) -> bool:
        """Check if text contains list items"""
        return bool(
            re.search(r"^\s*[-•*]\s+", text, re.MULTILINE)
            or re.search(r"^\s*\d+\.\s+", text, re.MULTILINE)
        )

    @staticmethod
    def detect_quotes(text: str) -> bool:
        """Check if text contains quotes"""
        return bool(re.search(r'["\'].*?["\']|["""].*?["""]', text))

    @staticmethod
    def get_segment_metadata(text: str) -> dict:
        """Extract metadata about a segment"""
        sentences = TextProcessor.split_sentences(text)
        return {
            "char_count": len(text),
            "word_count": len(text.split()),
            "sentence_count": len(sentences),
            "contains_list": TextProcessor.detect_list_items(text),
            "contains_quote": TextProcessor.detect_quotes(text),
        }
