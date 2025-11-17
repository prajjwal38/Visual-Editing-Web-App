"""Effect Registry service."""
from typing import Dict, List, Optional

from domain.editing.interfaces.effect import IEffect
from domain.editing.builtin_effects.blur_effect import BlurEffect
from domain.editing.builtin_effects.brightness_effect import BrightnessEffect
from domain.editing.builtin_effects.vintage_filter import VintageFilter
from domain.editing.builtin_effects.sharpen_effect import SharpenEffect
from domain.editing.builtin_effects.crop_effect import CropEffect


class EffectRegistry:
    """Registry for managing available effects.

    Domain service following DDD principles.
    Implements the Registry pattern for effect management.
    Provides extensibility for adding custom effects.
    """

    def __init__(self):
        self._effects: Dict[str, IEffect] = {}
        self._register_builtin_effects()

    def _register_builtin_effects(self) -> None:
        """Register all built-in effects."""
        builtin_effects = [
            BlurEffect(),
            BrightnessEffect(),
            VintageFilter(),
            SharpenEffect(),
            CropEffect()
        ]

        for effect in builtin_effects:
            self.register(effect)

    def register(self, effect: IEffect) -> None:
        """Register a new effect.

        Args:
            effect: Effect instance implementing IEffect

        Raises:
            ValueError: If effect with same name already exists
        """
        if effect.name in self._effects:
            raise ValueError(f"Effect '{effect.name}' is already registered")

        self._effects[effect.name] = effect

    def unregister(self, effect_name: str) -> None:
        """Unregister an effect.

        Args:
            effect_name: Name of the effect to unregister

        Raises:
            ValueError: If effect doesn't exist
        """
        if effect_name not in self._effects:
            raise ValueError(f"Effect '{effect_name}' is not registered")

        del self._effects[effect_name]

    def get_effect(self, effect_name: str) -> Optional[IEffect]:
        """Get an effect by name.

        Args:
            effect_name: Name of the effect

        Returns:
            Effect instance or None if not found
        """
        return self._effects.get(effect_name)

    def get_all_effects(self) -> List[IEffect]:
        """Get all registered effects.

        Returns:
            List of all effect instances
        """
        return list(self._effects.values())

    def get_effect_names(self) -> List[str]:
        """Get names of all registered effects.

        Returns:
            List of effect names
        """
        return list(self._effects.keys())

    def is_registered(self, effect_name: str) -> bool:
        """Check if an effect is registered.

        Args:
            effect_name: Name of the effect

        Returns:
            True if effect is registered, False otherwise
        """
        return effect_name in self._effects

    def get_effect_info(self, effect_name: str) -> Optional[Dict]:
        """Get information about an effect.

        Args:
            effect_name: Name of the effect

        Returns:
            Dictionary with effect info or None if not found
        """
        effect = self.get_effect(effect_name)
        if not effect:
            return None

        return {
            "name": effect.name,
            "description": effect.description,
            "default_parameters": effect.get_default_parameters()
        }

    def __len__(self) -> int:
        """Return number of registered effects."""
        return len(self._effects)
