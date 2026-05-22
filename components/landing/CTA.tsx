'use client';

import { ScrollReveal } from './ScrollReveal';

export function CTA() {
  return (
    <section id="contact" className="section">
      <div className="container">
        <ScrollReveal variant="zoom-in">
          <div className="cta-banner">
            <h2>Bereit für die Zukunft?</h2>
            <p>
              Treten Sie Terra Nature bei und transformieren Sie Ihre Industrie — von Abwärme zu
              messbarem Impact.
            </p>
            <div className="cta-buttons">
              <a href="mailto:eren@terranature.io" className="btn">
                Kontaktieren Sie uns <span aria-hidden>→</span>
              </a>
              <a href="#platform" className="btn btn-ghost-on-dark">Demo anfragen</a>
            </div>
            <ul className="cta-contact">
              <li>
                <span aria-hidden>✉️</span>
                <a href="mailto:eren@terranature.io">eren@terranature.io</a>
              </li>
              <li>
                <span aria-hidden>📞</span>
                <a href="tel:+4915221456897">+49 152 214 56 897</a>
              </li>
              <li>
                <span aria-hidden>🌐</span>
                <a href="https://terranature.io">terranature.io</a>
              </li>
            </ul>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
