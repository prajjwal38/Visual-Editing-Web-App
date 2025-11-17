import { useState } from 'react';
import { Modal } from '../ui/Modal';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { projectsApi } from '../../services/api';
import { useStore } from '../../store/useStore';
import type { Resolution } from '../../types';

interface CreateProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const PRESET_RESOLUTIONS: { name: string; resolution: Resolution }[] = [
  { name: 'HD 720p', resolution: { width: 1280, height: 720 } },
  { name: 'Full HD 1080p', resolution: { width: 1920, height: 1080 } },
  { name: '4K UHD', resolution: { width: 3840, height: 2160 } },
  { name: 'Instagram Story', resolution: { width: 1080, height: 1920 } },
  { name: 'Instagram Post', resolution: { width: 1080, height: 1080 } },
  { name: 'TikTok', resolution: { width: 1080, height: 1920 } },
  { name: 'YouTube Shorts', resolution: { width: 1080, height: 1920 } },
];

export function CreateProjectModal({ isOpen, onClose }: CreateProjectModalProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [selectedPreset, setSelectedPreset] = useState(0);
  const [fps, setFps] = useState(30);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { setProjects, projects } = useStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    setIsSubmitting(true);
    try {
      const newProject = await projectsApi.create({
        name: name.trim(),
        description: description.trim() || undefined,
        resolution: PRESET_RESOLUTIONS[selectedPreset].resolution,
        fps,
      });

      setProjects([...projects, newProject]);
      onClose();
      setName('');
      setDescription('');
      setSelectedPreset(0);
      setFps(30);
    } catch (error) {
      console.error('Failed to create project:', error);
      alert('Failed to create project. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create New Project">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Project Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="My Awesome Video"
          required
        />

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description (optional)
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Project description..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            rows={3}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Resolution Preset
          </label>
          <select
            value={selectedPreset}
            onChange={(e) => setSelectedPreset(Number(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            {PRESET_RESOLUTIONS.map((preset, index) => (
              <option key={index} value={index}>
                {preset.name} ({preset.resolution.width}x{preset.resolution.height})
              </option>
            ))}
          </select>
        </div>

        <Input
          label="FPS (Frames Per Second)"
          type="number"
          value={fps}
          onChange={(e) => setFps(Number(e.target.value))}
          min={1}
          max={120}
          required
        />

        <div className="flex justify-end gap-2 pt-4">
          <Button type="button" variant="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Creating...' : 'Create Project'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
