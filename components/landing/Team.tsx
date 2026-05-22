'use client';

import { ScrollReveal } from './ScrollReveal';
import type { AnimationVariant } from '@/lib/animation-config';

const TEAM = [
  {
    initials: 'EY',
    name: 'Eren Yergezen',
    role: 'CEO & Founder',
    bio: 'Energietechnik · Software · MRV',
  },
  {
    initials: 'YU',
    name: 'Yener Uysal',
    role: 'Assistant & Unterstützung',
    bio: 'Organisation · Umsetzung · Support',
  },
];

export function Team() {
  return (
    <section id="team" className="section">
      <div className="container">
        <ScrollReveal variant="slide-up">
          <div className="section-header">
            <div className="section-eyebrow">Team</div>
            <h2 className="section-title">
              Wer hinter <span className="gradient-text-terra">Terra Nature</span> steht.
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
                </article>
              </ScrollReveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
