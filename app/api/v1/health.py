"""Health API"""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", summary="Health check", description="Check if API is running")
async def health_check():
    """Simple health endpoint"""
    return {"status": "ok", "service": "robot-payment-platform"}


@router.get(
    "/detailed", summary="Detailed health", description="Get detailed service status"
)
async def detailed_health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {"api": "running", "database": "connected"},
    }
