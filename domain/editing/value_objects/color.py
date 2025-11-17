"""Color value object."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Color:
    """Represents a color in RGBA format.

    Value object following DDD principles - immutable and self-validating.
    """
    red: int
    green: int
    blue: int
    alpha: float = 1.0

    def __post_init__(self):
        if not (0 <= self.red <= 255):
            raise ValueError("Red value must be between 0 and 255")
        if not (0 <= self.green <= 255):
            raise ValueError("Green value must be between 0 and 255")
        if not (0 <= self.blue <= 255):
            raise ValueError("Blue value must be between 0 and 255")
        if not (0.0 <= self.alpha <= 1.0):
            raise ValueError("Alpha value must be between 0.0 and 1.0")

    @classmethod
    def from_hex(cls, hex_color: str) -> "Color":
        """Create color from hex string like '#FF5733' or '#FF5733AA'."""
        hex_color = hex_color.lstrip('#')

        if len(hex_color) == 6:
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            return cls(red=r, green=g, blue=b)
        elif len(hex_color) == 8:
            r, g, b, a = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16), int(hex_color[6:8], 16)
            return cls(red=r, green=g, blue=b, alpha=a / 255.0)
        else:
            raise ValueError(f"Invalid hex color: {hex_color}")

    @classmethod
    def black(cls) -> "Color":
        """Create black color."""
        return cls(red=0, green=0, blue=0)

    @classmethod
    def white(cls) -> "Color":
        """Create white color."""
        return cls(red=255, green=255, blue=255)

    @classmethod
    def transparent(cls) -> "Color":
        """Create transparent color."""
        return cls(red=0, green=0, blue=0, alpha=0.0)

    def to_hex(self, include_alpha: bool = False) -> str:
        """Convert to hex string."""
        if include_alpha:
            alpha_hex = format(int(self.alpha * 255), '02x')
            return f"#{self.red:02x}{self.green:02x}{self.blue:02x}{alpha_hex}"
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}"

    def to_rgba_tuple(self) -> tuple:
        """Convert to RGBA tuple."""
        return (self.red, self.green, self.blue, self.alpha)

    def __str__(self) -> str:
        return f"rgba({self.red}, {self.green}, {self.blue}, {self.alpha})"
