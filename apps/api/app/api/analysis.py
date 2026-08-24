import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, File, UploadFile
from app.services.processing import process_submission
from app.services.extraction import extract_fields
from app.services.validation import validate_compliance

router = APIRouter(
    prefix="/submissions",
    tags=["Analysis"],
)

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/{submission_id}/analyze")
async def analyze_submission(submission_id: str, file: UploadFile = File(...)):
    try:
        # 1. Save uploaded file to storage/uploads/{submission_id}.{ext}
        original_name = file.filename or "upload.png"
        ext = Path(original_name).suffix.lower()
        if ext not in {".pdf", ".png", ".jpg", ".jpeg"}:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {ext}. Use PDF, PNG, or JPG.",
            )

        dest = UPLOAD_DIR / f"{submission_id}{ext}"
        contents = await file.read()
        dest.write_bytes(contents)

        # 2. Run OCR (extracts text from saved image/PDF)
        raw_text = process_submission(submission_id)

        # 3. Extract structured fields
        extracted_data = extract_fields(raw_text)

        # 4. Run compliance validation
        validation = validate_compliance(extracted_data)

        return {
            "submission_id": submission_id,
            "status": validation["status"],
            "fields": extracted_data,
            "validation": validation.get("checks", {}),
            "raw_text": raw_text,
        }

    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis pipeline error: {str(e)}",
        )

