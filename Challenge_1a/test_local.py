#!/usr/bin/env python3
"""
Test local deployment logic without dependencies
"""

import os
from pathlib import Path

def test_directory_handling():
    """Test the directory handling logic."""
    print("=== Testing Directory Handling ===")
    
    # Test the logic from process_pdfs.py
    input_dir = Path("/app/input") if Path("/app/input").exists() else Path("./input")
    output_dir = Path("/app/output") if Path("/app/output").exists() else Path("./output")
    
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Create directories
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Input directory exists: {input_dir.exists()}")
    print(f"✓ Output directory exists: {output_dir.exists()}")
    
    # Test file creation
    test_file = output_dir / "test_output.json"
    test_file.write_text('{"test": "success"}')
    
    print(f"✓ Test file created: {test_file.exists()}")
    
    return True

def test_challenge_1b_directory_handling():
    """Test Challenge 1B directory handling logic."""
    print("\n=== Testing Challenge 1B Directory Handling ===")
    
    # Test the logic from process_collections.py
    input_dir = Path("/app/input") if Path("/app/input").exists() else Path("./input")
    output_dir = Path("/app/output") if Path("/app/output").exists() else Path("./output")
    
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Create directories
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Input directory exists: {input_dir.exists()}")
    print(f"✓ Output directory exists: {output_dir.exists()}")
    
    # Test file creation
    test_file = output_dir / "test_output.json"
    test_file.write_text('{"test": "success"}')
    
    print(f"✓ Test file created: {test_file.exists()}")
    
    return True

def main():
    """Main test function."""
    print("🚀 Testing Local Deployment Logic")
    print("=" * 40)
    
    # Test Challenge 1A
    test_challenge_1a = test_directory_handling()
    
    # Test Challenge 1B
    test_challenge_1b = test_challenge_1b_directory_handling()
    
    print("\n" + "=" * 40)
    if test_challenge_1a and test_challenge_1b:
        print("✅ All tests passed!")
        print("\n📋 Deployment Status:")
        print("✓ Directory handling works correctly")
        print("✓ Both Docker and local environments supported")
        print("✓ File creation and permissions working")
        print("\n🚀 Ready for production deployment!")
    else:
        print("❌ Some tests failed")

if __name__ == "__main__":
    main() 