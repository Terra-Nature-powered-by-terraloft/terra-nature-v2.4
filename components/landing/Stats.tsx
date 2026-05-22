'use client';

import { useScrollReveal } from '@/hooks/useScrollReveal';
import { useCounter } from '@/hooks/useCounter';
import { ScrollReveal } from './ScrollReveal';

interface StatProps {
  value: number;
  decimals?: number;
  suffix?: string;
  label: string;
  start: boolean;
}

function Stat({ value, decimals = 0, suffix = '', label, start }: StatProps) {
  const v = useCounter(value, { start, decimals, duration: 2500 });
  // German formatting: comma as decimal separator, thousands grouping on integers.
  const formatted =
    decimals > 0 ? v.toFixed(decimals).replace('.', ',') : Math.round(v).toLocaleString('de-DE');
  return (
    <div className="stat">
      <div className="stat-value">{formatted}{suffix}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}

export function Stats() {
  // Counters only start once the grid is in view, so users see the count-up
  // rather than a static final number on first paint.
  const { ref, revealed } = useScrollReveal<HTMLDivElement>({ threshold: 0.35 });

  return (
    <section id="impact" className="section stats">
      <div className="container">
        <ScrollReveal variant="slide-up">
          <div className="section-header">
            <div className="section-eyebrow stats-eyebrow">Impact in Zahlen</div>
            <h2 className="section-title">
              <span className="gradient-text-neon">Messbare Wirkung.</span>
            </h2>
            <p className="section-sub">Live aus unseren Pilotanlagen — aktualisiert pro Minute.</p>
          </div>
        </ScrollReveal>

        <div ref={ref} className="stats-grid">
          <Stat value={12.8} decimals={1} suffix=" MWh/t" label="Abwärme rückgewonnen" start={revealed} />
          <Stat value={2.46} decimals={2} suffix=" kt" label="CO₂ vermieden" start={revealed} />
          <Stat value={2.31} decimals={2} suffix=" MWh/t" label="Energieeffizienz" start={revealed} />
          <Stat value={99.9} decimals={1} suffix=" %" label="Systemverfügbarkeit" start={revealed} />
        </div>
      </div>
    </section>
  );
}
