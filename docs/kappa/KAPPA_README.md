# Kappa - Terra Nature Expert Assistant
## MVP Release Candidate (Phase 1-8 Complete)

**Status**: Technisch vollständig, dokumentiert und getestet  
**Version**: 0.1.0-phase8  
**Last Updated**: 2026-05-08  
**Test Suite**: 219/219 passing ✅

---

## Was ist Kappa?

Kappa ist der **lokale, projektgebundene Expertenassistent für Terra Nature powered by Terraloft**. 

Während das bestehende Terra-Nature Dashboard ein passives CO₂-Tracking-Visualisierungstool ist, ist Kappa ein **aktiver intelligenter Operator-Assistent**, der:

- **Sprachgesteuert** Fragen beantwortet („Wie viel CO₂ wurde heute kompensiert?")
- **Expertenregeln prüft** (technisch, wissenschaftlich, regulatorisch, bankfähig)
- **Projektkontext verwaltet** (Wissensbank, Gedächtnis, Entscheidungsprotokolle)
- **MRV-Nachweise führt** (Monitoring, Reporting, Verification)
- **Lokal läuft** (keine Cloud-Abhängigkeit, Datenschutz)

---

## Architektur

```
┌─────────────────────────────────────────┐
│  Terra Nature Dashboard (Next.js 14)    │
│  Benutzerinterface & CO₂-Metriken       │
└────────────┬────────────────────────────┘
             │ HTTP / REST
             │
┌────────────▼────────────────────────────┐
│  Kappa Bridge Layer (Next.js API)       │
│  Audit-Logging, Rate-Limiting, Token    │
│  Location: /app/api/kappa/              │
└────────────┬────────────────────────────┘
             │ localhost:8000 (HTTP)
             │
┌────────────▼────────────────────────────┐
│  Kappa Expert Engine (FastAPI)          │
│  Location: /kappa/ (separat)            │
├────────────────────────────────────────┤
│ • Intent Recognition                    │
│ • Knowledge Base (SQLite)               │
│ • Project Memory (JSON-LD)              │
│ • Expert Validation Engine (9 Modi)     │
│ • MRV Compliance Logic                  │
│ • Whisper Integration (Sprache)         │
│ • Claude Vision (Screenshots)           │
│ • Audit Trail (append-only)             │
└─────────────────────────────────────────┘
```

---

## Lokale Installation

### Anforderungen
- **Python 3.10+** (getestet mit 3.11)
- **Node.js 20+** (für Dashboard)
- **pip** (Python Package Manager)
- Optional: **OpenAI API Key** (Whisper) und **Anthropic API Key** (Claude)

### Schritt-für-Schritt

#### 1. Repository klonen
```bash
git clone https://github.com/terra-nature-powered-by-terraloft/terra-nature-v2.4.git
cd terra-nature-v2.4
git checkout claude/terra-nature-kappa-assistant-z35mP
```

#### 2. Python-Umgebung
```bash
# Virtual Environment (empfohlen)
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# oder
venv\Scripts\activate  # Windows

# Dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r kappa/requirements.txt
```

#### 3. Node.js-Umgebung
```bash
npm install
```

#### 4. Umgebungsvariablen
```bash
# Kopiere Beispiel
cp .env.example .env.local

# Bearbeite .env.local (optional: API-Keys)
# KAPPA_OPENAI_API_KEY=sk-...      (optional)
# KAPPA_ANTHROPIC_API_KEY=sk-ant-  (optional)

# Default: MOCK_MODE=true (funktioniert ohne Keys!)
```

#### 5. Datenverzeichnisse erstellen
```bash
mkdir -p kappa/data
mkdir -p kappa/rules
```

---

## Schnellstart (5 Minuten)

### Terminal 1: FastAPI Kappa Server
```bash
# Aktiviere venv
source venv/bin/activate

# Starte Kappa (localhost:8000)
python -m uvicorn kappa.main:app --host 127.0.0.1 --port 8000 --reload
```

### Terminal 2: Next.js Dashboard
```bash
# Neue Shell, nicht activate nötig
npm run dev
# Öffne http://localhost:3000
```

### Terminal 3: Tests
```bash
source venv/bin/activate
pytest kappa/tests/ tests/kappa/ -v
```

### Erste Schritte
1. **Health Check**: GET http://localhost:8000/api/kappa/health
2. **Test Query**: POST http://localhost:8000/api/kappa/query (Body: `{"text": "Test"}`)
3. **Dashboard**: Besuche http://localhost:3000

---

## Kommandos

### Kappa Server
```bash
# Entwicklungs-Modus (mit auto-reload)
python -m uvicorn kappa.main:app --reload

# Produktions-Modus
python -m uvicorn kappa.main:app --host 0.0.0.0 --port 8000

# Alternative: npm Script
npm run kappa:start
```

### Tests
```bash
# Alle Tests
pytest kappa/tests/ tests/kappa/ -v

# Nur Core Tests
pytest kappa/tests/test_engine.py kappa/tests/test_api.py -v

# Mit Coverage
pytest kappa/tests/ tests/kappa/ --cov=kappa --cov-report=html

# E2E Tests
pytest tests/kappa/test_kappa_voice_flow.py -v
pytest tests/kappa/test_terra_kappa_integration.py -v
```

### Dashboard
```bash
# Entwicklungs-Server
npm run dev

# Production Build
npm run build
npm start
```

---

## Mock-Modus

**Kappa funktioniert vollständig ohne API-Keys im Mock-Modus!**

```bash
# .env.local
KAPPA_MOCK_MODE=true
KAPPA_OPENAI_API_KEY=         # Leer
KAPPA_ANTHROPIC_API_KEY=      # Leer
```

Im Mock-Modus:
- ✅ Health Check funktioniert
- ✅ Query-Verarbeitung funktioniert (mit dummy responses)
- ✅ Validation funktioniert
- ✅ Memory speichert und ruft ab
- ✅ Audit Trail wird geschrieben
- ⚠️ Whisper (Speech-to-Text) nicht verfügbar
- ⚠️ Claude Vision nicht verfügbar
- ⚠️ Anthropic-basierte Validation limited

**Für Production-Features**: Setze API-Keys in `.env.local`

---

## Umgebungsvariablen

### Zentrale Konfiguration
```bash
# === SERVER ===
KAPPA_ENV=development          # development | production
KAPPA_DEBUG=true               # true | false
KAPPA_PORT=8000                # Port für FastAPI
KAPPA_HOST=127.0.0.1           # Host (lokal: 127.0.0.1)

# === SECURITY ===
KAPPA_JWT_SECRET=dev-secret    # Ändere in Production!

# === API KEYS (optional) ===
KAPPA_OPENAI_API_KEY=          # Für Whisper
KAPPA_ANTHROPIC_API_KEY=       # Für Claude Vision

# === FEATURE FLAGS ===
KAPPA_MOCK_MODE=true           # true = läuft ohne API-Keys
KAPPA_ENABLE_AUDIT=true        # Audit Logging

# === DATEN ===
KAPPA_KB_PATH=./kappa/data/kb.db
KAPPA_MEMORY_PATH=./kappa/data/memory.jsonld
KAPPA_AUDIT_PATH=./kappa/data/audit.jsonl
KAPPA_RULES_PATH=./kappa/rules

# === DASHBOARD ===
NEXT_PUBLIC_KAPPA_API_URL=http://localhost:8000
NEXT_PUBLIC_KAPPA_ENABLED=true
```

---

## Test-Abdeckung

**219 Tests** in 3 Kategorien:

| Category | Tests | Status |
|----------|-------|--------|
| Unit Tests (Engine, API, Services) | 59 | ✅ Bestanden |
| E2E Voice Flow | 20 | ✅ Bestanden |
| Terra-Kappa Integration | 26 | ✅ Bestanden |
| Phase 7 UI Integration | 13 | ✅ Bestanden |
| Knowledge Base, Memory, Security, Speech, Vision | 101 | ✅ Bestanden |
| **Total** | **219** | **✅ Bestanden** |

---

## Dateistruktur

```
terra-nature-v2.4/
├── kappa/                          # FastAPI Expert Engine
│   ├── main.py                    # Entry Point
│   ├── config.py                  # Konfiguration
│   ├── core/
│   │   ├── engine.py             # Expert Engine (zentral!)
│   │   ├── knowledge_base.py      # SQLite KB
│   │   ├── memory.py             # JSON-LD Memory
│   │   └── intent.py             # Intent Recognition
│   ├── services/
│   │   ├── expert_validator.py   # Multi-Expert Prüfung
│   │   ├── mrv.py               # MRV Compliance
│   │   ├── speech.py            # Whisper Integration
│   │   └── vision.py            # Claude Vision
│   ├── api/
│   │   ├── routes.py            # FastAPI Routes
│   │   └── models.py            # Pydantic Models
│   ├── utils/
│   │   ├── logging.py           # Structured Logging
│   │   ├── security.py          # JWT, Rate-Limiting
│   │   ├── audit.py             # Audit Trail
│   │   └── database.py          # SQLite Connection Pool
│   ├── data/
│   │   ├── kb.db               # Knowledge Base (SQLite)
│   │   ├── memory.jsonld       # Project Memory
│   │   └── audit.jsonl         # Audit Trail (JSON-L)
│   └── tests/
│       ├── test_engine.py      # Engine Tests (29)
│       ├── test_api.py         # API Tests (30)
│       └── ... weitere Tests
│
├── app/                           # Next.js Dashboard
│   ├── api/kappa/               # Bridge Routes
│   ├── kappa-ui/                # Kappa Orb UI
│   └── page.tsx                 # Main Dashboard
│
├── lib/kappa/                    # TypeScript Client
│   ├── types.ts                # Type-Definitionen
│   ├── client.ts               # FastAPI Client
│   └── audit/logger.ts         # Audit Logging
│
├── tests/kappa/                 # E2E Tests
│   ├── test_kappa_voice_flow.py
│   └── test_terra_kappa_integration.py
│
├── .github/workflows/            # CI/CD
│   ├── kappa-test.yml
│   └── kappa-health-check.yml
│
└── docs/kappa/                   # Dokumentation
    ├── KAPPA_README.md          # Dieses Dokument
    ├── KAPPA_QUICKSTART.md
    ├── KAPPA_API.md
    ├── KAPPA_EXPERT_MODES.md
    ├── KAPPA_SECURITY.md
    ├── KAPPA_TROUBLESHOOTING.md
    ├── KAPPA_RELEASE_CHECKLIST.md
    └── KAPPA_ARCHITECTURE_FINAL.md
```

---

## Bekannte Einschränkungen

| Limitation | Details | Workaround |
|------------|---------|-----------|
| **Whisper Integration** | Benötigt OpenAI API Key | KAPPA_MOCK_MODE=true |
| **Claude Vision** | Benötigt Anthropic API Key | KAPPA_MOCK_MODE=true |
| **Anthropic Validation** | Limited ohne API Key | Lokale Rule Engine verwenden |
| **Voice Output (TTS)** | Nicht implementiert | Text-Responses verwenden |
| **Distributed Deployment** | Nur lokal auf localhost | Für Cluster: Docker erforderlich |
| **Persistent Memory** | JSON-LD (dateibasiert) | Für Scale: PostgreSQL erforderlich |

---

## Nächste Schritte (Phase 9+)

- **Phase 9**: Performance Optimization
- **Phase 10**: Docker & Deployment
- **Phase 11**: CLI Tool & Desktop App
- **Phase 12**: Advanced ML Features

---

## Support & Issues

### Häufige Probleme
Siehe **KAPPA_TROUBLESHOOTING.md**

### Sicherheit
Siehe **KAPPA_SECURITY.md**

### API-Dokumentation
Siehe **KAPPA_API.md**

### Expert Modes
Siehe **KAPPA_EXPERT_MODES.md**

---

## Lizenz & Attribution

Terra Nature powered by Terraloft  
Kappa Expert Engine v0.1.0  
Entwicklung: 2026 Q2

---

**Status: MVP Release Candidate**  
Bereit für interne Demo und lokale Validierung.
