"""In-memory implementation of Media Asset Repository."""
from typing import Dict, List, Optional
import copy

from domain.media.entities.media_asset import MediaAsset
from domain.media.repositories.media_asset_repository import IMediaAssetRepository
from domain.shared.enums import MediaType


class InMemoryMediaAssetRepository(IMediaAssetRepository):
    """In-memory implementation of IMediaAssetRepository.

    Infrastructure layer - concrete implementation.
    Suitable for MVP, testing, and development.
    """

    def __init__(self):
        self._storage: Dict[str, MediaAsset] = {}

    async def save(self, asset: MediaAsset) -> MediaAsset:
        """Save a media asset.

        Args:
            asset: Media asset to save

        Returns:
            Saved media asset
        """
        self._storage[asset.id] = copy.deepcopy(asset)
        return copy.deepcopy(asset)

    async def find_by_id(self, asset_id: str) -> Optional[MediaAsset]:
        """Find a media asset by ID.

        Args:
            asset_id: ID of the media asset

        Returns:
            Media asset or None if not found
        """
        asset = self._storage.get(asset_id)
        if asset:
            return copy.deepcopy(asset)
        return None

    async def find_all(self) -> List[MediaAsset]:
        """Find all media assets.

        Returns:
            List of all media assets
        """
        return [copy.deepcopy(asset) for asset in self._storage.values()]

    async def find_by_type(self, media_type: MediaType) -> List[MediaAsset]:
        """Find media assets by type.

        Args:
            media_type: Type of media

        Returns:
            List of media assets of the specified type
        """
        return [
            copy.deepcopy(asset)
            for asset in self._storage.values()
            if asset.media_type == media_type
        ]

    async def delete(self, asset_id: str) -> bool:
        """Delete a media asset.

        Args:
            asset_id: ID of the media asset to delete

        Returns:
            True if deleted, False if not found
        """
        if asset_id in self._storage:
            del self._storage[asset_id]
            return True
        return False

    async def exists(self, asset_id: str) -> bool:
        """Check if a media asset exists.

        Args:
            asset_id: ID of the media asset

        Returns:
            True if exists, False otherwise
        """
        return asset_id in self._storage

    def clear(self) -> None:
        """Clear all media assets (useful for testing)."""
        self._storage.clear()
