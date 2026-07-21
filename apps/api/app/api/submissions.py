from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.submission import UploadResponse
from app.services.storage import save_uploaded_file

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
}


@router.post(
    "/artwork",
    response_model=UploadResponse,
)
async def upload_artwork(file: UploadFile = File(...)):
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type.",
        )

    saved = save_uploaded_file(file)

    return UploadResponse(
        submission_id=saved["submission_id"],
        original_filename=file.filename,
        stored_filename=saved["stored_filename"],
        content_type=file.content_type,
        status="uploaded",
    )