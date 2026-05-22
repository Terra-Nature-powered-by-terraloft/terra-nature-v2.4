'use client';

import { useEffect, useRef, useState } from 'react';
import { usePrefersReducedMotion } from './usePrefersReducedMotion';

// Per-element scroll parallax. Returns a pixel offset based on the
// element's distance from viewport center. Apply via translateY.
//
//   speed < 1   → slower than scroll (background feel)
//   speed > 1   → faster than scroll (foreground feel)
//   speed < 0   → moves opposite to scroll direction
//
// Parallax is disabled below 768px (it stutters on mobile scroll handoff)
// and under prefers-reduced-motion.
export function useParallax<T extends HTMLElement = HTMLDivElement>(speed = 0.3) {
  const ref = useRef<T | null>(null);
  const [offset, setOffset] = useState(0);
  const prefersReduced = usePrefersReducedMotion();

  useEffect(() => {
    if (prefersReduced) return;
    if (typeof window === 'undefined' || window.innerWidth < 768) return;

    const node = ref.current;
    if (!node) return;

    let frame = 0;
    const update = () => {
      const rect = node.getBoundingClientRect();
      const viewportH = window.innerHeight;
      // Distance from viewport center, normalised to roughly [-1, 1].
      const fromCenter = (rect.top + rect.height / 2 - viewportH / 2) / viewportH;
      setOffset(fromCenter * 100 * speed);
      frame = 0;
    };

    const onScroll = () => {
      if (frame) return;
      frame = requestAnimationFrame(update);
    };

    update();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    return () => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onScroll);
      if (frame) cancelAnimationFrame(frame);
    };
  }, [speed, prefersReduced]);

  return { ref, offset };
}
