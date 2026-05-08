# Kappa Troubleshooting - Häufige Probleme & Lösungen

**Version**: 0.1.0-phase8  
**Status**: MVP Release Candidate  
**Last Updated**: 2026-05-08

---

## Übersicht Fehler-Kategorien

1. **Installation & Setup** - Python venv, Dependencies
2. **Server-Start** - FastAPI/Uvicorn Fehler
3. **Connectivity** - Port, CORS, Networking
4. **API Fehler** - Invalid Requests, Missing Parameters
5. **External Services** - Whisper, Claude Vision, Anthropic
6. **Database** - SQLite, Memory, Knowledge Base
7. **Performance** - Slow Responses, Timeouts
8. **Security** - JWT, Rate Limiting, Secrets

---

## 1. Installation & Setup Fehler

### ❌ `ModuleNotFoundError: No module named 'kappa'`

**Symptom**:
```
python -m pytest kappa/tests/test_api.py
ModuleNotFoundError: No module named 'kappa'
```

**Ursachen**:
1. Python Virtual Environment nicht aktiviert
2. Dependencies nicht installiert
3. Working Directory falsch

**Fix**:
```bash
# 1. Prüfe venv
which python  # Should show /path/to/venv/bin/python

# Wenn NICHT im venv:
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# oder
venv\Scripts\activate  # Windows

# 2. Installiere Dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r kappa/requirements.txt

# 3. Prüfe Working Directory
pwd  # Should be /home/user/terra-nature-v2.4
cd terra-nature-v2.4

# 4. Teste Import
python -c "import kappa; print('OK')"
```

### ❌ `pip: command not found`

**Symptom**:
```
-bash: pip: command not found
```

**Fix**:
```bash
# Python nicht installiert oder Pfad falsch
python3 --version  # Check Python version
python3 -m pip --version  # Use python3 -m pip

# Oder installiere pip
python3 -m ensurepip --upgrade

# Oder längerer Weg
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

### ❌ `Permission denied: venv/bin/activate`

**Symptom**:
```
source venv/bin/activate
-bash: venv/bin/activate: Permission denied
```

**Fix**:
```bash
# Linux/macOS: Permissions setzen
chmod +x venv/bin/activate
source venv/bin/activate

# Oder venv neu erstellen
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
```

### ❌ `package requirements could not be resolved`

**Symptom**:
```
pip install -r requirements.txt
ERROR: Could not find a version that satisfies the requirement fastapi==0.104.1
```

**Fix**:
```bash
# Upgrade pip
pip install --upgrade pip

# Oder spezifische Python-Version
python3.11 -m pip install -r requirements.txt

# Oder probiere ohne spezifische Version
pip install fastapi uvicorn pydantic

# Oder nutze constraints
pip install -r requirements.txt --upgrade
```

---

## 2. Server-Start Fehler

### ❌ `Address already in use: 127.0.0.1:8000`

**Symptom**:
```
python -m uvicorn kappa.main:app --port 8000
ERROR: Address already in use
```

**Ursache**: Ein anderer Prozess nutzt Port 8000

**Fix**:
```bash
# 1. Finde Process der Port nutzt
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# 2. Kill den Process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# 3. Oder nutze anderen Port
python -m uvicorn kappa.main:app --port 8001

# 4. Oder killall
pkill -f uvicorn  # Kill all uvicorn processes
```

### ❌ `OSError: [Errno 48] Address already in use`

Siehe oben, aber auf macOS manchmal persistenter:

```bash
# Warte 60 Sekunden bis SO_REUSEADDR aktiv wird
sleep 60
python -m uvicorn kappa.main:app --port 8000

# Oder nutze --reload flag nicht bei Neustart
python -m uvicorn kappa.main:app --port 8000 --no-reload
```

### ❌ `ImportError: cannot import name 'engine' from 'kappa.core'`

**Symptom**:
```
python -m uvicorn kappa.main:app
ImportError: cannot import name 'engine' from 'kappa.core'
```

**Ursache**: Relative imports bei TestClient

**Fix**:
```python
# kappa/main.py - Verwende relative imports
# ❌ FALSCH
from config import KappaConfig
from api.routes import router

# ✅ RICHTIG
from .config import KappaConfig
from .api.routes import router
```

### ❌ `ModuleNotFoundError: No module named 'uvicorn'`

**Symptom**:
```
python -m uvicorn kappa.main:app
ModuleNotFoundError: No module named 'uvicorn'
```

**Fix**:
```bash
# Installiere uvicorn
pip install uvicorn

# Oder speziell mit Standard-Extras
pip install "uvicorn[standard]"

# Oder aus requirements.txt
pip install -r kappa/requirements.txt
```

---

## 3. Connectivity Fehler

### ❌ `Connection refused: http://127.0.0.1:8000`

**Symptom**:
```
curl http://127.0.0.1:8000/api/kappa/health
curl: (7) Failed to connect to 127.0.0.1 port 8000: Connection refused
```

**Ursache**: Kappa Server läuft nicht

**Fix**:
```bash
# 1. Prüfe ob Server läuft
ps aux | grep uvicorn

# 2. Starte Server in neuem Terminal
python -m uvicorn kappa.main:app --host 127.0.0.1 --port 8000

# 3. Warte auf Startup-Message
# Expected:
#   INFO:     Uvicorn running on http://127.0.0.1:8000

# 4. Teste in anderem Terminal
curl http://127.0.0.1:8000/api/kappa/health
```

### ❌ `CORS error: No 'Access-Control-Allow-Origin' header`

**Symptom** (Browser Console):
```
Access to XMLHttpRequest at 'http://localhost:8000/api/kappa/query'
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Ursache**: CORS nicht konfiguriert oder restrictiv

**Fix**:
```python
# kappa/main.py - Stelle sicher CORS ist konfiguriert
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Oder in Development (weniger sicher):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ❌ `Failed to establish a new connection`

**Symptom**:
```
requests.exceptions.ConnectionError: Failed to establish a new connection
```

**Ursache**: 
1. Server läuft nicht
2. Port ist falsch
3. Hostname ist falsch

**Fix**:
```bash
# 1. Prüfe Server läuft
curl http://127.0.0.1:8000/api/kappa/health

# 2. Prüfe Port-Konfiguration
echo $KAPPA_PORT  # Check env var
grep "port" kappa/config.py

# 3. Prüfe Hostname
ping 127.0.0.1
ping localhost

# 4. Alternative Adresse testen
curl http://localhost:8000/api/kappa/health
```

---

## 4. API Fehler

### ❌ `422 Unprocessable Entity`

**Symptom**:
```
curl -X POST http://localhost:8000/api/kappa/query
{"detail":[{"loc":["body","text"],"msg":"field required","type":"value_error.missing"}]}
```

**Ursache**: Required Field fehlt oder falscher Typ

**Fix**:
```bash
# ❌ FALSCH - text Field fehlt
curl -X POST http://localhost:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{}'

# ✅ RICHTIG
curl -X POST http://localhost:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello Kappa"}'

# ❌ FALSCH - mode hat ungültigen Wert
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test", "mode": "superadmin"}'

# ✅ RICHTIG
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test", "mode": "cto"}'
```

### ❌ `400 Bad Request: Input validation failed`

**Symptom**:
```
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "SELECT * FROM users; DROP TABLE--"}'
{"error": "Invalid input", "details": "Potential SQL injection detected"}
```

**Fix**:
```bash
# Nutze reguläre Queries
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Wie viel CO2 wurde kompensiert?"}'

# Oder nutze Quotes richtig
curl -X POST http://localhost:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Ist eine Effizienz von 80% realistisch?"}'
```

### ❌ `413 Request Entity Too Large`

**Symptom**:
```
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "AAAAAA...(10000 chars)...AAAAAA"}'
413 Request Entity Too Large
```

**Fix**:
```bash
# Text-Limit ist 5000 chars
wc -c <<< "your text"  # Count chars

# Oder teile in mehrere Requests auf
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "First part of query"}'

curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Second part of query"}'
```

### ❌ `429 Too Many Requests`

**Symptom**:
```
curl -X POST http://localhost:8000/api/kappa/query ...
429 Too Many Requests
Retry-After: 30
```

**Fix**:
```bash
# Rate limit ist 60 requests/min/user
# Warte oder benutze unterschiedliche user IDs
sleep 30

# Oder spezifiziere anderen user
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test", "user": "analyst"}'

# Oder prüfe .env Konfiguration
grep RATE_LIMIT .env.local
```

---

## 5. External Services Fehler

### ❌ `OpenAI API Error: Invalid API Key`

**Symptom**:
```
python -m pytest tests/kappa/test_kappa_voice_flow.py
kappa.services.speech.WhisperError: API request failed: Invalid API key provided
```

**Ursache**: 
1. API Key nicht gesetzt
2. API Key ungültig
3. API Key hat kein Whisper-Zugang

**Fix**:
```bash
# 1. Prüfe .env.local
grep OPENAI_API_KEY .env.local

# 2. Setze API Key
export KAPPA_OPENAI_API_KEY="sk-proj-..."
echo "KAPPA_OPENAI_API_KEY=sk-proj-..." >> .env.local

# 3. Oder nutze Mock Mode
export KAPPA_MOCK_MODE=true

# 4. Teste mit Mock Mode
python -c "
import os
os.environ['KAPPA_MOCK_MODE'] = 'true'
from kappa.services.speech import WhisperService
print('Mock mode active - no API key needed')
"
```

### ❌ `anthropic.APIConnectionError: Connection error`

**Symptom**:
```
kappa.services.vision.VisionError: Claude API connection failed
anthropic.APIConnectionError: Connection timeout
```

**Ursache**:
1. Netzwerk nicht verbunden
2. Anthropic API unreachbar
3. API Key ungültig

**Fix**:
```bash
# 1. Prüfe Netzwerk
ping api.anthropic.com

# 2. Prüfe API Key
export KAPPA_ANTHROPIC_API_KEY="sk-ant-..."

# 3. Oder nutze Mock Mode
export KAPPA_MOCK_MODE=true

# 4. Teste Connectivity
curl -I https://api.anthropic.com
```

### ⚠️ `Mock Mode: Whisper not available`

**Info**:
```
kappa.services.speech: Whisper in Mock Mode - returning dummy transcription
```

**Das ist NORMAL in Mock Mode!**

```bash
# Zum Aktivieren von Real Whisper:
export KAPPA_MOCK_MODE=false
export KAPPA_OPENAI_API_KEY="sk-proj-..."

# Zum Deaktivieren und Mock verwenden:
export KAPPA_MOCK_MODE=true
# Kein API Key nötig
```

---

## 6. Database Fehler

### ❌ `sqlite3.OperationalError: database is locked`

**Symptom**:
```
kappa.core.knowledge_base: Error accessing KB
sqlite3.OperationalError: database is locked
```

**Ursache**: SQLite DB ist von anderem Process gesperrt

**Fix**:
```bash
# 1. Finde Process der DB sperrt
lsof kappa/data/kb.db

# 2. Kill den Process
kill -9 <PID>

# 3. Oder starte neuen Python Interpreter
python -c "import kappa; kappa.core.knowledge_base.init()"

# 4. Oder lösche und neuinitialisiere DB
rm -f kappa/data/kb.db
python -m pytest kappa/tests/test_knowledge_base.py -v
```

### ❌ `FileNotFoundError: kappa/data/kb.db not found`

**Symptom**:
```
kappa.core.knowledge_base: KB not initialized
FileNotFoundError: [Errno 2] No such file or directory: 'kappa/data/kb.db'
```

**Fix**:
```bash
# 1. Erstelle data directory
mkdir -p kappa/data

# 2. Initialisiere DB
python -c "
from kappa.core.knowledge_base import KnowledgeBase
kb = KnowledgeBase('kappa/data/kb.db')
kb.init_schema()
print('KB initialized')
"

# 3. Oder führe Tests aus (auto-init)
pytest kappa/tests/test_knowledge_base.py -v
```

### ❌ `JSONDecodeError: memory.jsonld`

**Symptom**:
```
json.JSONDecodeError: Expecting value: line 1 column 1
File "kappa/data/memory.jsonld"
```

**Ursache**: Memory-Datei ist korrupt oder leer

**Fix**:
```bash
# 1. Prüfe Datei
cat kappa/data/memory.jsonld

# 2. Wenn leer oder invalid - neuinitialisieren
python -c "
from kappa.core.memory import ProjectMemory
mem = ProjectMemory('kappa/data/memory.jsonld')
mem.init()
print('Memory initialized')
"

# 3. Oder backup + delete + recreate
cp kappa/data/memory.jsonld kappa/data/memory.jsonld.bak
rm kappa/data/memory.jsonld
python tests/kappa/test_terra_kappa_integration.py -v
```

---

## 7. Performance Fehler

### ⚠️ `Slow response: Request took 15+ seconds`

**Symptom**:
```
curl -w "Time: %{time_total}s\n" -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test"}'
Time: 15.234s
```

**Ursache**:
1. Claude Vision oder Whisper ist langsam
2. Knowledge Base Query ist komplex
3. Network Latency zu OpenAI/Anthropic

**Fix**:
```bash
# 1. Prüfe Network Latency
ping -c 3 api.openai.com
ping -c 3 api.anthropic.com

# 2. Nutze Mock Mode zum Testen
export KAPPA_MOCK_MODE=true
curl -w "Time: %{time_total}s\n" -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test"}'
# Sollte <1 Sekunde sein

# 3. Profiling aktivieren
export KAPPA_DEBUG=true
# Loggt execution times für jede Komponente

# 4. Prüfe Netzwerk-Bandwidth
iftop -n  # Real-time network monitoring
```

### ⚠️ `Memory usage increasing`

**Symptom**:
```
# Nach 1 Stunde Betrieb
ps aux | grep uvicorn
... 500MB RSS (was 200MB at start)
```

**Ursache**: Memory Leak oder große Datenstrukturen

**Fix**:
```bash
# 1. Prüfe Audit Log Größe
ls -lh kappa/data/audit.jsonl
# Wenn > 500MB - zu groß

# 2. Archive alte Logs
gzip kappa/data/audit.jsonl
mv kappa/data/audit.jsonl.gz kappa/data/audit.jsonl.gz.2026-05-01

# 3. Reduziere Logging
export KAPPA_LOG_LEVEL=WARNING

# 4. Starte Server neu
pkill uvicorn
python -m uvicorn kappa.main:app
```

---

## 8. Security Fehler

### ❌ `401 Unauthorized: Invalid token`

**Symptom** (Production Mode):
```
curl -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test"}'
401 Unauthorized: Invalid or missing authentication credentials
```

**Fix**:
```bash
# 1. Generiere Token
TOKEN=$(python -c "
from kappa.utils.security import TokenValidator
tv = TokenValidator('dev-secret-change-me')
print(tv.create_token('founder'))
")

# 2. Nutze Token
curl -H "Authorization: Bearer $TOKEN" \
  -X POST http://localhost:8000/api/kappa/query \
  -d '{"text": "Test"}'

# 3. Oder wechsle zu Development Mode
export KAPPA_DEBUG=true
# JWT ist dann optional
```

### ⚠️ `Warning: API keys found in code`

**Symptom**:
```
git pre-commit hook
Warning: Potential secrets detected in kappa/config.py
sk-proj-... found
```

**Fix**:
```bash
# 1. Entferne API Keys aus Code
git diff HEAD

# ❌ Falsch
OPENAI_API_KEY = "sk-proj-real-key"

# ✅ Richtig
OPENAI_API_KEY = os.getenv("KAPPA_OPENAI_API_KEY")

# 2. Setze in .env.local statt Code
echo "KAPPA_OPENAI_API_KEY=sk-proj-..." >> .env.local

# 3. Sicherstelle .env.local ist in .gitignore
grep "\.env\.local" .gitignore

# 4. Falls bereits gecheckt - rewrite history
git filter-branch --tree-filter 'rm -f kappa/config.py' HEAD
# ⚠️ GEFÄHRLICH - nur wenn nicht gepusht
```

---

## 9. Testing Fehler

### ❌ `pytest: command not found`

**Symptom**:
```
pytest kappa/tests/
-bash: pytest: command not found
```

**Fix**:
```bash
# 1. Installiere pytest
pip install pytest pytest-asyncio

# 2. Oder nutze python -m
python -m pytest kappa/tests/ -v

# 3. Oder installiere aus requirements
pip install -r kappa/requirements.txt
```

### ❌ `TestClient: Relative import failed`

**Symptom**:
```
pytest kappa/tests/test_api.py
ImportError: cannot import name 'app' from 'kappa.main'
(import of kappa.main halted; None of error; absolute_import is enabled)
```

**Fix**:
```python
# kappa/main.py - Verwende relative imports
# ❌ FALSCH
from config import KappaConfig

# ✅ RICHTIG
from .config import KappaConfig
```

### ❌ `Test timeout: Request timed out after 30s`

**Symptom**:
```
pytest tests/kappa/test_kappa_voice_flow.py -v
FAILED test_voice_roundtrip - Request timed out after 30.0s
```

**Ursache**: External Service (Whisper/Claude) ist langsam oder down

**Fix**:
```bash
# 1. Nutze Mock Mode
export KAPPA_MOCK_MODE=true
pytest tests/kappa/test_kappa_voice_flow.py -v

# 2. Oder erhöhe Timeout
pytest tests/kappa/ -v --timeout=60

# 3. Oder skip Integration Tests
pytest kappa/tests/ -v -m "not integration"
```

---

## 10. Schnell-Referenz: 5-Minuten Fixes

| Problem | Command |
|---------|---------|
| Server läuft nicht | `python -m uvicorn kappa.main:app --reload` |
| Port belegt | `lsof -i :8000 && kill -9 <PID>` |
| API Key fehlt | `export KAPPA_MOCK_MODE=true` |
| Tests schlagen fehl | `pip install -r kappa/requirements.txt && pytest kappa/tests/` |
| CORS Error | Check `kappa/main.py` CORS config |
| DB Lock | `rm -f kappa/data/kb.db && mkdir -p kappa/data` |
| Slow Response | `export KAPPA_MOCK_MODE=true` and test |
| Memory Leak | `pkill uvicorn` and restart |
| Permission Denied | `chmod +x venv/bin/activate` |
| Module Not Found | `source venv/bin/activate` |

---

## Support & Escalation

### Wenn alles andere fehlschlägt:

1. **Sammle Logs**:
   ```bash
   tail -50 kappa/data/audit.jsonl
   ps aux | grep uvicorn
   env | grep KAPPA
   ```

2. **Führe Diagnose-Test aus**:
   ```bash
   python -m pytest kappa/tests/test_api.py::TestHealthEndpoint -vv
   ```

3. **Überprüfe .env.local**:
   ```bash
   cat .env.local | grep -E "KAPPA|NEXT_PUBLIC"
   ```

4. **Dokumentiere**:
   - Fehler-Nachricht (vollständig)
   - Ursache (wenn bekannt)
   - Umgebung (Python version, OS)
   - Bisherige Fix-Versuche

5. **Öffne Issue** in GitHub mit obigen Details

---

**Status**: Troubleshooting Guide vollständig  
**MVP Release Candidate bereit**

