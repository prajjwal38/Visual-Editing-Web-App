import { useEffect, useState } from 'react';
import { Sparkles, Plus } from 'lucide-react';
import { Button } from '../ui/Button';
import { Modal } from '../ui/Modal';
import { Input } from '../ui/Input';
import { effectsApi } from '../../services/api';
import { useStore } from '../../store/useStore';
import type { Effect, ApplyEffectRequest } from '../../types';

interface EffectsPanelProps {
  projectId: string;
  onEffectApplied: () => void;
}

export function EffectsPanel({ projectId, onEffectApplied }: EffectsPanelProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedEffect, setSelectedEffect] = useState<Effect | null>(null);
  const [parameters, setParameters] = useState<Record<string, number | string | boolean>>({});
  const { availableEffects, setAvailableEffects, selectedLayerId } = useStore();

  useEffect(() => {
    const loadEffects = async () => {
      try {
        const effects = await effectsApi.getAll();
        setAvailableEffects(effects);
      } catch (error) {
        console.error('Failed to load effects:', error);
      }
    };
    loadEffects();
  }, []);

  const handleEffectSelect = (effect: Effect) => {
    setSelectedEffect(effect);
    const defaultParams: Record<string, number | string | boolean> = {};
    effect.parameters.forEach((param) => {
      defaultParams[param.name] = param.default;
    });
    setParameters(defaultParams);
    setIsModalOpen(true);
  };

  const handleApplyEffect = async () => {
    if (!selectedEffect || !selectedLayerId) return;

    try {
      const request: ApplyEffectRequest = {
        effect_name: selectedEffect.name,
        parameters,
      };

      await effectsApi.applyToLayer(projectId, selectedLayerId, request);
      onEffectApplied();
      setIsModalOpen(false);
      setSelectedEffect(null);
    } catch (error) {
      console.error('Failed to apply effect:', error);
      alert('Failed to apply effect. Please try again.');
    }
  };

  return (
    <div className="bg-white border-l border-gray-200 w-80 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-2 mb-2">
          <Sparkles className="w-5 h-5 text-purple-600" />
          <h3 className="font-semibold">Effects</h3>
        </div>
        {!selectedLayerId && (
          <p className="text-sm text-gray-500">Select a layer to apply effects</p>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-2">
          {availableEffects.map((effect) => (
            <button
              key={effect.name}
              onClick={() => handleEffectSelect(effect)}
              disabled={!selectedLayerId}
              className="w-full p-3 text-left border border-gray-200 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <div className="font-medium text-sm">{effect.name}</div>
              <div className="text-xs text-gray-500 mt-1">{effect.description}</div>
            </button>
          ))}
        </div>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={`Apply ${selectedEffect?.name || 'Effect'}`}
      >
        {selectedEffect && (
          <div className="space-y-4">
            <p className="text-sm text-gray-600">{selectedEffect.description}</p>

            <div className="space-y-3">
              {selectedEffect.parameters.map((param) => (
                <div key={param.name}>
                  {param.type === 'int' || param.type === 'float' ? (
                    <Input
                      label={param.name}
                      type="number"
                      value={parameters[param.name] as number}
                      onChange={(e) =>
                        setParameters({
                          ...parameters,
                          [param.name]: parseFloat(e.target.value),
                        })
                      }
                      min={param.min}
                      max={param.max}
                      step={param.type === 'float' ? 0.1 : 1}
                    />
                  ) : param.type === 'bool' ? (
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={parameters[param.name] as boolean}
                        onChange={(e) =>
                          setParameters({
                            ...parameters,
                            [param.name]: e.target.checked,
                          })
                        }
                        className="rounded border-gray-300"
                      />
                      <span className="text-sm font-medium">{param.name}</span>
                    </label>
                  ) : (
                    <Input
                      label={param.name}
                      value={parameters[param.name] as string}
                      onChange={(e) =>
                        setParameters({
                          ...parameters,
                          [param.name]: e.target.value,
                        })
                      }
                    />
                  )}
                </div>
              ))}
            </div>

            <div className="flex justify-end gap-2 pt-4">
              <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleApplyEffect}>
                <Plus className="w-4 h-4 mr-1" />
                Apply Effect
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
