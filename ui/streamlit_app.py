import streamlit as st
import requests

st.set_page_config(page_title="SIH26188 Prototype", layout="wide")
st.title("AI-Based Fake Identity & Document Screening System")

backend_url = st.text_input("Backend URL", "http://127.0.0.1:8000")

doc_file = st.file_uploader("Upload document image", type=["png", "jpg", "jpeg"])
selfie_file = st.file_uploader("Upload selfie image", type=["png", "jpg", "jpeg"])

col1, col2 = st.columns(2)

with col1:
    if st.button("Analyze Document") and doc_file:
        try:
            with st.spinner("Analyzing document... OCR may take up to 2 minutes on first run."):
                files = {"file": (doc_file.name, doc_file.getvalue(), doc_file.type)}
                res = requests.post(f"{backend_url}/analyze-document", files=files, timeout=180)
                
                if res.status_code == 200:
                    result = res.json()
                    st.subheader("Document Analysis Result")
                    
                    # Show raw analysis
                    st.json(result)
                    
                    # Verification form for extracted fields
                    st.subheader("🔍 Verify Extracted Fields")
                    st.info("OCR may have errors. Please review and correct the extracted fields:")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        verified_name = st.text_input("Name", value=result['fields'].get('name') or "", key="name_verify")
                        verified_dob = st.text_input("Date of Birth (DD/MM/YYYY)", value=result['fields'].get('dob') or "", key="dob_verify")
                    
                    with col_b:
                        verified_doc_no = st.text_input("Document Number", value=result['fields'].get('doc_no') or "", key="docno_verify")
                        verified_expiry = st.text_input("Expiry Date (DD/MM/YYYY)", value=result['fields'].get('expiry') or "", key="exp_verify")
                    
                    # Save verified data
                    if st.button("✅ Confirm Verified Fields"):
                        st.session_state['verified_fields'] = {
                            'name': verified_name,
                            'dob': verified_dob,
                            'doc_no': verified_doc_no,
                            'expiry': verified_expiry,
                            'original_result': result
                        }
                        st.success("✅ Fields saved. You can now verify face or proceed with next steps.")
                else:
                    st.error(f"Error: {res.status_code} - {res.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to backend at {backend_url}. Make sure the server is running.")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. The backend is taking too long to respond.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with col2:
    if st.button("Verify Face") and doc_file and selfie_file:
        try:
            with st.spinner("Verifying face..."):
                files = {
                    "document_image": (doc_file.name, doc_file.getvalue(), doc_file.type),
                    "selfie_image": (selfie_file.name, selfie_file.getvalue(), selfie_file.type)
                }
                res = requests.post(f"{backend_url}/verify-face", files=files, timeout=180)
                
                if res.status_code == 200:
                    st.subheader("Face Verification Result")
                    st.json(res.json())
                else:
                    st.error(f"Error: {res.status_code} - {res.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to backend at {backend_url}. Make sure the server is running.")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. The backend is taking too long to respond.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")