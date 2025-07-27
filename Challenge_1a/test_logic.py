#!/usr/bin/env python3
"""
Simplified test for Challenge 1a core logic
"""

import re
import json

def test_heading_patterns():
    """Test the heading detection patterns."""
    
    heading_patterns = {
        'H1': [
            r'^[A-Z][A-Z\s]{2,}$',  # ALL CAPS titles
            r'^\d+\.\s+[A-Z][a-zA-Z\s]{3,}$',  # 1. Title format
            r'^[A-Z][a-zA-Z\s]{3,}$',  # Title Case
            r'^[A-Z][a-zA-Z\s]{2,}:$',  # Title with colon
        ],
        'H2': [
            r'^\d+\.\d+\s+[A-Z][a-zA-Z\s]{2,}$',  # 1.1 Subtitle
            r'^[A-Z][a-zA-Z\s]{2,}$',  # Title Case (shorter)
            r'^[A-Z][a-zA-Z\s]{2,}:$',  # Subtitle with colon
        ],
        'H3': [
            r'^\d+\.\d+\.\d+\s+[A-Z][a-zA-Z\s]{2,}$',  # 1.1.1 Sub-subtitle
            r'^[A-Z][a-zA-Z\s]{1,}$',  # Short title case
            r'^[a-z][a-zA-Z\s]{2,}:$',  # lowercase with colon
        ]
    }
    
    exclude_patterns = [
        r'^Page \d+$',
        r'^\d+$',
        r'^[A-Z\s]{1,3}$',  # Very short all caps
        r'^[a-z\s]{1,3}$',  # Very short all lowercase
        r'^[^\w\s]*$',  # Only special characters
    ]
    
    def detect_heading_level(text):
        """Detect heading level based on text patterns."""
        text = text.strip()
        
        # Skip if text matches exclusion patterns
        for pattern in exclude_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return None
        
        # Additional check for normal sentences (more than 4 words)
        words = text.split()
        if len(words) > 4 and not any(word.isupper() for word in words):
            return None
        
        # Check heading patterns from H1 to H3
        for level, patterns in heading_patterns.items():
            for pattern in patterns:
                if re.match(pattern, text):
                    return level
        
        return None
    
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
    
    print("Testing heading detection patterns...")
    for text, expected in test_cases:
        result = detect_heading_level(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text}' -> {result} (expected: {expected})")

def test_output_schema():
    """Test the output schema validation."""
    
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "outline": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "level": {"type": "string"},
                        "text": {"type": "string"},
                        "page": {"type": "integer"}
                    },
                    "required": ["level", "text", "page"]
                }
            }
        },
        "required": ["title", "outline"]
    }
    
    def validate_output(output):
        """Simple validation function."""
        try:
            # Check required fields
            if "title" not in output or "outline" not in output:
                return False
            
            # Check title is string
            if not isinstance(output["title"], str):
                return False
            
            # Check outline is list
            if not isinstance(output["outline"], list):
                return False
            
            # Check each outline item
            for item in output["outline"]:
                if not isinstance(item, dict):
                    return False
                if "level" not in item or "text" not in item or "page" not in item:
                    return False
                if not isinstance(item["level"], str) or not isinstance(item["text"], str) or not isinstance(item["page"], int):
                    return False
            
            return True
        except:
            return False
    
    # Test cases
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
    
    invalid_output = {
        "title": "Test Document"
        # Missing outline
    }
    
    print("\nTesting output schema validation...")
    print(f"Valid output: {validate_output(valid_output)}")
    print(f"Invalid output: {validate_output(invalid_output)}")

def test_json_generation():
    """Test JSON output generation."""
    
    # Sample output
    output = {
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
    
    # Generate JSON
    json_output = json.dumps(output, indent=2)
    
    print("\nTesting JSON generation...")
    print("Generated JSON:")
    print(json_output)
    
    # Verify it can be parsed back
    parsed = json.loads(json_output)
    print(f"\nJSON parsing successful: {parsed['title'] == 'Understanding AI'}")

if __name__ == "__main__":
    print("=== Challenge 1a Core Logic Test ===\n")
    
    test_heading_patterns()
    test_output_schema()
    test_json_generation()
    
    print("\n=== Core logic test completed ===") 