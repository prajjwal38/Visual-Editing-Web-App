import { create } from 'zustand';
import type { Project, Effect, MediaAsset } from '../types';

interface AppState {
  // Projects
  projects: Project[];
  currentProject: Project | null;
  setProjects: (projects: Project[]) => void;
  setCurrentProject: (project: Project | null) => void;
  updateCurrentProject: (project: Project) => void;

  // Effects
  availableEffects: Effect[];
  setAvailableEffects: (effects: Effect[]) => void;

  // Media
  mediaAssets: MediaAsset[];
  setMediaAssets: (assets: MediaAsset[]) => void;

  // UI State
  selectedLayerId: string | null;
  setSelectedLayerId: (id: string | null) => void;

  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;

  error: string | null;
  setError: (error: string | null) => void;
}

export const useStore = create<AppState>((set) => ({
  // Projects
  projects: [],
  currentProject: null,
  setProjects: (projects) => set({ projects }),
  setCurrentProject: (project) => set({ currentProject: project }),
  updateCurrentProject: (project) => set({ currentProject: project }),

  // Effects
  availableEffects: [],
  setAvailableEffects: (effects) => set({ availableEffects: effects }),

  // Media
  mediaAssets: [],
  setMediaAssets: (assets) => set({ mediaAssets: assets }),

  // UI State
  selectedLayerId: null,
  setSelectedLayerId: (id) => set({ selectedLayerId: id }),

  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),

  error: null,
  setError: (error) => set({ error }),
}));
