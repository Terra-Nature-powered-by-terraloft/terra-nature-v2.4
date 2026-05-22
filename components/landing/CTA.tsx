'use client';

import Link from 'next/link';
import { ScrollReveal } from './ScrollReveal';

export function CTA() {
  return (
    <section className="section">
      <div className="container">
        <ScrollReveal variant="zoom-in">
          <div className="cta-banner">
            <h2>Ready to see your site live?</h2>
            <p>Open the dashboard and start streaming metrics in under a minute.</p>
            <Link href="/dashboard" className="btn">Open dashboard →</Link>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
