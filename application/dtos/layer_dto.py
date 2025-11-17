"""Layer DTOs (Data Transfer Objects)."""
from dataclasses import dataclass
from typing import Optional, Dict, Any

from domain.shared.enums import LayerType


@dataclass
class LayerDTO:
    """Data Transfer Object for Layer."""
    id: str
    name: str
    layer_type: LayerType
    start_time: float  # in seconds
    duration: float    # in seconds
    media_asset_id: Optional[str]
    position_x: float
    position_y: float
    z_index: int
    opacity: float
    enabled: bool
    effect_count: int


@dataclass
class CreateLayerDTO:
    """DTO for creating a layer."""
    name: str
    layer_type: LayerType
    start_time: float
    duration: float
    media_asset_id: Optional[str] = None
    position_x: float = 0.0
    position_y: float = 0.0


@dataclass
class ApplyEffectDTO:
    """DTO for applying an effect to a layer."""
    effect_name: str
    parameters: Dict[str, Any]


@dataclass
class TrimLayerDTO:
    """DTO for trimming a layer."""
    new_duration: float  # in seconds
