'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

export function Navigation() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Lock body scroll while the mobile drawer is open.
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  const close = () => setOpen(false);

  return (
    <nav className={`nav ${scrolled ? 'is-scrolled' : ''}`} aria-label="Hauptnavigation">
      <div className="nav-inner">
        <a href="#" className="nav-logo">
          <span className="gradient-text-terra">Terra Nature</span>
        </a>
        <button
          className="nav-toggle"
          aria-expanded={open}
          aria-label={open ? 'Menü schließen' : 'Menü öffnen'}
          onClick={() => setOpen((v) => !v)}
        >
          <span />
        </button>
        <div className={`nav-links ${open ? 'is-open' : ''}`}>
          <a className="nav-link" href="#features" onClick={close}>Features</a>
          <a className="nav-link" href="#impact" onClick={close}>Impact</a>
          <a className="nav-link" href="#gallery" onClick={close}>Standorte</a>
          <a className="nav-link" href="#team" onClick={close}>Team</a>
          <Link className="nav-link" href="/dashboard" onClick={close}>Dashboard</Link>
        </div>
      </div>
    </nav>
  );
}
