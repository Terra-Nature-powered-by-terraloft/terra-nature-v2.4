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

  async analyzeImage(
    imageBase64: string,
    prompt: string = "Analysiere dieses Bild.",
    imageType: string = "image/png"
  ): Promise<{
    analysis: string;
    confidence: number;
    timestamp: string;
  }> {
    const url = `${this.baseUrl}/api/kappa/vision?image=${encodeURIComponent(imageBase64)}&prompt=${encodeURIComponent(prompt)}&image_type=${encodeURIComponent(imageType)}`;

    if (this.debug) {
      console.log(`[Kappa] POST /api/kappa/vision`, "[Base64 Image]");
    }

    try {
      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        throw new Error(`Kappa ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (this.debug) {
        console.error(`[Kappa] Vision analysis error:`, error);
      }
      throw error;
    }
  }

  async analyzeDashboard(
    imageBase64: string,
    context?: string
  ): Promise<{
    analysis: string;
    confidence: number;
    timestamp: string;
  }> {
    const params = new URLSearchParams({
      image: imageBase64,
      ...(context && { context }),
    });

    const url = `${this.baseUrl}/api/kappa/vision-dashboard?${params}`;

    if (this.debug) {
      console.log(`[Kappa] POST /api/kappa/vision-dashboard`, "[Base64 Image]");
    }

    try {
      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        throw new Error(`Kappa ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (this.debug) {
        console.error(`[Kappa] Dashboard analysis error:`, error);
      }
      throw error;
    }
  }

  async extractScreenshotContext(
    imageBase64: string
  ): Promise<{
    context: string;
    confidence: number;
    timestamp: string;
  }> {
    const url = `${this.baseUrl}/api/kappa/vision-context?image=${encodeURIComponent(imageBase64)}`;

    if (this.debug) {
      console.log(`[Kappa] POST /api/kappa/vision-context`, "[Base64 Image]");
    }

    try {
      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        throw new Error(`Kappa ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (this.debug) {
        console.error(`[Kappa] Context extraction error:`, error);
      }
      throw error;
    }
  }

  async verifyTechnicalClaim(
    imageBase64: string,
    claim: string
  ): Promise<{
    verified: boolean;
    reasoning: string;
    confidence: number;
    timestamp: string;
  }> {
    const params = new URLSearchParams({
      image: imageBase64,
      claim,
    });

    const url = `${this.baseUrl}/api/kappa/vision-verify?${params}`;

    if (this.debug) {
      console.log(`[Kappa] POST /api/kappa/vision-verify`, "[Base64 Image + Claim]");
    }

    try {
      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        throw new Error(`Kappa ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (this.debug) {
        console.error(`[Kappa] Technical verification error:`, error);
      }
      throw error;
    }
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
