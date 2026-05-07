/**
 * Dashboard Integration - Embed Kappa Orb Widget into Terra Dashboard
 * Provides seamless access to Kappa from the main dashboard
 */

'use client';

import React from 'react';
import { useMetrics } from '@/hooks/useMetrics';
import { useKappaOrb } from '@/app/kappa-ui/hooks/useKappaOrb';
import {
  extractMetricContext,
  formatMetricContextForKappa,
  recommendExpertMode,
  checkMetricAnomalies,
} from './terra-metrics-bridge';

interface KappaDashboardWidgetProps {
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left' | 'inline';
  autoModeSelection?: boolean;
  showMetricContext?: boolean;
}

/**
 * Compact Kappa Widget for embedding in Dashboard
 */
export function KappaDashboardWidget({
  position = 'bottom-right',
  autoModeSelection = true,
  showMetricContext = true,
}: KappaDashboardWidgetProps) {
  const { data: metric } = useMetrics();
  const {
    isListening,
    isProcessing,
    response,
    error,
    isHealthy,
    startListening,
    stopListening,
    clearResponse,
    query,
  } = useKappaOrb();

  const [showPanel, setShowPanel] = React.useState(false);
  const [selectedMode, setSelectedMode] = React.useState('default');

  // Auto-select mode based on metrics
  React.useEffect(() => {
    if (autoModeSelection && metric) {
      const mode = recommendExpertMode(metric);
      setSelectedMode(mode);
    }
  }, [metric, autoModeSelection]);

  // Check for metric anomalies
  React.useEffect(() => {
    if (metric) {
      const anomalies = checkMetricAnomalies(metric, []);
      if (anomalies.length > 0) {
        const anomalyStatement = `Anomalien erkannt: ${anomalies.join('; ')}`;
        // Could auto-query Kappa with anomaly
      }
    }
  }, [metric]);

  const positionStyles: Record<string, React.CSSProperties> = {
    'bottom-right': { bottom: '20px', right: '20px' },
    'bottom-left': { bottom: '20px', left: '20px' },
    'top-right': { top: '20px', right: '20px' },
    'top-left': { top: '20px', left: '20px' },
    inline: { position: 'relative' as const, width: '100%' },
  };

  if (position === 'inline') {
    return (
      <div style={{ margin: '20px 0' }}>
        <div
          style={{
            backgroundColor: '#f8f9fa',
            border: '1px solid #e0e0e0',
            borderRadius: '8px',
            padding: '16px',
          }}
        >
          <h3 style={{ margin: '0 0 12px 0', color: '#333' }}>🔮 Kappa Orb Mini</h3>

          <div style={{ marginBottom: '12px' }}>
            <button
              onClick={() => (isListening ? stopListening() : startListening())}
              style={{
                padding: '8px 16px',
                backgroundColor: isListening ? '#ef4444' : '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '13px',
              }}
              disabled={isProcessing}
            >
              {isListening ? '🎤 Stopp' : '🎤 Sprechen'}
            </button>

            {isHealthy && (
              <span
                style={{
                  marginLeft: '8px',
                  fontSize: '12px',
                  color: '#22c55e',
                }}
              >
                ✅ Kappa Online
              </span>
            )}
          </div>

          {showMetricContext && metric && (
            <div
              style={{
                backgroundColor: '#f0f9ff',
                border: '1px solid #bfdbfe',
                borderRadius: '4px',
                padding: '8px',
                fontSize: '11px',
                color: '#0c4a6e',
                marginBottom: '12px',
                maxHeight: '100px',
                overflowY: 'auto',
              }}
            >
              <strong>📊 Metriken Kontext:</strong>
              <div>{formatMetricContextForKappa(metric)}</div>
            </div>
          )}

          {response && (
            <div
              style={{
                backgroundColor: '#f0fdf4',
                border: '1px solid #bbf7d0',
                borderRadius: '4px',
                padding: '8px',
                fontSize: '12px',
                color: '#166534',
              }}
            >
              <strong>Antwort:</strong> {response.substring(0, 100)}...
              {response.length > 100 && (
                <button
                  onClick={() => setShowPanel(true)}
                  style={{
                    display: 'block',
                    marginTop: '6px',
                    padding: '4px 8px',
                    backgroundColor: 'transparent',
                    border: '1px solid #bbf7d0',
                    borderRadius: '2px',
                    cursor: 'pointer',
                    fontSize: '11px',
                    color: '#166534',
                  }}
                >
                  Vollständige Antwort anzeigen →
                </button>
              )}
            </div>
          )}

          {error && (
            <div
              style={{
                backgroundColor: '#fef2f2',
                border: '1px solid #fecaca',
                borderRadius: '4px',
                padding: '8px',
                fontSize: '12px',
                color: '#dc2626',
                marginTop: '8px',
              }}
            >
              ⚠️ {error.substring(0, 60)}...
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setShowPanel(!showPanel)}
        style={{
          position: 'fixed',
          ...positionStyles[position],
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          backgroundColor: isHealthy ? '#667eea' : '#ef4444',
          color: 'white',
          border: 'none',
          fontSize: '28px',
          cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          animation: isProcessing ? 'pulse 1s infinite' : 'none',
          zIndex: 1000,
          transition: 'all 0.2s ease',
          '&:hover': {
            transform: 'scale(1.1)',
          },
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.1)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
        }}
      >
        🔮
      </button>

      {/* Floating Panel */}
      {showPanel && (
        <div
          style={{
            position: 'fixed',
            ...positionStyles[position],
            width: '380px',
            maxHeight: '600px',
            backgroundColor: '#ffffff',
            borderRadius: '12px',
            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)',
            zIndex: 1001,
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            fontFamily: 'system-ui, -apple-system, sans-serif',
          }}
        >
          {/* Panel Header */}
          <div
            style={{
              padding: '16px',
              borderBottom: '1px solid #e0e0e0',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <h3 style={{ margin: 0, fontSize: '16px', color: '#333' }}>
              🔮 Kappa Orb
            </h3>
            <button
              onClick={() => setShowPanel(false)}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '20px',
                cursor: 'pointer',
              }}
            >
              ✕
            </button>
          </div>

          {/* Panel Content */}
          <div style={{ flex: 1, overflow: 'auto', padding: '16px' }}>
            {/* Health Status */}
            <div
              style={{
                marginBottom: '12px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
              }}
            >
              <div
                style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  backgroundColor: isHealthy ? '#22c55e' : '#ef4444',
                }}
              />
              <span style={{ fontSize: '12px', color: '#666' }}>
                {isHealthy ? 'Kappa Online' : 'Kappa Offline'}
              </span>
            </div>

            {/* Metric Context */}
            {showMetricContext && metric && (
              <div
                style={{
                  backgroundColor: '#f9fafb',
                  border: '1px solid #e5e7eb',
                  borderRadius: '6px',
                  padding: '12px',
                  marginBottom: '12px',
                  fontSize: '12px',
                  color: '#555',
                }}
              >
                <strong>📊 Kontext:</strong>
                <div style={{ marginTop: '6px', fontSize: '11px' }}>
                  {formatMetricContextForKappa(metric)}
                </div>
              </div>
            )}

            {/* Response */}
            {response && (
              <div
                style={{
                  backgroundColor: '#f0fdf4',
                  border: '1px solid #bbf7d0',
                  borderRadius: '6px',
                  padding: '12px',
                  fontSize: '13px',
                  color: '#166534',
                  marginBottom: '12px',
                }}
              >
                <strong>✅ Antwort:</strong>
                <p style={{ margin: '8px 0 0 0', lineHeight: '1.4' }}>
                  {response}
                </p>
                <button
                  onClick={clearResponse}
                  style={{
                    marginTop: '8px',
                    padding: '4px 8px',
                    backgroundColor: 'transparent',
                    border: '1px solid #bbf7d0',
                    borderRadius: '3px',
                    cursor: 'pointer',
                    fontSize: '11px',
                    color: '#166534',
                  }}
                >
                  Löschen
                </button>
              </div>
            )}

            {/* Error */}
            {error && (
              <div
                style={{
                  backgroundColor: '#fef2f2',
                  border: '1px solid #fecaca',
                  borderRadius: '6px',
                  padding: '12px',
                  fontSize: '12px',
                  color: '#dc2626',
                }}
              >
                ⚠️ {error}
              </div>
            )}
          </div>

          {/* Panel Footer */}
          <div
            style={{
              padding: '12px 16px',
              borderTop: '1px solid #e0e0e0',
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px',
            }}
          >
            <button
              onClick={() => (isListening ? stopListening() : startListening())}
              disabled={isProcessing}
              style={{
                padding: '8px',
                backgroundColor: isListening ? '#ef4444' : '#10b981',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: isProcessing ? 'not-allowed' : 'pointer',
                fontSize: '12px',
              }}
            >
              {isListening ? '🎤 Stopp' : '🎤 Sprechen'}
            </button>
            <a
              href="/kappa-ui"
              style={{
                padding: '8px',
                backgroundColor: '#667eea',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '12px',
                textAlign: 'center',
                textDecoration: 'none',
              }}
            >
              Orb starten
            </a>
          </div>
        </div>
      )}
    </>
  );
}
