#!/usr/bin/env python3
"""
Test script to verify deployment works correctly
"""

import os
import sys
import subprocess
from pathlib import Path

def test_challenge_1a():
    """Test Challenge 1A deployment."""
    print("=== Testing Challenge 1A ===")
    
    # Create test directories
    test_dir = Path("test_challenge_1a")
    input_dir = test_dir / "input"
    output_dir = test_dir / "output"
    
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a dummy PDF file for testing (or copy from sample if available)
    sample_pdf = Path("Challenge_1a/sample_dataset/pdfs")
    if sample_pdf.exists():
        # Copy sample PDFs
        for pdf_file in sample_pdf.glob("*.pdf"):
            import shutil
            shutil.copy(pdf_file, input_dir)
        print(f"✓ Copied sample PDFs to {input_dir}")
    else:
        # Create dummy file for testing
        dummy_file = input_dir / "test.pdf"
        dummy_file.write_text("This is a test PDF file")
        print(f"✓ Created dummy test file: {dummy_file}")
    
    # Test the script
    try:
        # Change to Challenge_1a directory
        os.chdir("Challenge_1a")
        
        # Run the script
        result = subprocess.run([
            sys.executable, "process_pdfs.py"
        ], capture_output=True, text=True, cwd="..")
        
        if result.returncode == 0:
            print("✓ Challenge 1A script executed successfully")
            print(f"Output: {result.stdout}")
        else:
            print("✗ Challenge 1A script failed")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"✗ Challenge 1A test failed: {e}")
    
    # Check output
    if output_dir.exists() and any(output_dir.glob("*.json")):
        print("✓ Challenge 1A output files generated")
    else:
        print("✗ Challenge 1A no output files found")

def test_challenge_1b():
    """Test Challenge 1B deployment."""
    print("\n=== Testing Challenge 1B ===")
    
    # Create test directories
    test_dir = Path("test_challenge_1b")
    input_dir = test_dir / "input"
    output_dir = test_dir / "output"
    
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy sample input JSON
    sample_input = Path("Challenge_1b/Collection 1/challenge1b_input.json")
    if sample_input.exists():
        import shutil
        shutil.copy(sample_input, input_dir)
        print(f"✓ Copied sample input: {sample_input}")
    else:
        # Create dummy input
        dummy_input = input_dir / "test_input.json"
        dummy_input.write_text('''{
  "challenge_info": {
    "challenge_id": "test_001",
    "test_case_name": "test_case"
  },
  "documents": [
    {"filename": "test.pdf", "title": "Test Document"}
  ],
  "persona": {"role": "Test User"},
  "job_to_be_done": {"task": "Test task"}
}''')
        print(f"✓ Created dummy input: {dummy_input}")
    
    # Test the script
    try:
        # Change to Challenge_1b directory
        os.chdir("Challenge_1b")
        
        # Run the script
        result = subprocess.run([
            sys.executable, "process_collections.py"
        ], capture_output=True, text=True, cwd="..")
        
        if result.returncode == 0:
            print("✓ Challenge 1B script executed successfully")
            print(f"Output: {result.stdout}")
        else:
            print("✗ Challenge 1B script failed")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"✗ Challenge 1B test failed: {e}")
    
    # Check output
    if output_dir.exists() and any(output_dir.glob("*.json")):
        print("✓ Challenge 1B output files generated")
    else:
        print("✗ Challenge 1B no output files found")

def test_docker_builds():
    """Test Docker builds."""
    print("\n=== Testing Docker Builds ===")
    
    # Test Challenge 1A Docker build
    try:
        os.chdir("Challenge_1a")
        result = subprocess.run([
            "docker", "build", "--platform", "linux/amd64", 
            "-t", "pdf-outline-extractor:test", "."
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Challenge 1A Docker build successful")
        else:
            print("✗ Challenge 1A Docker build failed")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"✗ Challenge 1A Docker test failed: {e}")
    
    # Test Challenge 1B Docker build
    try:
        os.chdir("../Challenge_1b")
        result = subprocess.run([
            "docker", "build", "--platform", "linux/amd64", 
            "-t", "persona-doc-analyzer:test", "."
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Challenge 1B Docker build successful")
        else:
            print("✗ Challenge 1B Docker build failed")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"✗ Challenge 1B Docker test failed: {e}")

def main():
    """Main test function."""
    print("🚀 Adobe India Hackathon 2025 - Deployment Test")
    print("=" * 50)
    
    # Test local deployment
    test_challenge_1a()
    test_challenge_1b()
    
    # Test Docker builds (if Docker is available)
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        test_docker_builds()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n⚠️  Docker not available - skipping Docker tests")
    
    print("\n" + "=" * 50)
    print("✅ Deployment test completed!")
    print("\n📋 Next Steps:")
    print("1. Review test results above")
    print("2. Check generated output files")
    print("3. Follow DEPLOYMENT_GUIDE.md for production deployment")

if __name__ == "__main__":
    main() 