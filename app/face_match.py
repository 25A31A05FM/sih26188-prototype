from deepface import DeepFace
import os

def compare_faces(img1_path: str, img2_path: str):
    """Compare two face images for identity verification.
    
    Args:
        img1_path: Path to document photo (e.g., Aadhaar card photo)
        img2_path: Path to selfie for verification
        
    Returns:
        dict with verified status, distance score, and model info
    """
    try:
        # Validate file paths exist and are readable
        if not os.path.exists(img1_path):
            return {"verified": False, "error": f"Document image not found: {img1_path}"}
        if not os.path.exists(img2_path):
            return {"verified": False, "error": f"Selfie image not found: {img2_path}"}
        
        if os.path.getsize(img1_path) == 0:
            return {"verified": False, "error": "Document image is empty"}
        if os.path.getsize(img2_path) == 0:
            return {"verified": False, "error": "Selfie image is empty"}
        
        # Run face verification
        result = DeepFace.verify(
            img1_path=img1_path,
            img2_path=img2_path,
            enforce_detection=False,
            silent=True
        )
        
        return {
            "verified": bool(result["verified"]),
            "distance": float(result["distance"]),
            "model": result.get("model", "VGG-Face"),
            "threshold": float(result.get("threshold", 0.6))
        }
    except ValueError as e:
        # DeepFace couldn't detect faces
        return {"verified": False, "error": f"Face detection failed: {str(e)}. Ensure both images contain clear faces."}
    except Exception as e:
        return {"verified": False, "error": f"Face comparison error: {str(e)}"}