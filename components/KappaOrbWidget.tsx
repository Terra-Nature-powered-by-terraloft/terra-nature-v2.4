/**
 * KappaOrbWidget - Visual interface for Kappa Expert Engine
 * Displays orb animation, handles voice input, and shows responses
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useKappaOrb } from '@/app/kappa-ui/hooks/useKappaOrb';

interface KappaOrbWidgetProps {
  compact?: boolean;
  embedded?: boolean;
  initialMode?: string;
}

export default function KappaOrbWidget({
  compact = false,
  embedded = false,
  initialMode = 'default',
}: KappaOrbWidgetProps) {
  const {
    isListening,
    isProcessing,
    response,
    error,
    isHealthy,
    validationResult,
    startListening,
    stopListening,
    clearResponse,
    checkHealth,
    query,
  } = useKappaOrb();

  const [mode, setMode] = useState(initialMode);
  const [inputText, setInputText] = useState('');
  const [showValidation, setShowValidation] = useState(false);

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, [checkHealth]);

  const handleTextQuery = async () => {
    if (inputText.trim()) {
      await query(inputText, mode);
      setInputText('');
    }
  };

  const handleVoiceToggle = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  if (compact) {
    return (
      <div
        style={{
          display: 'flex',
          gap: '8px',
          alignItems: 'center',
          padding: '8px',
          borderRadius: '8px',
          backgroundColor: '#f9fafb',
          border: '1px solid #e5e7eb',
        }}
      >
        <button
          onClick={handleVoiceToggle}
          disabled={isProcessing}
          style={{
            padding: '6px 12px',
            backgroundColor: isListening ? '#ef4444' : '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isProcessing ? 'not-allowed' : 'pointer',
            fontSize: '12px',
            fontWeight: '500',
          }}
        >
          {isListening ? '🎤 Stopp' : '🎤 Sprechen'}
        </button>

        <div
          style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: isHealthy ? '#22c55e' : '#ef4444',
            animation: isHealthy && isProcessing ? 'pulse 1s infinite' : 'none',
          }}
        />

        {response && (
          <span style={{ fontSize: '12px', color: '#4b5563', flex: 1 }}>{response.substring(0, 50)}...</span>
        )}
      </div>
    );
  }

  return (
    <div
      style={{
        maxWidth: embedded ? '100%' : '600px',
        margin: embedded ? '0' : '0 auto',
        padding: '24px',
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        boxShadow: embedded ? 'none' : '0 4px 6px rgba(0, 0, 0, 0.1)',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '24px',
          paddingBottom: '16px',
          borderBottom: '2px solid #e5e7eb',
        }}
      >
        <div>
          <h2 style={{ margin: '0 0 4px 0', color: '#1f2937', fontSize: '20px' }}>
            🔮 Kappa Orb
          </h2>
          <p style={{ margin: 0, color: '#6b7280', fontSize: '12px' }}>
            Terra Nature Expert Assistant
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div
            style={{
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              backgroundColor: isHealthy ? '#22c55e' : '#ef4444',
              animation: isHealthy ? 'pulse 2s infinite' : 'none',
            }}
          />
          <span style={{ fontSize: '12px', fontWeight: '500', color: isHealthy ? '#22c55e' : '#ef4444' }}>
            {isHealthy ? 'ONLINE' : 'OFFLINE'}
          </span>
        </div>
      </div>

      {/* Mode Selector */}
      <div style={{ marginBottom: '16px' }}>
        <label style={{ fontSize: '12px', fontWeight: '500', color: '#374151', display: 'block', marginBottom: '8px' }}>
          Expert Mode:
        </label>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          style={{
            width: '100%',
            padding: '8px 12px',
            border: '1px solid #d1d5db',
            borderRadius: '4px',
            fontSize: '14px',
            backgroundColor: '#ffffff',
          }}
        >
          <option value="default">Standard</option>
          <option value="cto">CTO / Technisch</option>
          <option value="bank">Bankfähigkeit</option>
          <option value="mrv">MRV / Compliance</option>
          <option value="funding">Fördermittel</option>
          <option value="professorale">Wissenschaftlich</option>
          <option value="industrial">Industriekundennutzen</option>
          <option value="business">Business Development</option>
        </select>
      </div>

      {/* Error Display */}
      {error && (
        <div
          style={{
            backgroundColor: '#fef2f2',
            border: '1px solid #fecaca',
            borderRadius: '6px',
            padding: '12px',
            marginBottom: '16px',
            color: '#dc2626',
            fontSize: '13px',
          }}
        >
          ⚠️ {error}
        </div>
      )}

      {/* Input Area */}
      <div style={{ marginBottom: '16px' }}>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Stelle eine Frage oder gib eine Aussage zum Validieren ein..."
          disabled={isProcessing || isListening}
          style={{
            width: '100%',
            padding: '12px',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
            fontSize: '14px',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            minHeight: '80px',
            backgroundColor: isProcessing ? '#f3f4f6' : '#ffffff',
            cursor: isProcessing ? 'not-allowed' : 'text',
            opacity: isProcessing ? 0.6 : 1,
          }}
        />
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
        <button
          onClick={handleTextQuery}
          disabled={isProcessing || !inputText.trim()}
          style={{
            padding: '12px',
            backgroundColor: isProcessing ? '#d1d5db' : '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: isProcessing ? 'not-allowed' : 'pointer',
            fontWeight: '500',
            fontSize: '14px',
          }}
        >
          {isProcessing ? '⏳ Verarbeitet...' : '📝 Query absenden'}
        </button>

        <button
          onClick={handleVoiceToggle}
          disabled={isProcessing}
          style={{
            padding: '12px',
            backgroundColor: isListening ? '#ef4444' : '#10b981',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: isProcessing ? 'not-allowed' : 'pointer',
            fontWeight: '500',
            fontSize: '14px',
          }}
        >
          {isListening ? '🎤 Stopp' : '🎤 Sprechen'}
        </button>
      </div>

      {/* Response Display */}
      {response && (
        <div
          style={{
            backgroundColor: '#f0fdf4',
            border: '1px solid #bbf7d0',
            borderRadius: '6px',
            padding: '16px',
            marginBottom: '16px',
            color: '#166534',
            fontSize: '14px',
            lineHeight: '1.5',
          }}
        >
          <strong>✅ Kappa Antwort:</strong>
          <p style={{ margin: '8px 0 0 0' }}>{response}</p>

          {validationResult && (
            <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: '1px solid #bbf7d0' }}>
              <strong>Validierungsergebnis:</strong>
              <div style={{ marginTop: '8px', fontSize: '13px' }}>
                <div>
                  <strong>Gesamtstatus:</strong>{' '}
                  <span style={{ color: validationResult.overall_approved ? '#16a34a' : '#dc2626' }}>
                    {validationResult.overall_approved ? 'GENEHMIGT' : 'ABGELEHNT'}
                  </span>
                </div>
                <div style={{ marginTop: '4px' }}>
                  <strong>Ebene:</strong> {validationResult.approval_level}
                </div>
              </div>
            </div>
          )}

          <button
            onClick={clearResponse}
            style={{
              marginTop: '12px',
              padding: '6px 12px',
              backgroundColor: 'transparent',
              border: '1px solid #bbf7d0',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '12px',
              color: '#166534',
          }}
          >
            Löschen
          </button>
        </div>
      )}

      {/* Validation Toggle */}
      {!showValidation && response && (
        <button
          onClick={() => setShowValidation(true)}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: '#f3f4f6',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '13px',
            fontWeight: '500',
            color: '#374151',
          }}
        >
          🔍 Im Validierungsmodus weiterbearbeiten
        </button>
      )}
    </div>
  );
}
