'use client';

import { ScrollReveal } from './ScrollReveal';

const STEPS = [
  {
    icon: '〰️',
    title: 'Abwärme zurückgewinnen',
    desc: 'Industrielle Abwärme wird erfasst und in nutzbare Energie umgewandelt.',
  },
  {
    icon: '⚡',
    title: 'Energie messbar machen',
    desc: 'Strom und Wärme werden in Echtzeit dokumentiert.',
  },
  {
    icon: '📋',
    title: 'Nachweise digital verankern',
    desc: 'MRV-konforme Zertifikate und Berichte — auditierbar und transparent.',
  },
];

export function ProcessFlow() {
  return (
    <section id="process" className="section">
      <div className="container">
        <ScrollReveal variant="slide-up">
          <div className="section-header">
            <div className="section-eyebrow">Unser Ansatz</div>
            <h2 className="section-title">
              Von Abwärme zu <span className="gradient-text-terra">Vertrauen</span>.
            </h2>
          </div>
        </ScrollReveal>

        <div className="process-grid">
          {STEPS.map((s, i) => (
            <ScrollReveal key={s.title} variant="slide-up" delay={i * 150}>
              <article className="process-step">
                <div className="process-num">{String(i + 1).padStart(2, '0')}</div>
                <div className="process-icon" aria-hidden>{s.icon}</div>
                <h3>{s.title}</h3>
                <p>{s.desc}</p>
              </article>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
}
