'use client';

import Link from 'next/link';
import { ScrollReveal } from './ScrollReveal';

export function CTA() {
  return (
    <section className="section">
      <div className="container">
        <ScrollReveal variant="zoom-in">
          <div className="cta-banner">
            <h2>Bereit für die Zukunft?</h2>
            <p>
              Treten Sie Terra Nature bei und transformieren Sie Ihre Industrie — von Abwärme zu
              messbarem Impact.
            </p>
            <Link href="/dashboard" className="btn">Dashboard öffnen →</Link>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
