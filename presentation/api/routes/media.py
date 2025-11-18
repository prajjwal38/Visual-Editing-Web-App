"""Media API routes."""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional

from presentation.schemas.media_schema import MediaAssetResponse, ResolutionSchema, DurationSchema
from presentation.api.dependencies import get_media_asset_repository
from application.use_cases.media.upload_media import UploadMediaUseCase, UploadMediaDTO
from domain.shared.enums import MediaType

router = APIRouter(prefix="/media", tags=["media"])


def get_upload_media_use_case(repository=Depends(get_media_asset_repository)):
    """Get upload media use case."""
    return UploadMediaUseCase(repository)


@router.post("/upload", response_model=MediaAssetResponse, status_code=201)
async def upload_media(
    file: UploadFile = File(...),
    media_type: str = Form(...),
    duration: Optional[float] = Form(None),
    width: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    use_case: UploadMediaUseCase = Depends(get_upload_media_use_case)
):
    """Upload a media file.

    Accepts video, image, or audio files and stores them locally.
    """
    try:
        # Validate media type
        try:
            media_type_enum = MediaType[media_type.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid media type: {media_type}")

        # Read file content
        content = await file.read()

        # Create DTO
        dto = UploadMediaDTO(
            filename=file.filename or "untitled",
            content=content,
            media_type=media_type_enum,
            duration=duration,
            width=width,
            height=height
        )

        # Execute upload
        asset = await use_case.execute(dto)

        # Build response
        response = MediaAssetResponse(
            id=asset.id,
            filename=asset.name,
            media_type=asset.media_type.value,
            file_path=asset.file_path,
            file_size=asset.file_size,
            created_at=asset.created_at
        )

        if asset.duration:
            response.duration = asset.duration.seconds
        if asset.resolution:
            response.resolution = ResolutionSchema(
                width=asset.resolution.width,
                height=asset.resolution.height
            )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/", response_model=List[MediaAssetResponse])
async def list_media(
    repository=Depends(get_media_asset_repository)
):
    """List all media assets."""
    try:
        assets = await repository.find_all()

        return [
            MediaAssetResponse(
                id=asset.id,
                filename=asset.name,
                media_type=asset.media_type.value,
                file_path=asset.file_path,
                file_size=asset.file_size,
                duration=asset.duration.seconds if asset.duration else None,
                resolution=ResolutionSchema(
                    width=asset.resolution.width,
                    height=asset.resolution.height
                ) if asset.resolution else None,
                created_at=asset.created_at
            )
            for asset in assets
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{media_id}", response_model=MediaAssetResponse)
async def get_media(
    media_id: str,
    repository=Depends(get_media_asset_repository)
):
    """Get a media asset by ID."""
    try:
        asset = await repository.find_by_id(media_id)

        if not asset:
            raise HTTPException(status_code=404, detail=f"Media asset {media_id} not found")

        response = MediaAssetResponse(
            id=asset.id,
            filename=asset.name,
            media_type=asset.media_type.value,
            file_path=asset.file_path,
            file_size=asset.file_size,
            created_at=asset.created_at
        )

        if asset.duration:
            response.duration = asset.duration.seconds
        if asset.resolution:
            response.resolution = ResolutionSchema(
                width=asset.resolution.width,
                height=asset.resolution.height
            )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{media_id}", status_code=204)
async def delete_media(
    media_id: str,
    repository=Depends(get_media_asset_repository)
):
    """Delete a media asset."""
    try:
        deleted = await repository.delete(media_id)

        if not deleted:
            raise HTTPException(status_code=404, detail=f"Media asset {media_id} not found")

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
