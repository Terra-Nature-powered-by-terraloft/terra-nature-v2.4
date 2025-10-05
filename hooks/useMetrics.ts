'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import type { MetricSample, MetricsHookState } from '@/lib/types';

/**
 * React hook for consuming metrics data with snapshot + streaming capabilities
 * Provides graceful error handling and connection management
 */
export function useMetrics(): MetricsHookState {
  const [data, setData] = useState<MetricSample | null>(null);
  const [connected, setConnected] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  const eventSourceRef = useRef<EventSource | null>(null);
  const retryTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const retryAttemptsRef = useRef<number>(0);
  const isComponentMounted = useRef<boolean>(true);

  // Function to fetch initial snapshot
  const fetchSnapshot = useCallback(async () => {
    try {
      const response = await fetch('/api/metrics');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const snapshot = await response.json();
      if (isComponentMounted.current) {
        setData(snapshot);
        setError(null);
      }
    } catch (err) {
      if (isComponentMounted.current) {
        setError(err instanceof Error ? err.message : 'Failed to fetch snapshot');
      }
    }
  }, []);

  // Function to establish SSE connection
  const connectToStream = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    if (retryTimeoutRef.current) {
      clearTimeout(retryTimeoutRef.current);
      retryTimeoutRef.current = null;
    }

    try {
      const eventSource = new EventSource('/api/stream');
      eventSourceRef.current = eventSource;

      const resetRetryState = () => {
        retryAttemptsRef.current = 0;
        if (retryTimeoutRef.current) {
          clearTimeout(retryTimeoutRef.current);
          retryTimeoutRef.current = null;
        }
      };

      const scheduleReconnect = () => {
        if (!isComponentMounted.current) {
          return;
        }

        if (retryTimeoutRef.current) {
          clearTimeout(retryTimeoutRef.current);
        }

        const attempt = retryAttemptsRef.current;
        const delay = Math.min(30000, 1000 * Math.pow(2, attempt));
        retryAttemptsRef.current = attempt + 1;

        retryTimeoutRef.current = setTimeout(() => {
          if (isComponentMounted.current) {
            connectToStream();
          }
        }, delay);
      };

      eventSource.onopen = () => {
        if (isComponentMounted.current) {
          resetRetryState();
          setConnected(true);
          setError(null);
        }
      };

      eventSource.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);

          if (!isComponentMounted.current) return;

          switch (message.type) {
            case 'connected':
              resetRetryState();
              setConnected(true);
              setError(null);
              break;

            case 'metric':
              // Extract metric data (remove type field)
              const { type, ...metricData } = message;
              resetRetryState();
              setData(metricData as MetricSample);
              setError(null);
              break;

            case 'error':
              setError(message.message || 'Stream error occurred');
              break;

            case 'close':
              setConnected(false);
              if (message.reason === 'idle_timeout') {
                setError('Connection closed due to idle timeout');
              }
              eventSource.close();
              if (eventSourceRef.current === eventSource) {
                eventSourceRef.current = null;
              }
              scheduleReconnect();
              break;
          }
        } catch (err) {
          if (isComponentMounted.current) {
            setError('Failed to parse stream message');
          }
        }
      };

      eventSource.onerror = () => {
        if (!isComponentMounted.current) {
          return;
        }

        eventSource.close();
        if (eventSourceRef.current === eventSource) {
          eventSourceRef.current = null;
        }

        setConnected(false);
        setError('Stream connection error');

        scheduleReconnect();
      };

    } catch (err) {
      if (!isComponentMounted.current) {
        return;
      }

      setError(err instanceof Error ? err.message : 'Failed to connect to stream');

      scheduleReconnect();
    }
  }, []);

  // Function to disconnect from stream
  const disconnect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setConnected(false);
    retryAttemptsRef.current = 0;
    if (retryTimeoutRef.current) {
      clearTimeout(retryTimeoutRef.current);
      retryTimeoutRef.current = null;
    }
  }, []);

  // Initialize hook - fetch snapshot then upgrade to streaming
  useEffect(() => {
    isComponentMounted.current = true;
    
    // Start with snapshot
    fetchSnapshot().then(() => {
      // Upgrade to streaming after snapshot
      if (isComponentMounted.current) {
        connectToStream();
      }
    });

    // Cleanup on unmount
    return () => {
      isComponentMounted.current = false;
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
      if (retryTimeoutRef.current) {
        clearTimeout(retryTimeoutRef.current);
        retryTimeoutRef.current = null;
      }
    };
  }, [fetchSnapshot, connectToStream]);

  return {
    data,
    connected,
    error,
    disconnect
  };
}

