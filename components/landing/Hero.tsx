'use client';

import Link from 'next/link';
import { useParallax } from '@/hooks/useParallax';
import { ScrollReveal } from './ScrollReveal';

export function Hero() {
  // Two gradient blobs scroll at different rates to create depth without
  // relying on a heavy background image.
  const blob1 = useParallax<HTMLDivElement>(-0.4);
  const blob2 = useParallax<HTMLDivElement>(0.25);

  return (
    <section className="hero">
      <div className="hero-bg" />
      <div
        ref={blob1.ref}
        className="hero-bg-blob one"
        style={{ transform: `translateY(${blob1.offset}px)` }}
        aria-hidden
      />
      <div
        ref={blob2.ref}
        className="hero-bg-blob two"
        style={{ transform: `translateY(${blob2.offset}px)` }}
        aria-hidden
      />

      <div className="hero-content">
        <ScrollReveal variant="fade-in">
          <span className="hero-eyebrow">Powered by Terraloft · v2.4</span>
        </ScrollReveal>
        <ScrollReveal variant="slide-up" delay={120}>
          <h1>
            Real-time energy intelligence,<br />
            <span className="accent gradient-text-terra">grounded in nature.</span>
          </h1>
        </ScrollReveal>
        <ScrollReveal variant="slide-up" delay={260}>
          <p className="hero-sub">
            Terra Nature streams live metrics from your site so you can see — and act on — every
            kilowatt-hour, in time to make it matter.
          </p>
        </ScrollReveal>
        <ScrollReveal variant="slide-up" delay={400}>
          <div className="hero-cta">
            <Link href="/dashboard" className="btn btn-primary">
              Open live dashboard <span aria-hidden>→</span>
            </Link>
            <a href="#features" className="btn btn-secondary">See what&apos;s inside</a>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
