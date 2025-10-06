# terra-nature-v2.4
Dashboards zur CO₂-Tracking, Terra Nature selbst ist ein Konzept zur CO₂-Kompensation mit technischen und ökonomischen Modellen.

## Demo WebSocket Servers

Zwei einfache Demo-Server erzeugen zufällige NRG-Event-Payloads.

## Agentenmodus

Um eventuelle Arbeitsanweisungen in `AGENTS.md`-Dateien zu prüfen, kann das Hilfsskript `tools/agentenmodus.py` ausgeführt werden:

```bash
python tools/agentenmodus.py
```

Es durchsucht das Repository (ausgenommen Caches und `node_modules`) und gibt alle gefundenen Instruktionen aus.

### Node.js
- Abhängigkeiten installieren: `npm install`
- Server starten: `node tools/ws_demo_server.js`

### Python
- Abhängigkeiten installieren: `pip install -r requirements.txt`
- Server starten: `python tools/ws_demo_server.py`

Jede Verbindung erhält Nachrichten wie `{"type": "NRG", "value": 0.42, "id": "..."}`.

## Tests

Unit-Tests für beide Implementierungen ausführen:

```bash
npm test
```
