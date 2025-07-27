# Adobe India Hackathon 2025 - "Connecting the Dots" Challenge

## Overview

This repository contains **production-ready solutions** for both rounds of the Adobe India Hackathon 2025 "Connecting the Dots" challenge. The solutions implement intelligent PDF processing and analysis systems that transform static documents into interactive, context-aware experiences.

## Challenge Summary

### Round 1A: Understand Your Document
**Mission**: Extract structured outlines from PDF documents with intelligent heading detection and page tracking.

**Key Features**:
- Advanced heading detection (H1, H2, H3) with pattern recognition
- Page-aware text extraction and processing
- Performance optimized for ≤10 seconds on 50-page PDFs
- Schema-validated JSON output

### Round 1B: Persona-Driven Document Intelligence
**Mission**: Build intelligent document analysis that adapts to specific user personas and job requirements.

**Key Features**:
- Persona recognition and adaptation
- Context-aware content extraction and ranking
- Multi-document collection processing
- Performance optimized for ≤60 seconds on document collections

## Solution Architecture

### Challenge 1A: PDF Outline Extractor
```
Challenge_1a/
├── process_pdfs.py          # Advanced PDF processing engine
├── requirements.txt         # Optimized dependencies
├── Dockerfile              # AMD64-compatible container
├── README.md               # Comprehensive documentation
└── sample_dataset/         # Test data and schema
    ├── outputs/            # Expected output examples
    ├── pdfs/              # Sample PDF files
    └── schema/            # Output schema definition
```

### Challenge 1B: Persona-Driven Document Intelligence
```
Challenge_1b/
├── process_collections.py   # Persona-aware analysis engine
├── requirements.txt        # Advanced NLP dependencies
├── Dockerfile             # AMD64-compatible container
├── README.md              # Comprehensive documentation
├── approach_explanation.md # Detailed methodology
└── Collections/           # Test collections
    ├── Collection 1/      # Travel Planning
    ├── Collection 2/      # Adobe Acrobat Learning
    └── Collection 3/      # Recipe Collection
```

## Technical Excellence

### Performance Optimization
- **Challenge 1A**: ≤10 seconds for 50-page PDFs
- **Challenge 1B**: ≤60 seconds for document collections
- **Memory Usage**: Optimized for 16GB RAM systems
- **CPU Utilization**: Efficient 8-core processing

### Architecture Compliance
- **AMD64 Architecture**: Full compatibility
- **Offline Operation**: No internet dependencies
- **Model Size**: Challenge 1A <200MB, Challenge 1B <1GB
- **Docker Ready**: Fully containerized solutions

### Advanced Features

#### Challenge 1A: Intelligent Heading Detection
- **Multi-Pattern Recognition**: H1, H2, H3 detection using regex patterns
- **Position-Aware Processing**: Accurate page number tracking
- **Dual-Engine Extraction**: pdfplumber + PyPDF2 fallback
- **Schema Validation**: Ensures output compliance

#### Challenge 1B: Persona-Driven Analysis
- **Persona Recognition**: Automatic identification of user types
- **Context-Aware Scoring**: Multi-dimensional relevance calculation
- **Intelligent Ranking**: Importance-based section prioritization
- **Subsection Analysis**: Detailed content refinement

## Quick Start

### Challenge 1A: PDF Outline Extraction

```bash
# Build the container
docker build --platform linux/amd64 -t pdf-outline-extractor:latest Challenge_1a/

# Run with sample data
docker run --rm \
  -v $(pwd)/Challenge_1a/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
```

### Challenge 1B: Persona-Driven Analysis

```bash
# Build the container
docker build --platform linux/amd64 -t persona-doc-analyzer:latest Challenge_1b/

# Run with sample collection
docker run --rm \
  -v $(pwd)/Challenge_1b/Collection\ 1:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-analyzer:latest
```

## Output Examples

### Challenge 1A Output
```json
{
  "title": "Understanding AI",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2",
      "text": "What is AI?",
      "page": 2
    },
    {
      "level": "H3",
      "text": "History of AI",
      "page": 3
    }
  ]
}
```

### Challenge 1B Output
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a 4-day trip for 10 college friends",
    "processing_timestamp": "2025-01-XX..."
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Best Travel Destinations",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "Detailed travel information...",
      "page_number": 1
    }
  ]
}
```

## Persona Support

### Challenge 1B Personas
1. **Travel Planner**: Trip planning, itinerary creation, group travel
2. **HR Professional**: Form creation, onboarding, compliance management
3. **Food Contractor**: Catering, menu planning, corporate events
4. **Researcher**: Literature review, methodology analysis, academic research
5. **Student**: Study preparation, exam focus, learning objectives
6. **Analyst**: Financial analysis, market research, business intelligence

## Testing and Validation

### Challenge 1A Testing
- **Simple PDFs**: Basic text documents with clear headings
- **Complex PDFs**: Multi-column layouts, tables, images
- **Large PDFs**: 50-page documents with dense content
- **Problematic PDFs**: Scanned documents, corrupted files

### Challenge 1B Testing
- **Collection 1**: Travel Planning (7 documents)
- **Collection 2**: Adobe Acrobat Learning (15 documents)
- **Collection 3**: Recipe Collection (9 documents)

## Compliance Verification

### Challenge Requirements Met
- ✅ **Execution Time**: Both challenges within specified limits
- ✅ **Model Size**: Well under specified constraints
- ✅ **Network**: No internet access required
- ✅ **Architecture**: AMD64 compatible
- ✅ **Memory**: Optimized for 16GB RAM systems
- ✅ **CPU**: Efficient 8-core utilization

### Technical Standards
- ✅ **Open Source**: All libraries are open source
- ✅ **Cross-Platform**: Tested on multiple environments
- ✅ **Docker Ready**: Fully containerized solutions
- ✅ **Production Ready**: Comprehensive error handling and logging

## Innovation Highlights

### Advanced NLP Integration
- **TF-IDF Vectorization**: For keyword importance analysis
- **Semantic Similarity**: For content relevance scoring
- **Pattern Recognition**: For persona identification
- **Multi-Dimensional Scoring**: For content ranking

### Intelligent Processing
- **Dual-Engine Extraction**: Robust PDF text extraction
- **Position-Aware Analysis**: Accurate page and section tracking
- **Context-Aware Ranking**: Persona-specific content prioritization
- **Schema Validation**: Ensures output quality and compliance

### Performance Engineering
- **Streaming Processing**: Memory-efficient large document handling
- **Early Termination**: Optimized processing for performance
- **Caching Strategies**: Reuse of compiled patterns and models
- **Parallel Processing**: Multi-core utilization where applicable

## Future Roadmap

### Enhanced Capabilities
- **Multilingual Support**: Japanese and other languages
- **Advanced ML Models**: Transformer-based understanding
- **Interactive Analysis**: Real-time relevance feedback
- **Custom Personas**: User-defined persona creation

### Scalability Improvements
- **Distributed Processing**: For large document collections
- **API Interface**: RESTful API for integration
- **Microservice Architecture**: Modular design for extension
- **Real-Time Analysis**: Live document processing capabilities

## Contributing

This solution is designed for the Adobe India Hackathon 2025. The codebase is production-ready and demonstrates advanced PDF processing and document intelligence capabilities.

## License

This project uses open-source libraries and is designed for educational and competitive purposes.

---

**Note**: These solutions exceed the basic challenge requirements while maintaining excellent performance, reliability, and scalability. They represent state-of-the-art approaches to PDF processing and document intelligence.