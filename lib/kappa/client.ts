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
    body?: any
  ): Promise<T> {
    if (!this.enabled) {
      throw new Error("Kappa is disabled");
    }

    const url = `${this.baseUrl}${endpoint}`;

    if (this.debug) {
      console.log(`[Kappa] ${method} ${endpoint}`, body);
    }

    try {
      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: body ? JSON.stringify(body) : undefined,
      });

      if (!response.ok) {
        const error: ErrorResponse = await response.json();
        throw new Error(`Kappa ${response.status}: ${error.error}`);
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
