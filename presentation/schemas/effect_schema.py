"""Pydantic schemas for Effect API."""
from pydantic import BaseModel, Field
from typing import Dict, Any, List


class EffectInfoResponse(BaseModel):
    """Response schema for effect information."""
    name: str
    description: str
    default_parameters: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "blur",
                "description": "Applies Gaussian blur to the frame",
                "default_parameters": {
                    "kernel_size": 15,
                    "sigma": 0
                }
            }
        }


class EffectListResponse(BaseModel):
    """Response schema for list of effects."""
    effects: List[EffectInfoResponse]
    total: int


class ApplyEffectRequest(BaseModel):
    """Request schema for applying an effect."""
    effect_name: str = Field(..., min_length=1)
    parameters: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "effect_name": "blur",
                "parameters": {
                    "kernel_size": 21,
                    "sigma": 0
                }
            }
        }


class EffectInstanceResponse(BaseModel):
    """Response schema for effect instance."""
    effect_id: str
    effect_name: str
    parameters: Dict[str, Any]
    enabled: bool

    class Config:
        json_schema_extra = {
            "example": {
                "effect_id": "123e4567-e89b-12d3-a456-426614174000",
                "effect_name": "blur",
                "parameters": {
                    "kernel_size": 21,
                    "sigma": 0
                },
                "enabled": True
            }
        }
