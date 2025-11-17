import { useState } from 'react';
import { Modal } from '../ui/Modal';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { timelineApi } from '../../services/api';
import type { LayerType, AddLayerRequest } from '../../types';

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
  const [startTime, setStartTime] = useState(0);
  const [duration, setDuration] = useState(5);
  const [positionX, setPositionX] = useState(0);
  const [positionY, setPositionY] = useState(0);
  const [zIndex, setZIndex] = useState(0);
  const [opacity, setOpacity] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const request: AddLayerRequest = {
        layer_type: layerType,
        start_time: startTime,
        duration,
        position: { x: positionX, y: positionY },
        z_index: zIndex,
        opacity,
      };

      await timelineApi.addLayer(projectId, request);
      onLayerAdded();
      onClose();

      // Reset form
      setLayerType('video');
      setStartTime(0);
      setDuration(5);
      setPositionX(0);
      setPositionY(0);
      setZIndex(0);
      setOpacity(1);
    } catch (error) {
      console.error('Failed to add layer:', error);
      alert('Failed to add layer. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Add New Layer">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Layer Type
          </label>
          <select
            value={layerType}
            onChange={(e) => setLayerType(e.target.value as LayerType)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="video">Video</option>
            <option value="image">Image</option>
            <option value="audio">Audio</option>
            <option value="text">Text</option>
          </select>
        </div>

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
            onChange={(e) => setPositionX(parseInt(e.target.value))}
          />
          <Input
            label="Position Y"
            type="number"
            value={positionY}
            onChange={(e) => setPositionY(parseInt(e.target.value))}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Z-Index"
            type="number"
            value={zIndex}
            onChange={(e) => setZIndex(parseInt(e.target.value))}
          />
          <Input
            label="Opacity"
            type="number"
            value={opacity}
            onChange={(e) => setOpacity(parseFloat(e.target.value))}
            min={0}
            max={1}
            step={0.1}
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
  );
}
