"""Effect interface."""
from abc import ABC, abstractmethod
from typing import Any, Dict
import numpy as np


class IEffect(ABC):
    """Interface for video/image effects.

    Following the Strategy pattern and Open/Closed principle.
    New effects can be added by implementing this interface.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the effect name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Get the effect description."""
        pass

    @abstractmethod
    def get_default_parameters(self) -> Dict[str, Any]:
        """Get default parameters for the effect."""
        pass

    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate effect parameters."""
        pass

    @abstractmethod
    def apply(self, frame: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
        """Apply the effect to a video frame.

        Args:
            frame: Input frame as numpy array (OpenCV format)
            parameters: Effect parameters

        Returns:
            Processed frame as numpy array
        """
        pass

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"
