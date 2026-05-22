'use client';

import Link from 'next/link';
import { ScrollReveal } from './ScrollReveal';

export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-grid">
          <ScrollReveal variant="slide-up" className="footer-brand">
            <h3><span className="gradient-text-terra">Terra Nature</span></h3>
            <p>Deep-Tech for Climate &amp; Industry.</p>
            <div className="footer-social">
              <a href="https://linkedin.com/in/terranature" className="footer-link" aria-label="LinkedIn">LinkedIn</a>
              <a href="https://terranature.io" className="footer-link" aria-label="Website">Website</a>
            </div>
          </ScrollReveal>
          <ScrollReveal variant="slide-up" delay={100} className="footer-col">
            <h4>Navigation</h4>
            <a href="#solution" className="footer-link">Lösung</a>
            <a href="#features" className="footer-link">Features</a>
            <a href="#team" className="footer-link">Team</a>
            <a href="#contact" className="footer-link">Kontakt</a>
            <Link href="/dashboard" className="footer-link">Dashboard</Link>
          </ScrollReveal>
          <ScrollReveal variant="slide-up" delay={200} className="footer-col">
            <h4>Kontakt</h4>
            <p className="footer-meta">Rosenheim · Bayern · Europa</p>
            <a href="mailto:eren@terranature.io" className="footer-link">eren@terranature.io</a>
            <a href="tel:+4915221456897" className="footer-link">+49 152 214 56 897</a>
            <a href="https://linkedin.com/in/terranature" className="footer-link">linkedin.com/in/terranature</a>
          </ScrollReveal>
          <ScrollReveal variant="slide-up" delay={300} className="footer-col">
            <h4>Rechtliches</h4>
            <a href="#" className="footer-link">Datenschutz</a>
            <a href="#" className="footer-link">Impressum</a>
            <a href="#" className="footer-link">AGB</a>
          </ScrollReveal>
        </div>
        <ScrollReveal variant="fade-in" delay={200}>
          <div className="footer-bottom">
            <span>© {year} Terra Nature GmbH · Alle Rechte vorbehalten.</span>
            <span className="footer-powered">
              Powered by <span className="terra-accent">Terraloft</span>
            </span>
          </div>
        </ScrollReveal>
      </div>
    </footer>
  );
}
