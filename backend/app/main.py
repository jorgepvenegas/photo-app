from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import engine
from app.api.v1.api import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"🚀 Starting {settings.APP_NAME}")
    print(f"   Environment: {'Development' if settings.DEBUG else 'Production'}")
    print(f"   Database: {settings.DATABASE_URL.split('@')[-1]}")
    print(f"   FRONTEND_URL: {settings.FRONTEND_URL}")

    
    # Create tables if they don't exist (for dev)
    # In production, use Alembic migrations
    if settings.DEBUG:
        from app.database import Base
        async with engine.begin() as conn:
            # Don't auto-create in production
            pass
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="A photo sharing application with FastAPI + Vue.js",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "docs": "/docs",
        "api": "/api/v1"
    }


@app.get("/api")
async def api_info():
    """API info endpoint."""
    return {
        "version": "v1",
        "endpoints": {
            "auth": "/api/v1/auth",
            "photos": "/api/v1/photos",
            "comments": "/api/v1/comments",
            "upload": "/api/v1/upload",
            "health": "/api/v1/health"
        }
    }
