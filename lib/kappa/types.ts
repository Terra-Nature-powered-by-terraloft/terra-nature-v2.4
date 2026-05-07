/**
 * Kappa Type Definitions
 * Central interface definitions for Terra Nature ↔ Kappa communication
 */

// === REQUEST TYPES ===

export type KappaExpertMode =
  | "default"
  | "cto"         // CTO / Climate Deep Tech
  | "mrv"         // MRV / Compliance
  | "bank"        // Bankfähigkeit
  | "funding"     // Fördermittel
  | "industrial"  // Industrial customers
  | "ip"          // IP / Governance
  | "communication" // Communication
  | "professorale" // Academic
  | "business";   // Business Development

export interface QueryRequest {
  text: string;
  mode?: KappaExpertMode;
  user?: string;
  context?: Record<string, any>;
}

export interface ValidationRequest {
  statement: string;
  modes?: string[];
  user?: string;
}

export interface MemorySaveRequest {
  key: string;
  value: any;
  category?: string;
  user?: string;
}

// === RESPONSE TYPES ===

export interface HealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  timestamp: string;
  version: string;
  components: Record<string, string>;
}

export interface QueryResponse {
  response: string;
  mode: string;
  confidence: number;
  sources: string[];
  timestamp: string;
  requires_approval: boolean;
  approval_level: "approved" | "conditional" | "requires_review";
}

export interface ValidationResult {
  expert: string;
  approved: boolean;
  confidence: number;
  feedback: string;
  suggestions: string[];
  conditions: string[];
}

export interface ValidationResponse {
  statement: string;
  timestamp: string;
  results: Record<string, ValidationResult>;
  overall_approved: boolean;
  approval_level: "approved" | "conditional" | "requires_review";
  user: string;
}

export interface MemoryResponse {
  key: string;
  value: any;
  category?: string;
  timestamp: string;
  user: string;
}

export interface AuditLogEntry {
  timestamp: string;
  type: string;
  user: string;
  status: string;
  data: Record<string, any>;
}

export interface ErrorResponse {
  error: string;
  code: string;
  timestamp: string;
  details?: Record<string, any>;
}

// === CONFIGURATION ===

export interface KappaConfig {
  api_url: string;
  enabled: boolean;
  debug: boolean;
  mock_mode: boolean;
}
