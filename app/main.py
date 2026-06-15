"""Main app"""

from pathlib import Path

from fastapi import FastAPI  # type: ignore[import]
from starlette.middleware.cors import CORSMiddleware  # type: ignore

from app.api.v1 import auth, health, robots, terminals
from app.core.config import settings

from app.core.logging_config import setup_logging

Path("logs").mkdir(exist_ok=True)
setup_logging()

app = FastAPI(
    title=settings.app_name,
    description="Payment Terminal Testing Platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(robots.router, prefix="/api/v1")
app.include_router(terminals.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Main Endpoint"""
    return {
        "message": "Robot Payment Testing Platform",
        "status": "running",
        "version": "2.0.0",
        "docs": "/docs",
    }


# Simple health endpoint
@app.get("/health", tags=["Root"])
async def simple_health():
    """Healthcheck"""
    return {"status": "ok"}
