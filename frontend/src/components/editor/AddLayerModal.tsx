import { useState, useEffect } from 'react';
import { Upload } from 'lucide-react';
import { Modal } from '../ui/Modal';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { MediaUploadModal } from './MediaUploadModal';
import { timelineApi, mediaApi } from '../../services/api';
import type { LayerType, AddLayerRequest, MediaAsset } from '../../types';

interface AddLayerModalProps {
  isOpen: boolean;
  onClose: () => void;
  projectId: string;
  onLayerAdded: () => void;
}

export function AddLayerModal({
  isOpen,
  onClose,
  projectId,
  onLayerAdded,
}: AddLayerModalProps) {
  const [layerType, setLayerType] = useState<LayerType>('video');
  const [layerName, setLayerName] = useState('');
  const [startTime, setStartTime] = useState(0);
  const [duration, setDuration] = useState(5);
  const [positionX, setPositionX] = useState(0);
  const [positionY, setPositionY] = useState(0);
  const [zIndex, setZIndex] = useState(0);
  const [opacity, setOpacity] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [mediaAssets, setMediaAssets] = useState<MediaAsset[]>([]);
  const [selectedMediaId, setSelectedMediaId] = useState<string>('');
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [isLoadingMedia, setIsLoadingMedia] = useState(false);

  // Load media assets when modal opens
  useEffect(() => {
    if (isOpen && layerType !== 'text') {
      loadMediaAssets();
    }
  }, [isOpen, layerType]);

  const loadMediaAssets = async () => {
    setIsLoadingMedia(true);
    try {
      const assets = await mediaApi.getAll();
      // Filter by media type
      const filtered = assets.filter(asset => {
        if (layerType === 'video') return asset.media_type === 'video';
        if (layerType === 'image') return asset.media_type === 'image';
        if (layerType === 'audio') return asset.media_type === 'audio';
        return true;
      });
      setMediaAssets(filtered);
    } catch (error) {
      console.error('Failed to load media assets:', error);
    } finally {
      setIsLoadingMedia(false);
    }
  };

  const handleMediaUploaded = async (asset: MediaAsset) => {
    await loadMediaAssets();
    setSelectedMediaId(asset.id);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate media selection for non-text layers
    if (layerType !== 'text' && !selectedMediaId) {
      alert('Please select or upload a media file');
      return;
    }

    setIsSubmitting(true);

    try {
      const request: any = {
        name: layerName || `${layerType} layer`,
        layer_type: layerType,
        start_time: startTime,
        duration,
        position_x: positionX,
        position_y: positionY,
      };

      if (layerType !== 'text') {
        request.media_asset_id = selectedMediaId;
      }

      await timelineApi.addLayer(projectId, request);
      onLayerAdded();
      onClose();

      // Reset form
      setLayerName('');
      setLayerType('video');
      setStartTime(0);
      setDuration(5);
      setPositionX(0);
      setPositionY(0);
      setZIndex(0);
      setOpacity(1);
      setSelectedMediaId('');
    } catch (error) {
      console.error('Failed to add layer:', error);
      alert('Failed to add layer. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} title="Add New Layer">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Layer Name"
            value={layerName}
            onChange={(e) => setLayerName(e.target.value)}
            placeholder={`${layerType} layer`}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Layer Type
            </label>
            <select
              value={layerType}
              onChange={(e) => {
                setLayerType(e.target.value as LayerType);
                setSelectedMediaId('');
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="video">Video</option>
              <option value="image">Image</option>
              <option value="audio">Audio</option>
              <option value="text">Text</option>
            </select>
          </div>

          {layerType !== 'text' && (
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="block text-sm font-medium text-gray-700">
                  Media Asset
                </label>
                <Button
                  type="button"
                  size="sm"
                  variant="ghost"
                  onClick={() => setIsUploadModalOpen(true)}
                  className="text-primary-600"
                >
                  <Upload className="w-4 h-4 mr-1" />
                  Upload New
                </Button>
              </div>

              {isLoadingMedia ? (
                <div className="text-sm text-gray-500 p-3 border border-gray-300 rounded-lg">
                  Loading media assets...
                </div>
              ) : mediaAssets.length === 0 ? (
                <div className="text-sm text-gray-500 p-3 border border-gray-300 rounded-lg">
                  No {layerType} assets available. Upload one to continue.
                </div>
              ) : (
                <select
                  value={selectedMediaId}
                  onChange={(e) => setSelectedMediaId(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  required={layerType !== 'text'}
                >
                  <option value="">Select a media file</option>
                  {mediaAssets.map((asset) => (
                    <option key={asset.id} value={asset.id}>
                      {asset.filename} ({(asset.file_size / 1024 / 1024).toFixed(2)} MB)
                    </option>
                  ))}
                </select>
              )}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Start Time (seconds)"
              type="number"
              value={startTime}
              onChange={(e) => setStartTime(parseFloat(e.target.value))}
              min={0}
              step={0.1}
              required
            />
            <Input
              label="Duration (seconds)"
              type="number"
              value={duration}
              onChange={(e) => setDuration(parseFloat(e.target.value))}
              min={0.1}
              step={0.1}
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Position X"
              type="number"
              value={positionX}
              onChange={(e) => setPositionX(parseFloat(e.target.value))}
            />
            <Input
              label="Position Y"
              type="number"
              value={positionY}
              onChange={(e) => setPositionY(parseFloat(e.target.value))}
            />
          </div>

          <div className="flex justify-end gap-2 pt-4">
            <Button type="button" variant="secondary" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Adding...' : 'Add Layer'}
            </Button>
          </div>
        </form>
      </Modal>

      <MediaUploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onUploadSuccess={handleMediaUploaded}
      />
    </>
  );
}
