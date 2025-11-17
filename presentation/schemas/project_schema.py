"""Pydantic schemas for Project API."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from domain.shared.enums import ProjectStatus


class ProjectCreateRequest(BaseModel):
    """Request schema for creating a project."""
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=1000)
    resolution_width: int = Field(default=1920, ge=1, le=7680)
    resolution_height: int = Field(default=1080, ge=1, le=4320)
    fps: float = Field(default=30.0, ge=1.0, le=120.0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Instagram Reel",
                "description": "Fitness motivation reel",
                "resolution_width": 1080,
                "resolution_height": 1920,
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
    resolution_width: int
    resolution_height: int
    fps: float
    created_at: datetime
    updated_at: datetime
    layer_count: int
    total_duration: float

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "My Instagram Reel",
                "description": "Fitness motivation reel",
                "status": "draft",
                "resolution_width": 1080,
                "resolution_height": 1920,
                "fps": 30.0,
                "created_at": "2025-01-15T10:30:00",
                "updated_at": "2025-01-15T10:30:00",
                "layer_count": 0,
                "total_duration": 0.0
            }
        }
