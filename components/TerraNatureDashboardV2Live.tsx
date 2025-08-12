'use client';

import React from 'react';
import { useMetrics } from '@/hooks/useMetrics';

/**
 * Live dashboard integration component for Terra Nature Dashboard V2
 * Demonstrates metric cards, live indicator, error surfacing, and export functionality
 */
export default function TerraNatureDashboardV2Live() {
  const { data, connected, error, disconnect } = useMetrics();

  const handleExportCSV = () => {
    const url = '/api/export?format=csv&minutes=1440'; // 24 hours
    window.open(url, '_blank');
  };

  const handleExportJSONL = () => {
    const url = '/api/export?format=jsonl&minutes=1440'; // 24 hours  
    window.open(url, '_blank');
  };

  return (
    <div style={{ 
      maxWidth: '1200px', 
      margin: '0 auto', 
      padding: '20px',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '30px',
        borderBottom: '2px solid #e0e0e0',
        paddingBottom: '20px'
      }}>
        <h1 style={{ 
          margin: 0, 
          color: '#333',
          fontSize: '28px',
          fontWeight: '600'
        }}>
          Terra Nature Dashboard V2 - Live Mode
        </h1>
        
        {/* Live Status Indicator */}
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '10px' 
        }}>
          <div style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: connected ? '#22c55e' : '#ef4444',
            animation: connected ? 'pulse 2s infinite' : 'none'
          }} />
          <span style={{ 
            fontWeight: '500',
            color: connected ? '#22c55e' : '#ef4444'
          }}>
            {connected ? 'LIVE' : 'DISCONNECTED'}
          </span>
          {connected && (
            <button
              onClick={disconnect}
              style={{
                padding: '4px 8px',
                fontSize: '12px',
                background: '#f3f4f6',
                border: '1px solid #d1d5db',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Disconnect
            </button>
          )}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div style={{
          background: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '8px',
          padding: '16px',
          marginBottom: '20px',
          color: '#dc2626'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Metrics Cards */}
      {data ? (
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '20px',
          marginBottom: '30px'
        }}>
          {/* Energy Card */}
          <div style={{
            background: 'white',
            border: '1px solid #e5e7eb',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ 
              margin: '0 0 8px 0', 
              color: '#374151',
              fontSize: '16px',
              fontWeight: '600'
            }}>
              Energy Consumption
            </h3>
            <div style={{ 
              fontSize: '32px', 
              fontWeight: '700',
              color: '#1f2937',
              marginBottom: '4px'
            }}>
              {data.energy_kWh}
            </div>
            <div style={{ 
              fontSize: '14px', 
              color: '#6b7280' 
            }}>
              kWh
            </div>
          </div>

          {/* Heat Card */}
          <div style={{
            background: 'white',
            border: '1px solid #e5e7eb',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ 
              margin: '0 0 8px 0', 
              color: '#374151',
              fontSize: '16px',
              fontWeight: '600'
            }}>
              Heat Generation
            </h3>
            <div style={{ 
              fontSize: '32px', 
              fontWeight: '700',
              color: '#dc2626',
              marginBottom: '4px'
            }}>
              {data.heat_kWh}
            </div>
            <div style={{ 
              fontSize: '14px', 
              color: '#6b7280' 
            }}>
              kWh
            </div>
          </div>

          {/* Power Card */}
          <div style={{
            background: 'white',
            border: '1px solid #e5e7eb',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ 
              margin: '0 0 8px 0', 
              color: '#374151',
              fontSize: '16px',
              fontWeight: '600'
            }}>
              Power Consumption
            </h3>
            <div style={{ 
              fontSize: '32px', 
              fontWeight: '700',
              color: '#2563eb',
              marginBottom: '4px'
            }}>
              {data.Pel_kW}
            </div>
            <div style={{ 
              fontSize: '14px', 
              color: '#6b7280' 
            }}>
              kW
            </div>
          </div>
        </div>
      ) : (
        <div style={{
          background: '#f9fafb',
          border: '1px solid #e5e7eb',
          borderRadius: '12px',
          padding: '40px',
          textAlign: 'center',
          color: '#6b7280',
          marginBottom: '30px'
        }}>
          {error ? 'Failed to load metrics data' : 'Loading metrics...'}
        </div>
      )}

      {/* Device Information */}
      {data && (
        <div style={{
          background: 'white',
          border: '1px solid #e5e7eb',
          borderRadius: '12px',
          padding: '24px',
          marginBottom: '30px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ 
            margin: '0 0 16px 0', 
            color: '#374151',
            fontSize: '18px',
            fontWeight: '600'
          }}>
            Device Information
          </h3>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: '1fr 1fr',
            gap: '16px',
            fontSize: '14px'
          }}>
            <div>
              <strong>Device ID:</strong> {data.device_id}
            </div>
            <div>
              <strong>Last Update:</strong> {new Date(data.timestamp).toLocaleString()}
            </div>
          </div>
        </div>
      )}

      {/* Export Controls */}
      <div style={{
        background: 'white',
        border: '1px solid #e5e7eb',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
      }}>
        <h3 style={{ 
          margin: '0 0 16px 0', 
          color: '#374151',
          fontSize: '18px',
          fontWeight: '600'
        }}>
          Export Historical Data (24 Hours)
        </h3>
        <div style={{ 
          display: 'flex', 
          gap: '12px',
          flexWrap: 'wrap'
        }}>
          <button
            onClick={handleExportCSV}
            style={{
              background: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              padding: '12px 24px',
              fontSize: '14px',
              fontWeight: '500',
              cursor: 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#1d4ed8'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#2563eb'}
          >
            Download CSV
          </button>
          <button
            onClick={handleExportJSONL}
            style={{
              background: '#059669',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              padding: '12px 24px',
              fontSize: '14px',
              fontWeight: '500',
              cursor: 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#047857'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#059669'}
          >
            Download JSONL
          </button>
        </div>
      </div>

      {/* CSS Animation for pulse effect */}
      <style jsx>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
        }
      `}</style>
    </div>
  );
}