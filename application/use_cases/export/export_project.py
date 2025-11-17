"""Export Project use case."""
from typing import TYPE_CHECKING

from domain.editing.repositories.project_repository import IProjectRepository
from domain.shared.enums import ExportFormat

if TYPE_CHECKING:
    from infrastructure.media_processing.ffmpeg_exporter import FFmpegExporter


class ExportProjectUseCase:
    """Use case for exporting a project to video.

    Application layer - orchestrates domain logic and infrastructure.
    """

    def __init__(
        self,
        project_repository: IProjectRepository,
        exporter: 'FFmpegExporter'
    ):
        self.project_repository = project_repository
        self.exporter = exporter

    async def execute(
        self,
        project_id: str,
        output_path: str,
        export_format: ExportFormat = ExportFormat.MP4
    ) -> dict:
        """Execute the use case.

        Args:
            project_id: ID of the project to export
            output_path: Path where the exported video will be saved
            export_format: Export format (default: MP4)

        Returns:
            Dictionary with export information

        Raises:
            ValueError: If project not found or export fails
        """
        # Load project
        project = await self.project_repository.find_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Validate timeline has layers
        if len(project.timeline.layers) == 0:
            raise ValueError("Cannot export empty timeline")

        # Export using infrastructure service
        result = await self.exporter.export(
            project=project,
            output_path=output_path,
            export_format=export_format
        )

        # Mark project as completed
        project.mark_completed()
        await self.project_repository.save(project)

        return result
