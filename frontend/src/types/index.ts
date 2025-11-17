// API Types matching backend schemas

export type ProjectStatus = 'draft' | 'in_progress' | 'completed' | 'archived';
export type LayerType = 'video' | 'image' | 'audio' | 'text' | 'effect';
export type MediaType = 'video' | 'image' | 'audio';
export type ExportFormat = 'mp4' | 'mov' | 'avi' | 'webm' | 'gif';

export interface Resolution {
  width: number;
  height: number;
}

export interface Position {
  x: number;
  y: number;
}

export interface Duration {
  seconds: number;
}

export interface Color {
  r: number;
  g: number;
  b: number;
}

export interface EffectParameter {
  name: string;
  value: number | string | boolean;
}

export interface EffectInstance {
  effect_name: string;
  parameters: Record<string, number | string | boolean>;
}

export interface Layer {
  id: string;
  layer_type: LayerType;
  media_asset_id?: string;
  start_time: Duration;
  duration: Duration;
  position: Position;
  z_index: number;
  opacity: number;
  is_enabled: boolean;
  effects: EffectInstance[];
}

export interface Timeline {
  layers: Layer[];
  total_duration: Duration;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  resolution: Resolution;
  fps: number;
  status: ProjectStatus;
  created_at: string;
  updated_at: string;
  timeline: Timeline;
}

export interface CreateProjectRequest {
  name: string;
  description?: string;
  resolution: Resolution;
  fps: number;
}

export interface AddLayerRequest {
  layer_type: LayerType;
  media_asset_id?: string;
  start_time: number;
  duration: number;
  position: Position;
  z_index?: number;
  opacity?: number;
}

export interface ApplyEffectRequest {
  effect_name: string;
  parameters: Record<string, number | string | boolean>;
}

export interface ExportProjectRequest {
  format: ExportFormat;
  output_filename?: string;
}

export interface Effect {
  name: string;
  description: string;
  parameters: {
    name: string;
    type: string;
    default: number | string | boolean;
    min?: number;
    max?: number;
    options?: string[];
  }[];
}

export interface MediaAsset {
  id: string;
  filename: string;
  media_type: MediaType;
  file_path: string;
  file_size: number;
  duration?: number;
  resolution?: Resolution;
  created_at: string;
}

export interface ExportResponse {
  message: string;
  export_path: string;
  project_id: string;
  format: ExportFormat;
}
