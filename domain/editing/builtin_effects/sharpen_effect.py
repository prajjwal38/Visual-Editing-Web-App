"""Sharpen effect implementation."""
from typing import Dict, Any
import numpy as np
import cv2

from domain.editing.interfaces.effect import IEffect


class SharpenEffect(IEffect):
    """Sharpen effect for videos and images."""

    @property
    def name(self) -> str:
        return "sharpen"

    @property
    def description(self) -> str:
        return "Sharpens the frame using unsharp masking"

    def get_default_parameters(self) -> Dict[str, Any]:
        return {
            "amount": 1.0,  # Range: 0.0 to 2.0
            "radius": 1.0   # Range: 0.5 to 5.0
        }

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate sharpen parameters."""
        amount = parameters.get("amount", 1.0)
        radius = parameters.get("radius", 1.0)

        if not isinstance(amount, (int, float)) or amount < 0.0 or amount > 2.0:
            return False

        if not isinstance(radius, (int, float)) or radius < 0.5 or radius > 5.0:
            return False

        return True

    def apply(self, frame: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
        """Apply sharpening to the frame using unsharp masking."""
        if not self.validate_parameters(parameters):
            raise ValueError("Invalid sharpen parameters")

        amount = parameters.get("amount", 1.0)
        radius = parameters.get("radius", 1.0)

        # Create Gaussian blur
        blurred = cv2.GaussianBlur(frame, (0, 0), radius)

        # Unsharp mask: original + amount * (original - blurred)
        sharpened = cv2.addWeighted(frame, 1.0 + amount, blurred, -amount, 0)

        return sharpened
