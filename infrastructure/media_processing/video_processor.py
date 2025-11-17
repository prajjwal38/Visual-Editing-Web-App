"""Video Processor using FFmpeg."""
import subprocess
from typing import Optional, Tuple
from pathlib import Path


class VideoProcessor:
    """Video processing service using FFmpeg.

    Infrastructure layer - wraps FFmpeg functionality.
    """

    def get_video_info(self, video_path: str) -> dict:
        """Get video information using ffprobe.

        Args:
            video_path: Path to video file

        Returns:
            Dictionary with video info (duration, resolution, fps)

        Raises:
            RuntimeError: If ffprobe fails
        """
        try:
            # Get duration
            duration_cmd = [
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            duration_result = subprocess.run(
                duration_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            duration = float(duration_result.stdout.strip())

            # Get resolution
            resolution_cmd = [
                'ffprobe', '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=s=x:p=0',
                video_path
            ]
            resolution_result = subprocess.run(
                resolution_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            width, height = map(int, resolution_result.stdout.strip().split('x'))

            # Get FPS
            fps_cmd = [
                'ffprobe', '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=r_frame_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            fps_result = subprocess.run(
                fps_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            fps_str = fps_result.stdout.strip()
            if '/' in fps_str:
                num, den = map(int, fps_str.split('/'))
                fps = num / den
            else:
                fps = float(fps_str)

            return {
                'duration': duration,
                'width': width,
                'height': height,
                'fps': fps
            }

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFprobe failed: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"Failed to get video info: {str(e)}")

    def extract_frame(
        self,
        video_path: str,
        output_path: str,
        timestamp: float = 0.0
    ) -> str:
        """Extract a frame from video.

        Args:
            video_path: Path to video file
            output_path: Path for output image
            timestamp: Timestamp in seconds

        Returns:
            Path to extracted frame

        Raises:
            RuntimeError: If frame extraction fails
        """
        try:
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(timestamp),
                '-i', video_path,
                '-vframes', '1',
                '-q:v', '2',
                output_path
            ]

            subprocess.run(cmd, capture_output=True, check=True)
            return output_path

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Frame extraction failed: {e.stderr}")

    def trim_video(
        self,
        input_path: str,
        output_path: str,
        start_time: float,
        duration: float
    ) -> str:
        """Trim video to specified duration.

        Args:
            input_path: Path to input video
            output_path: Path for output video
            start_time: Start time in seconds
            duration: Duration in seconds

        Returns:
            Path to trimmed video

        Raises:
            RuntimeError: If trimming fails
        """
        try:
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(start_time),
                '-t', str(duration),
                '-i', input_path,
                '-c', 'copy',
                output_path
            ]

            subprocess.run(cmd, capture_output=True, check=True)
            return output_path

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Video trimming failed: {e.stderr}")
