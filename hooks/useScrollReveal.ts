'use client';

import { useEffect, useRef, useState } from 'react';
import { usePrefersReducedMotion } from './usePrefersReducedMotion';

interface Options {
  threshold?: number;
  rootMargin?: string;
  once?: boolean;
}

// IntersectionObserver-based hook that flips `revealed` to true when the
// target enters the viewport. Drives every fade / slide / zoom reveal.
export function useScrollReveal<T extends HTMLElement = HTMLDivElement>(
  options: Options = {}
) {
  const { threshold = 0.2, rootMargin = '0px 0px -10% 0px', once = true } = options;
  const ref = useRef<T | null>(null);
  const [revealed, setRevealed] = useState(false);
  const prefersReduced = usePrefersReducedMotion();

  useEffect(() => {
    // Reduced-motion users see the final state immediately.
    if (prefersReduced) {
      setRevealed(true);
      return;
    }

    const node = ref.current;
    if (!node) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setRevealed(true);
          if (once) observer.unobserve(entry.target);
        } else if (!once) {
          setRevealed(false);
        }
      },
      { threshold, rootMargin }
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, [threshold, rootMargin, once, prefersReduced]);

  return { ref, revealed };
}
