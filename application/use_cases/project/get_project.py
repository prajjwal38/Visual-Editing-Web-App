"""Get Project use case."""
from typing import Optional

from domain.project.project import Project
from domain.editing.repositories.project_repository import IProjectRepository
from application.dtos.project_dto import ProjectDTO


class GetProjectUseCase:
    """Use case for retrieving a project.

    Application layer - orchestrates domain logic.
    """

    def __init__(self, project_repository: IProjectRepository):
        self.project_repository = project_repository

    async def execute(self, project_id: str) -> Optional[ProjectDTO]:
        """Execute the use case.

        Args:
            project_id: ID of the project to retrieve

        Returns:
            ProjectDTO or None if not found
        """
        project = await self.project_repository.find_by_id(project_id)

        if not project:
            return None

        return self._to_dto(project)

    def _to_dto(self, project: Project) -> ProjectDTO:
        """Convert Project entity to DTO."""
        return ProjectDTO(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
            resolution_width=project.timeline.resolution.width,
            resolution_height=project.timeline.resolution.height,
            fps=project.timeline.fps,
            created_at=project.created_at,
            updated_at=project.updated_at,
            layer_count=len(project.timeline.layers),
            total_duration=project.timeline.calculate_total_duration().seconds
        )
