from fastapi import APIRouter, HTTPException

from app.services.processing import process_submission

router = APIRouter(
    prefix="/ocr",
    tags=["OCR"],
)


@router.post("/{submission_id}")
async def run_ocr(submission_id: str):
    try:
        extracted_text = process_submission(submission_id)

        return {
            "submission_id": submission_id,
            "status": "completed",
            "extracted_text": extracted_text,
        }

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )