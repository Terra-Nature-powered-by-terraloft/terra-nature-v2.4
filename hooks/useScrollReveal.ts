'use client';

import { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { usePrefersReducedMotion } from './usePrefersReducedMotion';

// Idempotent — GSAP guards internally against double registration.
if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
}

interface Options {
  threshold?: number;
  once?: boolean;
}

// GSAP ScrollTrigger wrapped in a React-friendly hook.
// `revealed` flips to true when the element enters the viewport — the CSS
// reveal classes in globals.css watch for the .is-revealed flag this drives.
export function useScrollReveal<T extends HTMLElement = HTMLDivElement>(
  options: Options = {}
) {
  const { threshold = 0.2, once = true } = options;
  const ref = useRef<T | null>(null);
  const [revealed, setRevealed] = useState(false);
  const prefersReduced = usePrefersReducedMotion();

  useEffect(() => {
    if (prefersReduced) {
      setRevealed(true);
      return;
    }
    const node = ref.current;
    if (!node) return;

    // start: "top X%" — fires when the element's top crosses X% down the viewport.
    // threshold 0.2 → start at 80% (i.e. element 20% into view from the bottom).
    const startPos = `top ${Math.round((1 - threshold) * 100)}%`;

    const trigger = ScrollTrigger.create({
      trigger: node,
      start: startPos,
      once,
      onEnter: () => setRevealed(true),
      onLeaveBack: once ? undefined : () => setRevealed(false),
    });

    return () => {
      trigger.kill();
    };
  }, [threshold, once, prefersReduced]);

  return { ref, revealed };
}
