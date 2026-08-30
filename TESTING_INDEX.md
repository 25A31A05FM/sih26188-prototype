# 📚 SIH26188 Testing Documentation Index

## 🎯 Start Here (Choose Your Path)

### **I have 5 minutes** ⚡
→ **Read:** `START_TESTING.md`
→ **Run:** `python test_backend.py`
→ **Time:** 5 minutes to verify everything works

---

### **I have 15 minutes** ⏱️
→ **Read:** `QUICK_START_TESTING.md`
→ **Run:** Backend + automated tests + curl API test
→ **Check:** Document analysis with sample image

---

### **I have 1 hour** 📖
→ **Read:** `TESTING_GUIDE.md` (comprehensive)
→ **Follow:** All 8 testing phases
→ **Test:** Backend, API, UI, Performance, Security

---

### **I want a checklist** ✅
→ **Use:** `MANUAL_TEST_CHECKLIST.md`
→ **Check off:** Each test as you complete it
→ **Print:** Ready for QA documentation

---

## 📄 All Documentation Files

| File | Purpose | Time | Best For |
|------|---------|------|----------|
| `START_TESTING.md` | Get started instantly | 5 min | Quick verification |
| `QUICK_START_TESTING.md` | Fast reference guide | 15 min | Quick overview |
| `TESTING_GUIDE.md` | Complete procedures | 60 min | Comprehensive testing |
| `MANUAL_TEST_CHECKLIST.md` | Step-by-step checklist | 60 min | QA documentation |
| `TEST_SUMMARY.txt` | Testing overview | 5 min | Reference guide |
| `FIXES_APPLIED.md` | Details of bug fixes | 10 min | Understanding changes |
| `test_backend.py` | Automated test script | 1 min | Unit testing |

---

## 🚀 Running the Tests

### **Automated Testing (Recommended First)**
```bash
python test_backend.py
```
- Tests all modules automatically
- 4 test cases
- Takes ~30 seconds
- Shows pass/fail for each test

### **Manual API Testing**
```bash
# Test health endpoint
curl http://127.0.0.1:8000/health

# Test document analysis
curl -X POST http://127.0.0.1:8000/analyze-document ^
  -F "file=@document.jpg"

# Test face verification  
curl -X POST http://127.0.0.1:8000/verify-face ^
  -F "document_image=@doc.jpg" ^
  -F "selfie_image=@selfie.jpg"
```

### **UI Testing**
```bash
streamlit run ui/streamlit_app.py
# Opens http://localhost:8501
# Upload images and test through browser
```

---

## ✅ Test Coverage

### **Unit Testing** (test_backend.py)
- ✅ Health endpoint
- ✅ Rules validation
- ✅ Tamper detection
- ✅ OCR parsing

### **Integration Testing** (API endpoints)
- ✅ Document analysis
- ✅ Face verification
- ✅ Error handling
- ✅ File cleanup

### **UI Testing** (Streamlit)
- ✅ Page loading
- ✅ File upload
- ✅ Results display
- ✅ Error messages

### **Performance Testing**
- ✅ Response time (< 30 sec)
- ✅ Memory usage (< 500MB)
- ✅ File cleanup verification
- ✅ Concurrent requests

### **Security Testing**
- ✅ Path traversal prevention
- ✅ Filename sanitization
- ✅ Large file handling
- ✅ Error boundary testing

---

## 📊 Expected Results

### **Backend Health**
```
GET /health
Expected: HTTP 200
Response: {"status":"ok"}
```

### **Document Analysis**
```
POST /analyze-document
Expected: HTTP 200, JSON response with:
- risk_score: 0-100
- verdict: low_risk | medium_risk | high_risk
- fields: {name, dob, doc_no, expiry}
- reasons: [list of analysis reasons]
```

### **Risk Score Interpretation**
- `0-29`: ✅ low_risk (good document)
- `30-59`: ⚠️ medium_risk (some issues)
- `60-100`: 🔴 high_risk (likely forged/expired)

### **Test Scenarios**
| Scenario | Expected Result |
|----------|-----------------|
| Good quality document | risk_score: 0-15 |
| Expired document | risk_score >= 30, reason: "Document is expired" |
| Blurry image | Contains: "Image is very blurry" |
| Low resolution | Contains: "Low-resolution image" |
| All fields missing | risk_score: 65 |

---

## 🔍 Debugging Guide

### If automated tests fail:
1. Check backend is running: `curl http://127.0.0.1:8000/health`
2. Check Python imports: `python -c "from app.rules import validate_fields"`
3. Check dependencies: `pip list | grep -E "fastapi|easyocr|opencv"`
4. Check for port conflicts: `netstat -ano | findstr :8000`

### If API tests fail:
1. Verify backend is running
2. Check response format: `curl -v http://127.0.0.1:8000/health`
3. Try with different image: `curl -X POST ... -F "file=@different_image.jpg"`
4. Check logs in terminal where backend is running

### If UI tests fail:
1. Verify backend URL is correct
2. Check backend is running and accessible
3. Try hard refresh: F5 or Ctrl+Shift+R
4. Check browser console: F12 → Console tab

### If performance is slow:
1. First run: EasyOCR downloads models (~200MB) - this takes time
2. Monitor memory: Open Task Manager → find Python
3. Reduce image size: Use smaller test images
4. Restart Python: Kill process and start fresh

---

## 📋 Quick Verification Checklist

- [ ] Backend starts without errors
- [ ] `python test_backend.py` shows 4/4 PASS
- [ ] Health endpoint returns OK
- [ ] Document analysis returns valid JSON
- [ ] Risk score is always 0-100
- [ ] Verdict is one of: low_risk, medium_risk, high_risk
- [ ] Face verification works
- [ ] Error messages display gracefully
- [ ] Response time < 30 seconds
- [ ] Memory usage < 500MB
- [ ] uploads/ folder is cleaned up

---

## 🎯 Success Criteria

Your project is **READY FOR DEPLOYMENT** when:

1. ✅ All automated tests pass (test_backend.py)
2. ✅ All API endpoints respond correctly
3. ✅ UI loads and works smoothly
4. ✅ Performance is acceptable (< 30 sec per request)
5. ✅ Error handling is graceful (no crashes)
6. ✅ File cleanup works (no disk leaks)
7. ✅ Security measures are in place (sanitization, etc.)

---

## 🔗 Quick Links to Each Document

1. **[START_TESTING.md](START_TESTING.md)** - 5 minute quick start
2. **[QUICK_START_TESTING.md](QUICK_START_TESTING.md)** - Fast reference
3. **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive guide (50+ tests)
4. **[MANUAL_TEST_CHECKLIST.md](MANUAL_TEST_CHECKLIST.md)** - Step-by-step checklist
5. **[TEST_SUMMARY.txt](TEST_SUMMARY.txt)** - Testing overview
6. **[FIXES_APPLIED.md](FIXES_APPLIED.md)** - What was fixed
7. **[test_backend.py](test_backend.py)** - Automated test runner

---

## 🎓 Learning Path

### Complete Beginner:
1. Read: `START_TESTING.md`
2. Run: `python test_backend.py`
3. Success? → Project is working!

### Intermediate:
1. Read: `QUICK_START_TESTING.md`
2. Follow: Test scenarios section
3. Run: API tests with curl
4. Check: Performance metrics

### Advanced:
1. Read: `TESTING_GUIDE.md` (all phases)
2. Use: `MANUAL_TEST_CHECKLIST.md`
3. Complete: Security and performance tests
4. Document: Results in test report

---

## 📞 Support Resources

- **Errors during setup?** → See "Troubleshooting" section in TESTING_GUIDE.md
- **Need detailed procedures?** → Read TESTING_GUIDE.md Phase by phase
- **Want a checklist?** → Use MANUAL_TEST_CHECKLIST.md
- **Quick reference?** → Check TEST_SUMMARY.txt
- **Understanding fixes?** → Read FIXES_APPLIED.md

---

## 🏁 Next Steps

**Ready to test?**

1. ✅ Start backend: `uvicorn app.main:app --reload`
2. ✅ Run tests: `python test_backend.py`
3. ✅ Verify results: Check output shows 4/4 PASS
4. ✅ You're done! 🎉

**Need more details?**

→ Choose a document from the list above based on your time availability.

---

**Last Updated:** 2026-08-30
**Project:** SIH26188 AI-Based Fake Identity & Document Screening System
**Status:** ✅ Ready for Testing
