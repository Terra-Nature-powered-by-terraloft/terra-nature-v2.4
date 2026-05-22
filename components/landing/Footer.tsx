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
            <p>Real-time energy intelligence, grounded in nature.</p>
          </ScrollReveal>
          <ScrollReveal variant="slide-up" delay={100} className="footer-col">
            <h4>Product</h4>
            <a href="#features" className="footer-link">Features</a>
            <a href="#impact" className="footer-link">Impact</a>
            <Link href="/dashboard" className="footer-link">Dashboard</Link>
          </ScrollReveal>
          <ScrollReveal variant="slide-up" delay={200} className="footer-col">
            <h4>Resources</h4>
            <a href="#gallery" className="footer-link">Sites</a>
            <a href="/api/export?format=csv&minutes=1440" className="footer-link">Export CSV</a>
            <a href="/api/export?format=jsonl&minutes=1440" className="footer-link">Export JSONL</a>
          </ScrollReveal>
          <ScrollReveal variant="slide-up" delay={300} className="footer-col">
            <h4>Company</h4>
            <a href="#" className="footer-link">About</a>
            <a href="#" className="footer-link">Security</a>
            <a href="#" className="footer-link">Contact</a>
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
