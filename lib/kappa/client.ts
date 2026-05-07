/**
 * Kappa FastAPI Client
 * Handles HTTP communication between Next.js and Kappa FastAPI backend
 */

import {
  QueryRequest,
  QueryResponse,
  ValidationRequest,
  ValidationResponse,
  MemorySaveRequest,
  MemoryResponse,
  HealthResponse,
  AuditLogEntry,
  KappaConfig,
  ErrorResponse,
} from "./types";

export class KappaClient {
  private baseUrl: string;
  private enabled: boolean;
  private debug: boolean;

  constructor(config?: Partial<KappaConfig>) {
    this.baseUrl = config?.api_url || process.env.NEXT_PUBLIC_KAPPA_API_URL || "http://localhost:8000";
    this.enabled = config?.enabled !== false && process.env.NEXT_PUBLIC_KAPPA_ENABLED !== "false";
    this.debug = config?.debug || process.env.NODE_ENV === "development";
  }

  private async request<T>(
    method: string,
    endpoint: string,
    body?: any,
    isFormData: boolean = false
  ): Promise<T> {
    if (!this.enabled) {
      throw new Error("Kappa is disabled");
    }

    const url = `${this.baseUrl}${endpoint}`;

    if (this.debug) {
      console.log(`[Kappa] ${method} ${endpoint}`, isFormData ? "[FormData]" : body);
    }

    try {
      const fetchOptions: RequestInit = {
        method,
        headers: isFormData ? {} : {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      };

      if (isFormData) {
        fetchOptions.body = body;
      } else if (body) {
        fetchOptions.body = JSON.stringify(body);
      }

      const response = await fetch(url, fetchOptions);

      if (!response.ok) {
        let error: ErrorResponse | string;
        try {
          error = await response.json();
        } catch {
          error = response.statusText;
        }
        const errorMsg = typeof error === "string" ? error : error.error || response.statusText;
        throw new Error(`Kappa ${response.status}: ${errorMsg}`);
      }

      const data: T = await response.json();
      return data;
    } catch (error) {
      if (this.debug) {
        console.error(`[Kappa] Error:`, error);
      }
      throw error;
    }
  }

  // === PUBLIC METHODS ===

  async health(): Promise<HealthResponse> {
    return this.request<HealthResponse>("GET", "/api/kappa/health");
  }

  async query(request: QueryRequest): Promise<QueryResponse> {
    return this.request<QueryResponse>("POST", "/api/kappa/query", request);
  }

  async validate(request: ValidationRequest): Promise<ValidationResponse> {
    return this.request<ValidationResponse>("POST", "/api/kappa/validate", request);
  }

  async saveMemory(request: MemorySaveRequest): Promise<MemoryResponse> {
    return this.request<MemoryResponse>("POST", "/api/kappa/memory/save", request);
  }

  async getMemory(key: string): Promise<MemoryResponse> {
    return this.request<MemoryResponse>("GET", `/api/kappa/memory/${encodeURIComponent(key)}`);
  }

  async getAuditLog(limit: number = 100): Promise<AuditLogEntry[]> {
    return this.request<AuditLogEntry[]>("GET", `/api/kappa/audit-log?limit=${limit}`);
  }

  async transcribeAudio(
    audioBlob: Blob,
    language: string = "de"
  ): Promise<{
    text: string;
    confidence: number;
    language: string;
    timestamp: string;
  }> {
    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.wav");
    formData.append("language", language);

    const url = `${this.baseUrl}/api/kappa/listen?language=${encodeURIComponent(language)}`;

    if (this.debug) {
      console.log(`[Kappa] POST /api/kappa/listen`, "[Audio Blob]");
    }

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Kappa ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (this.debug) {
        console.error(`[Kappa] Transcription error:`, error);
      }
      throw error;
    }
  }

  async transcribeAndQuery(
    audioBlob: Blob,
    mode: string = "default",
    language: string = "de",
    user: string = "system"
  ): Promise<{
    transcribed_text: string;
    transcription_confidence: number;
    response: string;
    response_confidence: number;
    sources: string[];
    mode: string;
    timestamp: string;
  }> {
    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.wav");
    formData.append("mode", mode);
    formData.append("language", language);
    formData.append("user", user);

    const url = `${this.baseUrl}/api/kappa/listen-and-query?mode=${encodeURIComponent(mode)}&language=${encodeURIComponent(language)}&user=${encodeURIComponent(user)}`;

    if (this.debug) {
      console.log(`[Kappa] POST /api/kappa/listen-and-query`, "[Audio Blob]");
    }

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Kappa ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (this.debug) {
        console.error(`[Kappa] Listen-and-query error:`, error);
      }
      throw error;
    }
  }

  async listen(): Promise<any> {
    return this.request<any>("POST", "/api/kappa/listen");
  }

  async speak(text: string): Promise<any> {
    return this.request<any>("POST", `/api/kappa/speak?text=${encodeURIComponent(text)}`);
  }

  // === HELPER METHODS ===

  isEnabled(): boolean {
    return this.enabled;
  }

  setDebug(debug: boolean): void {
    this.debug = debug;
  }
}

// Global instance
export const kappa = new KappaClient();
