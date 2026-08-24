from pydantic import BaseModel


class UploadResponse(BaseModel):
    submission_id: str
    original_filename: str
    stored_filename: str
    content_type: str
    status: str