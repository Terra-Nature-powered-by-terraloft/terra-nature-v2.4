# Guidelines.de.md - Richtlinien für Entwicklung in Terra Nature v2.4

## Übersicht

Dieses Dokument beschreibt die Entwicklungsrichtlinien für das Terra Nature v2.4 Projekt - ein CO₂-Tracking Dashboard mit technischen und ökonomischen Modellen zur CO₂-Kompensation.

## Inhaltsverzeichnis

1. [Code-Richtlinien](#code-richtlinien)
2. [Git-Workflow](#git-workflow)
3. [Accessibility (A11y)](#accessibility-a11y)
4. [Performance-Richtlinien](#performance-richtlinien)
5. [Branching-Strategie](#branching-strategie)
6. [Commit-Konventionen](#commit-konventionen)
7. [Testing-Standards](#testing-standards)
8. [Storybook-Integration](#storybook-integration)

## Code-Richtlinien

### TypeScript Standards

```typescript
// ✅ Gut: Explizite Typen für öffentliche APIs
export interface NRGEvent {
  type: 'NRG'
  value: number
  id: string
  timestamp?: Date
}

// ✅ Gut: Funktionale Komponenten mit TypeScript
export const EnergyDisplay: React.FC<NRGEvent> = ({ value, id }) => {
  return <div data-testid={`energy-${id}`}>Energie: {value} kWh</div>
}

// ❌ Schlecht: Jeder any-Type vermeiden
const data: any = fetchData() // Verwende stattdessen spezifische Typen
```

### React-Komponenten Patterns

```typescript
// ✅ Gut: Props-Interface mit Dokumentation
interface ButtonProps {
  /**
   * Ist das der Haupt-Call-to-Action auf der Seite?
   */
  primary?: boolean
  /**
   * Button-Inhalt
   */
  children: React.ReactNode
  /**
   * Klick-Handler
   */
  onClick?: () => void
}

// ✅ Gut: Standardwerte verwenden
export const Button: React.FC<ButtonProps> = ({
  primary = false,
  children,
  onClick,
}) => {
  const className = `btn ${primary ? 'btn-primary' : 'btn-secondary'}`
  
  return (
    <button className={className} onClick={onClick}>
      {children}
    </button>
  )
}
```

### Styling-Konventionen

```css
/* ✅ Gut: BEM-ähnliche Klassennames für Komponenten */
.energy-dashboard {}
.energy-dashboard__header {}
.energy-dashboard__chart {}
.energy-dashboard__chart--loading {}

/* ✅ Gut: CSS Custom Properties für Themes */
:root {
  --color-primary: #0d6efd;
  --color-success: #198754;
  --color-warning: #ffc107;
  --color-danger: #dc3545;
  --spacing-unit: 0.25rem;
}

/* ✅ Gut: Responsive Design Mobile-First */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: calc(var(--spacing-unit) * 4);
}

@media (min-width: 768px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Git-Workflow

### Branch-Namen Konventionen

```bash
# Feature-Entwicklung
feature/energy-nft-integration
feature/co2-tracking-dashboard

# Bugfixes
fix/websocket-connection-timeout
fix/energy-calculation-precision

# Dokumentation
docs/setup-guide-de
docs/architecture-roadmap

# Chores/Tooling
chore/update-dependencies
chore/add-eslint-rules
```

### Pre-Commit Checks

```bash
# Automatisch ausgeführt durch Husky
npm run lint:fix    # ESLint mit Auto-Fix
npm run format      # Prettier Formatierung
npm run test:js     # TypeScript/React Tests
npm run test:py     # Python Tests
```

## Accessibility (A11y)

### Barrierefreiheits-Standards

```typescript
// ✅ Gut: Semantische HTML-Struktur
export const EnergyDialog: React.FC<DialogProps> = ({ isOpen, title, onClose }) => {
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="dialog-title"
      className="dialog-backdrop"
    >
      <div role="document" className="dialog-content">
        <h2 id="dialog-title">{title}</h2>
        <button 
          onClick={onClose}
          aria-label="Dialog schließen"
        >
          ×
        </button>
      </div>
    </div>
  )
}

// ✅ Gut: Keyboard-Navigation Support
const handleKeyDown = (e: React.KeyboardEvent) => {
  if (e.key === 'Escape') {
    onClose()
  }
}
```

### A11y Testing

```typescript
// ✅ Gut: Automatisierte A11y-Tests mit jest-axe
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

it('sollte keine Accessibility-Verletzungen haben', async () => {
  const { container } = render(<EnergyDashboard />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

## Performance-Richtlinien

### React Performance

```typescript
// ✅ Gut: React.memo für Pure Components
export const EnergyChart = React.memo<EnergyChartProps>(({ data }) => {
  return <Chart data={data} />
})

// ✅ Gut: useCallback für Event-Handler
const EnergyMonitor: React.FC = () => {
  const [readings, setReadings] = useState<NRGEvent[]>([])
  
  const handleNewReading = useCallback((reading: NRGEvent) => {
    setReadings(prev => [...prev.slice(-99), reading]) // Nur letzte 100 behalten
  }, [])
  
  return <WebSocketManager onReading={handleNewReading} />
}

// ✅ Gut: useMemo für aufwändige Berechnungen
const processedData = useMemo(() => {
  return readings.map(reading => ({
    ...reading,
    co2Equivalent: reading.value * CO2_CONVERSION_FACTOR
  }))
}, [readings])
```

### Bundle-Optimierung

```typescript
// ✅ Gut: Lazy Loading für Route-Komponenten
const EnergyDashboard = lazy(() => import('./components/EnergyDashboard'))
const NFTMarketplace = lazy(() => import('./components/NFTMarketplace'))

// ✅ Gut: Tree-Shaking durch Named Imports
import { formatEnergy, calculateCO2 } from '../utils/energy'
// ❌ Schlecht: import * as energyUtils from '../utils/energy'
```

## Branching-Strategie

### Git Flow Adaption

```bash
# Hauptbranches
main          # Produktionsreifer Code
develop       # Integration Branch für Features

# Feature Branches
feature/*     # Neue Features (von develop abzweigen)
fix/*         # Bugfixes (von develop oder main)
hotfix/*      # Kritische Fixes (von main)
release/*     # Release-Vorbereitung

# Beispiel Workflow
git checkout develop
git pull origin develop
git checkout -b feature/blockchain-nft-integration
# ... Entwicklung ...
git commit -m "feat: add NFT minting functionality"
git push origin feature/blockchain-nft-integration
# ... Pull Request erstellen ...
```

## Commit-Konventionen

### Conventional Commits (Deutsch)

```bash
# Format: <typ>[(bereich)]: <beschreibung>
# 
# Typen:
feat:     # Neue Funktionalität
fix:      # Bugfix
docs:     # Dokumentation
style:    # Code-Formatierung (keine Logik-Änderung)
refactor: # Code-Umstrukturierung
perf:     # Performance-Verbesserung
test:     # Tests hinzufügen/ändern
build:    # Build-System Änderungen
ci:       # CI/CD Konfiguration
chore:    # Maintenance/Tools

# Beispiele:
feat(energy): add real-time CO2 calculation
fix(websocket): resolve connection timeout in energy monitoring
docs(readme): update setup instructions for German developers
test(components): add accessibility tests for EnergyDialog
perf(dashboard): optimize chart rendering with virtualization
```

### Commit-Message Richtlinien

```bash
# ✅ Gut: Klare, aussagekräftige Messages
feat(nft): implement energy-backed NFT minting process

# Commit-Body (optional) für komplexe Änderungen:
feat(blockchain): integrate Ethereum NFT contract for energy certificates

- Add smart contract interface for NFT minting
- Implement energy-to-NFT conversion logic  
- Add transaction validation and error handling
- Include CO2 certificate metadata in NFT

Closes #123
```

## Testing-Standards

### Test-Struktur

```typescript
// ✅ Gut: Beschreibende Test-Namen
describe('EnergyCalculator', () => {
  describe('calculateCO2Equivalent', () => {
    it('sollte korrekte CO2-Äquivalente für Standardwerte berechnen', () => {
      const result = calculateCO2Equivalent(100) // 100 kWh
      expect(result).toBe(42) // 42 kg CO2
    })
    
    it('sollte Fehler bei negativen Werten werfen', () => {
      expect(() => calculateCO2Equivalent(-10)).toThrow('Energiewerte müssen positiv sein')
    })
  })
})

// ✅ Gut: Component Testing mit User Interactions
describe('EnergyDashboard', () => {
  it('sollte neue Energie-Readings anzeigen', async () => {
    const user = userEvent.setup()
    render(<EnergyDashboard />)
    
    const input = screen.getByLabelText(/energie eingeben/i)
    await user.type(input, '150')
    await user.click(screen.getByRole('button', { name: /hinzufügen/i }))
    
    expect(screen.getByText('150 kWh')).toBeInTheDocument()
  })
})
```

### Test Coverage Ziele

```bash
# Minimum Coverage Ziele:
# - Statements: 80%
# - Branches: 75%  
# - Functions: 80%
# - Lines: 80%

# Vitest Coverage Commands:
npm run test:coverage     # Coverage Report generieren
npm run test:watch        # Watch Mode für Entwicklung
```

## Storybook-Integration

### Story-Struktur

```typescript
// ✅ Gut: Comprehensive Stories mit Controls
import type { Meta, StoryObj } from '@storybook/react'
import { EnergyMeter } from './EnergyMeter'

const meta: Meta<typeof EnergyMeter> = {
  title: 'Dashboard/EnergyMeter',
  component: EnergyMeter,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Zeigt aktuelle Energiemessungen mit CO2-Berechnungen an.'
      }
    }
  },
  argTypes: {
    value: { control: { type: 'number', min: 0, max: 1000 } },
    unit: { control: { type: 'select', options: ['kWh', 'MWh', 'GWh'] } },
  },
}

export default meta
type Story = StoryObj<typeof meta>

export const Standard: Story = {
  args: {
    value: 150,
    unit: 'kWh',
    showCO2: true,
  },
}

export const HighConsumption: Story = {
  args: {
    value: 500,
    unit: 'kWh',
    showCO2: true,
    variant: 'warning'
  },
}

export const CriticalLevel: Story = {
  args: {
    value: 900,
    unit: 'kWh', 
    showCO2: true,
    variant: 'danger'
  },
}
```

## Code Review Richtlinien

### Reviewer Checklist

- [ ] **Funktionalität**: Code erfüllt Anforderungen korrekt
- [ ] **Accessibility**: ARIA-Labels, Keyboard-Navigation, Farbkontrast
- [ ] **Performance**: Keine unnötigen Re-Renders, effiziente Algorithmen
- [ ] **Testing**: Ausreichende Test-Coverage, Edge Cases abgedeckt
- [ ] **Types**: TypeScript-Typen sind korrekt und hilfreich
- [ ] **Documentation**: Komplexe Logik ist dokumentiert
- [ ] **Sicherheit**: Keine sensiblen Daten exponiert, Input-Validierung

### Pull Request Template

```markdown
## Beschreibung
Kurze Beschreibung der Änderungen und warum sie notwendig sind.

## Art der Änderung
- [ ] Bugfix (nicht-breaking Änderung, die ein Problem behebt)
- [ ] Neue Funktion (nicht-breaking Änderung, die Funktionalität hinzufügt)
- [ ] Breaking Change (Fix oder Feature, das bestehende Funktionalität bricht)
- [ ] Dokumentation Update

## Tests
- [ ] Unit Tests hinzugefügt/aktualisiert
- [ ] Integration Tests hinzugefügt/aktualisiert
- [ ] A11y Tests durchgeführt
- [ ] Manuelle Tests in verschiedenen Browsern

## Screenshots (falls UI-Änderungen)
[Screenshots oder GIFs der Änderungen]

## Checklist
- [ ] Code folgt den Projekt-Richtlinien
- [ ] Self-Review durchgeführt
- [ ] Code ist kommentiert, besonders in schwer verständlichen Bereichen
- [ ] Entsprechende Dokumentation aktualisiert
- [ ] Keine neuen Warnungen in der Konsole
```

## Troubleshooting & Häufige Probleme

### WebSocket Verbindungsprobleme

```typescript
// ✅ Gut: Robust WebSocket Implementation
useEffect(() => {
  const ws = new WebSocket('ws://localhost:8765')
  let reconnectTimer: NodeJS.Timeout
  
  ws.onopen = () => {
    console.log('WebSocket Verbindung hergestellt')
    clearTimeout(reconnectTimer)
  }
  
  ws.onclose = () => {
    console.log('WebSocket Verbindung getrennt, versuche Reconnect...')
    reconnectTimer = setTimeout(() => {
      // Reconnect logic
    }, 3000)
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket Fehler:', error)
  }
  
  return () => {
    clearTimeout(reconnectTimer)
    ws.close()
  }
}, [])
```

### TypeScript Compilation Errors

```bash
# Häufige Lösungen:
npm run type-check           # TypeScript Prüfung ohne Build
rm -rf node_modules && npm install  # Dependencies neu installieren
npx tsc --noEmit            # Type-Only Check
```

## Ressourcen & Links

- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Accessibility Guidelines WCAG](https://www.w3.org/WAI/WCAG21/quickref/)
- [Conventional Commits Spezifikation](https://www.conventionalcommits.org/)
- [Storybook Best Practices](https://storybook.js.org/docs/react/writing-stories/introduction)

---

**Letzte Aktualisierung**: 2024-12-10  
**Version**: 1.0.0  
**Maintainer**: Terra Nature Development Team