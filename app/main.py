"""Entrypoint Mainfile"""

from fastapi import FastAPI  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, robots, terminals, health


# Create database tables (only once, when app starts)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(robots.router, prefix="/api/v1")
app.include_router(terminals.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")


@app.get("/")
def root():
    """Main Endpoint"""
    return {"message": "Robot Payment Testing Platform", "status": "running"}


@app.get("/health")
def simple_health():
    """Healthcheck"""
    return {"status": "ok"}
