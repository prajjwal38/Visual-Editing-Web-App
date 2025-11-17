"""Shared domain enumerations."""
from enum import Enum


class MediaType(str, Enum):
    """Type of media asset."""
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"


class ProjectStatus(str, Enum):
    """Status of a project."""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class LayerType(str, Enum):
    """Type of layer in timeline."""
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"
    TEXT = "text"
    EFFECT = "effect"


class ExportFormat(str, Enum):
    """Supported export formats."""
    MP4 = "mp4"
    MOV = "mov"
    AVI = "avi"
    WEBM = "webm"
    GIF = "gif"


class Resolution(str, Enum):
    """Standard video resolutions."""
    HD_720 = "1280x720"
    FHD_1080 = "1920x1080"
    UHD_4K = "3840x2160"
    INSTAGRAM_SQUARE = "1080x1080"
    INSTAGRAM_STORY = "1080x1920"
    YOUTUBE_SHORT = "1080x1920"
    TIKTOK = "1080x1920"
