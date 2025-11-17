import { Image, Video, Music, Eye, EyeOff } from 'lucide-react';
import clsx from 'clsx';
import type { Layer, LayerType } from '../../types';

interface LayerItemProps {
  layer: Layer;
  isSelected: boolean;
  onClick: () => void;
}

const LAYER_ICONS: Record<LayerType, React.ComponentType<{ className?: string }>> = {
  video: Video,
  image: Image,
  audio: Music,
  text: () => <span>T</span>,
  effect: () => <span>FX</span>,
};

export function LayerItem({ layer, isSelected, onClick }: LayerItemProps) {
  const Icon = LAYER_ICONS[layer.layer_type];

  return (
    <div
      className={clsx(
        'p-3 rounded-lg border-2 cursor-pointer transition-all',
        isSelected
          ? 'border-primary-500 bg-primary-50'
          : 'border-gray-200 bg-white hover:border-gray-300'
      )}
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <Icon className="w-4 h-4 flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium truncate">
              {layer.layer_type.charAt(0).toUpperCase() + layer.layer_type.slice(1)} Layer
            </div>
            <div className="text-xs text-gray-500">
              {layer.start_time.seconds.toFixed(1)}s - {(layer.start_time.seconds + layer.duration.seconds).toFixed(1)}s
              {' • '}z-index: {layer.z_index}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          {layer.effects.length > 0 && (
            <span className="text-xs bg-purple-100 text-purple-800 px-2 py-0.5 rounded">
              {layer.effects.length} effect{layer.effects.length > 1 ? 's' : ''}
            </span>
          )}
          {layer.is_enabled ? (
            <Eye className="w-4 h-4 text-green-600" />
          ) : (
            <EyeOff className="w-4 h-4 text-gray-400" />
          )}
        </div>
      </div>
      <div className="mt-2">
        <div className="flex items-center gap-2 text-xs text-gray-600">
          <span>Opacity: {Math.round(layer.opacity * 100)}%</span>
          <span>•</span>
          <span>
            Position: ({layer.position.x}, {layer.position.y})
          </span>
        </div>
      </div>
    </div>
  );
}
