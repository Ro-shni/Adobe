#!/usr/bin/env python3
"""
PDF Outline Extractor for Adobe India Hackathon 2025 - Challenge 1a
Extracts structured outlines from PDF documents with title and heading hierarchy.
"""

import os
import json
import re
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import PyPDF2
import pdfplumber
from jsonschema import validate

class PDFOutlineExtractor:
    """Advanced PDF outline extractor with intelligent heading detection."""
    
    def __init__(self):
        self.heading_patterns = {
            'H1': [
                r'^[A-Z][A-Z\s]{2,}$',  # ALL CAPS titles
                r'^\d+\.\s+[A-Z][a-zA-Z\s]{3,}$',  # 1. Title format
                r'^[A-Z][a-zA-Z\s]{3,12}$',  # Title Case (short titles only, max 12 chars)
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
        
        self.exclude_patterns = [
            r'^Page \d+$',
            r'^\d+$',
            r'^[A-Z\s]{1,3}$',  # Very short all caps
            r'^[a-z\s]{1,3}$',  # Very short all lowercase
            r'^[^\w\s]*$',  # Only special characters
            r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+',  # Normal sentence patterns
            r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+',  # Longer normal sentences
            r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+',  # Even longer sentences
        ]
    
    def extract_text_with_positions(self, pdf_path: str) -> List[Tuple[str, int, float, float]]:
        """Extract text with page numbers and positions using pdfplumber."""
        text_elements = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text blocks with their positions
                    words = page.extract_words()
                    if words:
                        # Group words into lines based on y-position
                        lines = self._group_words_into_lines(words)
                        for line in lines:
                            if line.strip():
                                text_elements.append((line.strip(), page_num, 0, 0))
                    
                    # Also extract text directly for fallback
                    text = page.extract_text()
                    if text:
                        lines = text.split('\n')
                        for line in lines:
                            if line.strip():
                                text_elements.append((line.strip(), page_num, 0, 0))
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            # Fallback to PyPDF2
            return self._extract_text_pypdf2(pdf_path)
        
        return text_elements
    
    def _extract_text_pypdf2(self, pdf_path: str) -> List[Tuple[str, int, float, float]]:
        """Fallback text extraction using PyPDF2."""
        text_elements = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text:
                        lines = text.split('\n')
                        for line in lines:
                            if line.strip():
                                text_elements.append((line.strip(), page_num, 0, 0))
        except Exception as e:
            print(f"Error with PyPDF2 extraction: {e}")
        
        return text_elements
    
    def _group_words_into_lines(self, words: List[Dict]) -> List[str]:
        """Group words into lines based on y-position."""
        if not words:
            return []
        
        # Sort words by y-position (top to bottom)
        sorted_words = sorted(words, key=lambda w: (-w['top'], w['x0']))
        
        lines = []
        current_line = []
        current_y = None
        y_tolerance = 5  # pixels
        
        for word in sorted_words:
            if current_y is None:
                current_y = word['top']
                current_line.append(word['text'])
            elif abs(word['top'] - current_y) <= y_tolerance:
                current_line.append(word['text'])
            else:
                lines.append(' '.join(current_line))
                current_line = [word['text']]
                current_y = word['top']
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def detect_heading_level(self, text: str) -> Optional[str]:
        """Intelligently detect heading level based on text patterns."""
        text = text.strip()
        
        # Skip if text matches exclusion patterns
        for pattern in self.exclude_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return None
        
        # Additional check for normal sentences (more than 4 words)
        words = text.split()
        if len(words) > 4 and not any(word.isupper() for word in words):
            return None
        
        # Check heading patterns from H1 to H3
        for level, patterns in self.heading_patterns.items():
            for pattern in patterns:
                if re.match(pattern, text):
                    return level
        
        return None
    
    def extract_title(self, text_elements: List[Tuple[str, int, float, float]]) -> str:
        """Extract document title from first few pages."""
        # Look for title in first 3 pages
        title_candidates = []
        
        for text, page_num, _, _ in text_elements[:50]:  # Check first 50 elements
            if page_num <= 3:
                # Title patterns
                if (len(text) > 10 and len(text) < 100 and 
                    text[0].isupper() and 
                    not text.isupper() and
                    not re.match(r'^\d+', text)):
                    title_candidates.append(text)
        
        if title_candidates:
            # Return the first reasonable title candidate
            return title_candidates[0]
        
        return "Document Title"
    
    def extract_outline(self, pdf_path: str) -> Dict:
        """Extract complete outline from PDF."""
        start_time = time.time()
        
        # Extract text with page numbers
        text_elements = self.extract_text_with_positions(pdf_path)
        
        # Extract title
        title = self.extract_title(text_elements)
        
        # Extract headings
        outline = []
        seen_headings = set()
        
        for text, page_num, _, _ in text_elements:
            heading_level = self.detect_heading_level(text)
            
            if heading_level and text not in seen_headings:
                outline.append({
                    "level": heading_level,
                    "text": text,
                    "page": page_num
                })
                seen_headings.add(text)
        
        # Sort by page number and level
        outline.sort(key=lambda x: (x["page"], self._level_to_number(x["level"])))
        
        # Limit to reasonable number of headings
        outline = outline[:50]
        
        processing_time = time.time() - start_time
        print(f"Processed {pdf_path} in {processing_time:.2f} seconds")
        
        return {
            "title": title,
            "outline": outline
        }
    
    def _level_to_number(self, level: str) -> int:
        """Convert heading level to number for sorting."""
        return {"H1": 1, "H2": 2, "H3": 3}.get(level, 4)
    
    def validate_output(self, output: Dict) -> bool:
        """Validate output against schema."""
        try:
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
            validate(instance=output, schema=schema)
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False

def process_pdfs():
    """Main processing function."""
    print("Starting PDF outline extraction...")
    
    # Initialize extractor
    extractor = PDFOutlineExtractor()
    
    # Get input and output directories - handle both Docker and local environments
    input_dir = Path("/app/input") if Path("/app/input").exists() else Path("./input")
    output_dir = Path("/app/output") if Path("/app/output").exists() else Path("./output")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF
    for pdf_file in pdf_files:
        try:
            print(f"Processing {pdf_file.name}...")
            
            # Extract outline
            result = extractor.extract_outline(str(pdf_file))
            
            # Validate output
            if not extractor.validate_output(result):
                print(f"Warning: Output validation failed for {pdf_file.name}")
            
            # Create output JSON file
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Processed {pdf_file.name} -> {output_file.name}")
            
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {e}")
            # Create minimal output file
            minimal_output = {
                "title": pdf_file.stem,
                "outline": []
            }
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(minimal_output, f, indent=2, ensure_ascii=False)
    
    print("PDF processing completed!")

if __name__ == "__main__":
    process_pdfs()