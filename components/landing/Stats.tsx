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
  // Integers get locale formatting (e.g. 2,310); decimals keep their precision.
  const formatted = decimals > 0 ? v.toFixed(decimals) : Math.round(v).toLocaleString();
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
            <div className="section-eyebrow stats-eyebrow">Impact at a glance</div>
            <h2 className="section-title"><span className="gradient-text-neon">Numbers that move.</span></h2>
            <p className="section-sub">Live across the Terra Nature fleet, refreshed every minute.</p>
          </div>
        </ScrollReveal>

        <div ref={ref} className="stats-grid">
          <Stat value={2310} suffix=" kWh" label="Tracked this hour" start={revealed} />
          <Stat value={97.4} decimals={1} suffix="%" label="Stream uptime" start={revealed} />
          <Stat value={148} label="Connected devices" start={revealed} />
          <Stat value={32} suffix=" t CO₂e" label="Avoided this month" start={revealed} />
        </div>
      </div>
    </section>
  );
}
