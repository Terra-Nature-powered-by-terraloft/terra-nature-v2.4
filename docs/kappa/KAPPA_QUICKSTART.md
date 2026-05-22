# Kappa Quickstart - 5 Minuten zum Erfolg

**Ziel**: Kappa starten, Health Check durchführen, erste Query testen.

---

## Schritt 1: Vorbereitung (1 Min)

```bash
# Ins Projekt-Verzeichnis
cd terra-nature-v2.4
git checkout claude/terra-nature-kappa-assistant-z35mP

# Python Virtual Environment
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux (oder: venv\Scripts\activate auf Windows)

# Dependencies installieren
pip install -r requirements.txt
pip install -r kappa/requirements.txt
```

---

## Schritt 2: Kappa Server starten (30 Sekunden)

**Terminal 1:**
```bash
# Im venv
source venv/bin/activate

# Starte FastAPI Server
python -m uvicorn kappa.main:app --host 127.0.0.1 --port 8000 --reload
```

**Erwartet Output:**
```
{"event": "kappa_startup", "environment": "development", ...}
Uvicorn running on http://127.0.0.1:8000
```

✅ Server läuft!

---

## Schritt 3: Health Check (30 Sekunden)

**Terminal 2:**
```bash
# Health Check
curl http://127.0.0.1:8000/api/kappa/health

# Oder mit Python:
python -c "
import requests
r = requests.get('http://127.0.0.1:8000/api/kappa/health')
print(f'Status: {r.status_code}')
print(f'Health: {r.json()}')
"
```

**Erwartet:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-08T08:00:00Z",
  "version": "0.1.0-phase8",
  "components": {"engine": "ready", "memory": "ready", "kb": "ready"}
}
```

✅ Health Check bestanden!

---

## Schritt 4: Erste Query (1 Min)

**Option A: curl**
```bash
curl -X POST http://127.0.0.1:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Was ist ORC?", "mode": "default"}'
```

**Option B: Python**
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/kappa/query",
    json={"text": "Was ist ORC?", "mode": "default"}
)
print(response.json())
```

**Option C: JavaScript/Fetch**
```javascript
fetch("http://127.0.0.1:8000/api/kappa/query", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({text: "Was ist ORC?", mode: "default"})
})
.then(r => r.json())
.then(data => console.log(data))
```

**Erwartet Response:**
```json
{
  "response": "ORC ist ein Organic Rankine Cycle...",
  "mode": "default",
  "confidence": 0.85,
  "timestamp": "2026-05-08T08:00:00Z",
  "approval_level": "approved"
}
```

✅ Query erfolgreich!

---

## Schritt 5: Expert Mode Test (30 Sekunden)

Teste Kappa mit verschiedenen Expert Modes:

```bash
# CTO Mode (Technische Fachlichkeit)
curl -X POST http://127.0.0.1:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Ist eine Effizienz von 80% technisch realistisch?", "mode": "cto"}'

# MRV Mode (Compliance & Messung)
curl -X POST http://127.0.0.1:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Wie wird CO2-Einsparung verifiziert?", "mode": "mrv"}'

# Bank Mode (Finanzierungsfähigkeit)
curl -X POST http://127.0.0.1:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Ist das Projekt bankfähig?", "mode": "bank"}'
```

---

## Schritt 6: Tests ausführen (1 Min)

**Terminal 3:**
```bash
source venv/bin/activate

# Alle 219 Tests ausführen
pytest kappa/tests/ tests/kappa/ -v --tb=short

# Nur schnelle Tests
pytest kappa/tests/test_api.py::TestHealthEndpoint -v
```

**Erwartet:**
```
219 passed in 1.23s ✅
```

---

## Schritt 7: Dashboard starten (Optional, 1 Min)

```bash
# Terminal 4: Kein venv nötig
npm install  # erste Mal
npm run dev
# Öffne: http://localhost:3000
```

---

## Validieren Sie den Status

| Punkt | Command | Erwartet |
|-------|---------|----------|
| **Health** | `curl http://127.0.0.1:8000/api/kappa/health` | 200, status=healthy |
| **Query** | `curl -X POST ... /query` | 200, response text |
| **Validation** | `curl -X POST ... /validate` | 200 or 422 |
| **Memory Save** | `curl -X POST ... /memory/save` | 200 |
| **Tests** | `pytest kappa/tests/ -q` | 219 passed |
| **Dashboard** | Browser: http://localhost:3000 | UI lädt |

---

## Häufige Fehler & Fixes

### ❌ `ModuleNotFoundError: No module named 'kappa'`
```bash
# Fix: Sicherstelle venv ist aktiviert
source venv/bin/activate
pip install -r kappa/requirements.txt
```

### ❌ `Connection refused: http://127.0.0.1:8000`
```bash
# Server läuft nicht in Terminal 1
# Starte: python -m uvicorn kappa.main:app --reload
```

### ❌ `CORS Error im Dashboard`
```bash
# Prüfe .env.local:
# NEXT_PUBLIC_KAPPA_API_URL=http://localhost:8000
```

### ❌ Tests schlagen fehl
```bash
# Sicherstelle alle Dependencies sind installiert:
pip install -r requirements.txt
pip install -r kappa/requirements.txt
pip install pytest pytest-asyncio httpx
```

### ⚠️ Whisper/Vision funktioniert nicht
```bash
# Normal im Mock-Modus! Setze in .env.local:
KAPPA_MOCK_MODE=true
# Für echter Funktionalität: API-Keys hinzufügen
```

---

## Next Steps

1. **Weitere Queries testen**: Siehe `KAPPA_API.md`
2. **Expert Modes verstehen**: Siehe `KAPPA_EXPERT_MODES.md`
3. **Validation verstehen**: POST `/validate` mit verschiedenen Statements
4. **Memory testen**: Daten speichern und abrufen mit `/memory`
5. **Audit Trail prüfen**: GET `/audit-log` um alle Aktionen zu sehen

---

## Status

✅ **Kappa läuft lokal**  
✅ **219 Tests bestanden**  
✅ **Health Check erfolgreich**  
✅ **Mock-Modus aktiviert**  
✅ **Bereit zum Testen**

---

Benötigst du Hilfe? Siehe **KAPPA_TROUBLESHOOTING.md**
