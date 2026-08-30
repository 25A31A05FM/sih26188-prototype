# SIH26188 Prototype

## Run backend
uvicorn app.main:app --reload

## Run UI
streamlit run ui/streamlit_app.py

## What this prototype does
- OCR extraction
- Field parsing
- Rule-based validation
- Tamper scoring
- Face verification
- Final risk score

## What is still missing
- Real tamper-detection ML model
- Better OCR field extraction for real documents
- Document type classifier
- Dataset-based evaluation
- Audit logs and admin dashboard