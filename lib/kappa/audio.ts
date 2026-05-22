/**
 * Audio Recording Utilities for Kappa
 * Web Audio API based microphone recording and transcription
 */

export interface AudioRecorderOptions {
  sampleRate?: number;
  audioContext?: AudioContext;
  onRecordingStart?: () => void;
  onRecordingStop?: () => void;
  onRecordingError?: (error: Error) => void;
}

export interface RecordingResult {
  blob: Blob;
  duration: number;
  sampleRate: number;
}

/**
 * AudioRecorder - Records audio from user's microphone using Web Audio API
 */
export class AudioRecorder {
  private mediaStream: MediaStream | null = null;
  private mediaRecorder: MediaRecorder | null = null;
  private audioContext: AudioContext;
  private audioChunks: Blob[] = [];
  private startTime: number = 0;
  private isRecording: boolean = false;
  private sampleRate: number;
  private options: AudioRecorderOptions;

  constructor(options: AudioRecorderOptions = {}) {
    this.options = {
      sampleRate: 16000, // Optimal for speech recognition
      ...options,
    };
    this.sampleRate = this.options.sampleRate || 16000;
    this.audioContext =
      this.options.audioContext || new (window.AudioContext || (window as any).webkitAudioContext)();
  }

  /**
   * Request microphone access and start recording
   */
  async startRecording(): Promise<void> {
    try {
      // Check browser support
      const getUserMedia = navigator.mediaDevices?.getUserMedia;
      if (!getUserMedia) {
        throw new Error('getUserMedia not supported in this browser');
      }

      // Request microphone access
      this.mediaStream = await getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: this.sampleRate,
        },
      });

      // Create MediaRecorder
      const mimeType = this.getSupportedMimeType();
      this.mediaRecorder = new MediaRecorder(this.mediaStream, {
        mimeType,
      });

      // Setup event handlers
      this.audioChunks = [];
      this.startTime = Date.now();

      this.mediaRecorder.addEventListener('dataavailable', (e) => {
        this.audioChunks.push(e.data);
      });

      this.mediaRecorder.addEventListener('error', (e) => {
        const error = new Error(`Recording error: ${e.error}`);
        this.options.onRecordingError?.(error);
      });

      // Start recording
      this.mediaRecorder.start();
      this.isRecording = true;
      this.options.onRecordingStart?.();
    } catch (error) {
      const err = error instanceof Error ? error : new Error(String(error));
      this.options.onRecordingError?.(err);
      throw err;
    }
  }

  /**
   * Stop recording and return audio blob
   */
  stopRecording(): Promise<RecordingResult> {
    return new Promise((resolve, reject) => {
      if (!this.mediaRecorder || !this.isRecording) {
        reject(new Error('Recording not in progress'));
        return;
      }

      const duration = (Date.now() - this.startTime) / 1000;

      this.mediaRecorder.addEventListener('stop', () => {
        // Combine audio chunks into single blob
        const blob = new Blob(this.audioChunks, { type: 'audio/wav' });

        // Stop media stream
        if (this.mediaStream) {
          this.mediaStream.getTracks().forEach((track) => track.stop());
        }

        this.isRecording = false;
        this.options.onRecordingStop?.();

        resolve({
          blob,
          duration,
          sampleRate: this.sampleRate,
        });
      });

      this.mediaRecorder.stop();
    });
  }

  /**
   * Get supported MIME type for audio recording
   */
  private getSupportedMimeType(): string {
    const types = [
      'audio/wav',
      'audio/webm;codecs=opus',
      'audio/webm',
      'audio/mp4',
      'audio/ogg',
    ];

    for (const type of types) {
      if (MediaRecorder.isTypeSupported(type)) {
        return type;
      }
    }

    // Fallback to default
    return 'audio/wav';
  }

  /**
   * Get current recording state
   */
  isRecordingActive(): boolean {
    return this.isRecording;
  }

  /**
   * Cancel recording and cleanup
   */
  cancel(): void {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
    }

    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach((track) => track.stop());
    }

    this.audioChunks = [];
    this.isRecording = false;
  }
}

/**
 * Convert Blob to Base64 string
 */
export async function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = reader.result as string;
      // Remove the "data:audio/wav;base64," prefix
      const base64 = dataUrl.split(',')[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

/**
 * Convert Blob to ArrayBuffer
 */
export async function blobToArrayBuffer(blob: Blob): Promise<ArrayBuffer> {
  return blob.arrayBuffer();
}

/**
 * Simple microphone permission checker
 */
export async function checkMicrophonePermission(): Promise<boolean> {
  try {
    const permission = await navigator.permissions.query({ name: 'microphone' as PermissionName });
    return permission.state === 'granted' || permission.state === 'prompt';
  } catch {
    // Permission API not supported, assume we can try
    return true;
  }
}

/**
 * Format duration in seconds to readable string (MM:SS)
 */
export function formatDuration(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}
