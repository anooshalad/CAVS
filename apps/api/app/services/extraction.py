import re
from app.schemas.extraction import ExtractedFields

def extract_product_name(text: str) -> str | None:
    """
    Extract the product name by finding the first prominent line that is not metadata.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    ignore_keywords = {
        "batch", "exp", "expiry", "store", "below", "keep",
        "rx only", "warnings", "manufactured", "licence", "no:", "date", "mg", "ml", "mcg", "g/"
    }
    for line in lines:
        if any(kw in line.lower() for kw in ignore_keywords):
            continue
        # Skip pure numeric or symbol lines
        if re.match(r"^[0-9\s\-\.,/\\°C\(\)]+$", line):
            continue
        return line
    return lines[0] if lines else None

def extract_fields(text: str) -> ExtractedFields:
    batch = re.search(
        r"Batch\s*(?:No\.?|Number|Na|Num|#)?[:\s]*([A-Za-z0-9- \t]+)",
        text,
        re.IGNORECASE,
    )

    expiry = re.search(
        r"(?:EXP|Expiry)[:\s]*([0-9]{2}/[0-9]{4})",
        text,
        re.IGNORECASE,
    )

    dosage = re.search(
        r"([0-9]+(?:\.[0-9]+)?\s*(?:mg|g|ml|mcg))",
        text,
        re.IGNORECASE,
    )

    return ExtractedFields(
        product_name=extract_product_name(text),
        batch_number=batch.group(1).strip() if batch else None,
        expiry_date=expiry.group(1) if expiry else None,
        dosage=dosage.group(1) if dosage else None,
    )