"""Vintage filter effect implementation."""
from typing import Dict, Any
import numpy as np
import cv2

from domain.editing.interfaces.effect import IEffect


class VintageFilter(IEffect):
    """Vintage/sepia tone filter effect for videos and images."""

    @property
    def name(self) -> str:
        return "vintage"

    @property
    def description(self) -> str:
        return "Applies a vintage/sepia tone filter to the frame"

    def get_default_parameters(self) -> Dict[str, Any]:
        return {
            "intensity": 0.7  # Range: 0.0 to 1.0
        }

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate vintage filter parameters."""
        intensity = parameters.get("intensity", 0.7)

        if not isinstance(intensity, (int, float)):
            return False

        if intensity < 0.0 or intensity > 1.0:
            return False

        return True

    def apply(self, frame: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
        """Apply vintage filter to the frame."""
        if not self.validate_parameters(parameters):
            raise ValueError("Invalid vintage filter parameters")

        intensity = parameters.get("intensity", 0.7)

        # Sepia transformation matrix
        sepia_kernel = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ])

        # Apply sepia transformation
        sepia = cv2.transform(frame, sepia_kernel)

        # Blend original and sepia based on intensity
        result = cv2.addWeighted(frame, 1 - intensity, sepia, intensity, 0)

        # Clip values to valid range
        result = np.clip(result, 0, 255).astype(np.uint8)

        return result
