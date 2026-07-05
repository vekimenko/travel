# Article Ingestion & Parsing - Development Plan

## Phase 1: MVP

### Task 1: Core Text Processing
- [ ] Implement text cleaning pipeline
  - Whitespace normalization
  - HTML tag removal
  - Encoding fixes
- [ ] Create paragraph-based segmentation
- [ ] Implement basic sentence tokenization

### Task 2: Segment Classification
- [ ] Set up spaCy NLP pipeline
- [ ] Implement rule-based segment classifier
  - Introduction patterns (e.g., "In this article...", "The topic...")
  - Conclusion patterns (e.g., "In conclusion...", "Therefore...")
  - Use keyword heuristics for Premise/Fact/Evidence
- [ ] Test on sample articles

### Task 3: Entity & Keyword Extraction
- [ ] Integrate spaCy NER for entity extraction
- [ ] Implement keyword extraction (TF-IDF or KeyBERT)
- [ ] Create difficulty estimation (based on sentence length, entity count)

### Task 4: API Endpoint
- [ ] Create POST /api/articles endpoint
- [ ] Accept file upload and raw text
- [ ] Return segmented article with metadata
- [ ] Add error handling and validation

### Task 5: Database Persistence
- [ ] Create Article and Segment tables
- [ ] Implement insert logic for parsed articles
- [ ] Add retrieval queries by article_id

## Phase 2: Enhancement
- [ ] Support Markdown formatting preservation
- [ ] Add HTML table/list detection
- [ ] Implement semantic similarity for better context linking
- [ ] Add multi-language support
- [ ] Support URL-based article fetching

## Testing Strategy
- Unit tests for each processing step
- Integration tests with sample articles
- Edge case testing: long/short articles, special characters
- Performance benchmarking

## Estimated Effort
- **MVP**: 3-4 sprints
- **Enhancements**: 2-3 sprints
