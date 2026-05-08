# Kappa API Reference

**Version**: 0.1.0-phase8  
**Base URL**: `http://localhost:8000/api/kappa`  
**All endpoints**: Prefix `/api/kappa`

---

## Health Endpoint

### GET `/health`
Returns Kappa server health status and component information.

**Response 200:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-08T08:00:00.000Z",
  "version": "0.1.0-phase8",
  "components": {
    "engine": "ready",
    "memory": "ready",
    "knowledge_base": "ready",
    "audit": "ready",
    "security": "ready"
  },
  "stats": {
    "uptime_seconds": 3600,
    "queries_processed": 42,
    "validations_completed": 8
  }
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/api/kappa/health
```

---

## Query Endpoint

### POST `/query`
Process a natural language query through the expert engine.

**Request:**
```json
{
  "text": "Wie viel CO2 wurde heute kompensiert?",
  "mode": "default",
  "user": "founder",
  "context": {
    "project_phase": "phase_5",
    "current_metrics": {"efficiency": 0.75}
  }
}
```

**Parameters:**
- `text` (string, required): User input (1-5000 chars)
- `mode` (string, default: "default"): Expert mode
  - `default` - General queries
  - `cto` - Technical/Engineering perspective
  - `mrv` - MRV compliance and measurement
  - `bank` - Financing and banking
  - `funding` - Grant and subsidy requirements
  - `industrial` - Industrial customer needs
  - `ip` - Intellectual property
  - `communication` - Communication strategy
  - `professorale` - Academic/Scientific validation
  - `business` - Business development
- `user` (string, default: "system"): User identifier for audit
- `context` (object, optional): Additional context

**Response 200:**
```json
{
  "response": "Basierend auf den heutigen Metriken wurden 10.5 Tonnen CO2 kompensiert durch die ORC-Anlage...",
  "mode": "cto",
  "confidence": 0.87,
  "sources": ["knowledge_base", "memory"],
  "timestamp": "2026-05-08T08:00:00.000Z",
  "requires_approval": false,
  "approval_level": "approved"
}
```

**Examples:**

```bash
# Simple query (default mode)
curl -X POST http://127.0.0.1:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Was ist der Projektstatus?"
  }'

# Technical mode query
curl -X POST http://127.0.0.1:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Ist eine Effizienz von 85% technisch realistisch?",
    "mode": "cto"
  }'

# Query with context
curl -X POST http://127.0.0.1:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Analysiere die Rentabilität",
    "mode": "bank",
    "context": {
      "capex_million_euro": 2.5,
      "annual_savings": 0.25,
      "expected_roi_years": 8
    }
  }'
```

---

## Validation Endpoint

### POST `/validate`
Validate a statement against multiple expert perspectives.

**Request:**
```json
{
  "statement": "Der ORC erreicht 80% Effizienz bei 95°C Wärmeeingang",
  "modes": ["cto", "mrv"],
  "user": "founder"
}
```

**Parameters:**
- `statement` (string, required): Statement to validate (1-5000 chars)
- `modes` (array, default: ["all"]): Expert perspectives
  - See query endpoint for mode list
- `user` (string, default: "system"): User identifier

**Response 200:**
```json
{
  "statement": "Der ORC erreicht 80% Effizienz bei 95°C...",
  "timestamp": "2026-05-08T08:00:00.000Z",
  "results": {
    "cto": {
      "expert": "CTO/Engineering",
      "approved": true,
      "confidence": 0.92,
      "feedback": "Technisch plausibel. ORC-Systeme bei 80% Effizienz bekannt.",
      "suggestions": [
        "Spezifiziere die Wärmequelle",
        "Nennen Sie die verwendete Arbeitsflüssigkeit"
      ],
      "conditions": []
    },
    "mrv": {
      "expert": "MRV/Compliance",
      "approved": true,
      "confidence": 0.85,
      "feedback": "Messbar und verifizierbar",
      "suggestions": [],
      "conditions": [
        "Erfordert Messprotokoll",
        "Quarterly Verification erforderlich"
      ]
    }
  },
  "overall_approved": true,
  "approval_level": "approved",
  "user": "founder"
}
```

**Examples:**

```bash
# Validate technical statement
curl -X POST http://127.0.0.1:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Das System nutzt eine ORC für Abwärmenutzung",
    "modes": ["cto"]
  }'

# Validate financial statement
curl -X POST http://127.0.0.1:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "CAPEX beträgt €2.5M mit 8-Jahr ROI",
    "modes": ["bank", "funding"]
  }'

# Multi-mode validation
curl -X POST http://127.0.0.1:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Am 2026-05-08 wurden 10 tCO2 kompensiert",
    "modes": ["mrv", "professorale"]
  }'
```

---

## Memory Endpoints

### POST `/memory/save`
Save data to project memory.

**Request:**
```json
{
  "key": "current_efficiency",
  "value": 0.80,
  "category": "metrics",
  "user": "founder",
  "metadata": {
    "source": "dashboard",
    "timestamp_recorded": "2026-05-08T08:00:00Z"
  }
}
```

**Response 200:**
```json
{
  "key": "current_efficiency",
  "value": 0.80,
  "category": "metrics",
  "timestamp": "2026-05-08T08:00:00.000Z",
  "user": "founder"
}
```

### GET `/memory/{key}`
Retrieve data from project memory.

**Response 200:**
```json
{
  "key": "current_efficiency",
  "value": 0.80,
  "category": "metrics",
  "timestamp": "2026-05-08T08:00:00.000Z",
  "user": "founder"
}
```

**Response 404:**
```json
{
  "error": "Not found",
  "key": "nonexistent_key"
}
```

### GET `/memory-summary`
Get summary of all stored memory entries.

**Response 200:**
```json
{
  "total_entries": 42,
  "categories": {
    "metrics": 18,
    "decisions": 12,
    "tasks": 9,
    "technical": 3
  },
  "last_update": "2026-05-08T08:00:00.000Z"
}
```

**Examples:**

```bash
# Save metrics
curl -X POST http://127.0.0.1:8000/api/kappa/memory/save \
  -H "Content-Type: application/json" \
  -d '{
    "key": "co2_compensated_today",
    "value": 10.5,
    "category": "metrics"
  }'

# Retrieve metrics
curl http://127.0.0.1:8000/api/kappa/memory/co2_compensated_today

# Get memory summary
curl http://127.0.0.1:8000/api/kappa/memory-summary
```

---

## Vision Endpoint

### POST `/vision`
Analyze an image (dashboard screenshot, document, etc.).

**Request:**
```json
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA...",
  "mode": "default",
  "analysis_type": "dashboard_metrics"
}
```

**Response 200:**
```json
{
  "analysis": "Das Dashboard zeigt aktuelle CO2-Metriken von 45.5 Tonnen...",
  "detected_elements": [
    "efficiency_gauge: 78%",
    "co2_counter: 45.5t",
    "power_graph: trending_up"
  ],
  "confidence": 0.88,
  "timestamp": "2026-05-08T08:00:00.000Z"
}
```

**Example:**
```bash
# Note: In real use, capture screenshot first
curl -X POST http://127.0.0.1:8000/api/kappa/vision \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/png;base64,...",
    "analysis_type": "dashboard_metrics"
  }'
```

---

## Audio Endpoints

### POST `/listen`
Transcribe audio input (Whisper integration).

**Request:**
```json
{
  "audio_base64": "UklGRi4AAABXQVZF...",
  "format": "wav",
  "language": "de"
}
```

**Response 200:**
```json
{
  "text": "Wie viel CO2 wurde heute kompensiert",
  "language": "de",
  "confidence": 0.95,
  "timestamp": "2026-05-08T08:00:00.000Z"
}
```

### POST `/listen-and-query`
Transcribe audio and immediately process as query.

**Request:**
```json
{
  "audio_base64": "UklGRi4AAABXQVZF...",
  "format": "wav",
  "mode": "default"
}
```

**Response 200:**
```json
{
  "transcribed_text": "Wie viel CO2 wurde heute kompensiert",
  "response": "Basierend auf den Daten wurden heute 10.5 Tonnen kompensiert...",
  "mode": "default",
  "confidence": 0.92,
  "timestamp": "2026-05-08T08:00:00.000Z"
}
```

### POST `/speak`
Convert text to speech (TTS stub).

**Request:**
```json
{
  "text": "Das Projekt ist in Phase 5",
  "language": "de",
  "voice": "default"
}
```

**Response 200:**
```json
{
  "audio_base64": "//NExAAQAAgAA/...",
  "format": "wav",
  "duration_ms": 2340,
  "timestamp": "2026-05-08T08:00:00.000Z"
}
```

---

## Audit Log Endpoint

### GET `/audit-log`
Retrieve audit trail entries.

**Query Parameters:**
- `limit` (int, default: 100, max: 1000): Number of entries
- `user` (string, optional): Filter by user
- `event_type` (string, optional): Filter by event type (query, validation, memory, vision, security, decision)

**Response 200:**
```json
[
  {
    "timestamp": "2026-05-08T08:00:15.123Z",
    "event_type": "query",
    "action": "query_processed",
    "user": "founder",
    "mode": "cto",
    "query_length": 45,
    "response_length": 280,
    "status": "success",
    "version": "1.0"
  },
  {
    "timestamp": "2026-05-08T08:00:10.456Z",
    "event_type": "validation",
    "action": "statement_validated",
    "user": "founder",
    "modes": ["mrv"],
    "statement_length": 60,
    "approval_level": "approved",
    "version": "1.0"
  }
]
```

**Examples:**

```bash
# Last 50 entries
curl "http://127.0.0.1:8000/api/kappa/audit-log?limit=50"

# Filter by user
curl "http://127.0.0.1:8000/api/kappa/audit-log?user=founder&limit=20"

# Filter by event type
curl "http://127.0.0.1:8000/api/kappa/audit-log?event_type=validation&limit=10"
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input",
  "code": "VALIDATION_ERROR",
  "timestamp": "2026-05-08T08:00:00.000Z",
  "details": {
    "field": "text",
    "message": "String must be at least 1 character"
  }
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 503 Service Unavailable
```json
{
  "error": "Service unavailable",
  "code": "SERVICE_ERROR",
  "timestamp": "2026-05-08T08:00:00.000Z",
  "details": "Audit logging is disabled"
}
```

---

## Rate Limiting

Default: **60 requests per minute per user**

**Headers:**
- `X-RateLimit-Limit`: 60
- `X-RateLimit-Remaining`: 45
- `X-RateLimit-Reset`: 1683052860

---

## Authentication

Currently: **No authentication required** (local development mode)

For production: JWT token in `Authorization` header
```bash
curl -H "Authorization: Bearer <jwt_token>" ...
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request |
| 404 | Not found |
| 422 | Validation error |
| 503 | Service unavailable |
| 500 | Internal server error |

---

## Testing All Endpoints

```bash
# Health
curl http://127.0.0.1:8000/api/kappa/health

# Query
curl -X POST http://127.0.0.1:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Test"}'

# Validation
curl -X POST http://127.0.0.1:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{"statement": "Test statement"}'

# Memory
curl -X POST http://127.0.0.1:8000/api/kappa/memory/save \
  -H "Content-Type: application/json" \
  -d '{"key": "test", "value": "test"}'

curl http://127.0.0.1:8000/api/kappa/memory/test

# Audit
curl http://127.0.0.1:8000/api/kappa/audit-log
```

---

See also: **KAPPA_QUICKSTART.md** for examples and **KAPPA_TROUBLESHOOTING.md** for common issues.
