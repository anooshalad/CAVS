from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "CAVS API",
        "version": "0.1.0",
        "environment": "development",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }