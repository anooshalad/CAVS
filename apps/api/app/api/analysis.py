from fastapi import APIRouter, HTTPException
from app.services.processing import process_submission
from app.services.extraction import extract_fields
from app.services.validation import validate_compliance
from app.schemas.extraction import ExtractedFields

router = APIRouter(
    prefix="/submissions",
    tags=["Analysis"],
)

@router.post("/{submission_id}/analyze")
async def analyze_submission(submission_id: str):
    try:
        # 1. Run OCR (extracts text from image/PDF)
        raw_text = process_submission(submission_id)
        
        # 2. Extract structured fields
        extracted_data = extract_fields(raw_text)
        
        # 3. Run compliance validation
        validation = validate_compliance(extracted_data)
        
        return {
            "submission_id": submission_id,
            "status": validation["status"],
            "extracted_fields": extracted_data,
            "validation_results": validation,
            "raw_text": raw_text
        }

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except Exception as e:
        # Handle exceptions gracefully to prevent server crashes
        raise HTTPException(
            status_code=500,
            detail=f"Analysis pipeline error: {str(e)}",
        )
