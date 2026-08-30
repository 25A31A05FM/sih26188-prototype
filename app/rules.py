from datetime import datetime


def _is_aadhaar(fields: dict) -> bool:
    if fields.get("doc_type") == "aadhaar":
        return True
    doc_no = fields.get("doc_no") or ""
    return len(doc_no) == 12 and doc_no.isdigit()


def validate_fields(fields: dict):
    reasons = []
    score = 0
    is_aadhaar = _is_aadhaar(fields)

    if not fields.get("name"):
        reasons.append("Missing name")
        score += 15

    if not fields.get("dob"):
        reasons.append("Missing date of birth")
        score += 15

    if not fields.get("doc_no"):
        reasons.append("Missing document number")
        score += 20

    expiry = fields.get("expiry")
    if not expiry and not is_aadhaar:
        reasons.append("Missing expiry date")
        score += 15
    elif not expiry and is_aadhaar:
        pass  # Aadhaar has no expiry date
    else:
        try:
            exp_date = None
            date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%b-%Y", "%d-%B-%Y"]
            for fmt in date_formats:
                try:
                    exp_date = datetime.strptime(expiry.strip(), fmt)
                    break
                except ValueError:
                    continue
            
            if exp_date is None:
                reasons.append("Invalid expiry date format")
                score += 10
            elif exp_date.date() < datetime.now().date():
                reasons.append("Document is expired")
                score += 30
        except Exception:
            reasons.append("Invalid expiry date format")
            score += 10

    return min(score, 100), reasons