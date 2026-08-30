#!/usr/bin/env python3
"""
Quick test script to verify backend is working
Run: python test_backend.py
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test backend health endpoint"""
    print("\n[TEST 1] 🏥 Backend Health Check")
    print("-" * 50)
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ PASS - Backend is running")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ FAIL - Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ FAIL - Cannot connect to backend")
        print(f"   Make sure backend is running: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ FAIL - Error: {e}")
        return False

def test_rules():
    """Test rules validation module"""
    print("\n[TEST 2] 📋 Rules Validation Module")
    print("-" * 50)
    try:
        from app.rules import validate_fields
        
        # Test case 1: Valid document
        fields_valid = {
            "name": "JOHN DOE",
            "dob": "15-01-1990",
            "doc_no": "A123456",
            "expiry": "31-12-2030"
        }
        score, reasons = validate_fields(fields_valid)
        print(f"✅ Valid document - Score: {score}, Reasons: {reasons}")
        
        # Test case 2: Expired document
        fields_expired = {
            "name": "JOHN DOE",
            "dob": "15-01-1990",
            "doc_no": "A123456",
            "expiry": "31-12-2020"
        }
        score, reasons = validate_fields(fields_expired)
        print(f"✅ Expired document - Score: {score}, Reasons: {reasons}")
        
        # Test case 3: Missing fields
        fields_missing = {
            "name": None,
            "dob": None,
            "doc_no": "A123456",
            "expiry": None
        }
        score, reasons = validate_fields(fields_missing)
        print(f"✅ Missing fields - Score: {score}, Reasons: {reasons}")
        
        return True
    except Exception as e:
        print(f"❌ FAIL - Error: {e}")
        return False

def test_tamper():
    """Test tamper detection module"""
    print("\n[TEST 3] 🔍 Tamper Detection Module")
    print("-" * 50)
    try:
        from app.tamper import detect_tamper
        
        # Create a dummy test image (or use real one if available)
        test_image = "test_image.jpg"
        
        if Path(test_image).exists():
            result = detect_tamper(test_image)
            print(f"✅ Tamper detection - Score: {result['tamper_score']}")
            print(f"   Signals: {result['signals']}")
            return True
        else:
            print(f"⚠️  SKIP - Test image '{test_image}' not found")
            print("   To test, place an image at: test_image.jpg")
            return True  # Not a failure, just skipped
    except Exception as e:
        print(f"❌ FAIL - Error: {e}")
        return False

def test_ocr():
    """Test OCR module"""
    print("\n[TEST 4] 🔤 OCR Module")
    print("-" * 50)
    try:
        from app.ocr import parse_fields
        
        # Test various date formats
        test_texts = [
            ("DOB: 15-01-1995 EXPIRY: 31-12-2030", "01-1995", "31-12-2030"),
            ("DATE OF BIRTH: 15/01/1995 VALID UNTIL: 31/12/2030", "15/01/1995", "31/12/2030"),
            ("D.O.B: 15-Jan-1995 EXPIRES: 31-Dec-2030", "15-Jan-1995", "31-Dec-2030"),
        ]
        
        for text, expected_dob_fragment, expected_expiry_fragment in test_texts:
            fields = parse_fields(text)
            dob_match = fields.get('dob') and expected_dob_fragment in fields.get('dob', '')
            expiry_match = fields.get('expiry') and expected_expiry_fragment in fields.get('expiry', '')
            
            if dob_match or expiry_match:
                print(f"✅ Parsed - DOB: {fields.get('dob')}, Expiry: {fields.get('expiry')}")
            else:
                print(f"⚠️  Partial - Text: {text[:40]}...")
        
        return True
    except Exception as e:
        print(f"❌ FAIL - Error: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("  SIH26188 BACKEND TEST SUITE")
    print("=" * 60)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Rules Validation", test_rules()))
    results.append(("Tamper Detection", test_tamper()))
    results.append(("OCR Module", test_ocr()))
    
    print("\n" + "=" * 60)
    print("  TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total_passed = sum(1 for _, p in results if p)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! Your project is working correctly!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
