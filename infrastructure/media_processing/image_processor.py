"""Image Processor using OpenCV."""
import cv2
import numpy as np
from typing import Tuple, Optional


class ImageProcessor:
    """Image processing service using OpenCV.

    Infrastructure layer - wraps OpenCV functionality.
    """

    def get_image_info(self, image_path: str) -> dict:
        """Get image information.

        Args:
            image_path: Path to image file

        Returns:
            Dictionary with image info (width, height, channels)

        Raises:
            RuntimeError: If image cannot be read
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise RuntimeError(f"Failed to read image: {image_path}")

            height, width, channels = image.shape

            return {
                'width': width,
                'height': height,
                'channels': channels
            }

        except Exception as e:
            raise RuntimeError(f"Failed to get image info: {str(e)}")

    def resize_image(
        self,
        image_path: str,
        output_path: str,
        width: int,
        height: int,
        keep_aspect_ratio: bool = True
    ) -> str:
        """Resize an image.

        Args:
            image_path: Path to input image
            output_path: Path for output image
            width: Target width
            height: Target height
            keep_aspect_ratio: Whether to maintain aspect ratio

        Returns:
            Path to resized image

        Raises:
            RuntimeError: If resize fails
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise RuntimeError(f"Failed to read image: {image_path}")

            if keep_aspect_ratio:
                h, w = image.shape[:2]
                aspect = w / h
                target_aspect = width / height

                if aspect > target_aspect:
                    # Width is limiting factor
                    new_width = width
                    new_height = int(width / aspect)
                else:
                    # Height is limiting factor
                    new_height = height
                    new_width = int(height * aspect)

                resized = cv2.resize(image, (new_width, new_height))
            else:
                resized = cv2.resize(image, (width, height))

            cv2.imwrite(output_path, resized)
            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to resize image: {str(e)}")

    def create_thumbnail(
        self,
        image_path: str,
        output_path: str,
        max_size: int = 200
    ) -> str:
        """Create a thumbnail of an image.

        Args:
            image_path: Path to input image
            output_path: Path for thumbnail
            max_size: Maximum dimension size

        Returns:
            Path to thumbnail

        Raises:
            RuntimeError: If thumbnail creation fails
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise RuntimeError(f"Failed to read image: {image_path}")

            h, w = image.shape[:2]
            if h > w:
                new_height = max_size
                new_width = int(w * (max_size / h))
            else:
                new_width = max_size
                new_height = int(h * (max_size / w))

            thumbnail = cv2.resize(image, (new_width, new_height))
            cv2.imwrite(output_path, thumbnail)
            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to create thumbnail: {str(e)}")

    def apply_effect(
        self,
        image: np.ndarray,
        effect_func,
        parameters: dict
    ) -> np.ndarray:
        """Apply an effect to an image.

        Args:
            image: Input image as numpy array
            effect_func: Effect function to apply
            parameters: Effect parameters

        Returns:
            Processed image

        Raises:
            RuntimeError: If effect application fails
        """
        try:
            return effect_func.apply(image, parameters)
        except Exception as e:
            raise RuntimeError(f"Failed to apply effect: {str(e)}")
