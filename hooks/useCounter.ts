'use client';

import { useEffect, useState } from 'react';
import gsap from 'gsap';
import { usePrefersReducedMotion } from './usePrefersReducedMotion';

interface Options {
  // Duration in SECONDS (GSAP convention, not milliseconds).
  duration?: number;
  start?: boolean;
  decimals?: number;
}

// Eases a number from 0 → target via gsap.to + onUpdate. We tween a plain
// object, then push each frame's value into React state so the display
// re-renders. Cleaner than rolling our own requestAnimationFrame loop and
// gets us free easing curves.
export function useCounter(target: number, options: Options = {}) {
  const { duration = 2.5, start = true, decimals = 0 } = options;
  const [value, setValue] = useState(0);
  const prefersReduced = usePrefersReducedMotion();

  useEffect(() => {
    if (!start) return;
    if (prefersReduced) {
      setValue(target);
      return;
    }

    const obj = { v: 0 };
    const tween = gsap.to(obj, {
      v: target,
      duration,
      ease: 'power2.out',
      onUpdate: () => {
        setValue(Number(obj.v.toFixed(decimals)));
      },
    });

    return () => {
      tween.kill();
    };
  }, [target, duration, start, decimals, prefersReduced]);

  return value;
}
