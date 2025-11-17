import { Layers, Plus } from 'lucide-react';
import { Button } from '../ui/Button';
import { LayerItem } from './LayerItem';
import type { Layer } from '../../types';
import { useStore } from '../../store/useStore';

interface TimelineProps {
  layers: Layer[];
  onAddLayer: () => void;
}

export function Timeline({ layers, onAddLayer }: TimelineProps) {
  const { selectedLayerId, setSelectedLayerId } = useStore();

  return (
    <div className="bg-white border-t border-gray-200 h-64 flex flex-col">
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-gray-600" />
          <h3 className="font-semibold">Timeline</h3>
          <span className="text-sm text-gray-500">({layers.length} layers)</span>
        </div>
        <Button size="sm" onClick={onAddLayer}>
          <Plus className="w-4 h-4 mr-1" />
          Add Layer
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {layers.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400">
            <Layers className="w-12 h-12 mb-2" />
            <p className="text-sm">No layers yet. Add a layer to get started.</p>
          </div>
        ) : (
          <div className="p-2 space-y-1">
            {[...layers]
              .sort((a, b) => b.z_index - a.z_index)
              .map((layer) => (
                <LayerItem
                  key={layer.id}
                  layer={layer}
                  isSelected={selectedLayerId === layer.id}
                  onClick={() => setSelectedLayerId(layer.id)}
                />
              ))}
          </div>
        )}
      </div>
    </div>
  );
}
