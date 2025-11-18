"""Layer entity."""
from dataclasses import dataclass, field
from typing import List, Optional
import uuid

from domain.editing.value_objects.duration import Duration
from domain.editing.value_objects.position import Position
from domain.editing.entities.effect_instance import EffectInstance
from domain.shared.enums import LayerType


@dataclass
class Layer:
    """Represents a layer in the timeline.

    Entity following DDD principles - has identity and lifecycle.
    A layer can contain media (video/image/audio) and effects.
    """
    id: str
    name: str
    layer_type: LayerType
    start_time: Duration
    duration: Duration
    media_asset_id: Optional[str] = None
    position: Position = field(default_factory=Position.origin)
    z_index: int = 0
    opacity: float = 1.0
    effects: List[EffectInstance] = field(default_factory=list)
    enabled: bool = True

    def __post_init__(self):
        """Validate layer."""
        if not self.name:
            raise ValueError("Layer name cannot be empty")
        if not (0.0 <= self.opacity <= 1.0):
            raise ValueError("Opacity must be between 0 and 1")
        if self.duration.seconds <= 0:
            raise ValueError("Duration must be positive")

    @classmethod
    def create_video_layer(
        cls,
        name: str,
        media_asset_id: str,
        start_time: Duration,
        duration: Duration,
        position: Position = None
    ) -> "Layer":
        """Factory method to create a video layer."""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            layer_type=LayerType.VIDEO,
            start_time=start_time,
            duration=duration,
            media_asset_id=media_asset_id,
            position=position or Position.origin()
        )

    @classmethod
    def create_image_layer(
        cls,
        name: str,
        media_asset_id: str,
        start_time: Duration,
        duration: Duration,
        position: Position = None
    ) -> "Layer":
        """Factory method to create an image layer."""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            layer_type=LayerType.IMAGE,
            start_time=start_time,
            duration=duration,
            media_asset_id=media_asset_id,
            position=position or Position.origin()
        )

    @classmethod
    def create_audio_layer(
        cls,
        name: str,
        media_asset_id: str,
        start_time: Duration,
        duration: Duration
    ) -> "Layer":
        """Factory method to create an audio layer."""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            layer_type=LayerType.AUDIO,
            start_time=start_time,
            duration=duration,
            media_asset_id=media_asset_id
        )

    @classmethod
    def create_text_layer(
        cls,
        name: str,
        start_time: Duration,
        duration: Duration,
        position: Position = None
    ) -> "Layer":
        """Factory method to create a text layer."""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            layer_type=LayerType.TEXT,
            start_time=start_time,
            duration=duration,
            media_asset_id=None,
            position=position or Position.origin()
        )

    @property
    def end_time(self) -> Duration:
        """Calculate the end time of the layer."""
        return self.start_time + self.duration

    def add_effect(self, effect: EffectInstance) -> None:
        """Add an effect to the layer."""
        if effect in self.effects:
            raise ValueError(f"Effect {effect.id} already exists on layer")
        self.effects.append(effect)

    def remove_effect(self, effect_id: str) -> None:
        """Remove an effect from the layer."""
        effect = self.find_effect_by_id(effect_id)
        if not effect:
            raise ValueError(f"Effect {effect_id} not found on layer")
        self.effects.remove(effect)

    def find_effect_by_id(self, effect_id: str) -> Optional[EffectInstance]:
        """Find an effect by ID."""
        for effect in self.effects:
            if effect.id == effect_id:
                return effect
        return None

    def set_opacity(self, opacity: float) -> None:
        """Set layer opacity."""
        if not (0.0 <= opacity <= 1.0):
            raise ValueError("Opacity must be between 0 and 1")
        self.opacity = opacity

    def move_to(self, position: Position) -> None:
        """Move layer to a new position."""
        self.position = position

    def trim(self, new_duration: Duration) -> None:
        """Trim the layer to a new duration."""
        if new_duration.seconds <= 0:
            raise ValueError("Duration must be positive")
        self.duration = new_duration

    def enable(self) -> None:
        """Enable the layer."""
        self.enabled = True

    def disable(self) -> None:
        """Disable the layer."""
        self.enabled = False

    def overlaps_with(self, other: "Layer") -> bool:
        """Check if this layer overlaps with another layer in time."""
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)

    def __eq__(self, other) -> bool:
        """Compare by identity."""
        if not isinstance(other, Layer):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash by identity."""
        return hash(self.id)
