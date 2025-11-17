import { useNavigate } from 'react-router-dom';
import { Film, Trash2, Calendar, Settings } from 'lucide-react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import type { Project } from '../../types';
import { formatDistanceToNow } from 'date-fns';

interface ProjectCardProps {
  project: Project;
  onDelete: (id: string) => void;
}

const STATUS_COLORS = {
  draft: 'bg-gray-100 text-gray-800',
  in_progress: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
  archived: 'bg-orange-100 text-orange-800',
};

export function ProjectCard({ project, onDelete }: ProjectCardProps) {
  const navigate = useNavigate();

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm(`Are you sure you want to delete "${project.name}"?`)) {
      onDelete(project.id);
    }
  };

  return (
    <Card onClick={() => navigate(`/editor/${project.id}`)}>
      <div className="p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <Film className="w-5 h-5 text-primary-600" />
            <h3 className="font-semibold text-lg">{project.name}</h3>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleDelete}
            className="text-red-600 hover:text-red-700 hover:bg-red-50"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>

        {project.description && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {project.description}
          </p>
        )}

        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Settings className="w-4 h-4" />
            <span>
              {project.resolution.width}x{project.resolution.height} @ {project.fps} FPS
            </span>
          </div>

          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Calendar className="w-4 h-4" />
            <span>
              Updated {formatDistanceToNow(new Date(project.updated_at))} ago
            </span>
          </div>
        </div>

        <div className="mt-3 flex items-center justify-between">
          <span
            className={`px-2 py-1 rounded-full text-xs font-medium ${
              STATUS_COLORS[project.status]
            }`}
          >
            {project.status.replace('_', ' ')}
          </span>
          <span className="text-sm text-gray-500">
            {project.timeline.layers.length} layers
          </span>
        </div>
      </div>
    </Card>
  );
}
