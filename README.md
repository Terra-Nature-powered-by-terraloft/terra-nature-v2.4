# terra-nature-v2.4

Dashboards zur CO₂-Tracking, Terra Nature selbst ist ein Konzept zur CO₂-Kompensation mit technischen und ökonomischen Modellen.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- Python 3.8+
- Git

### Development Setup

```bash
# Repository klonen
git clone https://github.com/Terra-Nature-powered-by-terraloft/terra-nature-v2.4.git
cd terra-nature-v2.4

# Dependencies installieren
npm install
pip install -r requirements.txt

# Development Server starten
npm run storybook          # Storybook auf http://localhost:6006
npm run dev               # Vite Dev Server auf http://localhost:5173

# Tests ausführen
npm test                  # Vollständige Test-Suite (TypeScript + Python)
npm run test:watch        # Watch-Modus für Entwicklung
```

## 📚 Entwickler-Dokumentation

### Richtlinien & Standards

- **[Guidelines.de.md](./Guidelines.de.md)** - Umfassende Richtlinien für Code, Git, A11y, Performance, Branching und Commits
- **[Git-Workflow.de.md](./docs/git-workflow.de.md)** - Erweiterte Git-Befehle, Szenarien und Best Practices  
- **[Component Migration Checklist](./COMPONENT_MIGRATION_CHECKLIST.md)** - Qualitätssicherung für neue/überarbeitete Komponenten

### Tool-Setup & Konfiguration

- **[Storybook Setup](./STORYBOOK_SETUP.de.md)** - Komplette Anleitung für Storybook-Entwicklung und -Deployment
- **[Testing Setup](./TESTING_SETUP.de.md)** - Vitest, React Testing Library, Accessibility Testing
- **[Husky Hooks Setup](./HUSKY_HOOKS_SETUP.de.md)** - Git-Hooks für automatische Code-Qualität

### Architektur & Roadmap

- **[Architecture Roadmap](./docs/architecture-roadmap.de.md)** - Strategische Roadmap mit Epics, Meilensteinen und Sprint-Backlog für Modularisierung, Performance, Security, APIs, Automatisierung und Blockchain-Integration

## 🛠️ Demo WebSocket Servers

Zwei einfache Demo-Server erzeugen zufällige NRG-Event-Payloads für Entwicklung und Testing.

### Node.js Server

```bash
npm install
node tools/ws_demo_server.js
```

Server läuft auf `ws://localhost:8765`

### Python Server

```bash
pip install -r requirements.txt
python tools/ws_demo_server.py
```

Server läuft auf `ws://localhost:8765`

Jede Verbindung erhält Nachrichten wie:
```json
{
  "type": "NRG",
  "value": 0.42,
  "id": "uuid-here",
  "timestamp": "2024-12-10T10:30:00Z"
}
```

## 🧪 Testing

### Verfügbare Test-Suites

```bash
# Alle Tests
npm test                    # Node.js + Python Tests

# Spezifische Test-Typen  
npm run test:js            # TypeScript/React Tests (Vitest)
npm run test:py            # Python Tests (pytest)
npm run test:coverage      # Coverage Report
npm run test:a11y          # Accessibility Tests

# Development
npm run test:watch         # Watch-Modus
npm run test-storybook     # Storybook Interaction Tests
```

### Test-Struktur

```
tests/
├── setup.ts              # Test-Konfiguration
├── Button.test.tsx       # Component Unit Tests  
├── Dialog.a11y.test.tsx  # Accessibility Tests
├── test_ws_demo_server_py.py         # Python WebSocket Tests
└── test_nrg_nft_events_template.py   # Python Data Tests
```

## 📖 Storybook

Interaktive Komponenten-Dokumentation und -Entwicklung:

```bash
npm run storybook          # Development Server
npm run build-storybook    # Production Build
```

**Features:**
- 🎨 Component Library mit Design System
- ♿ Accessibility Testing mit A11y Addon
- 📱 Responsive Testing mit Viewport Addon
- 🎭 Interaction Testing mit Play Functions
- 📚 Automatische Dokumentation

## 🎯 Projekt-Features

### Aktuelle Features

- ✅ **Real-time Energy Monitoring** - WebSocket-basierte Energiedatenerfassung
- ✅ **CO₂-Berechnungen** - Automatische Umrechnung von Energieverbrauch zu CO₂-Äquivalenten
- ✅ **Component Library** - React-Komponenten mit TypeScript und Storybook
- ✅ **Testing Infrastructure** - Umfassende Tests mit Vitest, pytest und A11y-Validierung
- ✅ **Code Quality** - ESLint, Prettier, Husky Git-Hooks, Conventional Commits

### Roadmap Features (Siehe [Architecture Roadmap](./docs/architecture-roadmap.de.md))

- 🔄 **REST API Layer** - RESTful API mit OpenAPI 3.0 Spezifikation
- 📅 **IoT Integration** - Sensor-Datenerfassung und Edge Computing
- 📅 **Blockchain Integration** - NFT-basierte Energie-Zertifikate auf Ethereum
- 📅 **Audit Trail System** - Unveränderliche Logs für Compliance
- 📅 **Performance Monitoring** - Core Web Vitals und automatische Optimierung

## 🔧 Verfügbare Scripts

```bash
# Development
npm run dev                # Vite Development Server
npm run storybook          # Storybook Development
npm run test:watch         # Tests im Watch-Modus

# Building  
npm run build              # Production Build
npm run build-storybook    # Storybook Build
npm run preview            # Preview Production Build

# Code Quality
npm run lint               # ESLint Check
npm run lint:fix           # ESLint Auto-Fix
npm run format             # Prettier Format
npm run type-check         # TypeScript Check

# Testing
npm test                   # Alle Tests
npm run test:coverage      # Test Coverage
npm run test-storybook     # Storybook Tests
```

## 🏗️ Technologie-Stack

### Frontend
- **React 18** - UI Framework mit TypeScript
- **Vite** - Build Tool und Development Server
- **Vitest** - Test Framework
- **Storybook** - Component Development
- **ESLint + Prettier** - Code Quality

### Backend (Roadmap)
- **Node.js + Express** - REST API Server
- **GraphQL** - Flexible Query Layer
- **WebSocket** - Real-time Communication
- **PostgreSQL** - Hauptdatenbank

### Blockchain (Roadmap)
- **Ethereum** - Smart Contracts für NFTs
- **Solidity** - Contract Development
- **IPFS** - Dezentrale Datenspeicherung
- **MetaMask** - Wallet Integration

## 🤝 Contributing

1. Repository forken
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen committen (`git commit -m 'feat: add amazing feature'`)
4. Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request erstellen

Siehe [Guidelines.de.md](./Guidelines.de.md) für detaillierte Coding-Standards und [Git-Workflow.de.md](./docs/git-workflow.de.md) für Git-Best-Practices.

## 📄 Lizenz

Dieses Projekt steht unter der [MIT Lizenz](./LICENSE).

## 🆘 Support

- 📖 **Dokumentation**: Siehe [Entwickler-Dokumentation](#-entwickler-dokumentation)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Terra-Nature-powered-by-terraloft/terra-nature-v2.4/issues)
- 💬 **Diskussionen**: [GitHub Discussions](https://github.com/Terra-Nature-powered-by-terraloft/terra-nature-v2.4/discussions)

---

**Terra Nature v2.4** - Nachhaltige Technologie für eine bessere Zukunft 🌱
