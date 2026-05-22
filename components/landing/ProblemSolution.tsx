'use client';

import { ScrollReveal } from './ScrollReveal';

export function ProblemSolution() {
  return (
    <section id="solution" className="section solution">
      <div className="container">
        <div className="solution-grid">
          <ScrollReveal variant="slide-right" className="solution-text">
            <div className="section-eyebrow">Das Problem</div>
            <h2 className="section-title section-title--left">
              Unsere Abwärme geht <span className="gradient-text-terra">bisher verloren</span>.
            </h2>
            <div className="accent-bar" />
            <p>
              Terra Nature ist ein integriertes Deep-Tech-System, das industrielle Abwärme in
              Strom, nutzbare Wärme und digitale Nachweise umwandelt.
            </p>
            <p>
              Wir verbinden Energieumwandlung, Wärmerückführung und MRV-Nachweisführung zu
              einer Infrastruktur für Industrie, Stadtwerke und emissionsintensive Standorte.
            </p>
          </ScrollReveal>
          <ScrollReveal variant="slide-left" delay={150} className="solution-flow">
            <div className="flow-quote">
              <div className="flow-icon" aria-hidden>〰️</div>
              <p>„Unsere Abwärme geht bisher verloren.“</p>
            </div>
            <div className="flow-arrow" aria-hidden>
              <svg viewBox="0 0 24 48" width="24" height="48" role="img" aria-label="">
                <path
                  d="M12 4 V42 M6 36 L12 44 L18 36"
                  stroke="currentColor"
                  strokeWidth="2"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div className="flow-result">
              <div className="flow-icon flow-icon--filled" aria-hidden>⚡</div>
              <p>
                Terra Nature macht daraus <strong>Strom, Wärme und digitale Nachweise</strong>.
              </p>
            </div>
          </ScrollReveal>
        </div>
      </div>
    </section>
  );
}
