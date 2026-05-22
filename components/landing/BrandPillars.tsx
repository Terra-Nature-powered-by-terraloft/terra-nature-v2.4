'use client';

import { ScrollReveal } from './ScrollReveal';

const PILLARS = [
  {
    icon: '🌐',
    title: 'Climate Intelligence',
    desc: 'Data-driven insights for a measurable impact.',
  },
  {
    icon: '🏭',
    title: 'Industrial Impact',
    desc: 'Deep-tech systems for real-world scale.',
  },
  {
    icon: '🛡️',
    title: 'Verified Results',
    desc: 'Auditable outcomes and digital transparency.',
  },
  {
    icon: '🕸️',
    title: 'Scalable Systems',
    desc: 'Modular, interoperable and future-ready.',
  },
];

export function BrandPillars() {
  return (
    <section className="pillars" aria-label="Brand Pillars">
      <div className="container">
        <div className="pillars-grid">
          {PILLARS.map((p, i) => (
            <ScrollReveal key={p.title} variant="fade-in" delay={i * 100}>
              <div className="pillar">
                <div className="pillar-icon" aria-hidden>{p.icon}</div>
                <div className="pillar-title">{p.title}</div>
                <p className="pillar-desc">{p.desc}</p>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
}
