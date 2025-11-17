"""Create Project use case."""
from domain.project.project import Project
from domain.editing.value_objects.resolution import Resolution
from domain.editing.repositories.project_repository import IProjectRepository
from application.dtos.project_dto import CreateProjectDTO, ProjectDTO


class CreateProjectUseCase:
    """Use case for creating a new project.

    Application layer - orchestrates domain logic.
    """

    def __init__(self, project_repository: IProjectRepository):
        self.project_repository = project_repository

    async def execute(self, dto: CreateProjectDTO) -> ProjectDTO:
        """Execute the use case.

        Args:
            dto: Create project data transfer object

        Returns:
            ProjectDTO with created project information

        Raises:
            ValueError: If validation fails
        """
        # Create domain entities
        resolution = Resolution(
            width=dto.resolution_width,
            height=dto.resolution_height
        )

        project = Project.create(
            name=dto.name,
            description=dto.description,
            resolution=resolution,
            fps=dto.fps
        )

        # Persist
        saved_project = await self.project_repository.save(project)

        # Return DTO
        return self._to_dto(saved_project)

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
