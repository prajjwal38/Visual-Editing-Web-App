"""Project DTOs (Data Transfer Objects)."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.shared.enums import ProjectStatus


@dataclass
class ProjectDTO:
    """Data Transfer Object for Project."""
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
    total_duration: float  # in seconds


@dataclass
class CreateProjectDTO:
    """DTO for creating a project."""
    name: str
    description: str = ""
    resolution_width: int = 1920
    resolution_height: int = 1080
    fps: float = 30.0


@dataclass
class UpdateProjectDTO:
    """DTO for updating a project."""
    name: Optional[str] = None
    description: Optional[str] = None
