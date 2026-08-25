# CAVS — Compliance Artwork Verification System

A lightweight full-stack application for automated artwork compliance verification, focused on pharmaceutical artwork. CAVS processes uploaded PDFs or images, runs OCR, extracts structured fields (eg: product name, dosage, batch number, expiry), and validates them against compliance rules. It also includes a GPT-powered corrective layer that assists in identifying, proposing, and applying corrections to detected artwork compliance violations, followed by automated re-verification.

The project is organized as a monorepo with two main apps:

- apps/api — FastAPI backend that orchestrates file storage, OCR (EasyOCR), PDF rendering (PyMuPDF / fitz), field extraction, validation checks, and corrective workflows.
- apps/web — React + Vite frontend for uploading files and visualizing analysis results.

---

Key features

- Upload PDF or image artwork and run an analysis pipeline that:
  - Converts PDF pages to images (via PyMuPDF)
  - Runs EasyOCR to extract raw text
  - Extracts structured fields (product name, dosage, batch number, expiry date)
  - Runs compliance checks and returns PASS/FAIL with per-field messages
  - Identifies detected artwork compliance violations
  - Generates GPT-powered corrective suggestions for detected violations
  - Applies corrections and re-verifies the resulting artwork
- Simple, clean frontend for uploading and viewing results (live preview + raw OCR text)
- API-first design with FastAPI auto-generated docs (OpenAPI)

---

Architecture

- Frontend (apps/web)
  - React + TypeScript
  - Vite dev server
  - Uploads a file to backend endpoint: POST /submissions/{submission_id}/analyze
  - Reads and displays the structured result and validation checks
  - Displays detected compliance issues and corrective results

- Backend (apps/api)
  - FastAPI application (app.main)
  - API routers: /health, /submissions, /ocr, /submissions/{id}/analyze
  - Services:
    - services/pdf.py — render PDF → PNG images (PyMuPDF / fitz)
    - services/ocr.py — wrapper around EasyOCR (lazy-loaded)
    - services/processing.py — pipeline orchestration
    - services/extraction.py — regex-based field extraction
    - services/validation.py — compliance checks and pass/fail logic
    - services/storage.py — saves uploaded files to storage/uploads and returns submission IDs
    - corrective workflow — generates and applies corrective suggestions using the GPT integration, followed by re-verification

Storage layout (created at runtime)
- storage/uploads — incoming files named {submission_id}.{ext}
- storage/extracted — intermediate extracted images for PDFs (folder per submission)

---

Quickstart (local development)

Prerequisites
- Python 3.10+ (3.11 recommended)
- Node.js 18+ and npm or yarn
- Optional: a GPU and configured EasyOCR dependencies if you want GPU acceleration, otherwise CPU works

Backend (apps/api)

1. Create and activate a virtual environment:

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
````

2. Install the likely required packages (example requirements — adapt versions if needed):

   ```powershell
   pip install fastapi uvicorn[standard] python-multipart easyocr pymupdf openai
   ```

   Notes:

   * python-multipart is required for file uploads with FastAPI.
   * easyocr may require additional system dependencies (OpenCV, Torch). See EasyOCR documentation for platform-specific installation tips.
   * openai is required for the GPT-powered corrective layer.

3. Run the backend locally:

   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Visit the automatic API docs at:

   * Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   * ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Frontend (apps/web)

1. Install dependencies and run dev server:

   ```bash
   cd apps/web
   npm install
   npm run dev
   ```

2. By default the frontend will try to call [http://localhost:8000](http://localhost:8000). To change the API base URL, create a Vite env variable in a .env file:

   ```text
   VITE_API_BASE_URL=http://localhost:8000
   ```

3. Open the dev URL printed by Vite (typically [http://localhost:5173](http://localhost:5173)) and use the UI to upload files and analyze.

---

API Reference (important endpoints)

* GET / — service root (welcome message)

* GET /health — simple health check

* POST /submissions/artwork — upload an artwork file (PDF or image)

  * Request: multipart/form-data with key `file`
  * Response: UploadResponse { submission_id, original_filename, stored_filename, content_type, status }

* POST /submissions/{submission_id}/analyze — upload a file to analyze for a given submission_id

  * This endpoint saves the uploaded file to storage/uploads/{submission_id}.{ext} and runs the full pipeline (OCR → extraction → validation).
  * Response: analysis object with fields, validation checks, raw_text, and overall status (PASS/FAIL).

* POST /ocr/{submission_id} — run OCR for an existing saved submission (returns extracted_text)

* Corrective workflow

  * Uses GPT-powered suggestions to assist with resolving detected artwork compliance violations.
  * Corrected artwork is subsequently re-verified through the compliance validation pipeline.

Example: analyze an artwork from the command line

1. Generate a submission ID (or use one returned by /submissions/artwork). On modern systems you can use uuidgen or generate in the client.

2. Example curl (replace <submission_id> and path/to/artwork.pdf):

```bash
curl -X POST "http://localhost:8000/submissions/<submission_id>/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/artwork.pdf"
```

A successful response looks like:

{
"submission_id": "...",
"status": "PASS",
"fields": {
"product_name": "...",
"dosage": "500 mg",
"batch_number": "B12345",
"expiry_date": "12/2027"
},
"validation": [ ... ],
"raw_text": "..."
}

---

Troubleshooting & Notes

* EasyOCR & PyTorch: EasyOCR depends on PyTorch (torch). If installation fails, follow the official PyTorch installation instructions for your platform and CUDA version (if using GPU). For CPU-only usage, install CPU wheels.
* PDF rendering: The backend uses PyMuPDF (fitz) to render PDF pages to PNG at 300 DPI. Large PDFs will be converted to multiple images and OCR will be invoked for each page.
* Storage: Uploaded files and extracted images are stored under the repository `storage/` folder. Clean up as needed.
* Time-based checks: expiry validation currently compares against a hard-coded date used for deterministic testing. You may want to update validation to use datetime.now() for production.

---

Development

* FastAPI auto-reloads while running with uvicorn --reload.
* The frontend uses Vite for a fast development experience. The frontend expects an API base URL in VITE_API_BASE_URL, falling back to [http://localhost:8000](http://localhost:8000).
* To run the frontend production build:

  cd apps/web
  npm run build
  npm run preview

---

Contributing

Contributions are welcome. A suggested workflow:

1. Fork / branch
2. Create a new feature or fix
3. Run the backend and frontend locally and verify functionality
4. Open a PR with a clear description and screenshots (if applicable)

Please add tests for new behavior where possible and update documentation when adding or changing API endpoints.

---

License

No license file detected in the repository. Add a LICENSE (for example MIT) at the project root to clarify usage and contribution terms.

---

Credits

* Built with FastAPI, EasyOCR, PyMuPDF, React, and OpenAI API.

---
