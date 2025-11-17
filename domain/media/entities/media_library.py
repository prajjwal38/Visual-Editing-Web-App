"""Media Library entity."""
from dataclasses import dataclass, field
from typing import List, Optional
import uuid

from domain.media.entities.media_asset import MediaAsset
from domain.shared.enums import MediaType


@dataclass
class MediaLibrary:
    """Represents a collection of media assets.

    Aggregate following DDD principles.
    """
    id: str
    name: str
    assets: List[MediaAsset] = field(default_factory=list)

    def __post_init__(self):
        """Validate media library."""
        if not self.name:
            raise ValueError("Media library name cannot be empty")

    @classmethod
    def create(cls, name: str) -> "MediaLibrary":
        """Factory method to create a media library."""
        return cls(
            id=str(uuid.uuid4()),
            name=name
        )

    def add_asset(self, asset: MediaAsset) -> None:
        """Add a media asset to the library."""
        if asset in self.assets:
            raise ValueError(f"Asset {asset.id} already exists in library")
        self.assets.append(asset)

    def remove_asset(self, asset_id: str) -> None:
        """Remove a media asset from the library."""
        asset = self.find_asset_by_id(asset_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found in library")
        self.assets.remove(asset)

    def find_asset_by_id(self, asset_id: str) -> Optional[MediaAsset]:
        """Find an asset by ID."""
        for asset in self.assets:
            if asset.id == asset_id:
                return asset
        return None

    def get_assets_by_type(self, media_type: MediaType) -> List[MediaAsset]:
        """Get all assets of a specific type."""
        return [asset for asset in self.assets if asset.media_type == media_type]

    def get_total_size(self) -> int:
        """Calculate total size of all assets in bytes."""
        return sum(asset.file_size for asset in self.assets)

    def __len__(self) -> int:
        """Return number of assets."""
        return len(self.assets)
