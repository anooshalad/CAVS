from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.submissions import router as submissions_router

app = FastAPI(
    title="CAVS API",
    description="Corrective & Automated Verification System",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(submissions_router)

@app.get("/", tags=["System"])
def root():
    return {
        "service": "CAVS API",
        "version": "0.1.0",
        "status": "running",
        "message": "Welcome to the Corrective & Automated Verification System",
    }