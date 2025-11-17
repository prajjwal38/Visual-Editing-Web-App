"""Blur effect implementation."""
from typing import Dict, Any
import numpy as np
import cv2

from domain.editing.interfaces.effect import IEffect


class BlurEffect(IEffect):
    """Gaussian blur effect for videos and images."""

    @property
    def name(self) -> str:
        return "blur"

    @property
    def description(self) -> str:
        return "Applies Gaussian blur to the frame"

    def get_default_parameters(self) -> Dict[str, Any]:
        return {
            "kernel_size": 15,  # Must be odd number
            "sigma": 0  # Auto-calculated if 0
        }

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate blur parameters."""
        kernel_size = parameters.get("kernel_size", 15)
        sigma = parameters.get("sigma", 0)

        if not isinstance(kernel_size, int) or kernel_size < 1:
            return False

        if kernel_size % 2 == 0:
            return False  # Must be odd

        if not isinstance(sigma, (int, float)) or sigma < 0:
            return False

        return True

    def apply(self, frame: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
        """Apply Gaussian blur to the frame."""
        if not self.validate_parameters(parameters):
            raise ValueError("Invalid blur parameters")

        kernel_size = parameters.get("kernel_size", 15)
        sigma = parameters.get("sigma", 0)

        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1

        blurred = cv2.GaussianBlur(
            frame,
            (kernel_size, kernel_size),
            sigma
        )

        return blurred
