import os
import uuid
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from app.ocr import extract_text, parse_fields
from app.rules import validate_fields
from app.tamper import detect_tamper
from app.face_match import compare_faces

app = FastAPI(title="SIH26188 Prototype")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    """Remove potentially dangerous characters from filename"""
    return "".join(c for c in filename if c.isalnum() or c in "._- ")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    safe_filename = sanitize_filename(file.filename)
    path = os.path.join(UPLOAD_DIR, f"{file_id}_{safe_filename}")

    try:
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text(path)
        fields = parse_fields(text)
        rule_score, rule_reasons = validate_fields(fields)
        tamper = detect_tamper(path)

        rule_weight = 0.6
        tamper_weight = 0.4
        final_score = int((rule_score * rule_weight) + (tamper["tamper_score"] * tamper_weight))
        verdict = "high_risk" if final_score >= 60 else "medium_risk" if final_score >= 30 else "low_risk"

        return {
            "filename": file.filename,
            "ocr_text": text,
            "fields": fields,
            "rule_score": rule_score,
            "tamper_score": tamper["tamper_score"],
            "risk_score": final_score,
            "verdict": verdict,
            "reasons": rule_reasons + tamper["signals"]
        }
    finally:
        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass

@app.post("/verify-face")
async def verify_face(
    document_image: UploadFile = File(...),
    selfie_image: UploadFile = File(...)
):
    doc_id = str(uuid.uuid4())
    safe_doc_name = sanitize_filename(document_image.filename)
    safe_selfie_name = sanitize_filename(selfie_image.filename)
    doc_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{safe_doc_name}")
    selfie_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{safe_selfie_name}")

    try:
        # Save document image
        with open(doc_path, "wb") as buffer:
            shutil.copyfileobj(document_image.file, buffer)

        # Save selfie image
        with open(selfie_path, "wb") as buffer:
            shutil.copyfileobj(selfie_image.file, buffer)

        # Verify files exist and are readable
        if not os.path.exists(doc_path) or os.path.getsize(doc_path) == 0:
            return {"verified": False, "error": "Failed to save or read document image"}
        if not os.path.exists(selfie_path) or os.path.getsize(selfie_path) == 0:
            return {"verified": False, "error": "Failed to save or read selfie image"}

        # Convert to absolute paths for DeepFace
        doc_path = os.path.abspath(doc_path)
        selfie_path = os.path.abspath(selfie_path)

        result = compare_faces(doc_path, selfie_path)
        return result
    except Exception as e:
        return {"verified": False, "error": f"Face verification error: {str(e)}"}
    finally:
        for path in [doc_path, selfie_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass