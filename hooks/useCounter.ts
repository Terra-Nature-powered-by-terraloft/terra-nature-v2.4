'use client';

import { useEffect, useRef, useState } from 'react';
import { usePrefersReducedMotion } from './usePrefersReducedMotion';

interface Options {
  duration?: number;
  start?: boolean;
  decimals?: number;
}

// Eases a number from 0 → target over `duration` ms once `start` flips true.
// Uses easeOutQuad so it reaches near-final quickly then settles.
export function useCounter(target: number, options: Options = {}) {
  const { duration = 2500, start = true, decimals = 0 } = options;
  const [value, setValue] = useState(0);
  const prefersReduced = usePrefersReducedMotion();
  const startTime = useRef<number | null>(null);

  useEffect(() => {
    if (!start) return;
    if (prefersReduced) {
      setValue(target);
      return;
    }

    let frame = 0;
    startTime.current = null;

    const step = (now: number) => {
      if (startTime.current === null) startTime.current = now;
      const elapsed = now - startTime.current;
      const t = Math.min(elapsed / duration, 1);
      const eased = 1 - (1 - t) * (1 - t); // easeOutQuad
      setValue(Number((target * eased).toFixed(decimals)));
      if (t < 1) frame = requestAnimationFrame(step);
    };

    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame);
  }, [target, duration, start, decimals, prefersReduced]);

  return value;
}
