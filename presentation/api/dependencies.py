"""Dependency injection for FastAPI."""
from functools import lru_cache

from infrastructure.persistence.in_memory.project_repository_impl import InMemoryProjectRepository
from infrastructure.persistence.in_memory.media_asset_repository_impl import InMemoryMediaAssetRepository
from infrastructure.storage.file_storage_service import FileStorageService
from infrastructure.media_processing.video_processor import VideoProcessor
from infrastructure.media_processing.image_processor import ImageProcessor
from infrastructure.media_processing.ffmpeg_exporter import FFmpegExporter
from domain.editing.services.effect_registry import EffectRegistry

from application.use_cases.project.create_project import CreateProjectUseCase
from application.use_cases.project.get_project import GetProjectUseCase
from application.use_cases.editing.add_layer_to_timeline import AddLayerToTimelineUseCase
from application.use_cases.editing.apply_effect_to_layer import ApplyEffectToLayerUseCase
from application.use_cases.export.export_project import ExportProjectUseCase

# Singleton instances (for MVP - in production, use proper DI container)
_project_repository = InMemoryProjectRepository()
_media_asset_repository = InMemoryMediaAssetRepository()
_file_storage = FileStorageService()
_video_processor = VideoProcessor()
_image_processor = ImageProcessor()
_effect_registry = EffectRegistry()
_ffmpeg_exporter = FFmpegExporter(_media_asset_repository, _effect_registry)


# Repository Dependencies
def get_project_repository():
    """Get project repository instance."""
    return _project_repository


def get_media_asset_repository():
    """Get media asset repository instance."""
    return _media_asset_repository


# Service Dependencies
def get_file_storage():
    """Get file storage service instance."""
    return _file_storage


def get_video_processor():
    """Get video processor instance."""
    return _video_processor


def get_image_processor():
    """Get image processor instance."""
    return _image_processor


def get_effect_registry():
    """Get effect registry instance."""
    return _effect_registry


def get_ffmpeg_exporter():
    """Get FFmpeg exporter instance."""
    return _ffmpeg_exporter


# Use Case Dependencies
def get_create_project_use_case(
    project_repository=None
):
    """Get create project use case."""
    if project_repository is None:
        project_repository = get_project_repository()
    return CreateProjectUseCase(project_repository)


def get_get_project_use_case(
    project_repository=None
):
    """Get project use case."""
    if project_repository is None:
        project_repository = get_project_repository()
    return GetProjectUseCase(project_repository)


def get_add_layer_use_case(
    project_repository=None
):
    """Get add layer to timeline use case."""
    if project_repository is None:
        project_repository = get_project_repository()
    return AddLayerToTimelineUseCase(project_repository)


def get_apply_effect_use_case(
    project_repository=None,
    effect_registry=None
):
    """Get apply effect use case."""
    if project_repository is None:
        project_repository = get_project_repository()
    if effect_registry is None:
        effect_registry = get_effect_registry()
    return ApplyEffectToLayerUseCase(project_repository, effect_registry)


def get_export_project_use_case(
    project_repository=None,
    exporter=None
):
    """Get export project use case."""
    if project_repository is None:
        project_repository = get_project_repository()
    if exporter is None:
        exporter = get_ffmpeg_exporter()
    return ExportProjectUseCase(project_repository, exporter)
