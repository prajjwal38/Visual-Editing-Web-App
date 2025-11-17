"""Position value object."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """Represents a 2D position with x and y coordinates.

    Value object following DDD principles - immutable and self-validating.
    Can represent pixels or percentage-based positioning.
    """
    x: float
    y: float

    def __post_init__(self):
        if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
            raise ValueError("Position coordinates must be numeric")

    @classmethod
    def origin(cls) -> "Position":
        """Create position at origin (0, 0)."""
        return cls(x=0.0, y=0.0)

    @classmethod
    def center(cls, width: int, height: int) -> "Position":
        """Create position at center of given dimensions."""
        return cls(x=width / 2.0, y=height / 2.0)

    def translate(self, dx: float, dy: float) -> "Position":
        """Create new position translated by dx, dy."""
        return Position(x=self.x + dx, y=self.y + dy)

    def distance_to(self, other: "Position") -> float:
        """Calculate Euclidean distance to another position."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"
