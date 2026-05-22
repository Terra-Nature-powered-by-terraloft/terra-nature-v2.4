# Kappa Security - Sicherheitsmodell und Best Practices

**Version**: 0.1.0-phase8  
**Status**: MVP Release Candidate  
**Last Updated**: 2026-05-08  
**Security Level**: Development (Local) / Production Ready (with JWT)

---

## Sicherheits-Übersicht

Kappa folgt einem **Multi-Layer Security Model**:

```
┌─────────────────────────────────────────────────┐
│ Layer 1: Input Validation (Pydantic)            │
│ - Type checking, length limits, sanitization    │
├─────────────────────────────────────────────────┤
│ Layer 2: Authentication (JWT optional)          │
│ - Token validation, user identification         │
├─────────────────────────────────────────────────┤
│ Layer 3: Authorization (Role-based)             │
│ - User role checks, action approval             │
├─────────────────────────────────────────────────┤
│ Layer 4: Rate Limiting (per-user)               │
│ - 60 requests/min per user (configurable)       │
├─────────────────────────────────────────────────┤
│ Layer 5: Audit Logging (append-only)            │
│ - All actions recorded in audit.jsonl           │
├─────────────────────────────────────────────────┤
│ Layer 6: Secrets Management                     │
│ - API Keys in .env.local (never in git)         │
└─────────────────────────────────────────────────┘
```

---

## 1. Input Validation

### Pydantic Models (Type Safety)

Alle Requests werden durch Pydantic validiert:

```python
# kappa/api/models.py
from pydantic import BaseModel, Field, validator

class QueryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    mode: str = Field(default="default", pattern="^(default|cto|mrv|bank|funding|industrial|ip|communication|professorale|business)$")
    user: str = Field(default="system", min_length=1, max_length=256)
    context: dict = Field(default_factory=dict)
    
    @validator("text")
    def text_no_injection(cls, v):
        # No SQL injection patterns
        if any(pattern in v.lower() for pattern in ["drop ", "delete ", "--", "/*"]):
            raise ValueError("Potential SQL injection detected")
        return v
```

### Längen-Limits

| Field | Min | Max | Purpose |
|-------|-----|-----|---------|
| `text` (query) | 1 | 5000 | Prevent DoS from huge inputs |
| `statement` (validate) | 1 | 5000 | Same |
| `mode` | - | - | Whitelist only (enum) |
| `user` | 1 | 256 | User identification |
| `audio_base64` | 1 | 50MB | Prevent memory exhaustion |

### Validation Examples

```bash
# ✅ Valid
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Wie viel CO₂?"}'

# ❌ Invalid - too long
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "AAAA...(5001 chars)...AAAA"}'
# → 422 Unprocessable Entity: String must be <= 5000 characters

# ❌ Invalid - wrong mode
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test", "mode": "superadmin"}'
# → 422 Unprocessable Entity: Input should be 'default', 'cto', 'mrv', ...

# ❌ Invalid - potential injection
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "SELECT * FROM users; DROP TABLE--"}'
# → 422 Validation Error: Potential SQL injection detected
```

---

## 2. Authentication & Authorization

### JWT Token Model (Optional in Development, Required in Production)

```python
# kappa/utils/security.py
from fastapi.security import HTTPBearer, HTTPAuthCredential
import jwt
from datetime import datetime, timedelta

class TokenValidator:
    def __init__(self, secret: str):
        self.secret = secret
    
    async def validate_token(self, token: str) -> dict:
        """Validiert JWT Token und gibt Payload zurück"""
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=["HS256"]
            )
            # Token abgelaufen?
            if payload.get("exp") < datetime.utcnow().timestamp():
                raise ValueError("Token expired")
            
            return payload
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
    
    def create_token(self, user: str, duration_hours: int = 24) -> str:
        """Erstellt neuen JWT Token"""
        payload = {
            "sub": user,  # Subject (user identifier)
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=duration_hours)
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")
```

### Development vs Production

**Development Mode** (KAPPA_DEBUG=true):
```bash
# .env.local
KAPPA_DEBUG=true
KAPPA_JWT_SECRET=dev-secret-change-me
# → JWT validation ist optional, aber möglich
```

**Production Mode** (KAPPA_DEBUG=false):
```bash
# .env.local
KAPPA_DEBUG=false
KAPPA_JWT_SECRET=<strong-random-256bit-secret>
# → JWT validation ist ERFORDERLICH
# → Alle Requests ohne gültiges Token werden abgelehnt
```

### Token Usage

```bash
# ✅ With Token
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test"}'

# ❌ Without Token (Production)
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test"}'
# → 401 Unauthorized: Missing authentication credentials
```

### Role-Based Authorization

```python
# kappa/utils/security.py
ROLE_PERMISSIONS = {
    "founder": ["query", "validate", "memory", "vision", "listen", "speak", "audit-log"],
    "analyst": ["query", "validate", "memory", "audit-log"],
    "viewer": ["query", "audit-log"]
}

async def require_role(user: dict, required_roles: List[str]):
    user_role = user.get("role", "viewer")
    if user_role not in required_roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
```

---

## 3. Rate Limiting

### Per-User Rate Limiting

```python
# kappa/utils/security.py
from collections import defaultdict
from time import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.limit = requests_per_minute
        self.requests = defaultdict(list)  # user_id -> [timestamp1, timestamp2, ...]
    
    async def check_rate_limit(self, user: str) -> bool:
        """Returns True if request is allowed, False if rate-limited"""
        now = time()
        minute_ago = now - 60
        
        # Entferne alte Requests
        self.requests[user] = [ts for ts in self.requests[user] if ts > minute_ago]
        
        # Prüfe Limit
        if len(self.requests[user]) >= self.limit:
            return False
        
        # Registriere neuen Request
        self.requests[user].append(now)
        return True
```

### Rate Limit Headers

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1683052860  # Unix timestamp when limit resets
```

### Rate Limit Überschreitung

```bash
curl -X POST http://localhost:8000/api/kappa/query \
  -H "Authorization: Bearer <token>" \
  -d '{"text": "Test"}'
# ... nach 60 Requests in 60 Sekunden:
# → 429 Too Many Requests
# → Retry-After: 30 (seconds)
```

---

## 4. Audit Logging

### Append-Only Audit Trail

Alle Aktionen werden in `kappa/data/audit.jsonl` geloggt (JSON Lines Format):

```jsonl
{"timestamp": "2026-05-08T14:23:45.123Z", "user": "founder", "action": "query", "mode": "professorale", "input_length": 45, "output_length": 1240, "status": "success", "execution_ms": 2340, "version": "1.0"}
{"timestamp": "2026-05-08T14:24:12.456Z", "user": "founder", "action": "validate", "modes": ["cto", "mrv"], "status": "success", "execution_ms": 1500, "version": "1.0"}
{"timestamp": "2026-05-08T14:25:00.789Z", "user": "founder", "action": "memory_save", "key": "current_phase", "status": "success", "version": "1.0"}
```

### Audit Entry Schema

```python
# kappa/models/audit.py
class AuditLogEntry(BaseModel):
    timestamp: str  # ISO 8601
    user: str       # user identifier or "system"
    action: str     # query, validate, memory_save, vision, listen, decision, error
    mode: Optional[str]  # expert mode (for query/validate)
    status: str     # success, error, rate_limited, validation_error
    execution_ms: int  # execution time
    version: str    # API version
    
    # Optional fields (depends on action)
    input_length: Optional[int]
    output_length: Optional[int]
    modes: Optional[List[str]]
    key: Optional[str]
    error_code: Optional[str]
    error_message: Optional[str]
    ip_address: Optional[str]
    
    class Config:
        extra = "allow"  # Allow additional fields
```

### Audit Log API

```bash
# Abrufen aller Logs (limit 100)
curl http://localhost:8000/api/kappa/audit-log

# Filtern nach User
curl "http://localhost:8000/api/kappa/audit-log?user=founder"

# Filtern nach Event Type
curl "http://localhost:8000/api/kappa/audit-log?event_type=query&limit=50"

# Filtern nach Datum
curl "http://localhost:8000/api/kappa/audit-log?since=2026-05-08T00:00:00Z"
```

### Response Format

```json
[
  {
    "timestamp": "2026-05-08T14:23:45.123Z",
    "user": "founder",
    "action": "query",
    "mode": "cto",
    "status": "success",
    "execution_ms": 2340,
    "version": "1.0"
  }
]
```

---

## 5. Secrets Management

### Environment Variables (.env.local)

**Regel 1**: NIEMALS Secrets in Code einchecken

```bash
# ✅ Richtig (.env.local, nicht in Git)
KAPPA_JWT_SECRET=change-me-production-use-strong-256bit-secret
KAPPA_OPENAI_API_KEY=sk-proj-...
KAPPA_ANTHROPIC_API_KEY=sk-ant-...

# ❌ Falsch (in Code oder .env.example)
# KAPPA_OPENAI_API_KEY=sk-proj-real-key-here
```

### .gitignore

Stelle sicher, dass sensitive Dateien ignoriert sind:

```bash
# .gitignore
.env.local                     # Local environment (niemals committen!)
.env.*.local
kappa/data/                    # Runtime data (audit logs, memory, KB)
kappa/data/*.db
kappa/data/*.jsonl
kappa/data/*.jsonld
.secrets/
```

### Secret Rotation

Für Production:

```bash
# 1. Generate neuer Secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
# → output: _gU9L8Zf3K-xA9qM2bP5nR_J7c6V4eW1Y

# 2. Setze in Production Environment
export KAPPA_JWT_SECRET="_gU9L8Zf3K-xA9qM2bP5nR_J7c6V4eW1Y"

# 3. Alte Token sind ungültig, Clients müssen sich neu authentifizieren
```

### API Key Best Practices

**OpenAI API Key**:
```bash
# 1. Erstelle einen Project-spezifischen API Key
# → https://platform.openai.com/account/api-keys

# 2. Setze granulare Permissions
# → Nur "Speech to Text" (Whisper) erlauben
# → IP Whitelist: 127.0.0.1 (localhost only)

# 3. Monitore Usage in OpenAI Dashboard
# → Alerts bei unerwarteter Nutzung
```

**Anthropic API Key**:
```bash
# 1. Erstelle einen Project-spezifischen API Key
# → https://console.anthropic.com/account/keys

# 2. Setze IP Whitelist
# → 127.0.0.1 für Development
# → Production server IP für Deployment

# 3. Rate Limiting auf Anthropic-Seite
# → Default: 3500 RPM für Claude models
```

---

## 6. Critical Actions & Approval Workflow

### Kritische Aktionen (erfordern Audit-Trail + Approval)

```python
# kappa/utils/security.py
CRITICAL_ACTIONS = {
    "memory_save": True,      # Saving data to persistent memory
    "decision_record": True,   # Recording critical business decision
    "audit_export": True,      # Exporting audit logs
    "kb_update": True,         # Updating knowledge base
}

async def require_approval(action: str, user: str, details: dict):
    if not CRITICAL_ACTIONS.get(action):
        return True  # Non-critical, proceed immediately
    
    # Für critical actions:
    # 1. Log intent
    # 2. Warten auf user confirmation (if interactive)
    # 3. Log approval
    # 4. Execute
```

### Entscheidungs-Protokoll

Kritische Entscheidungen werden mit Kontext geloggt:

```bash
curl -X POST http://localhost:8000/api/kappa/decision \
  -d '{
    "title": "Proceed with Phase 3 Implementation",
    "reason": "All safety checks passed, team consensus",
    "context": {
      "safety_check": "passed",
      "team_votes": 5,
      "risk_level": "low"
    },
    "user": "founder"
  }'

# Response:
{
  "decision_id": "dec_20260508_001",
  "status": "recorded",
  "timestamp": "2026-05-08T14:30:00Z",
  "audit_entry": {...}
}
```

---

## 7. Known Security Limitations

### Development Mode (KAPPA_DEBUG=true)

| Limitation | Implication | Mitigation |
|-----------|-------------|-----------|
| JWT optional | Anyone can query | Use only on localhost:8000 |
| No HTTPS | Traffic in plaintext | Local network only |
| Mock API Keys | Real services not called | Add real keys in .env.local |
| No IP whitelist | Any local process can query | Firewall or proxy |

### Empfehlungen für Deployment

1. **Nie Debug-Mode in Production**
   ```bash
   # ❌ Never
   KAPPA_DEBUG=true  # Only for development!
   
   # ✅ Always
   KAPPA_DEBUG=false
   KAPPA_JWT_SECRET=<strong-256bit-secret>
   ```

2. **Reverse Proxy mit HTTPS**
   ```nginx
   server {
       listen 443 ssl;
       server_name kappa.terra-nature.local;
       
       ssl_certificate /etc/ssl/certs/kappa.crt;
       ssl_certificate_key /etc/ssl/private/kappa.key;
       
       location /api/kappa {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header X-Forwarded-For $remote_addr;
       }
   }
   ```

3. **Docker mit User Isolation**
   ```dockerfile
   FROM python:3.11-slim
   RUN useradd -m kappa
   USER kappa
   EXPOSE 8000
   CMD ["uvicorn", "kappa.main:app"]
   ```

4. **Kubernetes Network Policies**
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: kappa-isolation
   spec:
     podSelector:
       matchLabels:
         app: kappa
     policyTypes:
     - Ingress
     ingress:
     - from:
       - podSelector:
           matchLabels:
             app: dashboard
       ports:
       - protocol: TCP
         port: 8000
   ```

---

## 8. Common Security Issues & Fixes

### ❌ Issue 1: API Keys in Code

```python
# ❌ WRONG
from config import OPENAI_API_KEY
OPENAI_API_KEY = "sk-proj-..." # Hardcoded!
```

**Fix**:
```python
# ✅ CORRECT
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("KAPPA_OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("KAPPA_OPENAI_API_KEY not set in .env.local")
```

### ❌ Issue 2: No Input Validation

```python
# ❌ WRONG
@app.post("/query")
async def query(text: str):  # Raw string, no validation
    return engine.process(text)
```

**Fix**:
```python
# ✅ CORRECT
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

@app.post("/query")
async def query(req: QueryRequest):
    return engine.process(req.text)
```

### ❌ Issue 3: No Rate Limiting

```python
# ❌ WRONG
@app.post("/query")
async def query(req: QueryRequest):
    # Unbounded, anyone can spam
    return engine.process(req.text)
```

**Fix**:
```python
# ✅ CORRECT
from fastapi import Depends

@app.post("/query")
async def query(
    req: QueryRequest,
    rate_limiter: RateLimiter = Depends(get_rate_limiter)
):
    if not await rate_limiter.check_limit(req.user):
        raise HTTPException(status_code=429, detail="Rate limited")
    return engine.process(req.text)
```

### ❌ Issue 4: No Audit Trail

```python
# ❌ WRONG
@app.post("/query")
async def query(req: QueryRequest):
    return engine.process(req.text)
    # Keine Logs, unmöglich zu auditen
```

**Fix**:
```python
# ✅ CORRECT
from kappa.utils.audit import AuditLogger

audit = AuditLogger("kappa/data/audit.jsonl")

@app.post("/query")
async def query(req: QueryRequest):
    result = engine.process(req.text)
    
    await audit.log(
        action="query",
        user=req.user,
        mode=req.mode,
        status="success"
    )
    
    return result
```

### ❌ Issue 5: CORS too Permissive

```python
# ❌ WRONG
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any origin!
)
```

**Fix**:
```python
# ✅ CORRECT
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000"
    ],  # Explicit whitelist
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

---

## 9. Security Testing Checklist

Vor Production Deployment:

- [ ] JWT Secret ist ≥256 bits, zufällig
- [ ] .env.local ist in .gitignore und nicht gecheckt
- [ ] Alle External API Keys sind in .env.local
- [ ] Input Validation mit Pydantic auf allen Routes
- [ ] Rate Limiting ist aktiv (60 req/min/user)
- [ ] Audit Trail wird für alle kritischen Aktionen geloggt
- [ ] Error Messages geben keine sensitiven Informationen preis
  ```python
  # ❌ WRONG
  except Exception as e:
      return {"error": str(e)}  # Stacktrace exposed!
  
  # ✅ CORRECT
  except Exception as e:
      logger.error(f"Query failed: {e}")
      return {"error": "Internal server error"}  # Generic message
  ```
- [ ] HTTPS ist erzwungen (in Production)
- [ ] CORS ist restrictiv konfiguriert
- [ ] Secrets sind nicht in Logs
  ```python
  # ❌ WRONG
  logger.info(f"Using API Key: {OPENAI_API_KEY}")
  
  # ✅ CORRECT
  logger.info("Using OpenAI API")
  ```
- [ ] Regelmäßige Audit-Log Reviews

---

## 10. Compliance & Standards

### Anwendbare Standards

| Standard | Relevanz | Scope |
|----------|----------|-------|
| **GDPR** | Audit Trails, Datenscutz | EU, User Data |
| **ISO 27001** | Information Security Management | Production Deployment |
| **OWASP Top 10** | Web Application Security | All Kappa APIs |
| **CWE/SANS Top 25** | Common Weaknesses | Code Review |
| **SOC 2 Type II** | Security Controls | Production Hosting |

### GDPR Compliance

Kappa führt User-Aktionen in Audit-Trail auf:

```json
{
  "timestamp": "2026-05-08T14:23:45.123Z",
  "user": "founder",
  "action": "query",
  "ip_address": "127.0.0.1",
  "input_hash": "sha256:abc123..."  // Input anonymisiert
}
```

**Regeln**:
- User hat Recht auf Dateneinsicht (GET /audit-log?user=X)
- User hat Recht auf Löschung (DELETE /audit-log?user=X) nach Retention-Periode
- Standardmäßige Retention: 90 Tage

---

## Status

✅ Layer-basiertes Security Model  
✅ Pydantic Input Validation  
✅ JWT Token Support  
✅ Rate Limiting (60 req/min)  
✅ Append-Only Audit Trail  
✅ Secrets Management Best Practices  
✅ Known Limitations Documented  

**MVP Release Candidate bereit für Local Demo**  
**Production Readiness**: Requires HTTPS Reverse Proxy + JWT Secret Rotation

