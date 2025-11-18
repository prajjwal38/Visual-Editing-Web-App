"""Pydantic schemas for Project API."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from domain.shared.enums import ProjectStatus


class ResolutionSchema(BaseModel):
    """Schema for resolution."""
    width: int = Field(ge=1, le=7680)
    height: int = Field(ge=1, le=4320)


class DurationSchema(BaseModel):
    """Schema for duration."""
    seconds: float = Field(ge=0)


class PositionSchema(BaseModel):
    """Schema for position."""
    x: float
    y: float


class EffectInstanceSchema(BaseModel):
    """Schema for effect instance."""
    effect_name: str
    parameters: dict


class LayerSchema(BaseModel):
    """Schema for layer."""
    id: str
    layer_type: str
    media_asset_id: Optional[str] = None
    start_time: DurationSchema
    duration: DurationSchema
    position: PositionSchema
    z_index: int
    opacity: float = Field(ge=0, le=1)
    is_enabled: bool
    effects: List[EffectInstanceSchema] = []


class TimelineSchema(BaseModel):
    """Schema for timeline."""
    layers: List[LayerSchema] = []
    total_duration: DurationSchema


class ProjectCreateRequest(BaseModel):
    """Request schema for creating a project."""
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=1000)
    resolution: ResolutionSchema = Field(default=ResolutionSchema(width=1920, height=1080))
    fps: float = Field(default=30.0, ge=1.0, le=120.0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Instagram Reel",
                "description": "Fitness motivation reel",
                "resolution": {
                    "width": 1080,
                    "height": 1920
                },
                "fps": 30.0
            }
        }


class ProjectUpdateRequest(BaseModel):
    """Request schema for updating a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class ProjectResponse(BaseModel):
    """Response schema for project."""
    id: str
    name: str
    description: str
    status: ProjectStatus
    resolution: ResolutionSchema
    fps: float
    created_at: datetime
    updated_at: datetime
    timeline: TimelineSchema

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "My Instagram Reel",
                "description": "Fitness motivation reel",
                "status": "draft",
                "resolution": {
                    "width": 1080,
                    "height": 1920
                },
                "fps": 30.0,
                "created_at": "2025-01-15T10:30:00",
                "updated_at": "2025-01-15T10:30:00",
                "timeline": {
                    "layers": [],
                    "total_duration": {
                        "seconds": 0.0
                    }
                }
            }
        }
