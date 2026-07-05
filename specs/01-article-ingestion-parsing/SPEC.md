# Feature: Article Ingestion & Parsing

## Overview
Ingest articles in multiple formats and automatically segment them into logical chunks while preserving context and relationships.

## User Story
As a user, I want to upload articles so that they can be converted into interactive Q&A sessions automatically.

## Functional Requirements

### 1.1 Article Input
- **Accepted Formats**: Plain text (.txt), Markdown (.md), HTML
- **Constraints**: 
  - Max file size: 10MB
  - Support for copy-paste content
  - Support for URL-based article import (v2)
- **Metadata Extraction**:
  - Title (auto-detect or user-provided)
  - Author (if available)
  - Category (user selection or auto-classify)
  - Estimated reading time

### 1.2 Text Cleaning
- Remove HTML tags (if HTML input)
- Normalize whitespace
- Fix encoding issues
- Preserve paragraphs and logical structure
- Remove duplicate content

### 1.3 Segmentation Strategy
Identify logical boundaries by:
- **Paragraph-based**: Natural break points (paragraphs)
- **Sentence-aware**: Avoid splitting mid-idea
- **Semantic clustering**: Group related sentences
- **Heuristics**:
  - Min segment length: 20 characters
  - Max segment length: 500 characters
  - Preserve numbered/bulleted lists as units

### 1.4 Segment Classification
Classify each segment as one of:
- **Introduction**: Opening/context-setting content
- **Premise**: Hypothesis or foundational claim
- **Fact**: Verifiable statement
- **Evidence**: Supporting data or examples
- **Conclusion**: Summary or end-point
- **Transition**: Connecting ideas between sections

### 1.5 Context Enrichment
For each segment, extract:
- **Key entities**: Named persons, places, concepts
- **Keywords**: Important domain-specific terms
- **Related concepts**: Links to previous segments
- **Difficulty level**: 1-5 (estimated cognitive load)
- **Parent/child relationships**: For nested ideas

## Technical Specifications

### Input Schema
```json
{
  "article_id": "uuid",
  "title": "string",
  "content": "string (raw article)",
  "source_format": "txt|md|html",
  "metadata": {
    "author": "string (optional)",
    "category": "string",
    "difficulty_level": "beginner|intermediate|advanced",
    "source_url": "string (optional)"
  }
}
```

### Output Schema (Segments)
```json
{
  "segments": [
    {
      "id": "uuid",
      "article_id": "uuid",
      "position": 1,
      "content": "string",
      "type": "introduction|premise|fact|evidence|conclusion|transition",
      "char_count": 245,
      "entities": ["concept1", "concept2"],
      "keywords": ["key1", "key2"],
      "difficulty": 3,
      "context": {
        "previous_segment_id": "uuid",
        "related_concepts": ["concept_x", "concept_y"],
        "sentence_count": 2
      },
      "metadata": {
        "contains_list": false,
        "contains_quote": false,
        "generated_at": "timestamp"
      }
    }
  ],
  "total_segments": 15,
  "metadata": {
    "parsing_status": "success",
    "processing_time_ms": 1200,
    "content_quality_score": 0.85
  }
}
```

## Acceptance Criteria
- [ ] Parse plain text articles without errors
- [ ] Segment articles into 3-50 segments (depending on length)
- [ ] Classify segments correctly in ≥80% of cases
- [ ] Extract key entities for ≥70% of segments
- [ ] Process 10KB article in <2 seconds
- [ ] Preserve original content structure
- [ ] Handle edge cases: lists, quotes, tables

## Dependencies
- NLP library (spaCy or NLTK)
- Entity extraction (spaCy NER)
- Text preprocessing utilities

## Success Metrics
- Parse accuracy: ≥95%
- Segmentation quality (manual validation): ≥4/5
- Processing speed: <500ms per 1KB
- Classification accuracy: ≥80%
