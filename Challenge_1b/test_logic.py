#!/usr/bin/env python3
"""
Simplified test for Challenge 1b core logic
"""

import re
import json

def test_persona_recognition():
    """Test the persona recognition logic."""
    
    persona_keywords = {
        'travel_planner': [
            'travel', 'trip', 'vacation', 'tour', 'itinerary', 'booking', 'hotel', 'restaurant',
            'attraction', 'activity', 'transport', 'budget', 'planning', 'schedule', 'day',
            'group', 'friends', 'college', 'student', 'accommodation', 'dining', 'sightseeing'
        ],
        'hr_professional': [
            'form', 'onboarding', 'compliance', 'employee', 'hr', 'human resources', 'policy',
            'procedure', 'document', 'signature', 'fill', 'complete', 'submit', 'approval',
            'workflow', 'automation', 'digital', 'electronic', 'management', 'tracking'
        ],
        'food_contractor': [
            'recipe', 'cooking', 'food', 'meal', 'dinner', 'buffet', 'vegetarian', 'corporate',
            'catering', 'menu', 'ingredient', 'preparation', 'serving', 'quantity', 'portion',
            'dietary', 'restriction', 'allergy', 'nutrition', 'presentation', 'service'
        ]
    }
    
    def identify_persona_type(persona, job):
        """Identify persona type based on role and job description."""
        persona_lower = persona.lower()
        job_lower = job.lower()
        
        # Check for specific persona types
        if any(word in persona_lower for word in ['travel', 'planner', 'trip']):
            return 'travel_planner'
        elif any(word in persona_lower for word in ['hr', 'human resources', 'professional']):
            return 'hr_professional'
        elif any(word in persona_lower for word in ['food', 'catering', 'contractor']):
            return 'food_contractor'
        
        # Fallback based on job description
        if any(word in job_lower for word in ['trip', 'travel', 'vacation']):
            return 'travel_planner'
        elif any(word in job_lower for word in ['form', 'onboarding', 'compliance']):
            return 'hr_professional'
        elif any(word in job_lower for word in ['menu', 'buffet', 'catering']):
            return 'food_contractor'
        
        return 'general'
    
    # Test cases
    test_cases = [
        ("Travel Planner", "Plan a trip", "travel_planner"),
        ("HR Professional", "Create forms", "hr_professional"),
        ("Food Contractor", "Prepare buffet", "food_contractor"),
        ("Manager", "Plan vacation", "travel_planner"),
        ("Unknown", "Unknown task", "general"),
    ]
    
    print("Testing persona recognition...")
    for persona, job, expected in test_cases:
        result = identify_persona_type(persona, job)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{persona}' + '{job}' -> {result} (expected: {expected})")

def test_relevance_scoring():
    """Test the relevance scoring logic."""
    
    def calculate_relevance_score(text, persona_type, job_description):
        """Calculate relevance score for a text section."""
        text_lower = text.lower()
        job_lower = job_description.lower()
        
        # Persona-specific keywords
        persona_keywords = {
            'travel_planner': ['travel', 'trip', 'vacation', 'booking', 'hotel', 'restaurant'],
            'hr_professional': ['form', 'onboarding', 'compliance', 'employee', 'policy'],
            'food_contractor': ['recipe', 'cooking', 'food', 'meal', 'buffet', 'catering']
        }
        
        # Get relevant keywords
        keywords = persona_keywords.get(persona_type, [])
        
        # Calculate keyword matches
        keyword_score = sum(1 for keyword in keywords if keyword in text_lower)
        
        # Calculate job-specific relevance
        job_score = sum(1 for word in job_lower.split() if word in text_lower)
        
        # Calculate text length score (prefer medium-length sections)
        length_score = min(len(text.split()) / 50, 1.0)
        
        # Calculate section importance
        importance_score = 0
        if re.search(r'^[A-Z][A-Z\s]{2,}$', text[:50]):  # Heading-like text
            importance_score += 0.3
        if re.search(r'^\d+\.', text):  # Numbered list
            importance_score += 0.2
        if re.search(r'^[•\-\*]', text):  # Bullet points
            importance_score += 0.2
        
        # Combine scores
        total_score = (keyword_score * 0.4 + 
                      job_score * 0.3 + 
                      length_score * 0.2 + 
                      importance_score * 0.1)
        
        return total_score
    
    # Test cases
    test_cases = [
        ("Travel information and booking details", "travel_planner", "Plan a trip", 0.0),
        ("Form creation and compliance procedures", "hr_professional", "Create forms", 0.0),
        ("Recipe collection for buffet preparation", "food_contractor", "Prepare buffet", 0.0),
        ("General information about anything", "travel_planner", "Plan a trip", 0.0),
    ]
    
    print("\nTesting relevance scoring...")
    for text, persona, job, expected in test_cases:
        result = calculate_relevance_score(text, persona, job)
        print(f"'{text}' -> {result:.2f} (persona: {persona}, job: {job})")

def test_output_format():
    """Test the output format generation."""
    
    # Sample output
    output = {
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
                "refined_text": "Detailed travel information for planning your trip...",
                "page_number": 1
            }
        ]
    }
    
    # Generate JSON
    json_output = json.dumps(output, indent=2)
    
    print("\nTesting output format generation...")
    print("Generated JSON structure:")
    print(json_output)
    
    # Verify it can be parsed back
    parsed = json.loads(json_output)
    print(f"\nJSON parsing successful: {parsed['metadata']['persona'] == 'Travel Planner'}")

def test_text_refinement():
    """Test the text refinement logic."""
    
    def refine_text(text):
        """Refine text by removing noise and improving readability."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        
        # Remove page numbers and headers
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Clean up
        text = text.strip()
        
        return text
    
    # Test cases
    test_cases = [
        ("This   is   a   test   text", "This is a test text"),
        ("Page 1\nContent here\nPage 2", "Page 1\nContent here\nPage 2"),
        ("Special@#$%^&*()characters", "Special characters"),
    ]
    
    print("\nTesting text refinement...")
    for input_text, expected in test_cases:
        result = refine_text(input_text)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{input_text}' -> '{result}'")

if __name__ == "__main__":
    print("=== Challenge 1b Core Logic Test ===\n")
    
    test_persona_recognition()
    test_relevance_scoring()
    test_output_format()
    test_text_refinement()
    
    print("\n=== Core logic test completed ===") 