'use client';

import { CSSProperties, ReactNode } from 'react';
import { useScrollReveal } from '@/hooks/useScrollReveal';
import type { AnimationVariant } from '@/lib/animation-config';

interface Props {
  variant?: AnimationVariant;
  delay?: number;
  threshold?: number;
  className?: string;
  style?: CSSProperties;
  children: ReactNode;
}

// Wraps children in a div that fades / slides / zooms in when scrolled into
// view. The CSS classes (.scroll-fade-in, .scroll-slide-up, ...) live in
// app/globals.css; this component only orchestrates the trigger.
export function ScrollReveal({
  variant = 'fade-in',
  delay = 0,
  threshold = 0.2,
  className = '',
  style,
  children,
}: Props) {
  const { ref, revealed } = useScrollReveal<HTMLDivElement>({ threshold });
  return (
    <div
      ref={ref}
      className={`scroll-reveal scroll-${variant} ${revealed ? 'is-revealed' : ''} ${className}`.trim()}
      style={{
        ...style,
        transitionDelay: delay ? `${delay}ms` : undefined,
      }}
    >
      {children}
    </div>
  );
}
