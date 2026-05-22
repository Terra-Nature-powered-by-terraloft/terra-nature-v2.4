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
            <p>Turning waste heat into measurable impact.</p>
            <p className="footer-meta">Rosenheim · Bayern · Europa</p>
          </ScrollReveal>
          <ScrollReveal variant="slide-up" delay={100} className="footer-col">
            <h4>Produkt</h4>
            <a href="#features" className="footer-link">Features</a>
            <a href="#impact" className="footer-link">Impact</a>
            <Link href="/dashboard" className="footer-link">Dashboard</Link>
          </ScrollReveal>
          <ScrollReveal variant="slide-up" delay={200} className="footer-col">
            <h4>Ressourcen</h4>
            <a href="#gallery" className="footer-link">Standorte</a>
            <a href="/api/export?format=csv&minutes=1440" className="footer-link">CSV Export</a>
            <a href="/api/export?format=jsonl&minutes=1440" className="footer-link">JSONL Export</a>
          </ScrollReveal>
          <ScrollReveal variant="slide-up" delay={300} className="footer-col">
            <h4>Kontakt</h4>
            <a href="https://terranature.io" className="footer-link">terranature.io</a>
            <a href="https://linkedin.com/company/terranature" className="footer-link">LinkedIn</a>
            <a href="#team" className="footer-link">Team</a>
          </ScrollReveal>
        </div>
        <ScrollReveal variant="fade-in" delay={200}>
          <div className="footer-bottom">
            <span>© {year} Terra Nature · powered by Terraloft</span>
            <span>v2.4</span>
          </div>
        </ScrollReveal>
      </div>
    </footer>
  );
}
