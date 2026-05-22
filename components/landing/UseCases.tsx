'use client';

import { ScrollReveal } from './ScrollReveal';
import type { AnimationVariant } from '@/lib/animation-config';

const CASES = [
  {
    tag: '01',
    visual: 'one',
    title: 'Industrie & Produktion',
    desc:
      'Zement-, Stahl- und Chemiewerke mit hoher Abwärme profitieren von direkter Energierückgewinnung und digitaler MRV-Dokumentation.',
  },
  {
    tag: '02',
    visual: 'two',
    title: 'Stadtwerke & Energieversorger',
    desc:
      'Integration in bestehende Wärmenetze mit Echtzeit-Monitoring und transparenter Nachweisführung.',
  },
  {
    tag: '03',
    visual: 'three',
    title: 'Emissionsintensive Standorte',
    desc:
      'Skalierbare Systeme für Unternehmen, die ihre Emissionen reduzieren und digital dokumentieren müssen.',
  },
];

export function UseCases() {
  return (
    <section id="use-cases" className="section">
      <div className="container">
        <ScrollReveal variant="slide-up">
          <div className="section-header">
            <div className="section-eyebrow">Anwendungen</div>
            <h2 className="section-title">
              Wo <span className="gradient-text-terra">Terra Nature</span> wirkt.
            </h2>
          </div>
        </ScrollReveal>

        <div className="usecases">
          {CASES.map((c, i) => {
            const reversed = i % 2 === 1;
            const reveal: AnimationVariant = reversed ? 'slide-left' : 'slide-right';
            return (
              <ScrollReveal key={c.title} variant={reveal} delay={i * 100}>
                <article className={`usecase ${reversed ? 'usecase--reverse' : ''}`}>
                  <div className={`usecase-visual usecase-visual--${c.visual}`} aria-hidden>
                    <span className="usecase-tag">{c.tag}</span>
                  </div>
                  <div className="usecase-text">
                    <h3>{c.title}</h3>
                    <p>{c.desc}</p>
                    <a href="#contact" className="link-arrow">
                      Mehr erfahren <span aria-hidden>→</span>
                    </a>
                  </div>
                </article>
              </ScrollReveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
