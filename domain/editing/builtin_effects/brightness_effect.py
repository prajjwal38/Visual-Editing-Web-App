"""Brightness effect implementation."""
from typing import Dict, Any
import numpy as np
import cv2

from domain.editing.interfaces.effect import IEffect


class BrightnessEffect(IEffect):
    """Brightness adjustment effect for videos and images."""

    @property
    def name(self) -> str:
        return "brightness"

    @property
    def description(self) -> str:
        return "Adjusts the brightness of the frame"

    def get_default_parameters(self) -> Dict[str, Any]:
        return {
            "value": 0  # Range: -100 to 100
        }

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate brightness parameters."""
        value = parameters.get("value", 0)

        if not isinstance(value, (int, float)):
            return False

        if value < -100 or value > 100:
            return False

        return True

    def apply(self, frame: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
        """Apply brightness adjustment to the frame."""
        if not self.validate_parameters(parameters):
            raise ValueError("Invalid brightness parameters")

        value = parameters.get("value", 0)

        # Convert to HSV to adjust value (brightness) channel
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Adjust the V channel
        hsv[:, :, 2] = hsv[:, :, 2] + value
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)

        # Convert back to BGR
        result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        return result
