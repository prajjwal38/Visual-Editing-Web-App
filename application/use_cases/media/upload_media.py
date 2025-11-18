"""Upload media use case."""
from dataclasses import dataclass
from typing import Optional
import os
import uuid
from pathlib import Path

from domain.media.entities.media_asset import MediaAsset
from domain.media.repositories.media_asset_repository import MediaAssetRepository
from domain.shared.enums import MediaType
from domain.editing.value_objects.duration import Duration
from domain.editing.value_objects.resolution import Resolution


@dataclass
class UploadMediaDTO:
    """DTO for uploading media."""
    filename: str
    content: bytes
    media_type: MediaType
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None


class UploadMediaUseCase:
    """Use case for uploading media assets."""

    def __init__(self, repository: MediaAssetRepository, storage_path: str = "./storage/media"):
        self.repository = repository
        self.storage_path = storage_path
        self._ensure_storage_directory()

    def _ensure_storage_directory(self):
        """Ensure storage directory exists."""
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)
        for subdir in ['videos', 'images', 'audio']:
            Path(os.path.join(self.storage_path, subdir)).mkdir(parents=True, exist_ok=True)

    def _get_storage_subdir(self, media_type: MediaType) -> str:
        """Get storage subdirectory for media type."""
        if media_type == MediaType.VIDEO:
            return 'videos'
        elif media_type == MediaType.IMAGE:
            return 'images'
        elif media_type == MediaType.AUDIO:
            return 'audio'
        else:
            raise ValueError(f"Unknown media type: {media_type}")

    async def execute(self, dto: UploadMediaDTO) -> MediaAsset:
        """Execute media upload.

        Args:
            dto: Upload media data transfer object

        Returns:
            Created media asset

        Raises:
            ValueError: If media data is invalid
        """
        # Generate unique filename
        file_extension = Path(dto.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Determine storage path
        subdir = self._get_storage_subdir(dto.media_type)
        file_path = os.path.join(self.storage_path, subdir, unique_filename)

        # Save file to disk
        with open(file_path, 'wb') as f:
            f.write(dto.content)

        # Create media asset based on type
        if dto.media_type == MediaType.VIDEO:
            if not dto.duration or not dto.width or not dto.height:
                raise ValueError("Video assets require duration and resolution")
            asset = MediaAsset.create_video(
                name=dto.filename,
                file_path=file_path,
                file_size=len(dto.content),
                duration=Duration(seconds=dto.duration),
                resolution=Resolution(width=dto.width, height=dto.height)
            )
        elif dto.media_type == MediaType.IMAGE:
            if not dto.width or not dto.height:
                raise ValueError("Image assets require resolution")
            asset = MediaAsset.create_image(
                name=dto.filename,
                file_path=file_path,
                file_size=len(dto.content),
                resolution=Resolution(width=dto.width, height=dto.height)
            )
        elif dto.media_type == MediaType.AUDIO:
            if not dto.duration:
                raise ValueError("Audio assets require duration")
            asset = MediaAsset.create_audio(
                name=dto.filename,
                file_path=file_path,
                file_size=len(dto.content),
                duration=Duration(seconds=dto.duration)
            )
        else:
            raise ValueError(f"Unsupported media type: {dto.media_type}")

        # Save to repository
        await self.repository.save(asset)

        return asset
