import { useState, useRef } from 'react';
import { Modal } from '../ui/Modal';
import { Button } from '../ui/Button';
import { mediaApi } from '../../services/api';
import type { MediaAsset } from '../../types';

interface MediaUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess: (asset: MediaAsset) => void;
}

export function MediaUploadModal({ isOpen, onClose, onUploadSuccess }: MediaUploadModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const detectMediaType = (file: File): string => {
    if (file.type.startsWith('video/')) return 'video';
    if (file.type.startsWith('image/')) return 'image';
    if (file.type.startsWith('audio/')) return 'audio';
    return 'image'; // default
  };

  const getMediaMetadata = (file: File): Promise<{ duration?: number; width?: number; height?: number }> => {
    return new Promise((resolve) => {
      const mediaType = detectMediaType(file);

      if (mediaType === 'video') {
        const video = document.createElement('video');
        video.preload = 'metadata';
        video.onloadedmetadata = () => {
          window.URL.revokeObjectURL(video.src);
          resolve({
            duration: video.duration,
            width: video.videoWidth,
            height: video.videoHeight,
          });
        };
        video.onerror = () => {
          resolve({ duration: 0, width: 640, height: 480 });
        };
        video.src = URL.createObjectURL(file);
      } else if (mediaType === 'image') {
        const img = new Image();
        img.onload = () => {
          window.URL.revokeObjectURL(img.src);
          resolve({
            width: img.width,
            height: img.height,
          });
        };
        img.onerror = () => {
          resolve({ width: 640, height: 480 });
        };
        img.src = URL.createObjectURL(file);
      } else if (mediaType === 'audio') {
        const audio = document.createElement('audio');
        audio.preload = 'metadata';
        audio.onloadedmetadata = () => {
          window.URL.revokeObjectURL(audio.src);
          resolve({
            duration: audio.duration,
          });
        };
        audio.onerror = () => {
          resolve({ duration: 0 });
        };
        audio.src = URL.createObjectURL(file);
      } else {
        resolve({});
      }
    });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      const mediaType = detectMediaType(file);
      const metadata = await getMediaMetadata(file);

      const asset = await mediaApi.upload(file, mediaType, metadata);
      onUploadSuccess(asset);
      onClose();
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      console.error('Upload failed:', err);
      setError(err instanceof Error ? err.message : 'Failed to upload file');
    } finally {
      setIsUploading(false);
    }
  };

  const handleClose = () => {
    if (!isUploading) {
      setFile(null);
      setError(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      onClose();
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Upload Media">
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select File
          </label>
          <input
            ref={fileInputRef}
            type="file"
            accept="video/*,image/*,audio/*"
            onChange={handleFileChange}
            disabled={isUploading}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
          />
        </div>

        {file && (
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-700">
              <span className="font-medium">File:</span> {file.name}
            </p>
            <p className="text-sm text-gray-700">
              <span className="font-medium">Size:</span> {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
            <p className="text-sm text-gray-700">
              <span className="font-medium">Type:</span> {detectMediaType(file)}
            </p>
          </div>
        )}

        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <div className="flex justify-end gap-2 pt-4">
          <Button
            type="button"
            variant="secondary"
            onClick={handleClose}
            disabled={isUploading}
          >
            Cancel
          </Button>
          <Button
            type="button"
            onClick={handleUpload}
            disabled={!file || isUploading}
          >
            {isUploading ? 'Uploading...' : 'Upload'}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
