# Phase 1: Kappa FastAPI Core Setup

**Status**: ✅ Complete  
**Phase**: 1 of 8 (MVP Phase 1 of 5)  
**Components**: FastAPI Core, Health Check, Basic Stubs, Logging, Config

---

## What's Implemented

### FastAPI Backend (`/kappa/`)

- **main.py** - FastAPI application entry point with CORS, middleware, error handling
- **config.py** - Centralized configuration with environment variable support
- **requirements.txt** - Python dependencies (FastAPI, Pydantic, etc.)
- **logging.py** - Structured logging + append-only audit trail system
- **api/models.py** - Pydantic models for all request/response types
- **api/routes.py** - Initial API routes (Health, Query, Validation, Memory, Listen, Speak)

### Expert Rules Framework (`/kappa/rules/`)

- **cto.yaml** - CTO / Climate Deep Tech expert rules
- **mrv.yaml** - MRV / Compliance expert rules
- **bank.yaml** - Bankfähigkeit / Financial validation rules

### Next.js Bridge (`/lib/kappa/`, `/app/api/kappa/`)

- **lib/kappa/types.ts** - Central TypeScript type definitions
- **lib/kappa/client.ts** - FastAPI client wrapper (fetch-based)
- **lib/kappa/config.ts** - Configuration helper
- **app/api/kappa/health/route.ts** - Health check proxy in Next.js

### Development Tools

- **tools/kappa-cli/start_kappa.py** - Launcher script with debug/mock options
- **package.json** - Added `kappa:start`, `kappa:start:debug`, `kappa:start:mock`, `kappa:test` scripts

### Configuration

- **.env.example** - Template with all Kappa environment variables
- **kappa/data/.gitignore** - Ensures runtime data is not committed

---

## Quick Start

### 1. Install Dependencies

```bash
# Install Node.js dependencies (if not already done)
npm install

# Install Python dependencies
pip install -r requirements.txt
pip install -r kappa/requirements.txt
```

### 2. Setup Environment

```bash
# Copy example to local config
cp .env.example .env.local

# Optional: Edit for your environment
# - KAPPA_MOCK_MODE=true (no API keys needed)
# - KAPPA_PORT=8000
# - KAPPA_DEBUG=true
```

### 3. Start Kappa Server (Terminal 1)

```bash
# Simple start with mock mode
npm run kappa:start:mock

# Or with debug logging
npm run kappa:start:debug

# Or manually
python tools/kappa-cli/start_kappa.py --mock

# Server runs on http://localhost:8000
```

### 4. Start Next.js Dashboard (Terminal 2)

```bash
npm run dev

# Dashboard on http://localhost:3000
```

### 5. Test Health Check (Terminal 3)

```bash
# Direct FastAPI health
curl http://localhost:8000/api/kappa/health

# Via Next.js proxy
curl http://localhost:3000/api/kappa/health

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2026-05-07T...",
#   "components": {
#     "fastapi": "operational",
#     "config": "loaded",
#     "logging": "operational",
#     "audit": "operational",
#     "mock_mode": "enabled"
#   }
# }
```

---

## API Endpoints (Phase 1)

All endpoints are stubs and ready for Phase 2+ implementation.

### Health Check

```bash
GET /api/kappa/health
# Returns: HealthResponse with component status
```

### Query (STUB)

```bash
POST /api/kappa/query
Content-Type: application/json

{
  "text": "Wie viel MRV-relevante Energie wurde erfasst?",
  "mode": "default",
  "user": "founder"
}

# Response (STUB):
{
  "response": "[STUB] Received in mode 'default': ...",
  "mode": "default",
  "confidence": 0.5,
  "sources": ["stub"],
  "timestamp": "...",
  "approval_level": "approved"
}
```

### Validation (STUB)

```bash
POST /api/kappa/validate
{
  "statement": "Der ORC nutzt eine Arbeitsflüssigkeit mit TRL 7",
  "modes": ["cto", "mrv"],
  "user": "founder"
}

# Response (STUB): stub results, real rules in Phase 5
```

### Memory Operations (STUB)

```bash
POST /api/kappa/memory/save
{
  "key": "project_phase",
  "value": "Phase 1 Complete",
  "category": "project_status"
}

GET /api/kappa/memory/{key}
# Returns saved value
```

### Audit Log

```bash
GET /api/kappa/audit-log?limit=100
# Returns all logged events (append-only)
```

### Listen / Speak (STUBS)

```bash
POST /api/kappa/listen
# Audio input stub (Whisper in Phase 3)

POST /api/kappa/speak?text=Hallo
# TTS stub (Phase 3+)
```

---

## TypeScript Usage

From Next.js components, use the Kappa client:

```typescript
import { kappa } from "@/lib/kappa/client";

async function checkKappaHealth() {
  const health = await kappa.health();
  console.log(health.status); // "healthy"
}

async function queryKappa() {
  const response = await kappa.query({
    text: "Wie viel Energie?",
    mode: "default",
    user: "founder"
  });
  console.log(response.response);
}
```

---

## Logging & Audit Trail

### Console Logging

Kappa uses **structlog** for structured, JSON-based logging:

```
{"timestamp": "2026-05-07T...", "event": "query_received", "text": "...", "mode": "default", "user": "founder"}
{"timestamp": "...", "event": "http_response", "method": "POST", "status_code": 200}
```

### Audit Trail

Every query/validation/action is logged to `kappa/data/audit.jsonl`:

```json
{"timestamp": "2026-05-07T14:23:45.123Z", "type": "query", "user": "founder", "status": "success", "data": {...}}
{"timestamp": "2026-05-07T14:24:12.456Z", "type": "validation", "user": "founder", "status": "success", "data": {...}}
```

---

## Mock Mode

For development without API keys, start with `--mock`:

```bash
npm run kappa:start:mock
```

- All endpoints return stub responses
- No external API calls (OpenAI, Anthropic)
- Perfect for UI development and testing

---

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KAPPA_PORT` | 8000 | FastAPI server port |
| `KAPPA_HOST` | 127.0.0.1 | Bind to localhost only |
| `KAPPA_ENV` | development | Environment (development/production) |
| `KAPPA_DEBUG` | false | Enable debug mode |
| `KAPPA_MOCK_MODE` | false | Enable mock responses (no API keys) |
| `KAPPA_LOG_LEVEL` | DEBUG | Logging level |
| `NEXT_PUBLIC_KAPPA_API_URL` | http://localhost:8000 | Kappa backend URL |
| `NEXT_PUBLIC_KAPPA_ENABLED` | true | Enable Kappa integration |

### File Paths

- **Knowledge Base**: `kappa/data/kb.db` (SQLite, created in Phase 2)
- **Project Memory**: `kappa/data/memory.jsonld` (JSON-LD, created in Phase 2)
- **Audit Trail**: `kappa/data/audit.jsonl` (append-only log)
- **Expert Rules**: `kappa/rules/*.yaml` (rule definitions)

---

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│  Next.js Dashboard (Port 3000)          │
│  - React Components                     │
│  - API Routes (/app/api/kappa/*)       │
└────────────┬────────────────────────────┘
             │ HTTP to localhost:8000
             │
┌────────────▼────────────────────────────┐
│  FastAPI Kappa Server (Port 8000)       │
│  - Router: /api/kappa/*                 │
│  - Health, Query, Validate, Memory      │
│  - Logging, Audit, Config               │
└─────────────────────────────────────────┘
```

---

## Testing Phase 1

### 1. Verify Server Starts

```bash
npm run kappa:start:mock
# Should see: "Uvicorn running on http://127.0.0.1:8000"
```

### 2. Check Health Endpoint

```bash
curl -s http://localhost:8000/api/kappa/health | jq .
# Should return healthy status
```

### 3. API Documentation

FastAPI auto-generates docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. Test Query Stub

```bash
curl -X POST http://localhost:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Test query", "mode": "default"}'
```

### 5. Check Audit Log

```bash
curl http://localhost:8000/api/kappa/audit-log?limit=5
```

---

## Next Steps (Phase 2)

- [ ] Implement Knowledge Base (SQLite schema)
- [ ] Implement Project Memory (JSON-LD structure)
- [ ] Create Knowledge Base Manager class
- [ ] Memory synchronization with Terra metrics
- [ ] Load and parse YAML expert rules
- [ ] Begin Expert Engine core logic

---

## Troubleshooting

### "Port 8000 already in use"
```bash
# Use different port
npm run kappa:start:mock -- --port 8001
```

### "Module not found: pydantic"
```bash
# Install requirements
pip install -r requirements.txt
pip install -r kappa/requirements.txt
```

### "ImportError: No module named 'config'"
```bash
# Ensure you run from kappa directory or script does path setup
# The start_kappa.py script handles this
```

### "Kappa backend unreachable"
- Check if Kappa server is running: `ps aux | grep uvicorn`
- Verify URL in `.env.local`: `NEXT_PUBLIC_KAPPA_API_URL=http://localhost:8000`
- Check firewall: localhost:8000 should be accessible

---

## Key Files for Phase 1

**Core Logic**:
- `/kappa/main.py` - FastAPI setup
- `/kappa/config.py` - Configuration
- `/kappa/api/routes.py` - Endpoints

**Type Safety**:
- `/lib/kappa/types.ts` - Central types

**Testing**:
- `/tools/kappa-cli/start_kappa.py` - Local launcher
- `/app/api/kappa/health/route.ts` - Proxy to verify

**Expert Rules** (for Phase 5):
- `/kappa/rules/cto.yaml`
- `/kappa/rules/mrv.yaml`
- `/kappa/rules/bank.yaml`

---

**Status**: Phase 1 Core complete. Ready for Phase 2 Knowledge Base implementation.
