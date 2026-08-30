# SIH26188 Testing Guide

## Phase 1: Setup & Environment Check

### 1.1 Verify Installation
```bash
# Check Python version
python --version  # Should be 3.8+

# Check virtual environment
pip list | grep -E "fastapi|streamlit|easyocr|opencv|deepface"
```

### 1.2 Start Backend
```bash
cd C:\Users\tejom\OneDrive\Desktop\sih26188-prototype
uvicorn app.main:app --reload
# Expected: "Uvicorn running on http://127.0.0.1:8000"
```

### 1.3 Test Backend Health
```bash
# In a new terminal
curl http://127.0.0.1:8000/health
# Expected response: {"status": "ok"}
```

---

## Phase 2: Unit Testing (Test Individual Functions)

### 2.1 Test OCR Module
**File:** `test_ocr.py`

```python
from app.ocr import extract_text, parse_fields

# Test 1: Parse different date formats
test_texts = [
    "DOB: 15-01-1995",
    "DATE OF BIRTH: 15/01/1995",
    "D.O.B: 15-Jan-1995",
    "EXPIRY: 31-Dec-2030"
]

for text in test_texts:
    fields = parse_fields(text)
    print(f"Text: {text}")
    print(f"Parsed DOB: {fields.get('dob')}")
    print(f"Parsed Expiry: {fields.get('expiry')}\n")

# Expected: All dates should be captured correctly
```

### 2.2 Test Rules Module
**File:** `test_rules.py`

```python
from app.rules import validate_fields

# Test Case 1: All fields present and valid
fields_valid = {
    "name": "JOHN DOE",
    "dob": "15-01-1990",
    "doc_no": "A123456",
    "expiry": "31-12-2030"
}
score, reasons = validate_fields(fields_valid)
print(f"Valid document - Score: {score}, Reasons: {reasons}")
# Expected: score = 0, reasons = []

# Test Case 2: Expired document
fields_expired = {
    "name": "JOHN DOE",
    "dob": "15-01-1990",
    "doc_no": "A123456",
    "expiry": "31-12-2020"
}
score, reasons = validate_fields(fields_expired)
print(f"Expired document - Score: {score}, Reasons: {reasons}")
# Expected: score includes 30+ for expired

# Test Case 3: Missing fields
fields_missing = {
    "name": None,
    "dob": None,
    "doc_no": "A123456",
    "expiry": None
}
score, reasons = validate_fields(fields_missing)
print(f"Missing fields - Score: {score}, Reasons: {reasons}")
# Expected: score = 65 (15+15+20+15), multiple reasons

# Test Case 4: Invalid date format
fields_invalid_date = {
    "name": "JOHN DOE",
    "dob": "15-01-1990",
    "doc_no": "A123456",
    "expiry": "INVALID_DATE"
}
score, reasons = validate_fields(fields_invalid_date)
print(f"Invalid date - Score: {score}, Reasons: {reasons}")
# Expected: score includes 10 for invalid format
```

### 2.3 Test Tamper Detection
**File:** `test_tamper.py`

```python
from app.tamper import detect_tamper
import cv2
import numpy as np

# Test Case 1: High-quality image
result = detect_tamper("path_to_good_image.jpg")
print(f"Good image - Score: {result['tamper_score']}, Signals: {result['signals']}")
# Expected: low score (0-10), no obvious signals

# Test Case 2: Blurry image
result = detect_tamper("path_to_blurry_image.jpg")
print(f"Blurry image - Score: {result['tamper_score']}, Signals: {result['signals']}")
# Expected: includes "Image is very blurry"

# Test Case 3: Low resolution
result = detect_tamper("path_to_low_res_image.jpg")
print(f"Low-res image - Score: {result['tamper_score']}, Signals: {result['signals']}")
# Expected: includes "Low-resolution image"
```

---

## Phase 3: Integration Testing (Backend API)

### 3.1 Test Document Analysis Endpoint
```bash
# Using curl with a test image
curl -X POST "http://127.0.0.1:8000/analyze-document" \
  -H "accept: application/json" \
  -F "file=@/path/to/document.jpg"

# Expected response:
{
  "filename": "document.jpg",
  "ocr_text": "extracted text...",
  "fields": {
    "name": "JOHN DOE",
    "dob": "15-01-1990",
    "doc_no": "A123456",
    "expiry": "31-12-2030"
  },
  "rule_score": 0,
  "tamper_score": 5,
  "risk_score": 3,
  "verdict": "low_risk",
  "reasons": [...]
}
```

### 3.2 Test Face Verification Endpoint
```bash
curl -X POST "http://127.0.0.1:8000/verify-face" \
  -H "accept: application/json" \
  -F "document_image=@/path/to/doc_photo.jpg" \
  -F "selfie_image=@/path/to/selfie.jpg"

# Expected response:
{
  "verified": true/false,
  "distance": 0.45,
  "model": "VGG-Face",
  "threshold": 0.6
}
```

### 3.3 Test Error Handling
```bash
# Test with invalid file format
curl -X POST "http://127.0.0.1:8000/analyze-document" \
  -F "file=@test.txt"
# Expected: Error or graceful handling

# Test with missing parameter
curl -X POST "http://127.0.0.1:8000/verify-face" \
  -F "document_image=@doc.jpg"
# Expected: 422 validation error
```

---

## Phase 4: UI Testing (Streamlit App)

### 4.1 Start Streamlit
```bash
streamlit run ui/streamlit_app.py
# Navigate to: http://localhost:8501
```

### 4.2 Test Scenarios

**Test 1: Document Analysis**
- [ ] Upload a clear document image
- [ ] Click "Analyze Document"
- [ ] Verify JSON output displays
- [ ] Check risk_score is 0-100
- [ ] Verify verdict is one of: low_risk, medium_risk, high_risk

**Test 2: Face Verification**
- [ ] Upload document photo
- [ ] Upload matching selfie
- [ ] Click "Verify Face"
- [ ] Verify JSON output with verified: true/false

**Test 3: Error Handling**
- [ ] Stop backend server
- [ ] Try to analyze document
- [ ] Verify error message displays (not a crash)
- [ ] Restart backend, try again

**Test 4: Connection Issues**
- [ ] Change Backend URL to invalid address
- [ ] Try to upload
- [ ] Verify connection error displays gracefully

---

## Phase 5: End-to-End Testing with Real Documents

### 5.1 Test with Sample Images

**Prepare test images:**
1. **Good document** - Clear, well-lit, all text visible
2. **Expired document** - Valid format but expiry date passed
3. **Blurry document** - Intentionally blurred
4. **Tampered document** - Edited/compressed
5. **Low resolution** - Less than 300x300 pixels

**Run analysis on each:**
```python
import requests

test_files = {
    "good_doc.jpg": "low_risk",
    "expired_doc.jpg": "high_risk",
    "blurry_doc.jpg": "medium_risk",
    "low_res_doc.jpg": "medium_risk"
}

for filename, expected_verdict in test_files.items():
    with open(filename, 'rb') as f:
        files = {"file": f}
        response = requests.post(
            "http://127.0.0.1:8000/analyze-document",
            files=files
        )
    
    result = response.json()
    actual_verdict = result["verdict"]
    status = "✅" if actual_verdict == expected_verdict else "❌"
    
    print(f"{status} {filename}: Expected {expected_verdict}, Got {actual_verdict}")
```

---

## Phase 6: Performance Testing

### 6.1 Response Time Testing
```python
import time
import requests

image_path = "test_document.jpg"
times = []

for i in range(5):
    start = time.time()
    with open(image_path, 'rb') as f:
        files = {"file": f}
        requests.post("http://127.0.0.1:8000/analyze-document", files=files)
    elapsed = time.time() - start
    times.append(elapsed)

avg_time = sum(times) / len(times)
print(f"Average response time: {avg_time:.2f} seconds")
# Expected: < 10 seconds per document
```

### 6.2 Concurrent Request Testing
```python
import concurrent.futures
import requests

def analyze(img_path):
    with open(img_path, 'rb') as f:
        files = {"file": f}
        return requests.post("http://127.0.0.1:8000/analyze-document", files=files)

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(analyze, ["test.jpg"] * 5)
    for r in results:
        print(f"Status: {r.status_code}")
# Expected: All should succeed (200)
```

---

## Phase 7: Security Testing

### 7.1 Path Traversal Prevention
```bash
# Try to upload file with path traversal in name
curl -X POST "http://127.0.0.1:8000/analyze-document" \
  -F "file=@document.jpg;filename=../../../etc/passwd"
# Expected: File sanitized, no path traversal
```

### 7.2 File Upload Size
```bash
# Create large file
dd if=/dev/zero of=large.jpg bs=1M count=50  # 50MB

curl -X POST "http://127.0.0.1:8000/analyze-document" \
  -F "file=@large.jpg"
# Expected: Should handle gracefully or timeout (no crash)
```

### 7.3 File Cleanup
```bash
# Run 10 analyses
for i in {1..10}; do
    curl -X POST "http://127.0.0.1:8000/analyze-document" \
      -F "file=@test.jpg"
done

# Check uploads folder
ls -la uploads/
# Expected: Should be empty or minimal files
```

---

## Phase 8: Validation Checklist

### Backend
- [ ] Health endpoint responds with 200
- [ ] Document analysis returns valid JSON
- [ ] Face verification returns valid JSON
- [ ] Risk scores are 0-100
- [ ] Verdicts are one of: low_risk, medium_risk, high_risk
- [ ] Date parsing works for multiple formats
- [ ] Error handling doesn't crash server
- [ ] Files are cleaned up after processing

### Streamlit UI
- [ ] Page loads without errors
- [ ] File upload works
- [ ] Buttons show loading state
- [ ] Results display as JSON
- [ ] Error messages are user-friendly
- [ ] Connection errors handled gracefully
- [ ] Multiple uploads work sequentially

### Overall
- [ ] No memory leaks (check RAM over time)
- [ ] No disk space issues (uploads folder stays clean)
- [ ] Response times < 10 seconds
- [ ] Can handle multiple users
- [ ] Graceful degradation on errors

---

## Quick Test Script

Create `run_all_tests.py`:

```python
#!/usr/bin/env python3
import subprocess
import time
import requests
import sys

print("=" * 60)
print("SIH26188 AUTOMATED TEST SUITE")
print("=" * 60)

# Test 1: Backend Health
print("\n[TEST 1] Backend Health Check")
try:
    response = requests.get("http://127.0.0.1:8000/health", timeout=5)
    if response.status_code == 200:
        print("✅ Backend is running")
    else:
        print("❌ Backend returned non-200 status")
        sys.exit(1)
except Exception as e:
    print(f"❌ Backend not accessible: {e}")
    sys.exit(1)

# Test 2: Document Analysis
print("\n[TEST 2] Document Analysis")
try:
    with open("test_image.jpg", "rb") as f:
        files = {"file": f}
        response = requests.post(
            "http://127.0.0.1:8000/analyze-document",
            files=files,
            timeout=30
        )
    if response.status_code == 200:
        data = response.json()
        if "risk_score" in data and "verdict" in data:
            print(f"✅ Analysis successful - Risk: {data['risk_score']}, Verdict: {data['verdict']}")
        else:
            print("❌ Response missing required fields")
    else:
        print(f"❌ Analysis failed with status {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Rules Validation
print("\n[TEST 3] Rules Validation")
try:
    from app.rules import validate_fields
    
    test_cases = [
        ({"name": "JOHN", "dob": "15-01-1990", "doc_no": "A123", "expiry": "31-12-2030"}, 0),
        ({"name": None, "dob": None, "doc_no": None, "expiry": None}, 65),
    ]
    
    for fields, expected_min_score in test_cases:
        score, _ = validate_fields(fields)
        if score >= expected_min_score:
            print(f"✅ Validation test passed - Score: {score}")
        else:
            print(f"❌ Validation test failed - Expected >= {expected_min_score}, got {score}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("TEST SUITE COMPLETE")
print("=" * 60)
```

Run it:
```bash
python run_all_tests.py
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Check if port 8000 is in use: `lsof -i :8000` |
| OCR extraction fails | Image might be too small or text too blurry |
| Face verification fails | Faces might not be clear enough or too different |
| Streamlit connection error | Verify backend URL and ensure backend is running |
| Slow response times | OCR and face detection are CPU-intensive; give it time |
| Memory issues | Check EasyOCR model is cached: `~/.EasyOCR/model/` |

