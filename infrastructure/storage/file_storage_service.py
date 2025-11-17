"""File Storage Service."""
import os
import shutil
from pathlib import Path
from typing import Optional
import hashlib
from datetime import datetime


class FileStorageService:
    """Service for managing file storage.

    Infrastructure layer - handles file system operations.
    """

    def __init__(self, storage_base_path: str = "./storage"):
        """Initialize file storage service.

        Args:
            storage_base_path: Base path for file storage
        """
        self.storage_base_path = Path(storage_base_path)
        self._ensure_storage_directories()

    def _ensure_storage_directories(self) -> None:
        """Ensure storage directories exist."""
        directories = [
            self.storage_base_path / "media" / "videos",
            self.storage_base_path / "media" / "images",
            self.storage_base_path / "media" / "audio",
            self.storage_base_path / "exports",
            self.storage_base_path / "thumbnails"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def save_file(self, source_path: str, category: str) -> str:
        """Save a file to storage.

        Args:
            source_path: Path to the source file
            category: Category (videos/images/audio)

        Returns:
            Path to the saved file

        Raises:
            FileNotFoundError: If source file doesn't exist
            ValueError: If category is invalid
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file not found: {source_path}")

        if category not in ["videos", "images", "audio"]:
            raise ValueError(f"Invalid category: {category}")

        # Generate unique filename
        source_file = Path(source_path)
        file_hash = self._calculate_file_hash(source_path)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{file_hash[:8]}{source_file.suffix}"

        # Destination path
        dest_path = self.storage_base_path / "media" / category / unique_filename

        # Copy file
        shutil.copy2(source_path, dest_path)

        return str(dest_path)

    def delete_file(self, file_path: str) -> bool:
        """Delete a file from storage.

        Args:
            file_path: Path to the file

        Returns:
            True if deleted, False if file doesn't exist
        """
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False

    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes.

        Args:
            file_path: Path to the file

        Returns:
            File size in bytes

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return path.stat().st_size

    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists.

        Args:
            file_path: Path to the file

        Returns:
            True if file exists, False otherwise
        """
        return Path(file_path).exists()

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of a file.

        Args:
            file_path: Path to the file

        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_export_path(self, filename: str) -> str:
        """Get path for export file.

        Args:
            filename: Name of the export file

        Returns:
            Full path to the export file
        """
        return str(self.storage_base_path / "exports" / filename)

    def get_thumbnail_path(self, filename: str) -> str:
        """Get path for thumbnail file.

        Args:
            filename: Name of the thumbnail file

        Returns:
            Full path to the thumbnail file
        """
        return str(self.storage_base_path / "thumbnails" / filename)
