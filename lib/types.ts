/**
 * Core TypeScript type definitions for Terra Nature metrics and data export
 */

export interface MetricSample {
  /** Timestamp in ISO 8601 format */
  timestamp: string;
  /** Device identifier */
  device_id: string;
  /** Energy consumption in kWh */
  energy_kWh: number;
  /** Heat generation in kWh */
  heat_kWh: number;
  /** Power consumption in kW (derived with perturbation) */
  Pel_kW: number;
}

export interface JsonlRecord {
  /** Timestamp in ISO 8601 format */
  ts: string;
  /** Device identifier */
  device: string;
  /** Energy consumption in kWh */
  energy_kWh: number;
  /** Heat generation in kWh */
  heat_kWh: number;
  /** SHA-256 proof hash for data integrity */
  proof_id: string;
}

export type ExportFormat = 'csv' | 'jsonl';

export interface ExportRequest {
  format: ExportFormat;
  minutes: number;
}

export interface MetricsHookState {
  data: MetricSample | null;
  connected: boolean;
  error: string | null;
  disconnect: () => void;
}