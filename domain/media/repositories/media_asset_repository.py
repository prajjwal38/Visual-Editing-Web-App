"""Media Asset Repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.media.entities.media_asset import MediaAsset
from domain.shared.enums import MediaType


class IMediaAssetRepository(ABC):
    """Repository interface for MediaAsset.

    Following repository pattern from DDD.
    Infrastructure layer will provide concrete implementations.
    """

    @abstractmethod
    async def save(self, asset: MediaAsset) -> MediaAsset:
        """Save a media asset."""
        pass

    @abstractmethod
    async def find_by_id(self, asset_id: str) -> Optional[MediaAsset]:
        """Find a media asset by ID."""
        pass

    @abstractmethod
    async def find_all(self) -> List[MediaAsset]:
        """Find all media assets."""
        pass

    @abstractmethod
    async def find_by_type(self, media_type: MediaType) -> List[MediaAsset]:
        """Find media assets by type."""
        pass

    @abstractmethod
    async def delete(self, asset_id: str) -> bool:
        """Delete a media asset."""
        pass

    @abstractmethod
    async def exists(self, asset_id: str) -> bool:
        """Check if a media asset exists."""
        pass
