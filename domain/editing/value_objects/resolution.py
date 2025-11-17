"""Resolution value object."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Resolution:
    """Represents video/image resolution.

    Value object following DDD principles - immutable and self-validating.
    """
    width: int
    height: int

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive")

    @property
    def aspect_ratio(self) -> float:
        """Calculate aspect ratio."""
        return self.width / self.height

    @property
    def total_pixels(self) -> int:
        """Calculate total pixel count."""
        return self.width * self.height

    def is_landscape(self) -> bool:
        """Check if resolution is landscape orientation."""
        return self.width > self.height

    def is_portrait(self) -> bool:
        """Check if resolution is portrait orientation."""
        return self.height > self.width

    def is_square(self) -> bool:
        """Check if resolution is square."""
        return self.width == self.height

    @classmethod
    def from_string(cls, resolution_str: str) -> "Resolution":
        """Create resolution from string like '1920x1080'."""
        try:
            width, height = resolution_str.split('x')
            return cls(width=int(width), height=int(height))
        except ValueError:
            raise ValueError(f"Invalid resolution string: {resolution_str}")

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"
