"""Effects API routes."""
from fastapi import APIRouter, HTTPException, Depends

from presentation.schemas.effect_schema import (
    EffectInfoResponse,
    EffectListResponse,
    ApplyEffectRequest,
    EffectInstanceResponse
)
from presentation.api.dependencies import (
    get_effect_registry,
    get_apply_effect_use_case
)
from application.dtos.layer_dto import ApplyEffectDTO

router = APIRouter(tags=["effects"])


@router.get("/effects", response_model=EffectListResponse)
async def list_effects(
    registry=Depends(get_effect_registry)
):
    """List all available effects.

    Returns a list of all registered effects with their parameters.
    """
    try:
        effects = registry.get_all_effects()

        effect_list = [
            EffectInfoResponse(
                name=effect.name,
                description=effect.description,
                default_parameters=effect.get_default_parameters()
            )
            for effect in effects
        ]

        return EffectListResponse(
            effects=effect_list,
            total=len(effect_list)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/effects/{effect_name}", response_model=EffectInfoResponse)
async def get_effect_info(
    effect_name: str,
    registry=Depends(get_effect_registry)
):
    """Get information about a specific effect.

    Returns effect details including default parameters.
    """
    try:
        info = registry.get_effect_info(effect_name)

        if not info:
            raise HTTPException(status_code=404, detail=f"Effect '{effect_name}' not found")

        return EffectInfoResponse(
            name=info["name"],
            description=info["description"],
            default_parameters=info["default_parameters"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post(
    "/projects/{project_id}/layers/{layer_id}/effects",
    response_model=EffectInstanceResponse,
    status_code=201
)
async def apply_effect_to_layer(
    project_id: str,
    layer_id: str,
    request: ApplyEffectRequest,
    use_case=Depends(get_apply_effect_use_case)
):
    """Apply an effect to a layer.

    Adds an effect to the specified layer with given parameters.
    """
    try:
        dto = ApplyEffectDTO(
            effect_name=request.effect_name,
            parameters=request.parameters
        )

        result = await use_case.execute(project_id, layer_id, dto)

        return EffectInstanceResponse(
            effect_id=result["effect_id"],
            effect_name=result["effect_name"],
            parameters=result["parameters"],
            enabled=result["enabled"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
