import cv2
import numpy as np

def detect_tamper(image_path: str):
    img = cv2.imread(image_path)
    if img is None:
        return {
            "tamper_score": 50,
            "signals": ["Image could not be read"]
        }

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.Laplacian(gray, cv2.CV_64F).var()

    signals = []
    tamper_score = 0

    if blur < 80:
        signals.append("Image is very blurry")
        tamper_score += 15

    height, width = gray.shape
    if height < 300 or width < 300:
        signals.append("Low-resolution image")
        tamper_score += 10

    if len(np.unique(gray)) < 15:
        signals.append("Low pixel variation, possibly compressed or edited")
        tamper_score += 10

    return {
        "tamper_score": min(tamper_score, 100),
        "signals": signals if signals else ["No obvious tamper signals detected"]
    }