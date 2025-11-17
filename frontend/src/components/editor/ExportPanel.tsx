import { useState } from 'react';
import { Download, FileVideo } from 'lucide-react';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Modal } from '../ui/Modal';
import { exportApi } from '../../services/api';
import type { ExportFormat } from '../../types';

interface ExportPanelProps {
  projectId: string;
  projectName: string;
}

export function ExportPanel({ projectId, projectName }: ExportPanelProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [format, setFormat] = useState<ExportFormat>('mp4');
  const [filename, setFilename] = useState('');
  const [isExporting, setIsExporting] = useState(false);
  const [exportSuccess, setExportSuccess] = useState(false);

  const handleExport = async () => {
    setIsExporting(true);
    setExportSuccess(false);

    try {
      const result = await exportApi.exportProject(projectId, {
        format,
        output_filename: filename || undefined,
      });

      console.log('Export successful:', result);
      setExportSuccess(true);
      setTimeout(() => {
        setIsModalOpen(false);
        setExportSuccess(false);
      }, 2000);
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to export project. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <>
      <Button variant="secondary" onClick={() => setIsModalOpen(true)}>
        <Download className="w-4 h-4 mr-2" />
        Export
      </Button>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Export Project"
      >
        <div className="space-y-4">
          <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
            <FileVideo className="w-10 h-10 text-primary-600" />
            <div>
              <h4 className="font-medium">{projectName}</h4>
              <p className="text-sm text-gray-600">Ready to export</p>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Export Format
            </label>
            <select
              value={format}
              onChange={(e) => setFormat(e.target.value as ExportFormat)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="mp4">MP4 (Recommended)</option>
              <option value="mov">MOV</option>
              <option value="avi">AVI</option>
              <option value="webm">WebM</option>
              <option value="gif">GIF</option>
            </select>
          </div>

          <Input
            label="Output Filename (optional)"
            value={filename}
            onChange={(e) => setFilename(e.target.value)}
            placeholder={`${projectName}.${format}`}
          />

          {exportSuccess && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg text-green-800 text-sm">
              Export completed successfully!
            </div>
          )}

          <div className="flex justify-end gap-2 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setIsModalOpen(false)}
              disabled={isExporting}
            >
              Cancel
            </Button>
            <Button onClick={handleExport} disabled={isExporting}>
              {isExporting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                  Exporting...
                </>
              ) : (
                <>
                  <Download className="w-4 h-4 mr-2" />
                  Export Video
                </>
              )}
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
}
