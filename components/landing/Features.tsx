'use client';

import { ScrollReveal } from './ScrollReveal';

const FEATURES = [
  { icon: '⚡', title: 'Live metrics', desc: 'WebSocket-streamed energy, heat, and power readings with sub-second resolution.' },
  { icon: '🌿', title: 'Nature-aware', desc: 'Designed for sites where ecology and efficiency are the same goal.' },
  { icon: '📈', title: 'Trend visibility', desc: '24-hour rollups, comparative baselines, and anomaly hints, all in one view.' },
  { icon: '📤', title: 'Export ready', desc: 'CSV or JSONL exports for the last 24 hours, integrated with your BI stack.' },
  { icon: '🔒', title: 'Secure by default', desc: 'Encrypted transports, scoped credentials, and audit trails out of the box.' },
  { icon: '🛰️', title: 'Multi-device', desc: 'Aggregate readings across distributed Terraloft units in a single canvas.' },
];

export function Features() {
  return (
    <section id="features" className="section">
      <div className="container">
        <ScrollReveal variant="slide-up">
          <div className="section-header">
            <div className="section-eyebrow">What&apos;s inside</div>
            <h2 className="section-title">
              Built for sites where <span className="gradient-text-terra">every watt counts</span>.
            </h2>
            <p className="section-sub">
              Six capabilities that turn raw telemetry into decisions you can defend.
            </p>
          </div>
        </ScrollReveal>

        <div className="features-grid">
          {FEATURES.map((f, i) => (
            // Stagger the cards by ~120ms so they arrive as a wave, not a wall.
            <ScrollReveal key={f.title} variant="slide-up" delay={i * 120}>
              <article className="feature-card">
                <div className="feature-icon" aria-hidden>{f.icon}</div>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </article>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
}
