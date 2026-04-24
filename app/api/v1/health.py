"""Route to check health"""

from fastapi import APIRouter  # type: ignore[reportMissingImports]  # pylint: disable=import-error

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health():
    """Healthcheck"""
    return {"status": "ok"}
