'use client';

import Link from 'next/link';
import { useParallax } from '@/hooks/useParallax';
import { ScrollReveal } from './ScrollReveal';

export function Hero() {
  // Two gradient blobs scrub at different rates to create depth without
  // shipping a heavy background image. GSAP owns the transform via the
  // useParallax hook, so React doesn't re-render on scroll.
  const blob1 = useParallax<HTMLDivElement>(-0.4);
  const blob2 = useParallax<HTMLDivElement>(0.25);

  return (
    <section className="hero">
      <div className="hero-bg" />
      <div ref={blob1.ref} className="hero-bg-blob one" aria-hidden />
      <div ref={blob2.ref} className="hero-bg-blob two" aria-hidden />

      <div className="hero-content">
        <ScrollReveal variant="fade-in">
          <span className="hero-eyebrow">Deep-Tech for Climate &amp; Industry</span>
        </ScrollReveal>
        <ScrollReveal variant="slide-up" delay={120}>
          <h1>
            Abwärme zu <span className="gradient-text-terra">Energie</span>.<br />
            Energie zu <span className="gradient-text-terra">Nachweis</span>.<br />
            Nachweis zu <span className="gradient-text-terra">Vertrauen</span>.
          </h1>
        </ScrollReveal>
        <ScrollReveal variant="slide-up" delay={260}>
          <p className="hero-sub">
            Terra Nature wandelt industrielle Abwärme in Strom, nutzbare Wärme und digitale
            Nachweise um — Infrastruktur für Industrie, Stadtwerke und emissionsintensive
            Standorte.
          </p>
        </ScrollReveal>
        <ScrollReveal variant="slide-up" delay={400}>
          <div className="hero-cta">
            <Link href="/dashboard" className="btn btn-primary">
              Jetzt starten <span aria-hidden>→</span>
            </Link>
            <a href="#features" className="btn btn-secondary">Mehr erfahren</a>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
