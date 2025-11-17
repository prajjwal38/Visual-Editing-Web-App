"""Apply Effect to Layer use case."""
from domain.editing.repositories.project_repository import IProjectRepository
from domain.editing.entities.effect_instance import EffectInstance
from domain.editing.services.effect_registry import EffectRegistry
from application.dtos.layer_dto import ApplyEffectDTO


class ApplyEffectToLayerUseCase:
    """Use case for applying an effect to a layer.

    Application layer - orchestrates domain logic.
    """

    def __init__(
        self,
        project_repository: IProjectRepository,
        effect_registry: EffectRegistry
    ):
        self.project_repository = project_repository
        self.effect_registry = effect_registry

    async def execute(
        self,
        project_id: str,
        layer_id: str,
        dto: ApplyEffectDTO
    ) -> dict:
        """Execute the use case.

        Args:
            project_id: ID of the project
            layer_id: ID of the layer
            dto: Apply effect data transfer object

        Returns:
            Dictionary with effect instance information

        Raises:
            ValueError: If project, layer, or effect not found
        """
        # Load project
        project = await self.project_repository.find_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Find layer
        layer = project.timeline.find_layer_by_id(layer_id)
        if not layer:
            raise ValueError(f"Layer {layer_id} not found")

        # Validate effect exists
        effect = self.effect_registry.get_effect(dto.effect_name)
        if not effect:
            raise ValueError(f"Effect '{dto.effect_name}' not found")

        # Validate parameters
        if not effect.validate_parameters(dto.parameters):
            raise ValueError(f"Invalid parameters for effect '{dto.effect_name}'")

        # Create and add effect instance
        effect_instance = EffectInstance.create(
            effect_name=dto.effect_name,
            parameters=dto.parameters
        )
        layer.add_effect(effect_instance)

        # Persist
        await self.project_repository.save(project)

        # Return effect info
        return {
            "effect_id": effect_instance.id,
            "effect_name": effect_instance.effect_name,
            "parameters": effect_instance.parameters,
            "enabled": effect_instance.enabled
        }
