# Manual Testing Checklist for SIH26188

## Pre-Test Setup

### Prerequisites
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Virtual environment activated
- [ ] Project folder: `C:\Users\tejom\OneDrive\Desktop\sih26188-prototype`

### Sample Images Prepared
- [ ] Good quality document image
- [ ] Expired document image  
- [ ] Blurry document image
- [ ] Low-resolution image (< 300x300)
- [ ] Face photo matching document
- [ ] Different face for mismatch test

---

## Phase 1: Backend Startup

### Step 1.1: Start Backend Server
```bash
cd C:\Users\tejom\OneDrive\Desktop\sih26188-prototype
uvicorn app.main:app --reload
```

**Checklist:**
- [ ] No error messages
- [ ] Output shows "Uvicorn running on http://127.0.0.1:8000"
- [ ] Output shows "Application startup complete"

### Step 1.2: Verify Backend Health
```bash
# In another terminal
curl http://127.0.0.1:8000/health
```

**Expected:** `{"status":"ok"}`
- [ ] Response is 200 OK
- [ ] Response contains `"status":"ok"`

---

## Phase 2: Run Unit Tests

### Step 2.1: Run Backend Test Script
```bash
python test_backend.py
```

**Expected Output:**
```
✅ PASS - Backend Health Check
✅ PASS - Rules Validation Module
✅ PASS - Tamper Detection Module
✅ PASS - OCR Module

Total: 4/4 tests passed
```

**Checklist:**
- [ ] All 4 tests show ✅ PASS
- [ ] No error messages
- [ ] Script completes without crashing

---

## Phase 3: API Testing (Manual)

### Step 3.1: Test Document Analysis Endpoint

**Using cURL:**
```bash
curl -X POST http://127.0.0.1:8000/analyze-document \
  -F "file=@path/to/good_document.jpg"
```

**Expected Response Format:**
```json
{
  "filename": "good_document.jpg",
  "ocr_text": "...",
  "fields": {
    "name": "...",
    "dob": "...",
    "doc_no": "...",
    "expiry": "..."
  },
  "rule_score": 0,
  "tamper_score": 5,
  "risk_score": 3,
  "verdict": "low_risk",
  "reasons": [...]
}
```

**Checklist:**
- [ ] HTTP Status: 200 OK
- [ ] Response is valid JSON
- [ ] All required fields present
- [ ] `risk_score` is 0-100
- [ ] `verdict` is one of: low_risk, medium_risk, high_risk
- [ ] `fields` object contains: name, dob, doc_no, expiry
- [ ] Response time < 30 seconds

---

### Step 3.2: Test with Different Documents

Test each image and record results:

#### Test Image 1: Good Quality Document
```bash
curl -X POST http://127.0.0.1:8000/analyze-document \
  -F "file=@good_document.jpg"
```

**Expected:**
- [ ] verdict: "low_risk"
- [ ] rule_score: 0-15
- [ ] tamper_score: 0-10

#### Test Image 2: Expired Document
```bash
curl -X POST http://127.0.0.1:8000/analyze-document \
  -F "file=@expired_document.jpg"
```

**Expected:**
- [ ] verdict: "high_risk" or "medium_risk"
- [ ] Contains reason: "Document is expired"
- [ ] rule_score >= 30

#### Test Image 3: Blurry Document
```bash
curl -X POST http://127.0.0.1:8000/analyze-document \
  -F "file=@blurry_document.jpg"
```

**Expected:**
- [ ] Contains signal: "Image is very blurry"
- [ ] tamper_score >= 15

#### Test Image 4: Low Resolution
```bash
curl -X POST http://127.0.0.1:8000/analyze-document \
  -F "file=@low_res_document.jpg"
```

**Expected:**
- [ ] Contains signal: "Low-resolution image"
- [ ] tamper_score >= 10

---

### Step 3.3: Test Face Verification Endpoint

```bash
curl -X POST http://127.0.0.1:8000/verify-face \
  -F "document_image=@doc_photo.jpg" \
  -F "selfie_image=@selfie.jpg"
```

**Expected Response Format:**
```json
{
  "verified": true,
  "distance": 0.45,
  "model": "VGG-Face",
  "threshold": 0.6
}
```

**Checklist:**
- [ ] HTTP Status: 200 OK
- [ ] Response is valid JSON
- [ ] Contains: verified, distance, model, threshold
- [ ] verified is boolean (true/false)
- [ ] distance is number (0-1)

---

### Step 3.4: Test Error Scenarios

#### Test 4A: Missing File Parameter
```bash
curl -X POST http://127.0.0.1:8000/analyze-document
```

**Expected:**
- [ ] HTTP Status: 422 (Validation Error)
- [ ] Error message indicates file is required

#### Test 4B: Invalid File Type
```bash
curl -X POST http://127.0.0.1:8000/analyze-document \
  -F "file=@document.txt"
```

**Expected:**
- [ ] Server handles gracefully (doesn't crash)
- [ ] Returns error response

#### Test 4C: Missing Face Parameter
```bash
curl -X POST http://127.0.0.1:8000/verify-face \
  -F "document_image=@doc.jpg"
```

**Expected:**
- [ ] HTTP Status: 422 (Validation Error)
- [ ] Error indicates selfie_image is required

#### Test 4D: Non-existent Backend URL (Streamlit test)
- [ ] Change URL to `http://invalid-url:9999`
- [ ] Try to upload
- [ ] Expected: Error message displayed (not crash)
- [ ] [ ] UI shows: "❌ Cannot connect to backend"

---

## Phase 4: Streamlit UI Testing

### Step 4.1: Start Streamlit App
```bash
streamlit run ui/streamlit_app.py
```

**Expected:**
- [ ] No error messages
- [ ] Browser opens to `http://localhost:8501`
- [ ] Page shows "AI-Based Fake Identity & Document Screening System"
- [ ] Backend URL field shows "http://127.0.0.1:8000"
- [ ] Two file upload buttons visible
- [ ] Two analysis buttons visible

### Step 4.2: Test Document Upload and Analysis

1. [ ] Upload a good quality document image
2. [ ] Click "Analyze Document"
3. [ ] Loading spinner appears
4. [ ] JSON results display below
5. [ ] Check results are accurate

### Step 4.3: Test Face Verification

1. [ ] Upload document photo
2. [ ] Upload matching selfie
3. [ ] Click "Verify Face"
4. [ ] Loading spinner appears
5. [ ] JSON results with "verified" field display

### Step 4.4: Test Error Handling

1. [ ] Stop the backend server
2. [ ] Try to upload document
3. [ ] Check error message displays: "Cannot connect to backend"
4. [ ] UI doesn't crash
5. [ ] Can restart backend and try again
6. [ ] Restart backend and retry - should work

### Step 4.5: Test Invalid Backend URL

1. [ ] Change Backend URL to invalid: `http://invalid:9999`
2. [ ] Try to upload
3. [ ] Error message displays gracefully
4. [ ] Fix URL and try again

---

## Phase 5: Performance Testing

### Step 5.1: Response Time Measurement

Run this in Python:

```python
import time
import requests

times = []
for i in range(3):
    start = time.time()
    with open("good_document.jpg", "rb") as f:
        files = {"file": f}
        requests.post("http://127.0.0.1:8000/analyze-document", files=files)
    elapsed = time.time() - start
    times.append(elapsed)
    print(f"Request {i+1}: {elapsed:.2f} seconds")

avg = sum(times) / len(times)
print(f"Average: {avg:.2f} seconds")
```

**Expected:**
- [ ] Each request takes 5-15 seconds
- [ ] No request exceeds 30 seconds
- [ ] Consistent timing across requests

### Step 5.2: Memory Check

**Monitor during processing:**
- [ ] Open Task Manager (Ctrl+Shift+Esc)
- [ ] Watch Python process memory usage
- [ ] Expected: Doesn't exceed 500MB
- [ ] Memory returns to baseline after processing

### Step 5.3: Disk Space Check

```bash
# Before running analysis
dir uploads/

# Run several analyses (5+)
# After completing analyses
dir uploads/

# Expected: uploads/ folder is empty or only has a few files
```

---

## Phase 6: File Cleanup Verification

### Step 6.1: Check File Cleanup

1. [ ] Note the size of `uploads/` folder
2. [ ] Run document analysis 10 times
3. [ ] Check `uploads/` folder size
4. [ ] Expected: No significant growth or empty

```bash
# Check directory
Get-ChildItem uploads/ | Measure-Object -Sum Length

# Expected: Minimal files or empty
```

---

## Phase 7: Security Testing

### Step 7.1: Filename Sanitization

```bash
# Try to upload with suspicious filename
curl -X POST http://127.0.0.1:8000/analyze-document \
  -F 'file=@document.jpg;filename=../../../etc/passwd'
```

**Expected:**
- [ ] Server sanitizes filename
- [ ] No error or path traversal vulnerability
- [ ] File stored safely

### Step 7.2: Large File Handling

```bash
# Create a large test file (if needed)
# Try to upload very large file (100MB+)
```

**Expected:**
- [ ] Server handles gracefully
- [ ] Times out or returns error (not crash)

---

## Final Verification

### All Tests Passed? ✅

- [ ] Backend starts without errors
- [ ] All 4 automated tests pass
- [ ] API endpoints respond correctly
- [ ] Document analysis works for different image types
- [ ] Face verification works
- [ ] Error handling is graceful
- [ ] Streamlit UI is user-friendly
- [ ] Performance is acceptable
- [ ] Files are cleaned up
- [ ] No security vulnerabilities detected

---

## Summary Report

**Date:** _______________

**Tester Name:** _______________

**Overall Status:** 
- [ ] ✅ PASS - Ready for deployment
- [ ] ⚠️  PARTIAL - Some issues need fixing
- [ ] ❌ FAIL - Major issues found

**Issues Found:**
1. _____________________________
2. _____________________________
3. _____________________________

**Notes:**
___________________________________________
___________________________________________

---

## Quick Test Commands Reference

```bash
# Start backend
uvicorn app.main:app --reload

# Start Streamlit
streamlit run ui/streamlit_app.py

# Run tests
python test_backend.py

# Test health
curl http://127.0.0.1:8000/health

# Test document analysis
curl -X POST http://127.0.0.1:8000/analyze-document \
  -F "file=@document.jpg"

# Test face verification
curl -X POST http://127.0.0.1:8000/verify-face \
  -F "document_image=@doc.jpg" \
  -F "selfie_image=@selfie.jpg"

# Check uploads folder
dir uploads/

# Monitor performance
Get-Process python | Select-Object WorkingSet
```
