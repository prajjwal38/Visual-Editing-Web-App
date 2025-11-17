"""Effect Instance entity."""
from dataclasses import dataclass, field
from typing import Dict, Any, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from domain.editing.interfaces.effect import IEffect


@dataclass
class EffectInstance:
    """Represents an instance of an effect applied to a layer.

    Entity following DDD principles - has identity.
    Separates the effect definition (IEffect) from its application (EffectInstance).
    """
    id: str
    effect_name: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True

    def __post_init__(self):
        """Validate effect instance."""
        if not self.effect_name:
            raise ValueError("Effect name cannot be empty")

    @classmethod
    def create(cls, effect_name: str, parameters: Dict[str, Any] = None) -> "EffectInstance":
        """Factory method to create an effect instance."""
        return cls(
            id=str(uuid.uuid4()),
            effect_name=effect_name,
            parameters=parameters or {}
        )

    def set_parameter(self, key: str, value: Any) -> None:
        """Set an effect parameter."""
        self.parameters[key] = value

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get an effect parameter."""
        return self.parameters.get(key, default)

    def enable(self) -> None:
        """Enable the effect."""
        self.enabled = True

    def disable(self) -> None:
        """Disable the effect."""
        self.enabled = False

    def toggle(self) -> None:
        """Toggle the effect enabled state."""
        self.enabled = not self.enabled

    def __eq__(self, other) -> bool:
        """Compare by identity."""
        if not isinstance(other, EffectInstance):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash by identity."""
        return hash(self.id)
