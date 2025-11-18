"""Timeline API routes."""
from fastapi import APIRouter, HTTPException, Depends

from presentation.schemas.media_schema import LayerCreateRequest
from presentation.schemas.project_schema import ProjectResponse, ResolutionSchema, TimelineSchema, LayerSchema, DurationSchema, PositionSchema, EffectInstanceSchema
from presentation.api.dependencies import get_add_layer_use_case, get_project_repository
from application.dtos.layer_dto import CreateLayerDTO
from domain.shared.enums import LayerType

router = APIRouter(prefix="/projects/{project_id}/timeline", tags=["timeline"])


@router.post("/layers", response_model=ProjectResponse, status_code=201)
async def add_layer(
    project_id: str,
    request: LayerCreateRequest,
    use_case=Depends(get_add_layer_use_case),
    repository=Depends(get_project_repository)
):
    """Add a layer to the project timeline.

    Adds a video, image, audio, or text layer to the timeline and returns the updated project.
    """
    try:
        # Convert layer_type string to enum
        layer_type_map = {
            "video": LayerType.VIDEO,
            "image": LayerType.IMAGE,
            "audio": LayerType.AUDIO,
            "text": LayerType.TEXT
        }

        layer_type = layer_type_map.get(request.layer_type.lower())
        if not layer_type:
            raise ValueError(f"Invalid layer type: {request.layer_type}")

        dto = CreateLayerDTO(
            name=request.name,
            layer_type=layer_type,
            start_time=request.start_time,
            duration=request.duration,
            media_asset_id=request.media_asset_id,
            position_x=request.position_x,
            position_y=request.position_y
        )

        await use_case.execute(project_id, dto)

        # Fetch updated project
        project = await repository.find_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        # Build response with layers
        layers = []
        for layer in project.timeline.layers:
            effects = [
                EffectInstanceSchema(
                    effect_name=effect.effect_name,
                    parameters=effect.parameters
                )
                for effect in layer.effects
            ]

            layers.append(LayerSchema(
                id=layer.id,
                layer_type=layer.layer_type.value,
                media_asset_id=layer.media_asset_id,
                start_time=DurationSchema(seconds=layer.start_time.seconds),
                duration=DurationSchema(seconds=layer.duration.seconds),
                position=PositionSchema(x=layer.position.x, y=layer.position.y),
                z_index=layer.z_index,
                opacity=layer.opacity,
                is_enabled=layer.enabled,
                effects=effects
            ))

        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
            resolution=ResolutionSchema(
                width=project.timeline.resolution.width,
                height=project.timeline.resolution.height
            ),
            fps=project.timeline.fps,
            created_at=project.created_at,
            updated_at=project.updated_at,
            timeline=TimelineSchema(
                layers=layers,
                total_duration=DurationSchema(
                    seconds=project.timeline.calculate_total_duration().seconds
                )
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
