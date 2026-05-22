'use client';

import { ScrollReveal } from './ScrollReveal';
import type { AnimationVariant } from '@/lib/animation-config';

const TEAM = [
  {
    initials: 'EY',
    name: 'Eren Yergezen',
    role: 'CEO & Founder',
    bio: 'Energietechnik · Software · MRV',
    personal:
      'Eren Yergezen durchlief eine prägende und schwierige Lebensphase. In dieser Zeit schrieb er das Buch „Ich & Ich“ mit 21 Kapiteln. Im Laufe dieses persönlichen und kreativen Prozesses entstand auch Terra Nature.',
  },
  {
    initials: 'YU',
    name: 'Yener Uysal',
    role: 'Assistant & Unterstützung',
    bio: 'Organisation · Umsetzung · Support',
    personal:
      'Er ist ein begeisterter Musiker mit großer Leidenschaft für künstlerischen Ausdruck und Ästhetik.',
  },
];

export function Team() {
  return (
    <section id="team" className="section">
      <div className="container">
        <ScrollReveal variant="slide-up">
          <div className="section-header">
            <div className="section-eyebrow">Unser Team</div>
            <h2 className="section-title">
              Die Menschen hinter <span className="gradient-text-terra">Terra Nature</span>.
            </h2>
            <p className="section-sub">
              Ein kleines Team aus Rosenheim. Energietechnik, Software und MRV-Nachweis unter
              einem Dach.
            </p>
          </div>
        </ScrollReveal>

        <div className="team-grid">
          {TEAM.map((m, i) => {
            // Outer members slide in from the side they sit on.
            const reveal: AnimationVariant = i === 0 ? 'slide-right' : 'slide-left';
            return (
              <ScrollReveal key={m.name} variant={reveal} delay={i * 150}>
                <article className="team-member">
                  <div className="team-avatar" aria-hidden>{m.initials}</div>
                  <h3>{m.name}</h3>
                  <p className="team-role">{m.role}</p>
                  <p className="team-bio">{m.bio}</p>
                  <div className="team-personal">
                    <span className="team-personal-tag">Persönlich</span>
                    <p>{m.personal}</p>
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
