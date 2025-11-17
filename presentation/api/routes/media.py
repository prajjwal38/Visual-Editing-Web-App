"""Media API routes (placeholder for MVP)."""
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/media", tags=["media"])


@router.get("/")
async def list_media():
    """List all media assets.

    Note: File upload functionality would be implemented here in full version.
    For MVP, media assets can be added programmatically.
    """
    return {
        "message": "Media upload endpoints will be implemented in full version",
        "note": "For MVP, use the file system directly to add media assets"
    }
