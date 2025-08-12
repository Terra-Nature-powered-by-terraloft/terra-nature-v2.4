import { createHash } from 'crypto';
import { MetricSample, JsonlRecord } from './types';

/**
 * Deterministic-style mock data generator with controlled noise and plausible baselines
 */

const DEVICE_ID = 'asic-rack-01';
const BASE_ENERGY_KWH = 12.5; // Base energy consumption
const BASE_HEAT_KWH = 8.3;    // Base heat generation

/**
 * Generate a deterministic pseudo-random value based on timestamp
 * This provides controlled variation while maintaining reproducibility
 */
function deterministicRandom(timestamp: string, seed: string): number {
  const hash = createHash('sha256').update(timestamp + seed).digest('hex');
  // Convert first 8 chars of hash to number and normalize to [0,1]
  const value = parseInt(hash.substring(0, 8), 16) / 0xffffffff;
  return value;
}

/**
 * Generate a MetricSample with realistic values and minor perturbation
 */
export function sample(): MetricSample {
  const timestamp = new Date().toISOString();
  
  // Use timestamp as seed for deterministic variation
  const energyVariation = deterministicRandom(timestamp, 'energy') * 0.2 - 0.1; // ±10%
  const heatVariation = deterministicRandom(timestamp, 'heat') * 0.15 - 0.075;   // ±7.5%
  const powerVariation = deterministicRandom(timestamp, 'power') * 0.3 - 0.15;   // ±15%
  
  const energy_kWh = BASE_ENERGY_KWH * (1 + energyVariation);
  const heat_kWh = BASE_HEAT_KWH * (1 + heatVariation);
  
  // Derive Pel_kW from energy with additional perturbation
  const Pel_kW = (energy_kWh * 0.85) * (1 + powerVariation);
  
  return {
    timestamp,
    device_id: DEVICE_ID,
    energy_kWh: Math.round(energy_kWh * 1000) / 1000, // Round to 3 decimal places
    heat_kWh: Math.round(heat_kWh * 1000) / 1000,
    Pel_kW: Math.round(Pel_kW * 1000) / 1000
  };
}

/**
 * Generate JSONL record with SHA-256 proof hash for minute-resolution data
 */
export function jsonl(minutesAgo: number = 0): JsonlRecord {
  const now = new Date();
  now.setMinutes(now.getMinutes() - minutesAgo);
  // Round to nearest minute
  now.setSeconds(0);
  now.setMilliseconds(0);
  
  const timestamp = now.toISOString();
  
  // Generate deterministic values for this specific minute
  const energyVariation = deterministicRandom(timestamp, 'energy_jsonl') * 0.2 - 0.1;
  const heatVariation = deterministicRandom(timestamp, 'heat_jsonl') * 0.15 - 0.075;
  
  const energy_kWh = BASE_ENERGY_KWH * (1 + energyVariation);
  const heat_kWh = BASE_HEAT_KWH * (1 + heatVariation);
  
  // Create canonical payload string for hash generation
  const canonicalPayload = `${timestamp}|device:${DEVICE_ID}|${energy_kWh}|${heat_kWh}`;
  const proof_id = createHash('sha256').update(canonicalPayload).digest('hex');
  
  return {
    ts: timestamp,
    device: DEVICE_ID,
    energy_kWh: Math.round(energy_kWh * 1000) / 1000,
    heat_kWh: Math.round(heat_kWh * 1000) / 1000,
    proof_id
  };
}