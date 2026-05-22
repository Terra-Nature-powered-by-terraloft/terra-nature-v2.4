// Centralized animation tokens. Adjust these to retune the whole site
// without touching individual components.

export const ANIMATION_CONFIG = {
  duration: {
    fast: 400,
    medium: 700,
    slow: 1200,
    counter: 2500,
  },
  easing: {
    out: 'cubic-bezier(0.16, 1, 0.3, 1)',
    inOut: 'cubic-bezier(0.65, 0, 0.35, 1)',
    organic: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    linear: 'linear',
  },
  stagger: {
    tight: 80,
    base: 150,
    loose: 250,
  },
  threshold: {
    early: 0.05,
    base: 0.2,
    late: 0.45,
  },
  parallax: {
    subtle: 0.15,
    medium: 0.35,
    strong: 0.6,
  },
  breakpoints: {
    mobile: 768,
    tablet: 1024,
    desktop: 1440,
  },
} as const;

export type AnimationVariant =
  | 'fade-in'
  | 'slide-up'
  | 'slide-down'
  | 'slide-left'
  | 'slide-right'
  | 'zoom-in'
  | 'blur-in'
  | 'rotate-in';
