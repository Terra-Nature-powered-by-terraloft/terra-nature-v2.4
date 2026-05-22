'use client';

import { useParallax } from '@/hooks/useParallax';
import { ScrollReveal } from './ScrollReveal';
import type { AnimationVariant } from '@/lib/animation-config';

const ITEMS = [
  { variant: 'one',   title: 'Stahlwerk · Süd',     sub: 'Hochofen-Abwärme, 4,2 MWh/t Recovery.' },
  { variant: 'two',   title: 'Chemiepark · Ost',    sub: 'Wärmekopplung mit MRV-Verifikation.' },
  { variant: 'three', title: 'Stadtwerke-Verbund',  sub: 'Distrikt-Wärmenetz, 12 Gebäude.' },
  { variant: 'four',  title: 'Datacenter-Loop',     sub: 'Rack-Wärmerückgewinnung, 24/7.' },
];

function GalleryItem({
  variant,
  title,
  sub,
  speed,
}: {
  variant: string;
  title: string;
  sub: string;
  speed: number;
}) {
  // The bg layer is oversized (inset: -10%) so the parallax translate never
  // exposes the underlying card colour at the edges.
  const { ref, offset } = useParallax<HTMLDivElement>(speed);
  return (
    <div className="gallery-item">
      <div
        ref={ref}
        className={`gallery-bg ${variant}`}
        style={{ transform: `translateY(${offset}px) scale(1.1)` }}
        aria-hidden
      />
      <div className="gallery-content">
        <h3>{title}</h3>
        <p>{sub}</p>
      </div>
    </div>
  );
}

export function Gallery() {
  return (
    <section id="gallery" className="section">
      <div className="container">
        <ScrollReveal variant="slide-up">
          <div className="section-header">
            <div className="section-eyebrow">Standorte</div>
            <h2 className="section-title">
              Vier Pilotanlagen. <span className="gradient-text-terra">Ein Nachweis-Layer.</span>
            </h2>
            <p className="section-sub">
              Eine kleine Auswahl der Standorte, die heute in Terra Nature einspeisen.
            </p>
          </div>
        </ScrollReveal>

        <div className="gallery-grid">
          {ITEMS.map((item, i) => {
            // Alternate the entry direction and parallax sign for visual rhythm.
            const reveal: AnimationVariant = i % 2 === 0 ? 'slide-right' : 'slide-left';
            const speed = i % 2 === 0 ? -0.2 : 0.2;
            return (
              <ScrollReveal key={item.title} variant={reveal} delay={i * 100}>
                <GalleryItem {...item} speed={speed} />
              </ScrollReveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
