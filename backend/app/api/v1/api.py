from fastapi import APIRouter

from app.api.v1.endpoints import auth, photos, comments, upload

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(photos.router, prefix="/photos", tags=["photos"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])


@api_router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
