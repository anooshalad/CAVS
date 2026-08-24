from pathlib import Path

import fitz


def pdf_to_images(pdf_path: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    document = fitz.open(pdf_path)

    image_paths = []

    for page_number in range(len(document)):
        page = document.load_page(page_number)

        pix = page.get_pixmap(dpi=300)

        image_path = output_dir / f"page_{page_number + 1}.png"

        pix.save(image_path)

        image_paths.append(image_path)

    document.close()

    return image_paths