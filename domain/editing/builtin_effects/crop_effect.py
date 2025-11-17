"""Crop effect implementation."""
from typing import Dict, Any
import numpy as np
import cv2

from domain.editing.interfaces.effect import IEffect


class CropEffect(IEffect):
    """Crop effect for videos and images."""

    @property
    def name(self) -> str:
        return "crop"

    @property
    def description(self) -> str:
        return "Crops the frame to specified dimensions"

    def get_default_parameters(self) -> Dict[str, Any]:
        return {
            "x": 0,          # Top-left x coordinate
            "y": 0,          # Top-left y coordinate
            "width": None,   # Crop width (None = full width)
            "height": None   # Crop height (None = full height)
        }

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate crop parameters."""
        x = parameters.get("x", 0)
        y = parameters.get("y", 0)
        width = parameters.get("width")
        height = parameters.get("height")

        if not isinstance(x, int) or x < 0:
            return False

        if not isinstance(y, int) or y < 0:
            return False

        if width is not None and (not isinstance(width, int) or width <= 0):
            return False

        if height is not None and (not isinstance(height, int) or height <= 0):
            return False

        return True

    def apply(self, frame: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
        """Apply cropping to the frame."""
        if not self.validate_parameters(parameters):
            raise ValueError("Invalid crop parameters")

        x = parameters.get("x", 0)
        y = parameters.get("y", 0)
        width = parameters.get("width")
        height = parameters.get("height")

        frame_height, frame_width = frame.shape[:2]

        # Use full dimensions if not specified
        if width is None:
            width = frame_width - x
        if height is None:
            height = frame_height - y

        # Ensure crop boundaries are within frame
        x = max(0, min(x, frame_width))
        y = max(0, min(y, frame_height))
        width = min(width, frame_width - x)
        height = min(height, frame_height - y)

        # Crop the frame
        cropped = frame[y:y+height, x:x+width]

        return cropped
