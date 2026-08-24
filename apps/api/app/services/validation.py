import re
from datetime import datetime
from app.schemas.extraction import ExtractedFields

def validate_compliance(fields: ExtractedFields) -> dict:
    """
    Validates extracted artwork data against compliance standards.
    """
    checks = []
    overall_pass = True

    # 1. Product Name Check
    if not fields.product_name:
        checks.append({
            "field": "product_name",
            "status": "FAIL",
            "message": "Product name is missing."
        })
        overall_pass = False
    else:
        checks.append({
            "field": "product_name",
            "status": "PASS",
            "message": f"Product name found: '{fields.product_name}'"
        })

    # 2. Dosage Check
    if not fields.dosage:
        checks.append({
            "field": "dosage",
            "status": "FAIL",
            "message": "Dosage information is missing."
        })
        overall_pass = False
    else:
        # Verify format (e.g. "500 mg", "10 ml")
        if re.match(r"^\d+(?:\.\d+)?\s*(mg|g|ml|mcg)$", fields.dosage, re.IGNORECASE):
            checks.append({
                "field": "dosage",
                "status": "PASS",
                "message": f"Dosage format is valid: '{fields.dosage}'"
            })
        else:
            checks.append({
                "field": "dosage",
                "status": "FAIL",
                "message": f"Dosage format is invalid: '{fields.dosage}'"
            })
            overall_pass = False

    # 3. Batch Number Check
    if not fields.batch_number:
        checks.append({
            "field": "batch_number",
            "status": "FAIL",
            "message": "Batch number is missing."
        })
        overall_pass = False
    else:
        # Check alphanumeric (allow spaces and hyphens)
        if re.match(r"^[A-Za-z0-9-\s]+$", fields.batch_number):
            checks.append({
                "field": "batch_number",
                "status": "PASS",
                "message": f"Batch number is valid: '{fields.batch_number}'"
            })
        else:
            checks.append({
                "field": "batch_number",
                "status": "FAIL",
                "message": f"Batch number has invalid characters: '{fields.batch_number}'"
            })
            overall_pass = False

    # 4. Expiry Date Check
    if not fields.expiry_date:
        checks.append({
            "field": "expiry_date",
            "status": "FAIL",
            "message": "Expiry date is missing."
        })
        overall_pass = False
    else:
        # Verify format (MM/YYYY)
        match = re.match(r"^([0-9]{2})/([0-9]{4})$", fields.expiry_date)
        if match:
            month = int(match.group(1))
            year = int(match.group(2))
            
            if 1 <= month <= 12:
                # Check if expired (relative to current date: Aug 2026)
                current_year = 2026
                current_month = 8
                
                if year < current_year or (year == current_year and month < current_month):
                    checks.append({
                        "field": "expiry_date",
                        "status": "FAIL",
                        "message": f"Product has expired: '{fields.expiry_date}'"
                    })
                    overall_pass = False
                else:
                    checks.append({
                        "field": "expiry_date",
                        "status": "PASS",
                        "message": f"Expiry date is valid and active: '{fields.expiry_date}'"
                    })
            else:
                checks.append({
                    "field": "expiry_date",
                    "status": "FAIL",
                    "message": f"Expiry date month is invalid: '{fields.expiry_date}'"
                })
                overall_pass = False
        else:
            checks.append({
                "field": "expiry_date",
                "status": "FAIL",
                "message": f"Expiry date format should be MM/YYYY: '{fields.expiry_date}'"
            })
            overall_pass = False

    return {
        "status": "PASS" if overall_pass else "FAIL",
        "checks": checks
    }
