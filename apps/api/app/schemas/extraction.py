from pydantic import BaseModel

class ExtractedFields(BaseModel):
    product_name: str| None = None
    dosage: str | None = None
    batch_number:str | None = None
    expiry_date : str | None = None