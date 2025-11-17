"""FFmpeg Exporter for project export."""
import subprocess
from typing import Optional
from pathlib import Path

from domain.project.project import Project
from domain.shared.enums import ExportFormat
from domain.media.repositories.media_asset_repository import IMediaAssetRepository
from domain.editing.services.effect_registry import EffectRegistry


class FFmpegExporter:
    """Service for exporting projects to video using FFmpeg.

    Infrastructure layer - handles video rendering and export.
    """

    def __init__(
        self,
        media_asset_repository: IMediaAssetRepository,
        effect_registry: EffectRegistry
    ):
        self.media_asset_repository = media_asset_repository
        self.effect_registry = effect_registry

    async def export(
        self,
        project: Project,
        output_path: str,
        export_format: ExportFormat = ExportFormat.MP4
    ) -> dict:
        """Export project to video file.

        Args:
            project: Project to export
            output_path: Output file path
            export_format: Export format

        Returns:
            Dictionary with export information

        Raises:
            ValueError: If export fails
        """
        try:
            # For MVP, we'll create a simple concatenation of video layers
            # In a full implementation, this would render each frame with effects
            video_layers = project.timeline.get_video_layers()

            if not video_layers:
                raise ValueError("No video layers to export")

            # Get video paths for all layers
            video_paths = []
            for layer in video_layers:
                if layer.media_asset_id:
                    asset = await self.media_asset_repository.find_by_id(
                        layer.media_asset_id
                    )
                    if asset:
                        video_paths.append(asset.file_path)

            if not video_paths:
                raise ValueError("No video assets found for layers")

            # For MVP: Simple concatenation
            # In production, would render frame-by-frame with effects
            await self._simple_export(
                video_paths,
                output_path,
                project.timeline.resolution.width,
                project.timeline.resolution.height,
                project.timeline.fps,
                export_format
            )

            return {
                'output_path': output_path,
                'format': export_format.value,
                'resolution': f"{project.timeline.resolution.width}x{project.timeline.resolution.height}",
                'fps': project.timeline.fps,
                'layers_exported': len(video_layers)
            }

        except Exception as e:
            raise ValueError(f"Export failed: {str(e)}")

    async def _simple_export(
        self,
        video_paths: list,
        output_path: str,
        width: int,
        height: int,
        fps: float,
        export_format: ExportFormat
    ) -> None:
        """Simple export using FFmpeg concat.

        Args:
            video_paths: List of video file paths
            output_path: Output file path
            width: Output width
            height: Output height
            fps: Output FPS
            export_format: Export format

        Raises:
            RuntimeError: If FFmpeg fails
        """
        try:
            # Create concat file
            concat_file = Path(output_path).parent / "concat_list.txt"
            with open(concat_file, 'w') as f:
                for video_path in video_paths:
                    f.write(f"file '{video_path}'\n")

            # FFmpeg command
            codec_map = {
                ExportFormat.MP4: 'libx264',
                ExportFormat.MOV: 'libx264',
                ExportFormat.AVI: 'libxvid',
                ExportFormat.WEBM: 'libvpx',
                ExportFormat.GIF: 'gif'
            }

            codec = codec_map.get(export_format, 'libx264')

            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-vf', f'scale={width}:{height}',
                '-r', str(fps),
                '-c:v', codec,
                '-preset', 'medium',
                '-crf', '23',
                output_path
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            # Clean up concat file
            concat_file.unlink()

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg export failed: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"Export failed: {str(e)}")
