import re
import os
import uuid
import easyocr
import cv2

# Initialize reader with English + Telugu (Hindi not compatible with Telugu in EasyOCR)
reader = easyocr.Reader(["te", "en"], gpu=False)

HEADER_BLOCKLIST = re.compile(
    r"government|india|authority|unique|identification|enrollment|aadhaar|aadhar|"
    r"uidai|proof|identity|citizenship|verification|authentication|registration|"
    r"enrolment|enrollmen|govemn|govorn|govar",
    re.IGNORECASE,
)


def preprocess_image(image_path: str) -> str:
    """Read, deskew, denoise and binarize image. Returns path to preprocessed file."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return image_path

    h, w = img.shape
    max_dim = 2000
    if max(h, w) > max_dim:
        scale = max_dim / float(max(h, w))
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    img = cv2.fastNlMeansDenoising(img, None, 30, 7, 21)
    img = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
    )

    coords = cv2.findNonZero(cv2.bitwise_not(img))
    if coords is not None:
        rect = cv2.minAreaRect(coords)
        angle = rect[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = img.shape
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        img = cv2.warpAffine(
            img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )

    out_path = os.path.join("uploads", f"pre_{uuid.uuid4().hex}.png")
    cv2.imwrite(out_path, img)
    return out_path


def _ocr_lines(image_path: str) -> list[str]:
    results = reader.readtext(image_path, detail=1)
    return [r[1] for r in results if r[1].strip()]


def _card_region_path(image_path: str) -> str | None:
    """Crop and upscale the wallet-card section where DOB/name are printed."""
    img = cv2.imread(image_path)
    if img is None:
        return None

    h, w = img.shape[:2]
    crop = img[int(h * 0.52) :, :]
    crop = cv2.resize(crop, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.4, beta=8)

    out_path = os.path.join("uploads", f"card_{uuid.uuid4().hex}.png")
    cv2.imwrite(out_path, gray)
    return out_path


def _merge_lines(all_lines: list[str], seen: set[str], lines: list[str]) -> None:
    for line in lines:
        key = line.strip().lower()
        if key and key not in seen:
            seen.add(key)
            all_lines.append(line.strip())


def _fields_incomplete(text: str) -> bool:
    fields = parse_fields(text)
    return not fields.get("name") or not fields.get("dob") or not fields.get("doc_no")


def extract_text(image_path: str) -> str:
    """Run OCR on raw image; card-region crop only if key fields are still missing."""
    temp_files: list[str] = []
    all_lines: list[str] = []
    seen: set[str] = set()

    try:
        _merge_lines(all_lines, seen, _ocr_lines(image_path))
        text = "\n".join(all_lines)

        if _fields_incomplete(text):
            card = _card_region_path(image_path)
            if card:
                temp_files.append(card)
                _merge_lines(all_lines, seen, _ocr_lines(card))
    except Exception:
        results = reader.readtext(image_path, detail=0)
        _merge_lines(all_lines, seen, results)

    for path in temp_files:
        try:
            if path.startswith("uploads") and os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

    return "\n".join(all_lines)


def _is_aadhaar(text: str, doc_no: str | None) -> bool:
    if doc_no and len(doc_no) == 12:
        return True
    return bool(re.search(r"\baadhaar\b|\baadhar\b|uidai|your aadhaar", text, re.I))


def _looks_like_person_name(line: str) -> bool:
    line = line.strip()
    if not line or HEADER_BLOCKLIST.search(line):
        return False
    words = line.split()
    if not (1 < len(words) <= 4):
        return False
    if not all(re.match(r"^[A-Za-z\.]+$", w) for w in words):
        return False
    if line.isupper() and len(line) > 12:
        return False
    return True


def _extract_name(text: str) -> str | None:
    patterns = [
        r"(?:NAME|FULL NAME|नाम|పేరు|పుట్టిన)[:\s/]+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)+)",
        r"(?:DOB|DATE OF BIRTH)[^\n]{0,40}\n([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m and _looks_like_person_name(m.group(1)):
            return m.group(1).strip()

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    title_case = [
        ln for ln in lines if re.match(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+$", ln)
    ]
    if title_case:
        return title_case[0]

    for ln in lines:
        if _looks_like_person_name(ln):
            return ln

    return None


def _normalize_ocr_date(raw: str) -> str:
    """Fix common OCR digit confusions in dates (I/l -> 1, O -> 0, spaces)."""
    cleaned = raw.strip()
    cleaned = cleaned.replace("I", "1").replace("l", "1").replace("O", "0").replace("o", "0")
    cleaned = re.sub(r"[^\d/\-]", "", cleaned)
    if re.match(r"^\d{8}$", cleaned):
        cleaned = f"{cleaned[:2]}/{cleaned[2:4]}/{cleaned[4:]}"
    return cleaned


def _is_plausible_dob(date_str: str) -> bool:
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", date_str)
    if not m:
        return False
    day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return False
    if not (1920 <= year <= 2026):
        return False
    return True


def _extract_dob(text: str) -> str | None:
    labeled_patterns = [
        r"(?:DOB|DATE OF BIRTH|D\.O\.B|BIRTH DATE)[,\s:/]*([0-9IlOo/\-\s]{8,14})",
        r"(?:పుట్టిన\s*ర[ఎe]?[దd]?[ీi]?)[,\s:/]*([0-9IlOo/\-\s]{8,14})",
    ]
    fallback_patterns = [
        r"(?:Male|Female|Male|Female|పురుష|స్త్రీ)[^\n]{0,30}([0-9IlOo/\-\s]{8,14})",
        r"\b([0-9IlOo]{1,2}[/\-][0-9IlOo]{1,2}[/\-][0-9IlOo]{4})\b",
    ]

    for pattern in labeled_patterns + fallback_patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            candidate = _normalize_ocr_date(m.group(1))
            if _is_plausible_dob(candidate):
                return candidate

    return None


def parse_fields(text: str) -> dict:
    """Extract fields using labeled regexes and Aadhaar-aware heuristics."""
    fields = {"name": None, "dob": None, "doc_no": None, "expiry": None, "doc_type": None}

    m = re.search(r"\b(\d{4}\s*\d{4}\s*\d{4})\b", text)
    if not m:
        m = re.search(r"\b(\d{12})\b", text)
    if m:
        fields["doc_no"] = re.sub(r"\s+", "", m.group(1))

    if _is_aadhaar(text, fields["doc_no"]):
        fields["doc_type"] = "aadhaar"

    fields["name"] = _extract_name(text)
    fields["dob"] = _extract_dob(text)

    expiry_pattern = (
        r"(?:EXPIRY|EXP DATE|VALID UNTIL|VALIDITY|EXPIRES|EXPIRY DATE)"
        r"[:\s]+([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})"
    )
    m = re.search(expiry_pattern, text, re.IGNORECASE)
    if m:
        fields["expiry"] = m.group(1).strip()

    return fields
