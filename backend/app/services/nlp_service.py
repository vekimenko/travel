"""NLP service for segment classification and entity extraction"""
import re
from typing import List, Tuple, Dict
from enum import Enum


class SegmentType(str, Enum):
    """Segment classification types"""

    INTRODUCTION = "introduction"
    PREMISE = "premise"
    FACT = "fact"
    EVIDENCE = "evidence"
    CONCLUSION = "conclusion"
    TRANSITION = "transition"


class NLPService:
    """NLP operations: classification, entity extraction, keyword extraction"""

    # Patterns for segment classification
    INTRODUCTION_PATTERNS = [
        r"^\s*(in this|this|here|let's?|we)\s+(article|essay|piece|document|section)",
        r"^\s*(introduction|overview|background|context)",
        r"^\s*(first|initially|to begin)",
    ]

    CONCLUSION_PATTERNS = [
        r"^\s*(in conclusion|in summary|in short|therefore|thus|hence)",
        r"^\s*(conclusion|summary|final thoughts|takeaway)",
        r"^\s*(ultimately|in the end|finally|to summarize)",
    ]

    PREMISE_PATTERNS = [
        r"(assume|suppose|hypothes|propose|suggest|claim)",
        r"^\s*(if|assuming|given that|suppose)",
    ]

    EVIDENCE_PATTERNS = [
        r"(study|research|data|figure|table|statistic|research|experiment|show|demonstrate|found|result)",
        r"(according to|according studies|research shows|data indicate)",
    ]

    TRANSITION_PATTERNS = [
        r"^\s*(however|moreover|furthermore|additionally|nevertheless|meanwhile|likewise|similarly|conversely|on the other hand)",
    ]

    # Keywords to identify difficulty
    COMPLEX_KEYWORDS = [
        "algorithm",
        "methodology",
        "analysis",
        "theoretical",
        "abstract",
        "complex",
        "sophisticated",
        "mechanism",
        "architecture",
        "paradigm",
    ]

    @staticmethod
    def classify_segment(text: str, position: int = 0, total_segments: int = 1) -> str:
        """Classify a segment into one of the types"""
        if not text:
            return SegmentType.TRANSITION

        text_lower = text.lower()

        # Check position-based heuristics
        if position == 0:
            # First segment is often introduction
            for pattern in NLPService.INTRODUCTION_PATTERNS:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return SegmentType.INTRODUCTION

        if position == total_segments - 1:
            # Last segment is often conclusion
            for pattern in NLPService.CONCLUSION_PATTERNS:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return SegmentType.CONCLUSION

        # Check content patterns
        for pattern in NLPService.CONCLUSION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return SegmentType.CONCLUSION

        for pattern in NLPService.TRANSITION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return SegmentType.TRANSITION

        for pattern in NLPService.EVIDENCE_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return SegmentType.EVIDENCE

        for pattern in NLPService.PREMISE_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return SegmentType.PREMISE

        # Default to fact
        return SegmentType.FACT

    @staticmethod
    def extract_entities(text: str) -> List[str]:
        """Extract named entities and key concepts from text
        
        Uses simple pattern matching + heuristics
        For production, would use spaCy NER
        """
        entities = set()

        # Capitalized phrases (likely names)
        capitalized = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", text)
        entities.update(capitalized)

        # Quoted phrases
        quotes = re.findall(r'["\']([^"\']+)["\']|["""]([^"""]+)["""]', text)
        for match in quotes:
            phrase = match[0] or match[1]
            if len(phrase) > 2:
                entities.add(phrase.strip())

        # Domain concepts (all-caps or special patterns)
        acronyms = re.findall(r"\b[A-Z]{2,}\b", text)
        entities.update(acronyms)

        # Common noun phrases with prepositions
        noun_phrases = re.findall(
            r"\b(?:theory of|law of|principle of|concept of)\s+([A-Za-z\s]+?)(?:[.,;!?]|\s{2}|$)",
            text,
        )
        entities.update(noun_phrases)

        # Filter and clean
        entities = [
            e.strip()
            for e in entities
            if 2 < len(e.split()) <= 5 and not e.isdigit()
        ]

        return list(entities)[:5]  # Top 5 entities

    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        """Extract keywords using TF-IDF-like heuristics"""
        if not text:
            return []

        # Remove common words
        stopwords = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "is",
            "are",
            "was",
            "were",
            "be",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "can",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
        }

        words = re.findall(r"\b[a-z]{3,}\b", text.lower())
        word_freq = {}

        for word in words:
            if word not in stopwords:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_words[:5]]

        return keywords

    @staticmethod
    def estimate_difficulty(text: str, position: int = 0, total_segments: int = 1) -> int:
        """Estimate difficulty level (1-5) for a segment
        
        Factors:
        - Sentence length (longer = harder)
        - Complex vocabulary
        - Entity count
        - Position in article (later = often harder)
        """
        difficulty = 2  # Base difficulty

        # Sentence length factor
        sentences = text.split(".")
        avg_sent_length = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
        if avg_sent_length > 20:
            difficulty += 1
        if avg_sent_length > 30:
            difficulty += 1

        # Vocabulary complexity
        for keyword in NLPService.COMPLEX_KEYWORDS:
            if keyword.lower() in text.lower():
                difficulty += 1
                break

        # Entity count (more entities = more complex)
        entities = NLPService.extract_entities(text)
        if len(entities) > 3:
            difficulty += 1

        # Position factor (later segments often more complex)
        if position > total_segments * 0.7:
            difficulty += 1

        # Clamp to 1-5
        return max(1, min(5, difficulty))

    @staticmethod
    def calculate_content_quality(text: str) -> float:
        """Estimate quality score (0-1) of content"""
        score = 0.5  # Base score

        # Length factor
        word_count = len(text.split())
        if 50 < word_count < 1000:
            score += 0.2
        elif 20 < word_count <= 50:
            score += 0.1

        # Punctuation factor (well-punctuated text)
        punctuation_ratio = sum(1 for c in text if c in ".!?") / max(1, word_count)
        if 0.05 < punctuation_ratio < 0.2:
            score += 0.15

        # Capitalization factor
        capitalized = sum(1 for w in text.split() if w and w[0].isupper())
        if capitalized / max(1, word_count) > 0.1:
            score += 0.15

        return min(1.0, score)
