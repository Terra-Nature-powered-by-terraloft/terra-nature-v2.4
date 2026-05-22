/**
 * useKappaOrb - React Hook for Kappa Expert Engine communication
 * Handles queries, audio input, vision analysis, and validation
 */

'use client';

import { useState, useCallback, useRef } from 'react';
import { KappaClient } from '@/lib/kappa/client';
import { QueryResponse, ValidationResponse, HealthResponse } from '@/lib/kappa/types';

export interface KappaOrbState {
  isListening: boolean;
  isProcessing: boolean;
  response: string | null;
  error: string | null;
  isHealthy: boolean;
  lastQuery: string | null;
  validationResult: ValidationResponse | null;
}

interface UseKappaOrbReturn extends KappaOrbState {
  query: (text: string, mode?: string) => Promise<void>;
  startListening: () => Promise<void>;
  stopListening: () => void;
  clearResponse: () => void;
  validate: (statement: string, modes?: string[]) => Promise<void>;
  checkHealth: () => Promise<void>;
}

export function useKappaOrb(): UseKappaOrbReturn {
  const [state, setState] = useState<KappaOrbState>({
    isListening: false,
    isProcessing: false,
    response: null,
    error: null,
    isHealthy: false,
    lastQuery: null,
    validationResult: null,
  });

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const clientRef = useRef<KappaClient>(
    new KappaClient(process.env.NEXT_PUBLIC_KAPPA_API_URL || 'http://localhost:8000')
  );

  const query = useCallback(
    async (text: string, mode: string = 'default') => {
      setState((s) => ({ ...s, isProcessing: true, error: null }));
      try {
        setState((s) => ({ ...s, lastQuery: text }));
        const response = await clientRef.current.query(text, mode);
        setState((s) => ({ ...s, response: response.response, isProcessing: false }));
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        setState((s) => ({ ...s, error: message, isProcessing: false }));
      }
    },
    []
  );

  const startListening = useCallback(async () => {
    try {
      setState((s) => ({ ...s, isListening: true, error: null }));
      audioChunksRef.current = [];

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await transcribeAudio(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      mediaRecorderRef.current = mediaRecorder;
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setState((s) => ({ ...s, error: message, isListening: false }));
    }
  }, []);

  const stopListening = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      setState((s) => ({ ...s, isListening: false }));
    }
  }, []);

  const transcribeAudio = useCallback(async (audioBlob: Blob) => {
    setState((s) => ({ ...s, isProcessing: true }));
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'audio.wav');

      const response = await fetch('/api/kappa/listen', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      await query(data.text);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setState((s) => ({ ...s, error: message, isProcessing: false }));
    }
  }, [query]);

  const validate = useCallback(
    async (statement: string, modes: string[] = ['default']) => {
      setState((s) => ({ ...s, isProcessing: true, error: null }));
      try {
        const response = await clientRef.current.validate(statement, modes);
        setState((s) => ({
          ...s,
          validationResult: response,
          response: `Validierungsergebnis: ${response.overall_approved ? 'GENEHMIGT' : 'ABGELEHNT'}`,
          isProcessing: false,
        }));
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        setState((s) => ({ ...s, error: message, isProcessing: false }));
      }
    },
    []
  );

  const clearResponse = useCallback(() => {
    setState((s) => ({ ...s, response: null, error: null, validationResult: null }));
  }, []);

  const checkHealth = useCallback(async () => {
    try {
      const health = await clientRef.current.health();
      setState((s) => ({ ...s, isHealthy: health.status === 'healthy' }));
    } catch {
      setState((s) => ({ ...s, isHealthy: false }));
    }
  }, []);

  return {
    ...state,
    query,
    startListening,
    stopListening,
    clearResponse,
    validate,
    checkHealth,
  };
}
