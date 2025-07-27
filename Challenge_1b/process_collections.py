#!/usr/bin/env python3
"""
Persona-Driven Document Intelligence for Adobe India Hackathon 2025 - Challenge 1b
Extracts relevant sections from document collections based on specific personas and use cases.
"""

import os
import json
import re
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import PyPDF2
import pdfplumber
from jsonschema import validate
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class PersonaDocumentAnalyzer:
    """Advanced persona-driven document analysis system."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        # Persona-specific keywords and patterns
        self.persona_keywords = {
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
            ],
            'researcher': [
                'research', 'study', 'analysis', 'methodology', 'data', 'results', 'conclusion',
                'literature', 'review', 'paper', 'publication', 'experiment', 'hypothesis',
                'finding', 'evidence', 'statistical', 'benchmark', 'performance', 'evaluation'
            ],
            'student': [
                'study', 'learn', 'education', 'course', 'exam', 'test', 'assignment', 'homework',
                'concept', 'theory', 'practice', 'exercise', 'review', 'preparation', 'grade',
                'academic', 'curriculum', 'syllabus', 'textbook', 'lecture', 'tutorial'
            ],
            'analyst': [
                'analysis', 'report', 'data', 'trend', 'financial', 'market', 'performance',
                'revenue', 'investment', 'strategy', 'business', 'corporate', 'annual', 'quarterly',
                'metrics', 'kpi', 'forecast', 'projection', 'comparison', 'benchmark'
            ]
        }
        
        # Job-specific patterns
        self.job_patterns = {
            'travel_planning': ['plan', 'trip', 'itinerary', 'schedule', 'booking', 'accommodation'],
            'form_creation': ['create', 'form', 'fillable', 'digital', 'automation', 'workflow'],
            'catering': ['prepare', 'menu', 'buffet', 'catering', 'service', 'quantity'],
            'research': ['review', 'literature', 'methodology', 'analysis', 'findings'],
            'study': ['study', 'learn', 'prepare', 'exam', 'concept', 'practice'],
            'analysis': ['analyze', 'report', 'trend', 'performance', 'financial', 'market']
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Tuple[str, int, str]]:
        """Extract text with page numbers and sections from PDF."""
        text_sections = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    text = page.extract_text()
                    if text:
                        # Split into sections (paragraphs)
                        sections = self._split_into_sections(text)
                        for section in sections:
                            if section.strip():
                                text_sections.append((section.strip(), page_num, pdf_path))
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            # Fallback to PyPDF2
            return self._extract_text_pypdf2(pdf_path)
        
        return text_sections
    
    def _extract_text_pypdf2(self, pdf_path: str) -> List[Tuple[str, int, str]]:
        """Fallback text extraction using PyPDF2."""
        text_sections = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text:
                        sections = self._split_into_sections(text)
                        for section in sections:
                            if section.strip():
                                text_sections.append((section.strip(), page_num, pdf_path))
        except Exception as e:
            print(f"Error with PyPDF2 extraction: {e}")
        
        return text_sections
    
    def _split_into_sections(self, text: str) -> List[str]:
        """Split text into meaningful sections."""
        # Split by double newlines or section markers
        sections = re.split(r'\n\s*\n|\n\s*[A-Z][A-Z\s]{2,}\n', text)
        return [s.strip() for s in sections if s.strip()]
    
    def identify_persona_type(self, persona: str, job: str) -> str:
        """Identify the type of persona based on role and job description."""
        persona_lower = persona.lower()
        job_lower = job.lower()
        
        # Check for specific persona types
        if any(word in persona_lower for word in ['travel', 'planner', 'trip']):
            return 'travel_planner'
        elif any(word in persona_lower for word in ['hr', 'human resources', 'professional']):
            return 'hr_professional'
        elif any(word in persona_lower for word in ['food', 'catering', 'contractor']):
            return 'food_contractor'
        elif any(word in persona_lower for word in ['researcher', 'phd', 'academic']):
            return 'researcher'
        elif any(word in persona_lower for word in ['student', 'undergraduate', 'college']):
            return 'student'
        elif any(word in persona_lower for word in ['analyst', 'investment', 'financial']):
            return 'analyst'
        
        # Fallback based on job description
        if any(word in job_lower for word in ['trip', 'travel', 'vacation']):
            return 'travel_planner'
        elif any(word in job_lower for word in ['form', 'onboarding', 'compliance']):
            return 'hr_professional'
        elif any(word in job_lower for word in ['menu', 'buffet', 'catering']):
            return 'food_contractor'
        elif any(word in job_lower for word in ['research', 'literature', 'review']):
            return 'researcher'
        elif any(word in job_lower for word in ['study', 'learn', 'exam']):
            return 'student'
        elif any(word in job_lower for word in ['analyze', 'report', 'financial']):
            return 'analyst'
        
        return 'general'
    
    def calculate_relevance_score(self, text: str, persona_type: str, job_description: str) -> float:
        """Calculate relevance score for a text section."""
        text_lower = text.lower()
        job_lower = job_description.lower()
        
        # Get relevant keywords
        persona_keywords = self.persona_keywords.get(persona_type, [])
        
        # Calculate keyword matches
        keyword_score = sum(1 for keyword in persona_keywords if keyword in text_lower)
        
        # Calculate job-specific relevance
        job_score = sum(1 for pattern in self.job_patterns.get(persona_type, []) 
                       if pattern in job_lower and pattern in text_lower)
        
        # Calculate text length score (prefer medium-length sections)
        length_score = min(len(text.split()) / 50, 1.0)  # Normalize to 0-1
        
        # Calculate section importance (headings, lists, etc.)
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
    
    def extract_sections(self, text_sections: List[Tuple[str, int, str]], 
                        persona_type: str, job_description: str, 
                        max_sections: int = 10) -> List[Dict]:
        """Extract and rank relevant sections."""
        scored_sections = []
        
        for text, page_num, doc_path in text_sections:
            relevance_score = self.calculate_relevance_score(text, persona_type, job_description)
            
            if relevance_score > 0.1:  # Minimum relevance threshold
                scored_sections.append({
                    'text': text,
                    'page_number': page_num,
                    'document': os.path.basename(doc_path),
                    'relevance_score': relevance_score
                })
        
        # Sort by relevance score and take top sections
        scored_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Create final output format
        extracted_sections = []
        for i, section in enumerate(scored_sections[:max_sections], 1):
            extracted_sections.append({
                'document': section['document'],
                'section_title': self._extract_section_title(section['text']),
                'importance_rank': i,
                'page_number': section['page_number']
            })
        
        return extracted_sections
    
    def _extract_section_title(self, text: str) -> str:
        """Extract a meaningful title from section text."""
        lines = text.split('\n')
        
        # Look for heading-like lines
        for line in lines[:3]:  # Check first 3 lines
            line = line.strip()
            if (len(line) > 5 and len(line) < 100 and 
                line[0].isupper() and 
                not line.isupper()):
                return line
        
        # Fallback: use first meaningful line
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 100:
                return line[:80] + "..." if len(line) > 80 else line
        
        return "Section"
    
    def analyze_subsections(self, text_sections: List[Tuple[str, int, str]], 
                           extracted_sections: List[Dict]) -> List[Dict]:
        """Analyze subsections for detailed content extraction."""
        subsection_analysis = []
        
        # Get page numbers of extracted sections
        relevant_pages = {section['page_number'] for section in extracted_sections}
        
        for text, page_num, doc_path in text_sections:
            if page_num in relevant_pages:
                # Refine text by removing common noise
                refined_text = self._refine_text(text)
                
                if len(refined_text) > 50:  # Minimum meaningful length
                    subsection_analysis.append({
                        'document': os.path.basename(doc_path),
                        'refined_text': refined_text,
                        'page_number': page_num
                    })
        
        return subsection_analysis[:20]  # Limit to 20 subsections
    
    def _refine_text(self, text: str) -> str:
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
    
    def process_collection(self, input_json_path: str) -> Dict:
        """Process a document collection based on persona and job requirements."""
        start_time = time.time()
        
        # Load input configuration
        with open(input_json_path, 'r', encoding='utf-8') as f:
            input_config = json.load(f)
        
        # Extract configuration
        documents = input_config.get('documents', [])
        persona = input_config.get('persona', {}).get('role', '')
        job_to_be_done = input_config.get('job_to_be_done', {}).get('task', '')
        
        # Identify persona type
        persona_type = self.identify_persona_type(persona, job_to_be_done)
        
        # Extract text from all documents
        all_text_sections = []
        input_dir = Path(input_json_path).parent / "PDFs"
        
        for doc_info in documents:
            doc_path = input_dir / doc_info['filename']
            if doc_path.exists():
                text_sections = self.extract_text_from_pdf(str(doc_path))
                all_text_sections.extend(text_sections)
        
        # Extract relevant sections
        extracted_sections = self.extract_sections(
            all_text_sections, persona_type, job_to_be_done
        )
        
        # Analyze subsections
        subsection_analysis = self.analyze_subsections(
            all_text_sections, extracted_sections
        )
        
        # Create output
        output = {
            'metadata': {
                'input_documents': [doc['filename'] for doc in documents],
                'persona': persona,
                'job_to_be_done': job_to_be_done,
                'processing_timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.%f')
            },
            'extracted_sections': extracted_sections,
            'subsection_analysis': subsection_analysis
        }
        
        processing_time = time.time() - start_time
        print(f"Processed collection in {processing_time:.2f} seconds")
        
        return output

def process_collections():
    """Main processing function for document collections."""
    print("Starting persona-driven document analysis...")
    
    # Initialize analyzer
    analyzer = PersonaDocumentAnalyzer()
    
    # Get input and output directories - handle both Docker and local environments
    input_dir = Path("/app/input") if Path("/app/input").exists() else Path("./input")
    output_dir = Path("/app/output") if Path("/app/output").exists() else Path("./output")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all input JSON files
    input_files = list(input_dir.glob("*.json"))
    
    if not input_files:
        print("No input JSON files found")
        return
    
    print(f"Found {len(input_files)} input files to process")
    
    # Process each input file
    for input_file in input_files:
        try:
            print(f"Processing {input_file.name}...")
            
            # Process collection
            result = analyzer.process_collection(str(input_file))
            
            # Create output JSON file
            output_file = output_dir / f"{input_file.stem}_output.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Processed {input_file.name} -> {output_file.name}")
            
        except Exception as e:
            print(f"✗ Error processing {input_file.name}: {e}")
    
    print("Collection processing completed!")

if __name__ == "__main__":
    process_collections() 