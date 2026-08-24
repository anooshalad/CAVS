from pathlib import Path

_reader = None

def get_ocr_reader():
    """
    Lazy load and return the EasyOCR Reader instance.
    This prevents startup crashes if EasyOCR initialization fails.
    """
    global _reader
    if _reader is None:
        try:
            import easyocr
            _reader = easyocr.Reader(["en"], gpu=False)
        except Exception as e:
            raise RuntimeError(f"EasyOCR initialization failed: {str(e)}")
    return _reader


def extract_text(image_path: str) -> str:
    """
    Extract text from one image.
    """
    try:
        reader = get_ocr_reader()
        result = reader.readtext(image_path, detail=0)
        return "\n".join(result)
    except Exception as e:
        # Handle OCR failure gracefully as requested by requirements
        raise RuntimeError(f"OCR processing failed: {str(e)}")


def extract_text_from_images(image_paths: list[Path]) -> str:
    """
    Extract text from multiple images.
    """
    pages = []

    for image in image_paths:
        pages.append(extract_text(str(image)))

    return "\n\n".join(pages)