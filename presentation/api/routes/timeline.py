"""Timeline API routes."""
from fastapi import APIRouter, HTTPException, Depends

from presentation.schemas.media_schema import LayerCreateRequest, LayerResponse
from presentation.api.dependencies import get_add_layer_use_case
from application.dtos.layer_dto import CreateLayerDTO
from domain.shared.enums import LayerType

router = APIRouter(prefix="/projects/{project_id}/timeline", tags=["timeline"])


@router.post("/layers", response_model=LayerResponse, status_code=201)
async def add_layer(
    project_id: str,
    request: LayerCreateRequest,
    use_case=Depends(get_add_layer_use_case)
):
    """Add a layer to the project timeline.

    Adds a video, image, or audio layer to the timeline.
    """
    try:
        # Convert layer_type string to enum
        layer_type_map = {
            "video": LayerType.VIDEO,
            "image": LayerType.IMAGE,
            "audio": LayerType.AUDIO
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

        result = await use_case.execute(project_id, dto)

        return LayerResponse(
            id=result.id,
            name=result.name,
            layer_type=result.layer_type.value,
            start_time=result.start_time,
            duration=result.duration,
            media_asset_id=result.media_asset_id,
            position_x=result.position_x,
            position_y=result.position_y,
            z_index=result.z_index,
            opacity=result.opacity,
            enabled=result.enabled,
            effect_count=result.effect_count
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
