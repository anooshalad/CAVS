from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.submissions import router as submissions_router
from app.api.ocr import router as ocr_router
from app.api.analysis import router as analysis_router


app = FastAPI(
    title="CAVS API",
    description="Corrective & Automated Verification System",
    version="0.1.0",
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(submissions_router)
app.include_router(ocr_router)
app.include_router(analysis_router)


@app.get("/", tags=["System"])
def root():
    return {
        "service": "CAVS API",
        "version": "0.1.0",
        "status": "running",
        "message": "Welcome to the Corrective & Automated Verification System",
    }