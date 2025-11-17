"""Pydantic schemas for Media API."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from domain.shared.enums import MediaType


class MediaAssetResponse(BaseModel):
    """Response schema for media asset."""
    id: str
    name: str
    media_type: MediaType
    file_path: str
    file_size: int
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "workout_clip.mp4",
                "media_type": "video",
                "file_path": "/storage/media/videos/20250115_103000_abc12345.mp4",
                "file_size": 15728640,
                "duration": 15.5,
                "width": 1920,
                "height": 1080,
                "created_at": "2025-01-15T10:30:00"
            }
        }


class LayerCreateRequest(BaseModel):
    """Request schema for creating a layer."""
    name: str = Field(..., min_length=1, max_length=255)
    layer_type: str = Field(..., pattern="^(video|image|audio)$")
    start_time: float = Field(..., ge=0)
    duration: float = Field(..., gt=0)
    media_asset_id: Optional[str] = None
    position_x: float = Field(default=0.0)
    position_y: float = Field(default=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Main Video",
                "layer_type": "video",
                "start_time": 0.0,
                "duration": 15.5,
                "media_asset_id": "123e4567-e89b-12d3-a456-426614174000",
                "position_x": 0.0,
                "position_y": 0.0
            }
        }


class LayerResponse(BaseModel):
    """Response schema for layer."""
    id: str
    name: str
    layer_type: str
    start_time: float
    duration: float
    media_asset_id: Optional[str]
    position_x: float
    position_y: float
    z_index: int
    opacity: float
    enabled: bool
    effect_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Main Video",
                "layer_type": "video",
                "start_time": 0.0,
                "duration": 15.5,
                "media_asset_id": "123e4567-e89b-12d3-a456-426614174000",
                "position_x": 0.0,
                "position_y": 0.0,
                "z_index": 0,
                "opacity": 1.0,
                "enabled": True,
                "effect_count": 0
            }
        }


class ExportRequest(BaseModel):
    """Request schema for exporting a project."""
    output_filename: str = Field(..., min_length=1)
    format: str = Field(default="mp4", pattern="^(mp4|mov|avi|webm|gif)$")

    class Config:
        json_schema_extra = {
            "example": {
                "output_filename": "my_reel.mp4",
                "format": "mp4"
            }
        }


class ExportResponse(BaseModel):
    """Response schema for export."""
    output_path: str
    format: str
    resolution: str
    fps: float
    layers_exported: int

    class Config:
        json_schema_extra = {
            "example": {
                "output_path": "/storage/exports/my_reel.mp4",
                "format": "mp4",
                "resolution": "1080x1920",
                "fps": 30.0,
                "layers_exported": 3
            }
        }
