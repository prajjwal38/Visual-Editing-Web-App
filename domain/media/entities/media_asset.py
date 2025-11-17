"""Media Asset entity."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

from domain.shared.enums import MediaType
from domain.editing.value_objects.duration import Duration
from domain.editing.value_objects.resolution import Resolution


@dataclass
class MediaAsset:
    """Represents a media asset (video, image, or audio file).

    Entity following DDD principles - has identity and lifecycle.
    """
    id: str
    name: str
    media_type: MediaType
    file_path: str
    file_size: int  # in bytes
    created_at: datetime = field(default_factory=datetime.utcnow)
    duration: Optional[Duration] = None
    resolution: Optional[Resolution] = None
    thumbnail_path: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Validate media asset."""
        if not self.name:
            raise ValueError("Media asset name cannot be empty")
        if not self.file_path:
            raise ValueError("File path cannot be empty")
        if self.file_size < 0:
            raise ValueError("File size cannot be negative")

    @classmethod
    def create_video(
        cls,
        name: str,
        file_path: str,
        file_size: int,
        duration: Duration,
        resolution: Resolution,
        thumbnail_path: Optional[str] = None
    ) -> "MediaAsset":
        """Factory method to create a video asset."""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            media_type=MediaType.VIDEO,
            file_path=file_path,
            file_size=file_size,
            duration=duration,
            resolution=resolution,
            thumbnail_path=thumbnail_path
        )

    @classmethod
    def create_image(
        cls,
        name: str,
        file_path: str,
        file_size: int,
        resolution: Resolution
    ) -> "MediaAsset":
        """Factory method to create an image asset."""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            media_type=MediaType.IMAGE,
            file_path=file_path,
            file_size=file_size,
            resolution=resolution
        )

    @classmethod
    def create_audio(
        cls,
        name: str,
        file_path: str,
        file_size: int,
        duration: Duration
    ) -> "MediaAsset":
        """Factory method to create an audio asset."""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            media_type=MediaType.AUDIO,
            file_path=file_path,
            file_size=file_size,
            duration=duration
        )

    def update_metadata(self, key: str, value: any) -> None:
        """Update metadata."""
        self.metadata[key] = value

    def is_video(self) -> bool:
        """Check if asset is a video."""
        return self.media_type == MediaType.VIDEO

    def is_image(self) -> bool:
        """Check if asset is an image."""
        return self.media_type == MediaType.IMAGE

    def is_audio(self) -> bool:
        """Check if asset is audio."""
        return self.media_type == MediaType.AUDIO

    def __eq__(self, other) -> bool:
        """Compare by identity."""
        if not isinstance(other, MediaAsset):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash by identity."""
        return hash(self.id)
