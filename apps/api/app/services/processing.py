from pathlib import Path

from app.services.ocr import extract_text, extract_text_from_images
from app.services.pdf import pdf_to_images


def process_submission(submission_id: str) -> str:
    """
    Orchestrates the complete document processing pipeline.
    """

    upload_dir = Path("storage/uploads")
    extracted_dir = Path("storage/extracted")

    supported_extensions = [
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
    ]

    for extension in supported_extensions:
        candidate = upload_dir / f"{submission_id}{extension}"

        if candidate.exists():

            # PDF Processing
            if extension == ".pdf":
                image_output_dir = extracted_dir / submission_id

                image_paths = pdf_to_images(
                    pdf_path=candidate,
                    output_dir=image_output_dir,
                )

                return extract_text_from_images(image_paths)

            # Image Processing
            return extract_text(str(candidate))

    raise FileNotFoundError(
        f"Submission '{submission_id}' not found."
    )
    