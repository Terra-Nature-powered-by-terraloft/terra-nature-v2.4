'use client';

import { ScrollReveal } from './ScrollReveal';

export function DashboardPreview() {
  return (
    <section id="platform" className="section platform">
      <div className="container">
        <ScrollReveal variant="slide-up">
          <div className="section-header">
            <div className="section-eyebrow stats-eyebrow">Platform Preview</div>
            <h2 className="section-title">
              Ihre Daten. <span className="gradient-text-neon">In Echtzeit.</span>
            </h2>
          </div>
        </ScrollReveal>

        <ScrollReveal variant="zoom-in" delay={200}>
          <div className="platform-mockup" aria-hidden>
            <div className="platform-glow" />
            <div className="platform-frame">
              <div className="platform-head">
                <span className="platform-dot" />
                <span className="platform-dot" />
                <span className="platform-dot" />
                <span className="platform-title">Impact Overview</span>
                <span className="platform-tabs">
                  <span>7D</span>
                  <span className="is-active">30D</span>
                  <span>90D</span>
                  <span>1Y</span>
                </span>
              </div>
              <div className="platform-stats">
                <div className="platform-stat">
                  <span className="platform-stat-label">Waste Heat</span>
                  <span className="platform-stat-value">12,8 <em>MWh/t</em></span>
                  <span className="platform-trend">↑ 6,2 %</span>
                </div>
                <div className="platform-stat">
                  <span className="platform-stat-label">CO₂ Avoided</span>
                  <span className="platform-stat-value">2,46 <em>kt</em></span>
                  <span className="platform-trend">↑ 6,7 %</span>
                </div>
                <div className="platform-stat">
                  <span className="platform-stat-label">Efficiency</span>
                  <span className="platform-stat-value">2,31 <em>MWh/t</em></span>
                  <span className="platform-trend">↑ 5,4 %</span>
                </div>
              </div>
              <div className="platform-chart">
                <svg viewBox="0 0 600 160" preserveAspectRatio="none" aria-hidden>
                  <defs>
                    <linearGradient id="chart-fill" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="0%" stopColor="#FF6B35" stopOpacity="0.4" />
                      <stop offset="100%" stopColor="#FF6B35" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                  <path
                    d="M0 120 L60 100 L120 110 L180 80 L240 90 L300 60 L360 70 L420 40 L480 55 L540 30 L600 35 L600 160 L0 160 Z"
                    fill="url(#chart-fill)"
                  />
                  <path
                    d="M0 120 L60 100 L120 110 L180 80 L240 90 L300 60 L360 70 L420 40 L480 55 L540 30 L600 35"
                    fill="none"
                    stroke="#FF6B35"
                    strokeWidth="2.5"
                    strokeLinejoin="round"
                    strokeLinecap="round"
                  />
                </svg>
              </div>
            </div>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
