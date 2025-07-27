#!/usr/bin/env python3
"""
Test script for Challenge 1a solution
"""

import json
from process_pdfs import PDFOutlineExtractor

def test_heading_detection():
    """Test the heading detection logic."""
    extractor = PDFOutlineExtractor()
    
    # Test cases
    test_cases = [
        ("INTRODUCTION", "H1"),
        ("1. Introduction", "H1"),
        ("1.1 Background", "H2"),
        ("1.1.1 Details", "H3"),
        ("Page 1", None),  # Should be excluded
        ("123", None),     # Should be excluded
        ("A", None),       # Too short
        ("This is a normal paragraph", None),
    ]
    
    print("Testing heading detection...")
    for text, expected in test_cases:
        result = extractor.detect_heading_level(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text}' -> {result} (expected: {expected})")

def test_title_extraction():
    """Test the title extraction logic."""
    extractor = PDFOutlineExtractor()
    
    # Mock text elements
    text_elements = [
        ("This is a document title", 1, 0, 0),
        ("Page 1", 1, 0, 0),
        ("1. Introduction", 2, 0, 0),
        ("Some content here", 2, 0, 0),
    ]
    
    title = extractor.extract_title(text_elements)
    print(f"\nExtracted title: '{title}'")

def test_output_validation():
    """Test the output validation logic."""
    extractor = PDFOutlineExtractor()
    
    # Valid output
    valid_output = {
        "title": "Test Document",
        "outline": [
            {
                "level": "H1",
                "text": "Introduction",
                "page": 1
            }
        ]
    }
    
    # Invalid output (missing required field)
    invalid_output = {
        "title": "Test Document"
        # Missing outline
    }
    
    print("\nTesting output validation...")
    print(f"Valid output: {extractor.validate_output(valid_output)}")
    print(f"Invalid output: {extractor.validate_output(invalid_output)}")

def test_level_sorting():
    """Test the level sorting logic."""
    extractor = PDFOutlineExtractor()
    
    print(f"\nLevel sorting:")
    print(f"H1 -> {extractor._level_to_number('H1')}")
    print(f"H2 -> {extractor._level_to_number('H2')}")
    print(f"H3 -> {extractor._level_to_number('H3')}")

if __name__ == "__main__":
    print("=== Challenge 1a Solution Test ===\n")
    
    test_heading_detection()
    test_title_extraction()
    test_output_validation()
    test_level_sorting()
    
    print("\n=== Test completed ===") 