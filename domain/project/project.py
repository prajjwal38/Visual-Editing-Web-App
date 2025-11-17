"""Project aggregate root."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

from domain.editing.entities.timeline import Timeline
from domain.editing.value_objects.resolution import Resolution
from domain.shared.enums import ProjectStatus


@dataclass
class Project:
    """Project aggregate root.

    Following DDD aggregate pattern.
    Manages the entire video editing project including timeline.
    """
    id: str
    name: str
    description: str
    timeline: Timeline
    status: ProjectStatus = ProjectStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Validate project."""
        if not self.name:
            raise ValueError("Project name cannot be empty")

    @classmethod
    def create(
        cls,
        name: str,
        description: str = "",
        resolution: Resolution = None,
        fps: float = 30.0
    ) -> "Project":
        """Factory method to create a new project.

        Args:
            name: Project name
            description: Project description
            resolution: Video resolution (defaults to 1920x1080)
            fps: Frames per second

        Returns:
            New project instance
        """
        if resolution is None:
            resolution = Resolution(width=1920, height=1080)

        timeline = Timeline.create(resolution=resolution, fps=fps)

        return cls(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            timeline=timeline,
            status=ProjectStatus.DRAFT
        )

    def update_name(self, name: str) -> None:
        """Update project name."""
        if not name:
            raise ValueError("Project name cannot be empty")
        self.name = name
        self._mark_updated()

    def update_description(self, description: str) -> None:
        """Update project description."""
        self.description = description
        self._mark_updated()

    def mark_in_progress(self) -> None:
        """Mark project as in progress."""
        if self.status == ProjectStatus.ARCHIVED:
            raise ValueError("Cannot modify archived project")
        self.status = ProjectStatus.IN_PROGRESS
        self._mark_updated()

    def mark_completed(self) -> None:
        """Mark project as completed."""
        if self.status == ProjectStatus.ARCHIVED:
            raise ValueError("Cannot modify archived project")
        self.status = ProjectStatus.COMPLETED
        self._mark_updated()

    def archive(self) -> None:
        """Archive the project."""
        self.status = ProjectStatus.ARCHIVED
        self._mark_updated()

    def restore_from_archive(self) -> None:
        """Restore project from archive."""
        if self.status != ProjectStatus.ARCHIVED:
            raise ValueError("Project is not archived")
        self.status = ProjectStatus.DRAFT
        self._mark_updated()

    def update_metadata(self, key: str, value: any) -> None:
        """Update project metadata."""
        self.metadata[key] = value
        self._mark_updated()

    def _mark_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def is_archived(self) -> bool:
        """Check if project is archived."""
        return self.status == ProjectStatus.ARCHIVED

    def is_completed(self) -> bool:
        """Check if project is completed."""
        return self.status == ProjectStatus.COMPLETED

    def __eq__(self, other) -> bool:
        """Compare by identity."""
        if not isinstance(other, Project):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash by identity."""
        return hash(self.id)
