# 🚀 START TESTING YOUR SIH26188 PROJECT

## 📋 3-Step Quick Start

### **STEP 1: Start Backend (30 seconds)**
```bash
cd C:\Users\tejom\OneDrive\Desktop\sih26188-prototype
uvicorn app.main:app --reload
```
✅ Wait for: `Application startup complete`

---

### **STEP 2: Run Automated Tests (30 seconds)**
```bash
# Open NEW terminal, run this:
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

### **STEP 3: Test Document Analysis (1 minute)**
```bash
# Option A: Using curl (if you have an image file)
curl -X POST http://127.0.0.1:8000/analyze-document ^
  -F "file=@C:\path\to\your\document.jpg"

# Option B: Using Streamlit UI
streamlit run ui/streamlit_app.py
# Then upload image via browser at http://localhost:8501
```

---

## ✅ What to Check

| Check | How | Expected |
|-------|-----|----------|
| Health | `curl http://127.0.0.1:8000/health` | `{"status":"ok"}` |
| Analysis | `python test_backend.py` | All 4 tests pass ✅ |
| Scoring | Upload good document | risk_score: 0-15, verdict: low_risk |
| Errors | Upload expired document | risk_score >= 30, verdict: high_risk |
| Cleanup | Check folder size | `dir uploads/` → empty or small |

---

## 📊 Test Results Template

```
PROJECT: SIH26188
TESTED BY: _____________________
DATE: _____________________

✅ BACKEND TESTS
  [✓] Health check: PASS
  [✓] Rules validation: PASS
  [✓] Tamper detection: PASS
  [✓] OCR parsing: PASS

✅ API TESTS
  [✓] Document analysis: PASS
  [✓] Face verification: PASS
  [✓] Error handling: PASS

✅ PERFORMANCE
  [✓] Response time: < 30 sec
  [✓] Memory usage: < 500MB
  [✓] File cleanup: OK

✅ UI TESTS
  [✓] Streamlit loads: PASS
  [✓] File upload: PASS
  [✓] Error messages: PASS

OVERALL: ✅ READY FOR DEPLOYMENT
```

---

## 📁 Testing Documents (Created for You)

1. **test_backend.py** - Automated tests (run this first!)
2. **QUICK_START_TESTING.md** - 5-minute guide
3. **TESTING_GUIDE.md** - Comprehensive testing (50+ test cases)
4. **MANUAL_TEST_CHECKLIST.md** - Step-by-step checklist with boxes
5. **FIXES_APPLIED.md** - Details of all bug fixes
6. **TEST_SUMMARY.txt** - This complete reference

---

## 🎯 Success Criteria

Your project is **✅ WORKING PERFECTLY** when:

- ✅ `python test_backend.py` shows 4/4 PASS
- ✅ Document analysis returns risk_score (0-100)
- ✅ Verdict is one of: low_risk, medium_risk, high_risk
- ✅ Expired documents get high risk scores
- ✅ Blurry images are detected
- ✅ Face verification works
- ✅ Error messages display gracefully (no crashes)
- ✅ Response time < 30 seconds
- ✅ Memory usage < 500MB
- ✅ uploads/ folder stays clean

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Port 8000 in use: `netstat -ano \| findstr :8000` |
| Tests fail | Make sure backend is running first |
| Slow OCR | First run downloads ML models (~200MB) - takes time |
| Connection refused | Check backend URL and ensure backend is running |
| Memory issues | Restart Python process |

---

## 📞 Need Help?

1. **Quick issues?** → Check QUICK_START_TESTING.md
2. **Step-by-step?** → Use MANUAL_TEST_CHECKLIST.md
3. **Detailed testing?** → Read TESTING_GUIDE.md
4. **What was fixed?** → See FIXES_APPLIED.md

---

## 🎉 You're All Set!

Your SIH26188 project is ready to test. Start with:

```bash
python test_backend.py
```

Good luck! 🚀
