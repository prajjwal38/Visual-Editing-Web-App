"""Duration value object."""
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Duration:
    """Represents a duration of time in seconds.

    Value object following DDD principles - immutable and self-validating.
    """
    seconds: float

    def __post_init__(self):
        if self.seconds < 0:
            raise ValueError("Duration cannot be negative")

    @classmethod
    def from_milliseconds(cls, milliseconds: float) -> "Duration":
        """Create duration from milliseconds."""
        return cls(seconds=milliseconds / 1000.0)

    @classmethod
    def from_frames(cls, frames: int, fps: float = 30.0) -> "Duration":
        """Create duration from frame count and FPS."""
        return cls(seconds=frames / fps)

    def to_milliseconds(self) -> float:
        """Convert to milliseconds."""
        return self.seconds * 1000.0

    def to_frames(self, fps: float = 30.0) -> int:
        """Convert to frame count."""
        return int(self.seconds * fps)

    def __add__(self, other: "Duration") -> "Duration":
        """Add two durations."""
        return Duration(seconds=self.seconds + other.seconds)

    def __sub__(self, other: "Duration") -> "Duration":
        """Subtract two durations."""
        result = self.seconds - other.seconds
        if result < 0:
            raise ValueError("Resulting duration cannot be negative")
        return Duration(seconds=result)

    def __lt__(self, other: "Duration") -> bool:
        return self.seconds < other.seconds

    def __le__(self, other: "Duration") -> bool:
        return self.seconds <= other.seconds

    def __gt__(self, other: "Duration") -> bool:
        return self.seconds > other.seconds

    def __ge__(self, other: "Duration") -> bool:
        return self.seconds >= other.seconds

    def __str__(self) -> str:
        return f"{self.seconds:.2f}s"
