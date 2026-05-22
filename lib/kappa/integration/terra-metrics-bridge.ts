/**
 * Terra Metrics Bridge - Integration between Terra Dashboard and Kappa
 * Provides real-time metric context to Kappa Expert Engine
 */

import { MetricSample } from '@/lib/types';

export interface TerrametricContext {
  current_energy_kWh: number;
  current_heat_kWh: number;
  current_power_kW: number;
  daily_energy_total: number;
  daily_heat_total: number;
  co2_compensation_kg: number;
  efficiency_percent: number;
  device_id: string;
  timestamp: string;
  status: 'healthy' | 'degraded' | 'error';
}

export interface MetricTrend {
  metric: 'energy' | 'heat' | 'power' | 'co2';
  current: number;
  average: number;
  trend: 'increasing' | 'stable' | 'decreasing';
  change_percent: number;
}

/**
 * Extract contextual information from current metrics for Kappa queries
 */
export function extractMetricContext(metric: MetricSample | null): Partial<TerrametricContext> {
  if (!metric) {
    return {
      status: 'error',
    };
  }

  // CO₂ compensation calculation: roughly 0.4 kg CO₂ per kWh of energy
  const co2_compensation_kg = metric.energy_kWh * 0.4;

  // Efficiency: heat output / energy input
  const efficiency_percent = metric.heat_kWh > 0 ? (metric.heat_kWh / metric.energy_kWh) * 100 : 0;

  return {
    current_energy_kWh: metric.energy_kWh,
    current_heat_kWh: metric.heat_kWh,
    current_power_kW: metric.Pel_kW,
    co2_compensation_kg: Math.round(co2_compensation_kg * 100) / 100,
    efficiency_percent: Math.round(efficiency_percent * 100) / 100,
    device_id: metric.device_id,
    timestamp: metric.timestamp,
    status: 'healthy',
  };
}

/**
 * Format metric context into natural language for Kappa queries
 */
export function formatMetricContextForKappa(metric: MetricSample | null): string {
  const ctx = extractMetricContext(metric);

  if (ctx.status === 'error') {
    return 'Keine aktuellen Metriken verfügbar';
  }

  return `
Aktuelle Terra Nature Metriken (${ctx.timestamp}):
- Stromverbrauch: ${ctx.current_energy_kWh} kWh
- Wärmeerzeugung: ${ctx.current_heat_kWh} kWh
- Leistung: ${ctx.current_power_kW} kW
- Effizienz: ${ctx.efficiency_percent}%
- CO₂-Kompensation: ${ctx.co2_compensation_kg} kg
- Gerät: ${ctx.device_id}
  `.trim();
}

/**
 * Detect trends in metrics for contextual awareness
 */
export function detectMetricTrends(
  current: MetricSample | null,
  history: MetricSample[]
): MetricTrend[] {
  const trends: MetricTrend[] = [];

  if (!current || history.length === 0) {
    return trends;
  }

  // Energy trend
  const avgEnergy = history.reduce((sum, m) => sum + m.energy_kWh, 0) / history.length;
  trends.push({
    metric: 'energy',
    current: current.energy_kWh,
    average: avgEnergy,
    trend: current.energy_kWh > avgEnergy ? 'increasing' : 'decreasing',
    change_percent: ((current.energy_kWh - avgEnergy) / avgEnergy) * 100,
  });

  // Heat trend
  const avgHeat = history.reduce((sum, m) => sum + m.heat_kWh, 0) / history.length;
  trends.push({
    metric: 'heat',
    current: current.heat_kWh,
    average: avgHeat,
    trend: current.heat_kWh > avgHeat ? 'increasing' : 'decreasing',
    change_percent: ((current.heat_kWh - avgHeat) / avgHeat) * 100,
  });

  // Power trend
  const avgPower = history.reduce((sum, m) => sum + m.Pel_kW, 0) / history.length;
  trends.push({
    metric: 'power',
    current: current.Pel_kW,
    average: avgPower,
    trend: current.Pel_kW > avgPower ? 'increasing' : 'decreasing',
    change_percent: ((current.Pel_kW - avgPower) / avgPower) * 100,
  });

  // CO₂ trend
  const currentCO2 = current.energy_kWh * 0.4;
  const avgCO2 = history.reduce((sum, m) => sum + m.energy_kWh * 0.4, 0) / history.length;
  trends.push({
    metric: 'co2',
    current: currentCO2,
    average: avgCO2,
    trend: currentCO2 > avgCO2 ? 'increasing' : 'decreasing',
    change_percent: ((currentCO2 - avgCO2) / avgCO2) * 100,
  });

  return trends;
}

/**
 * Check if metrics indicate anomalies
 */
export function checkMetricAnomalies(metric: MetricSample, history: MetricSample[]): string[] {
  const anomalies: string[] = [];

  if (history.length < 2) {
    return anomalies;
  }

  // Check for extreme power consumption
  const avgPower = history.reduce((sum, m) => sum + m.Pel_kW, 0) / history.length;
  if (metric.Pel_kW > avgPower * 1.5) {
    anomalies.push('Leistungsverbrauch über 50% des Durchschnitts');
  }

  // Check for zero heat output
  if (metric.heat_kWh === 0 && history.some((m) => m.heat_kWh > 0)) {
    anomalies.push('Wärmeerzeugung liegt bei null');
  }

  // Check for zero energy consumption
  if (metric.energy_kWh === 0) {
    anomalies.push('Keine Stromzufuhr erkannt');
  }

  // Check for implausible efficiency (>100%)
  const efficiency = (metric.heat_kWh / metric.energy_kWh) * 100;
  if (efficiency > 100) {
    anomalies.push('Effizienz über 100% - technisch unmöglich');
  }

  return anomalies;
}

/**
 * Generate a summary statement for Kappa validation
 */
export function generateMetricStatement(metric: MetricSample, context: string = ''): string {
  const ctx = extractMetricContext(metric);
  const efficiency = ctx.efficiency_percent || 0;

  let statement = `Das System produziert ${ctx.current_heat_kWh} kWh Wärme bei ${ctx.current_energy_kWh} kWh Stromverbrauch, was einer Effizienz von ${efficiency.toFixed(1)}% entspricht.`;

  if (context) {
    statement += ` Im Kontext: ${context}`;
  }

  return statement;
}

/**
 * Extract expert mode recommendation based on metrics
 */
export function recommendExpertMode(metric: MetricSample | null): string {
  if (!metric) return 'default';

  const efficiency = (metric.heat_kWh / metric.energy_kWh) * 100;

  // Select mode based on metric characteristics
  if (efficiency > 80) {
    return 'cto'; // High efficiency = technical discussion
  }

  if (metric.energy_kWh > 100) {
    return 'industrial'; // High energy consumption = industrial context
  }

  // Default to MRV for verification/compliance
  return 'mrv';
}
