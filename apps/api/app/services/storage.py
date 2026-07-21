from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file: UploadFile):
    extension = Path(file.filename).suffix.lower()

    submission_id = str(uuid4())
    stored_filename = f"{submission_id}{extension}"

    destination = UPLOAD_DIR / stored_filename

    with destination.open("wb") as buffer:
        buffer.write(file.file.read())

    return {
        "submission_id": submission_id,
        "stored_filename": stored_filename,
        "destination": destination,
    }