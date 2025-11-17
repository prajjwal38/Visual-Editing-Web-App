"""Add Layer to Timeline use case."""
from domain.editing.repositories.project_repository import IProjectRepository
from domain.editing.entities.layer import Layer
from domain.editing.value_objects.duration import Duration
from domain.editing.value_objects.position import Position
from domain.shared.enums import LayerType
from application.dtos.layer_dto import CreateLayerDTO, LayerDTO


class AddLayerToTimelineUseCase:
    """Use case for adding a layer to a project timeline.

    Application layer - orchestrates domain logic.
    """

    def __init__(self, project_repository: IProjectRepository):
        self.project_repository = project_repository

    async def execute(self, project_id: str, dto: CreateLayerDTO) -> LayerDTO:
        """Execute the use case.

        Args:
            project_id: ID of the project
            dto: Create layer data transfer object

        Returns:
            LayerDTO with created layer information

        Raises:
            ValueError: If project not found or validation fails
        """
        # Load project
        project = await self.project_repository.find_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Create layer entity
        start_time = Duration(seconds=dto.start_time)
        duration = Duration(seconds=dto.duration)
        position = Position(x=dto.position_x, y=dto.position_y)

        if dto.layer_type == LayerType.VIDEO and dto.media_asset_id:
            layer = Layer.create_video_layer(
                name=dto.name,
                media_asset_id=dto.media_asset_id,
                start_time=start_time,
                duration=duration,
                position=position
            )
        elif dto.layer_type == LayerType.IMAGE and dto.media_asset_id:
            layer = Layer.create_image_layer(
                name=dto.name,
                media_asset_id=dto.media_asset_id,
                start_time=start_time,
                duration=duration,
                position=position
            )
        elif dto.layer_type == LayerType.AUDIO and dto.media_asset_id:
            layer = Layer.create_audio_layer(
                name=dto.name,
                media_asset_id=dto.media_asset_id,
                start_time=start_time,
                duration=duration
            )
        else:
            raise ValueError(f"Invalid layer type or missing media asset")

        # Add to timeline
        project.timeline.add_layer(layer)

        # Persist
        await self.project_repository.save(project)

        # Return DTO
        return self._to_dto(layer)

    def _to_dto(self, layer: Layer) -> LayerDTO:
        """Convert Layer entity to DTO."""
        return LayerDTO(
            id=layer.id,
            name=layer.name,
            layer_type=layer.layer_type,
            start_time=layer.start_time.seconds,
            duration=layer.duration.seconds,
            media_asset_id=layer.media_asset_id,
            position_x=layer.position.x,
            position_y=layer.position.y,
            z_index=layer.z_index,
            opacity=layer.opacity,
            enabled=layer.enabled,
            effect_count=len(layer.effects)
        )
