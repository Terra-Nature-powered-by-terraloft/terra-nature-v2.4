'use client';

import { ScrollReveal } from './ScrollReveal';

const FEATURES = [
  {
    icon: '🔥',
    title: 'Abwärme nutzbar machen',
    desc: 'Industrielle Abwärme, die heute verloren geht, wird zu Strom, Wärme und Nachweis.',
  },
  {
    icon: '⚡',
    title: 'Energieeffizienz steigern',
    desc: 'Wir verbinden Energieumwandlung, Wärmerückführung und MRV-Nachweise in einem System.',
  },
  {
    icon: '📊',
    title: 'Digitale Nachweise schaffen',
    desc: 'Auditfähige Daten und transparente Wirkung — jederzeit nachvollziehbar.',
  },
  {
    icon: '🛡️',
    title: 'Vertrauen & Wirkung nachweisen',
    desc: 'Verifikation und Transparenz für messbaren Impact im industriellen Maßstab.',
  },
];

export function Features() {
  return (
    <section id="features" className="section">
      <div className="container">
        <ScrollReveal variant="slide-up">
          <div className="section-header">
            <div className="section-eyebrow">Was wir tun</div>
            <h2 className="section-title">
              Vier Bausteine. <span className="gradient-text-terra">Ein integriertes System.</span>
            </h2>
            <p className="section-sub">
              Von der Abwärme bis zum auditfähigen Nachweis — Terra Nature schließt die Kette.
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
