# Quick Start Testing Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Start Backend
```bash
cd C:\Users\tejom\OneDrive\Desktop\sih26188-prototype
uvicorn app.main:app --reload
```
Wait for: `Application startup complete`

---

### Step 2: Run Automated Tests
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
🎉 All tests passed! Your project is working correctly!
```

---

### Step 3: Test Backend API
```bash
# Test health
curl http://127.0.0.1:8000/health
# Expected: {"status":"ok"}

# Test with document (replace path with your image)
curl -X POST http://127.0.0.1:8000/analyze-document ^
  -F "file=@C:\path\to\document.jpg"
# Expected: JSON with risk_score, verdict, and analysis results
```

---

### Step 4: Test UI (Optional)
```bash
streamlit run ui/streamlit_app.py
# Opens http://localhost:8501
# Upload document and click "Analyze Document"
```

---

## 📋 Key Test Scenarios

### Test 1: Good Document ✅
- Clear, well-lit image
- All text visible
- Valid, non-expired date
- **Expected:** risk_score: 0-15, verdict: low_risk

### Test 2: Expired Document ⚠️
- Any document with past expiry date
- **Expected:** Contains "Document is expired"
- **Expected:** risk_score >= 30, verdict: high_risk

### Test 3: Blurry Document 🌫️
- Blurry/out-of-focus image
- **Expected:** Contains "Image is very blurry"
- **Expected:** tamper_score >= 15

### Test 4: Low Resolution 📉
- Image < 300x300 pixels
- **Expected:** Contains "Low-resolution image"
- **Expected:** tamper_score >= 10

### Test 5: Face Verification 👤
- Document photo
- Selfie from same person
- **Expected:** verified: true, distance < 0.6

---

## ✅ Success Criteria

| Component | Test | Expected Result |
|-----------|------|-----------------|
| Backend | Health check | HTTP 200, {"status":"ok"} |
| API | Document analysis | HTTP 200, JSON with all fields |
| API | Face verification | HTTP 200, verified true/false |
| Scoring | Risk score range | Always 0-100 |
| Verdict | Valid verdicts | low_risk, medium_risk, high_risk |
| Rules | Date parsing | Works with multiple formats |
| Tamper | Detection | Identifies blur, low-res, compression |
| Error Handling | Invalid requests | Graceful error, no crash |
| Cleanup | File management | uploads/ folder stays clean |
| Performance | Response time | < 30 seconds per request |

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check if port 8000 is free: `netstat -ano \| findstr :8000` |
| Connection refused | Make sure backend is running before tests |
| Slow OCR | First run downloads ML models (~200MB), be patient |
| Face detection fails | Ensure faces are clear and visible in images |
| Streamlit won't connect | Verify backend URL and backend is running |
| Memory issues | Restart Python process and try again |

---

## 📊 Performance Targets

- **Document Analysis:** 5-15 seconds
- **Face Verification:** 3-10 seconds  
- **Memory Usage:** < 500MB
- **Disk Cleanup:** Automatic after each request

---

## 📁 Important Files

- `test_backend.py` - Run automated tests
- `TESTING_GUIDE.md` - Comprehensive testing procedures
- `MANUAL_TEST_CHECKLIST.md` - Step-by-step checklist
- `FIXES_APPLIED.md` - Details of bug fixes

---

## ✨ Quick Commands Reference

```bash
# Setup
cd C:\Users\tejom\OneDrive\Desktop\sih26188-prototype
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload

# Run tests  
python test_backend.py

# Test health
curl http://127.0.0.1:8000/health

# Test document
curl -X POST http://127.0.0.1:8000/analyze-document -F "file=@doc.jpg"

# Run UI
streamlit run ui/streamlit_app.py

# Check cleanup
dir uploads
```

---

## 🎯 Next Steps

1. ✅ Run `python test_backend.py`
2. ✅ Test with your own document images
3. ✅ Check results match expectations
4. ✅ Test error scenarios
5. ✅ Monitor performance
6. 🎉 Deploy!

**Any issues?** Check `TESTING_GUIDE.md` for detailed troubleshooting.
