# Kappa Expert Modes - Perspektiven und Validierung

**Version**: 0.1.0-phase8  
**Status**: MVP Release Candidate  
**Last Updated**: 2026-05-08

---

## Übersicht der Expert Modes

Kappa verfügt über **9 spezialisierte Expert-Perspektiven**, die verschiedene Aspekte der Terra-Nature-Mission validieren und bewerten.

| Mode | Fokus | Anwendungsfall | Validierungskriterien |
|------|-------|-----------------|----------------------|
| **cto** | Technische Realität | Engineering-Fragen | Physikalische Machbarkeit, Standards |
| **mrv** | Regulatorische Konformität | Nachweise & Messung | Messbar, verifizierbar, Standards-konform |
| **bank** | Bankfähigkeit | Finanzierungsgespräche | Rentabilität, Kreditfähigkeit, Risiko |
| **funding** | Fördermittel-Eignung | Zuschussanträge | EXIST, WIPANO, BayStartUP-Kriterien |
| **industrial** | Kundenrelevanz | Industriepartner | Problemlösung für Stadtwerke, MHKW |
| **ip** | Schutzrechte | IP-Strategie | Patent-Freiheit, Geheimhaltung, Lizenz |
| **communication** | Messaging-Fähigkeit | PR & Marketing | Verständlichkeit, Compliance, Tonalität |
| **professorale** | Wissenschaftlichkeit | Akademische Validierung | Peer-Review-Standard, Methodologie |
| **business** | Geschäftsentwicklung | Skalierungsstrategie | Markt, Wettbewerb, Geschäftsmodell |

---

## 1. CTO / Technische Perspektive

### Beschreibung
Die CTO-Perspektive validiert Aussagen gegen **ingenieurwissenschaftliche Standards und praktische Machbarkeit**. Sie wird von der Frage geleitet: "Ist das technisch realistisch und implementierbar?"

### Validierungskriterien
- ✅ Physikalische Plausibilität (Thermodynamik, Fluiddynamik für ORC)
- ✅ Einhaltung von technischen Standards (DIN, EN, IEC)
- ✅ Bekannte Engineering-Grenzen und -Toleranzen
- ✅ Materialwissenschaft und Verfügbarkeit
- ✅ Integrationsmöglichkeit mit bestehenden Systemen
- ⚠️ Neu-Entwicklung benötigt zusätzliche Validierung

### Confidence Level Indikatoren
- **0.9+**: Bewährte Technologie, mehrfach implementiert
- **0.7-0.9**: Technisch validiert, aber begrenzte Einsätze
- **0.5-0.7**: Konzeptmäßig korrekt, Implementierung unklar
- **<0.5**: Hohe technische Risiken oder unbekannte Faktoren

### Beispiele

**Query 1: ORC-Effizienz-Validierung**
```bash
curl -X POST http://localhost:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Ist eine Effizienz von 80% für einen ORC bei 95°C Wärmeeingang realistisch?",
    "mode": "cto"
  }'
```

**Response (CTO Mode)**
```json
{
  "response": "Eine ORC-Effizienz von 80% bei 95°C ist technisch unrealistisch. 
              Typische Werte liegen bei 15-25% brutto. Grund: Carnot-Limit bei 
              ΔT=70°C beträgt ~19%. Mit Arbeitsflüssigkeit R245fa sind 18-22% 
              realistisch. Empfehlung: Zieleffizienz auf 20% senken oder 
              Wärmequelle auf 120°C+ erhöhen.",
  "mode": "cto",
  "confidence": 0.92,
  "feedback": "Technisch plausibel bei Anpassung. ORC-Systeme dieser Größe sind etabliert.",
  "suggestions": [
    "Spezifiziere die Arbeitsflüssigkeit (R245fa, R134a, Pentan?)",
    "Nennen Sie die Wärmequelle genauer (Motorabgas, Abwärme aus X)",
    "Klären Sie die Effizienzreferenz (brutto vs. netto, inklusive Generator?)"
  ],
  "conditions": [
    "Effizienz muss auf physikalisch realistische 18-22% angepasst werden"
  ]
}
```

**Query 2: Systemintegration**
```bash
curl -X POST http://localhost:8000/api/kappa/query \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Können wir den ORC auf bestehende Heizungsanlagen ohne Umbau retrofitten?",
    "mode": "cto"
  }'
```

**Response (CTO Mode)**
```json
{
  "response": "Retrofit auf bestehende Anlagen ist möglich, erfordert aber 
              Wärmetauscher-Integration. Typische Anpassungen: 1) Separate 
              Wärmekreislauf-Planung, 2) Druckbehälter + Sicherheitsventile, 
              3) Steuer-Integration (zeitliche Abstimmung mit Lastprofil). 
              Kosten ca. €5-15k für Komponenten + Installation.",
  "mode": "cto",
  "confidence": 0.85,
  "feedback": "Technisch machbar mit Standard-Komponenten. Keine Spezial-Entwicklung nötig.",
  "suggestions": [
    "Definieren Sie die Zielanlage (Heizwerk, Industrieofen, BHKW?)",
    "Klären Sie die verfügbare Wärmemenge und -profil",
    "Prüfen Sie Platzbeschränkungen für Wärmetauscher"
  ],
  "conditions": [
    "Wärmequelle muss stabil >80°C für >500h/Jahr sein",
    "Kühlwasser-Verfügbarkeit für Kondensator erforderlich"
  ]
}
```

---

## 2. MRV / Compliance und Measurement

### Beschreibung
MRV = **Monitoring, Reporting, Verification**. Diese Perspektive validiert, ob Aussagen **messbar, verifizierbar und dokumentierbar** sind. Sie stellt sicher, dass CO₂-Einsparungen regulatorisch anerkannt werden (EnEfG, EU-ETS, CDM-Standards).

### Validierungskriterien
- ✅ Daten sind messbar mit bekannten Instrumenten
- ✅ Messprotokolle existieren und sind dokumentiert
- ✅ Unsicherheit der Messungen quantifizierbar (<10% typisch)
- ✅ Audit-Trail vorhanden (wer, wann, wie gemessen?)
- ✅ Unabhängige Verifikation möglich
- ✅ Konformität mit EnEfG, EU-ETS, oder äquivalenten Standards

### Approval Levels
- **approved**: Messbar und verifizierbar nach Standards
- **conditional**: Messbar mit zusätzlichen Instrumenten oder Kalibrierung
- **requires_review**: Methodologie unklar oder nicht-standard

### Beispiele

**Query 1: CO₂-Einsparung Verification**
```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Heute wurden 5 Tonnen CO₂ durch unsere ORC-Anlage eingespart",
    "modes": ["mrv"]
  }'
```

**Response (MRV Validation)**
```json
{
  "results": {
    "mrv": {
      "expert": "MRV/Compliance",
      "approved": false,
      "confidence": 0.65,
      "feedback": "Aussage ist unvollständig für MRV-Konformität. Mehrere kritische 
                   Informationen fehlen: Basislinie, Messprotokoll, Zeitstempel.",
      "suggestions": [
        "Definiere die Baseline (Szenario ohne ORC)",
        "Spezifiziere die Messmethode (Energiezähler, Thermografie, Modell?)",
        "Nenne das Messintervall und die Messunsicherheit"
      ],
      "conditions": [
        "Zeitstempel erforderlich (Datum + Uhrzeit exakt)",
        "Messprotokoll gemäß DIN EN ISO 50001 oder äquivalent erforderlich",
        "Unabhängige Verifikation durch Dritte erforderlich",
        "Kalibrierung der Messinstrumente muss dokumentiert sein"
      ]
    }
  },
  "overall_approved": false
}
```

**Query 2: Messprotokoll-Validierung**
```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Am 2026-05-08 10:00 UTC gemäß Messprotokoll MP-001 wurden 
                  4.7 tCO₂ Wärmeverwertung mit ±8% Genauigkeit gemessen",
    "modes": ["mrv"]
  }'
```

**Response (MRV Validation)**
```json
{
  "results": {
    "mrv": {
      "expert": "MRV/Compliance",
      "approved": true,
      "confidence": 0.92,
      "feedback": "Aussage erfüllt MRV-Anforderungen. Ausreichend spezifisch für 
                   Audit-Trail und externe Verifikation.",
      "suggestions": [
        "Speichere die Messdaten in Audit-System für Langzeit-Tracking",
        "Quartalsweise externe Verifikation empfohlen"
      ],
      "conditions": [
        "Messprotokoll MP-001 muss beim Betreiber dokumentiert sein",
        "Kalibrierung der Messinstrumente muss ≤1 Jahr alt sein"
      ]
    }
  },
  "overall_approved": true,
  "approval_level": "approved"
}
```

---

## 3. BANK / Finanzierungsperspektive

### Beschreibung
Die Bank-Perspektive validiert **Bankfähigkeit und Finanzierbarkeit**. Sie bewertet Aussagen aus der Perspektive eines Kreditgebers (KfW, Geschäftsbank): "Ist das Projekt rentabel und rückzahlungsfähig?"

### Validierungskriterien
- ✅ Kalkulation realistisch (Annahmen überprüfbar)
- ✅ CAPEX, OPEX, Lebensdauer definiert
- ✅ ROI oder Payback Period aussagekräftig
- ✅ Risikominderung durch Sicherheiten/Versicherung
- ✅ Umsatzprognose konservativ
- ✅ Schuldendienst-Fähigkeit gegeben

### Red Flags für Banken
- ❌ Zu optimistische Annahmen (>20% über Markt)
- ❌ Keine klare Exit-Strategie
- ❌ Unerprobte Technologie
- ❌ Zu hohes Leverage (Schulden > 70% CAPEX)
- ❌ Lange Amortisationsdauer (>15 Jahre)

### Beispiele

**Query 1: Finanzierungsfähigkeit prüfen**
```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "CAPEX €2.5M, jährliche Einsparungen €250k, erwarteter ROI 10 Jahre, 
                  Finanzierung 60% Fremdkapital",
    "modes": ["bank"]
  }'
```

**Response (Bank Validation)**
```json
{
  "results": {
    "bank": {
      "expert": "Bank/Financing",
      "approved": true,
      "confidence": 0.88,
      "feedback": "Finanzierungsstruktur ist bankfähig. DSCR (Debt Service Coverage 
                   Ratio) liegt bei 1.2, was über Mindestschwelle von 1.0 liegt.",
      "suggestions": [
        "Erwägen Sie erhöhte Fremdfinanzierung (bis 70%) zur Verbesserung der ROE",
        "Vergleichen Sie mit vergleichbaren Projekten (Benchmark)",
        "Definieren Sie Covenant-Trigger (z.B. Sparbeschränkung wenn ROI <5%)"
      ],
      "conditions": [
        "Kreditgebühren (Zinsen ~4-5%) müssen in OPEX-Kalkulation enthalten sein",
        "Lebenszyklusanalyse muss mindestens 15 Jahre Horizont haben",
        "Sicherheiten müssen ≥100% des Darlehens sein (Maschine + Grundpfandrecht)"
      ]
    }
  },
  "overall_approved": true,
  "approval_level": "approved"
}
```

---

## 4. FUNDING / Fördermitteleignung

### Beschreibung
Diese Perspektive validiert Eignung für **deutsche und europäische Förderprogramme**: EXIST (Gründerförderung), WIPANO (Energieeffizienz), BayStartUP (Bayern), Horizon Europe, etc.

### Förderprogramm-Raster
- **EXIST-Gründerstipendium**: Early-stage, Hochschul-Ausgründung
- **WIPANO**: Energieeffizienz in KMU
- **KfW 261/262**: Erneuerbare Energien, Wärmepumpen
- **BayStartUP**: Bayern-spezifisch, Technologie-Fokus
- **Horizon Europe**: EU-weite Innovation

### Validierungskriterien (Beispiel EXIST)
- ✅ Team hat wirtschaftliche + technische Kompetenz
- ✅ Geschäftsidee ist innovativ
- ✅ Gründer ist Student/Absolvent der letzten 5 Jahre
- ✅ Geschäftsplan ist schlüssig
- ✅ Markt-Potenzial >€10M

### Beispiele

**Query 1: EXIST-Fähigkeit prüfen**
```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Unser Team: Dr.-Ing. (TUM, 2 Jahre Erfahrung), 
                  MBA (Harvard), beide Gründer. Kernidee: ORC-Retrofit 
                  für Stadtwerke. Zielmarkt: Deutschland + EU (20 Städte bis 2030)",
    "modes": ["funding"]
  }'
```

**Response (Funding Validation)**
```json
{
  "results": {
    "funding": {
      "expert": "Funding/Subsidies",
      "approved": true,
      "confidence": 0.80,
      "feedback": "Team-Komposition erfüllt EXIST-Kriterien. Technologie-Fokus 
                   und Marktgröße sprechen für Horizon Europe Zusatzfinanzierung.",
      "suggestions": [
        "Beantragen Sie EXIST-Gründerstipendium (bis €300k/12 Monate)",
        "Parallel KfW-261 Darlehen für CAPEX einplanen",
        "Horizon Europe Innovation Actions (€2-5M) für 3-Jahr-Projekt prüfen"
      ],
      "conditions": [
        "Mindestens ein Gründer muss noch als Student/Absolvent der letzten 5 Jahre zählen",
        "Detailliertes Businessplan-Dokument (>50 Seiten) erforderlich",
        "Impact-Metriken definieren (CO₂ Einsparung in tpa, Jobs)"
      ]
    }
  },
  "overall_approved": true
}
```

---

## 5. INDUSTRIAL / Kundenrelevanzperspektive

### Beschreibung
Diese Perspektive validiert Lösung aus Sicht von **Industriekunden**: Stadtwerke, MHKW, Papierindustrie, Lebensmittel-Verarbeitung. Frage: "Löst das ein echtes Problem für den Kunden?"

### Kundentypen
- 🏭 **Stadtwerke**: Wärmeverluste in Fernwärmenetzen (5-15% Verlust)
- 🔥 **MHKW** (Müllheizkraftwerke): Abgaswärme-Nutzung
- 📄 **Papierindustrie**: Prozesswärme-Recycling
- 🍖 **Lebensmittel**: Kühlwasser-Verwertung

### Validierungskriterien
- ✅ Problem ist für Kunden quantifiziert (€/Jahr)
- ✅ Kosten-Nutzen für Kunden positiv
- ✅ Montage/Integration ohne Betriebsunterbrechung
- ✅ Wartung in bestehenden Service-Prozessen
- ✅ Kundensupport verfügbar

### Beispiele

**Query 1: Stadtwerke-Validierung**
```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Unser ORC-System nutzt Fernwärme-Netzwärmeverluste 
                  (bisher ungenutzbar) und generiert 50 kW Strom. 
                  Stadt München: ~200k Haushalte mit 8% Wärmeverlusten = 
                  potenziell 1.5 MWh/Jahr zusätzliche Stromerzeugung.",
    "modes": ["industrial"]
  }'
```

**Response (Industrial Validation)**
```json
{
  "results": {
    "industrial": {
      "expert": "Industrial/Customers",
      "approved": true,
      "confidence": 0.82,
      "feedback": "Lösung adressiert reales und quantifiziertes Kundenproblem. 
                   Wärmeverluste in Fernwärmenetzen sind bekanntes Issue für 
                   größere Städte (aktuell meist unkompensiert).",
      "suggestions": [
        "Validieren Sie mit Stadtwerke München konkrete Integrationsmöglichkeit",
        "Erstellen Sie Wertproposition: €/kW ROI für Kundenrechnung",
        "Entwickeln Sie Standard-Schnittstellenprotokoll (Hardware + Software)"
      ],
      "conditions": [
        "Pilotanlage mit echtem Kunden erforderlich vor Skalierung",
        "24/7 Service-Support für Fernwärme-kritische Infrastruktur nötig",
        "Sicherheits-Zertifikation (ÖVE/ÖNORM für Österreich z.B.) erforderlich"
      ]
    }
  },
  "overall_approved": true
}
```

---

## 6. IP / Intellectual Property Perspektive

### Beschreibung
Die IP-Perspektive schützt **Schutzrechte, Geheimhaltung und Lizenz-Strategie**. Sie validiert, ob Innovationen patentiert/geschützt sind und ob Aussagen die IP-Strategie gefährden.

### IP-Kategorien
- 🔒 **Patent-Schutz**: Neuheit, Erfindungshöhe (Non-Obvious)
- 🤐 **Geschäftsgeheimnis**: Knowhow, Formulierungen, Prozesse
- 📚 **Markenrechte**: Terra-Nature Branding
- 📜 **Lizenz**: Fremdtechnologie-Integration

### Validierungskriterien
- ✅ Patent-Recherche abgeschlossen (kein Freiheitsverstoß)
- ✅ Geheime Informationen nicht öffentlich gemacht
- ✅ Drittanbieter-Code korrekt lizenziert (GPL, MIT, etc.)
- ✅ Partnerschafts-Geheimnisse respektiert

### Beispiele

**Query 1: Patent-Freiheit prüfen**
```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Unser ORC nutzt eine proprietäre Arbeitsflüssigkeit-Mischung 
                  aus 85% R245fa + 15% Additiv XYZ zur Viskositäts-Optimierung",
    "modes": ["ip"]
  }'
```

**Response (IP Validation)**
```json
{
  "results": {
    "ip": {
      "expert": "IP/Governance",
      "approved": false,
      "confidence": 0.90,
      "feedback": "Aussage ist kritisch für IP-Schutz. Die Formulierung 
                   offenbart Kerngeheimnis (Additiv-Zusammensetzung). 
                   Nicht öffentlich kommunizieren vor Patent-Anmeldung.",
      "suggestions": [
        "Formulierung nur intern oder unter NDA teilen",
        "Patent-Anmeldung prioritär (Nachteile wenn später offenbart)",
        "Ersetze in Public-Communications: '...proprietäre Optimierungsformulierung'"
      ],
      "conditions": [
        "Vor öffentlicher Diskussion muss Patent DE/EU angemeldet sein",
        "NDAs mit Partnern + Mitarbeitern müssen aktuell sein",
        "Lab-Reports mit Formulierung dürfen nicht in Public Repos gespeichert sein"
      ]
    }
  },
  "overall_approved": false
}
```

---

## 7. COMMUNICATION / Messaging-Perspektive

### Beschreibung
Diese Perspektive validiert **Verständlichkeit und Compliance von Kommunikation**. Sie stellt sicher, dass Messaging für verschiedene Zielgruppen (Gründer, Investoren, Regulierer) klipp und klar ist.

### Zielgruppen
- 👨‍💼 **Investoren**: Fokus auf ROI, Markt, Risiko
- 🧑‍🔬 **Techniker**: Fokus auf Spezifikationen, Komplexität
- 🏛️ **Regulierer**: Fokus auf Compliance, Standards
- 🗣️ **Öffentlichkeit**: Fokus auf Verständlichkeit, Impact

### Validierungskriterien
- ✅ Aussagen sind zielgruppen-gerecht
- ✅ Technische Komplexität ist vereinfacht (1-2 Sätze max.)
- ✅ Keine zu optimistischen Versprechungen
- ✅ Disclaimer vorhanden, wo erforderlich
- ✅ Konsistent über alle Kanäle

### Beispiele

**Query 1: Investor Pitch validieren**
```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Unser Organic Rankine Cycle nutzt Abwärme um Strom zu erzeugen. 
                  Wir adressieren einen €50B Markt in Europa.",
    "modes": ["communication"]
  }'
```

**Response (Communication Validation)**
```json
{
  "results": {
    "communication": {
      "expert": "Communication/Strategy",
      "approved": true,
      "confidence": 0.85,
      "feedback": "Aussage ist Investor-gerecht. Einfache Erklärung, 
                   klare Marktgröße. Aber: Marktgröße sollte adressierbar sein, 
                   nicht total available market.",
      "suggestions": [
        "Ersetze '€50B Markt' mit 'Adressierbare Marktsegmente: Stadtwerke (€2-3B SAM)'",
        "Füge hinzu: 'Wir zielen auf Top 50 deutsche Städte im 5-Jahres-Plan'",
        "Spezifiziere: 'ROI für Kunden: 8-10 Jahre Payback'"
      ],
      "conditions": [
        "Marktgröße-Claims müssen mit Third-Party-Reports (Frost & Sullivan, McKinsey) belegt sein"
      ]
    }
  },
  "overall_approved": true
}
```

---

## 8. PROFESSORALE / Wissenschaftliche Perspektive

### Beschreibung
Diese Perspektive validiert **wissenschaftliche Rigorosität und Peer-Review-Standard**. Sie wird von der Frage geleitet: "Würde das in einem Top-Journal akzeptiert?"

### Validierungskriterien
- ✅ Methodik ist klar und reproduzierbar
- ✅ Datenquellen sind verifizierbar
- ✅ Ergebnisse sind statistisch signifikant
- ✅ Limitationen werden ehrlich diskutiert
- ✅ Literatur-Review ist umfassend
- ✅ Konflikt-Interessen offengelegt

### Publikations-Standards
- 📊 **Nature Energy**: Impact ≥ 20% Effizienz-Verbesserung
- 📊 **Applied Energy**: Validierung mit realen Daten
- 📊 **Renewable Energy**: Novel Technology Demonstration

### Beispiele

**Query 1: Wissenschaftliche Aussage validieren**
```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "In unserem Test erreichte der ORC 22% isentropic efficiency 
                  bei 100°C Wärmeeintritt. n=5 Messungen, σ=±1.2%, 
                  mit Kalibrierung nach ISO 1271. Vergleich mit Literatur zeigt 
                  12% Verbesserung gegenüber vergleichbarer R245fa-Systeme.",
    "modes": ["professorale"]
  }'
```

**Response (Professorale Validation)**
```json
{
  "results": {
    "professorale": {
      "expert": "Professorale/Academic",
      "approved": true,
      "confidence": 0.88,
      "feedback": "Aussage ist wissenschaftlich rigoros. Spezifisch, quantifiziert, 
                   Unsicherheiten explizit. Publikation in fachlichem Journal 
                   (Applied Thermal Engineering) wäre möglich.",
      "suggestions": [
        "Ergänze: Welche r1/r2-Verhältnisse wurden getestet?",
        "Dokumentiere: Welche Literatur-Systeme als Benchmark?",
        "Spezifiziere: Wie wurde Kalibrierung durchgeführt (Kalibrierblock, Referenz-Flüssigkeit)?"
      ],
      "conditions": [
        "Vollständige experimentelle Dokumentation erforderlich",
        "Datenblatt mit allen Mess-Rohwerten (nicht nur Mittelwerte)",
        "Unsicherheitsbudget aller Messgrößen dokumentieren"
      ]
    }
  },
  "overall_approved": true
}
```

---

## 9. BUSINESS / Geschäftsentwicklungsperspektive

### Beschreibung
Diese Perspektive validiert **Geschäftsstrategie und Marktfähigkeit**. Sie bewertet: "Ist das ein skalierbares Geschäftsmodell?"

### Geschäftsmodell-Kategorien
- 💰 **Direct Sales**: Verkauf an Stadtwerke
- 🔧 **Service Model**: Betrieb + Wartung als Service (OPEX)
- 🤝 **Lizenz**: Technologie-Lizenz an OEM
- 📊 **Daten**: Energiedaten als Business (Sekundär)

### Validierungskriterien
- ✅ Skalierungspfad definiert (von 1 auf 100 Anlagen)
- ✅ Konkurrenzanalyse durchgeführt
- ✅ Distribution-Kanal klar
- ✅ Kundenakquisitions-Kosten < Lifetime Value
- ✅ Margin-Struktur nachhaltig (>30%)

### Beispiele

**Query 1: Geschäftsmodell-Validierung**
```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Unser Geschäftsmodell: 1) Direkt-Verkauf an Top-50 Stadtwerke 
                  (€500k/Anlage), 2) Service-Betrieb (10% jährlich der CAPEX), 
                  3) Performance-Garantie (85% verfügbar). 
                  Skalierung auf 100 Anlagen in 5 Jahren.",
    "modes": ["business"]
  }'
```

**Response (Business Validation)**
```json
{
  "results": {
    "business": {
      "expert": "Business/Development",
      "approved": true,
      "confidence": 0.79,
      "feedback": "Geschäftsmodell ist schlüssig und skalierbar. Mix aus 
                   CAPEX + OPEX Revenue ist gesund. Aber: 100 Anlagen in 
                   5 Jahren = aggressiv für B2B-Feldgeräte.",
      "suggestions": [
        "Validiere: Top-50 Stadtwerke haben tatsächlich 8%+ Wärmeverluste (Potenzial)",
        "Entwickle 2-3 Pilot-Projekte mit Lead-Customers als Referenzen",
        "Definiere Service-Netzwerk: Können Sie 100 Anlagen wartbar halten?",
        "Konkurrenz-Analyse: Welche anderen Efficiency-Technologien konkurrieren?"
      ],
      "conditions": [
        "Kundenakquisition: Max. €50k pro Anlage (sonst Break-Even unmöglich)",
        "Gewinn-Margin: Min. 30% (sonst nicht VC-finanzierbar)",
        "Market Share: Realistische 2-3% der Stadtwerke in 5 Jahren (20-25 Anlagen)"
      ]
    }
  },
  "overall_approved": true
}
```

---

## Anwendungsbeispiel: Multi-Expert Validation

**Szenario**: Gründer möchte folgende Aussage testen:
> "Unser ORC-System erzeugt 50 kW aus Industrieabwärme mit 20% Effizienz und kostet €400k. ROI ist 8 Jahre."

```bash
curl -X POST http://localhost:8000/api/kappa/validate \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Unser ORC-System erzeugt 50 kW aus Industrieabwärme mit 20% Effizienz und kostet €400k. ROI ist 8 Jahre.",
    "modes": ["cto", "bank", "professorale"]
  }'
```

**Response: Multi-Expert Validation**
```json
{
  "statement": "Unser ORC-System erzeugt 50 kW aus Industrieabwärme mit 20% Effizienz und kostet €400k. ROI ist 8 Jahre.",
  "timestamp": "2026-05-08T14:30:00.000Z",
  "results": {
    "cto": {
      "expert": "CTO/Engineering",
      "approved": true,
      "confidence": 0.90,
      "feedback": "20% Effizienz ist realistisch und konservativ für etablierte ORC-Technologie.",
      "conditions": []
    },
    "bank": {
      "expert": "Bank/Financing",
      "approved": true,
      "confidence": 0.85,
      "feedback": "8-Jahres-ROI ist bankfähig. Bei 50 kW Dauerleistung = ~€40k/Jahr Stromerzeugung.",
      "conditions": [
        "Wärmequelle muss stabil >3000 h/Jahr verfügbar sein"
      ]
    },
    "professorale": {
      "expert": "Professorale/Academic",
      "approved": true,
      "confidence": 0.88,
      "feedback": "Effizienz ist wissenschaftlich plausibel. Aber: Quellangabe für 20% erforderlich.",
      "suggestions": [
        "Vergleiche mit Literatur-Daten (z.B. Quoilin et al., Applied Energy)"
      ]
    }
  },
  "overall_approved": true,
  "approval_level": "approved"
}
```

---

## Häufige Kombinationen von Expert Modes

### Startup-Pitch (Investor Deck)
Empfohlen: **business + communication + bank**
- Business: Markt, Skalierung
- Communication: Verständlichkeit
- Bank: Finanzierbarkeit

### Zuschuss-Antrag (EXIST, WIPANO)
Empfohlen: **funding + cto + professorale**
- Funding: Programmfähigkeit
- CTO: Technische Realität
- Professorale: Wissenschaftlichkeit

### Regulatorischer Report (EnEfG, EU-ETS)
Empfohlen: **mrv + bank + professorale**
- MRV: Compliance
- Bank: Wirtschaftlichkeit
- Professorale: Methodologie

### Industriepartner-Gespräch
Empfohlen: **industrial + cto + business**
- Industrial: Kundennutzen
- CTO: Technische Integration
- Business: Geschäftsmodell

---

## Fehlerbehandlung

### "Mode nicht erkannt"
```
curl -X POST http://localhost:8000/api/kappa/validate \
  -d '{"text": "...", "mode": "unknown"}'
→ 400 Bad Request: "Invalid mode 'unknown'. Allowed: cto, mrv, bank, funding, industrial, ip, communication, professorale, business"
```

### "Mode nicht verfügbar" (API Key fehlt)
```
→ 503 Service Unavailable: "Mode 'professorale' requires KAPPA_ANTHROPIC_API_KEY in mock=false"
```

---

## Status

✅ Alle 9 Expert Modes implementiert  
✅ Mock-Mode für Entwicklung ohne API-Keys  
✅ Multi-Mode Validation möglich  
✅ Audit-Trail für alle Validierungen  

**MVP Release Candidate bereit für Demo**

