"""Main app"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, robots, terminals, health

# Create database tables (only once, when app starts)
Base.metadata.create_all(bind=engine)  # TODO I need to use Alembic

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
