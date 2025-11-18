import axios from 'axios';
import type {
  Project,
  CreateProjectRequest,
  AddLayerRequest,
  ApplyEffectRequest,
  ExportProjectRequest,
  ExportResponse,
  Effect,
  MediaAsset,
} from '../types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Projects API
export const projectsApi = {
  create: async (data: CreateProjectRequest): Promise<Project> => {
    const response = await api.post<Project>('/projects/', data);
    return response.data;
  },

  getAll: async (): Promise<Project[]> => {
    const response = await api.get<Project[]>('/projects/');
    return response.data;
  },

  getById: async (projectId: string): Promise<Project> => {
    const response = await api.get<Project>(`/projects/${projectId}`);
    return response.data;
  },

  delete: async (projectId: string): Promise<void> => {
    await api.delete(`/projects/${projectId}`);
  },
};

// Timeline API
export const timelineApi = {
  addLayer: async (projectId: string, data: AddLayerRequest): Promise<Project> => {
    const response = await api.post<Project>(
      `/projects/${projectId}/timeline/layers`,
      data
    );
    return response.data;
  },
};

// Effects API
export const effectsApi = {
  getAll: async (): Promise<Effect[]> => {
    const response = await api.get<Effect[]>('/effects');
    return response.data;
  },

  getByName: async (effectName: string): Promise<Effect> => {
    const response = await api.get<Effect>(`/effects/${effectName}`);
    return response.data;
  },

  applyToLayer: async (
    projectId: string,
    layerId: string,
    data: ApplyEffectRequest
  ): Promise<Project> => {
    const response = await api.post<Project>(
      `/projects/${projectId}/layers/${layerId}/effects`,
      data
    );
    return response.data;
  },
};

// Export API
export const exportApi = {
  exportProject: async (
    projectId: string,
    data: ExportProjectRequest
  ): Promise<ExportResponse> => {
    const response = await api.post<ExportResponse>(
      `/projects/${projectId}/export`,
      data
    );
    return response.data;
  },
};

// Media API
export const mediaApi = {
  getAll: async (): Promise<MediaAsset[]> => {
    const response = await api.get<MediaAsset[]>('/media/');
    return response.data;
  },

  upload: async (
    file: File,
    mediaType: string,
    metadata?: { duration?: number; width?: number; height?: number }
  ): Promise<MediaAsset> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('media_type', mediaType);

    if (metadata?.duration !== undefined) {
      formData.append('duration', metadata.duration.toString());
    }
    if (metadata?.width !== undefined) {
      formData.append('width', metadata.width.toString());
    }
    if (metadata?.height !== undefined) {
      formData.append('height', metadata.height.toString());
    }

    const response = await api.post<MediaAsset>('/media/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export default api;
