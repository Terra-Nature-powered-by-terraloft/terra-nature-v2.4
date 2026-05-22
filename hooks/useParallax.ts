'use client';

import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { usePrefersReducedMotion } from './usePrefersReducedMotion';

if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
}

// GSAP-driven parallax. Unlike the old IntersectionObserver version, GSAP
// owns the transform directly via scrub — React never re-renders on scroll,
// and the easing has the slight lag that makes the motion feel weighted.
//
//   speed > 0 → moves down as you scroll past (slower than scroll feel)
//   speed < 0 → moves up as you scroll past (foreground feel)
//
// Disabled below 768px (mobile scroll handoff causes jitter) and under
// prefers-reduced-motion.
export function useParallax<T extends HTMLElement = HTMLDivElement>(speed = 0.3) {
  const ref = useRef<T | null>(null);
  const prefersReduced = usePrefersReducedMotion();

  useEffect(() => {
    if (prefersReduced) return;
    if (typeof window === 'undefined' || window.innerWidth < 768) return;
    const node = ref.current;
    if (!node) return;

    // yPercent is relative to the element's own height — stable across resizes.
    const tween = gsap.to(node, {
      yPercent: speed * 40,
      ease: 'none',
      scrollTrigger: {
        trigger: node,
        start: 'top bottom',
        end: 'bottom top',
        scrub: 1,
      },
    });

    return () => {
      tween.scrollTrigger?.kill();
      tween.kill();
    };
  }, [speed, prefersReduced]);

  return { ref };
}
