import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Timeline } from '../components/editor/Timeline';
import { EffectsPanel } from '../components/editor/EffectsPanel';
import { ExportPanel } from '../components/editor/ExportPanel';
import { AddLayerModal } from '../components/editor/AddLayerModal';
import { projectsApi } from '../services/api';
import { useStore } from '../store/useStore';

export function Editor() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const { currentProject, setCurrentProject } = useStore();
  const [isLoading, setIsLoading] = useState(true);
  const [isAddLayerModalOpen, setIsAddLayerModalOpen] = useState(false);

  const loadProject = async () => {
    if (!projectId) return;

    setIsLoading(true);
    try {
      const project = await projectsApi.getById(projectId);
      setCurrentProject(project);
    } catch (error) {
      console.error('Failed to load project:', error);
      alert('Failed to load project');
      navigate('/');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadProject();
    return () => setCurrentProject(null);
  }, [projectId]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-gray-500">Loading project...</div>
      </div>
    );
  }

  if (!currentProject) {
    return null;
  }

  return (
    <div className="h-screen flex flex-col bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/')}
              className="text-gray-300 hover:text-white"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <div>
              <h1 className="text-lg font-semibold text-white">
                {currentProject.name}
              </h1>
              <p className="text-xs text-gray-400">
                {currentProject.resolution.width}x{currentProject.resolution.height} @{' '}
                {currentProject.fps} FPS
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" className="text-gray-300">
              <Save className="w-4 h-4 mr-2" />
              Auto-saved
            </Button>
            <ExportPanel
              projectId={currentProject.id}
              projectName={currentProject.name}
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Canvas Area */}
        <div className="flex-1 flex items-center justify-center bg-gray-900 p-8">
          <div
            className="bg-gray-800 border-2 border-gray-700 rounded-lg shadow-2xl"
            style={{
              width: currentProject.resolution.width / 2,
              height: currentProject.resolution.height / 2,
              maxWidth: '90%',
              maxHeight: '90%',
            }}
          >
            <div className="w-full h-full flex items-center justify-center text-gray-500">
              <div className="text-center">
                <div className="text-4xl mb-2">🎬</div>
                <p className="text-sm">Preview Area</p>
                <p className="text-xs text-gray-600 mt-1">
                  {currentProject.timeline.layers.length} layers •{' '}
                  {currentProject.timeline.total_duration.seconds.toFixed(1)}s
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Effects Panel */}
        <EffectsPanel projectId={currentProject.id} onEffectApplied={loadProject} />
      </div>

      {/* Timeline */}
      <Timeline
        layers={currentProject.timeline.layers}
        onAddLayer={() => setIsAddLayerModalOpen(true)}
      />

      {/* Add Layer Modal */}
      <AddLayerModal
        isOpen={isAddLayerModalOpen}
        onClose={() => setIsAddLayerModalOpen(false)}
        projectId={currentProject.id}
        onLayerAdded={loadProject}
      />
    </div>
  );
}
