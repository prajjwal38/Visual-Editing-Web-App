"""Timeline entity."""
from dataclasses import dataclass, field
from typing import List, Optional

from domain.editing.entities.layer import Layer
from domain.editing.value_objects.duration import Duration
from domain.editing.value_objects.resolution import Resolution
from domain.shared.enums import LayerType


@dataclass
class Timeline:
    """Represents a video editing timeline.

    Aggregate root following DDD principles.
    Manages layers and ensures timeline consistency.
    """
    resolution: Resolution
    fps: float = 30.0
    layers: List[Layer] = field(default_factory=list)

    def __post_init__(self):
        """Validate timeline."""
        if self.fps <= 0:
            raise ValueError("FPS must be positive")

    @classmethod
    def create(cls, resolution: Resolution, fps: float = 30.0) -> "Timeline":
        """Factory method to create a timeline."""
        return cls(resolution=resolution, fps=fps)

    def add_layer(self, layer: Layer) -> None:
        """Add a layer to the timeline."""
        if layer in self.layers:
            raise ValueError(f"Layer {layer.id} already exists in timeline")
        self.layers.append(layer)
        self._reorder_layers()

    def remove_layer(self, layer_id: str) -> None:
        """Remove a layer from the timeline."""
        layer = self.find_layer_by_id(layer_id)
        if not layer:
            raise ValueError(f"Layer {layer_id} not found in timeline")
        self.layers.remove(layer)

    def find_layer_by_id(self, layer_id: str) -> Optional[Layer]:
        """Find a layer by ID."""
        for layer in self.layers:
            if layer.id == layer_id:
                return layer
        return None

    def get_layers_by_type(self, layer_type: LayerType) -> List[Layer]:
        """Get all layers of a specific type."""
        return [layer for layer in self.layers if layer.layer_type == layer_type]

    def get_video_layers(self) -> List[Layer]:
        """Get all video layers."""
        return self.get_layers_by_type(LayerType.VIDEO)

    def get_audio_layers(self) -> List[Layer]:
        """Get all audio layers."""
        return self.get_layers_by_type(LayerType.AUDIO)

    def get_layers_at_time(self, time: Duration) -> List[Layer]:
        """Get all active layers at a specific time."""
        return [
            layer for layer in self.layers
            if layer.enabled and layer.start_time <= time < layer.end_time
        ]

    def _reorder_layers(self) -> None:
        """Reorder layers by z-index."""
        self.layers.sort(key=lambda layer: layer.z_index)

    def set_layer_z_index(self, layer_id: str, z_index: int) -> None:
        """Set the z-index of a layer."""
        layer = self.find_layer_by_id(layer_id)
        if not layer:
            raise ValueError(f"Layer {layer_id} not found")
        layer.z_index = z_index
        self._reorder_layers()

    def calculate_total_duration(self) -> Duration:
        """Calculate the total duration of the timeline."""
        if not self.layers:
            return Duration(seconds=0)

        max_end_time = max(layer.end_time for layer in self.layers)
        return max_end_time

    def validate_timeline(self) -> bool:
        """Validate timeline integrity."""
        # Check for duplicate layer IDs
        layer_ids = [layer.id for layer in self.layers]
        if len(layer_ids) != len(set(layer_ids)):
            return False

        # Ensure all layers have valid durations
        for layer in self.layers:
            if layer.duration.seconds <= 0:
                return False

        return True

    def __len__(self) -> int:
        """Return number of layers."""
        return len(self.layers)
