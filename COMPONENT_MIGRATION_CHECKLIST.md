# Component Migration Checklist - Qualitätssicherung für Terra Nature v2.4

## Übersicht

Diese Checkliste dient der Qualitätssicherung beim Hinzufügen neuer oder Überarbeiten bestehender Komponenten im Terra Nature v2.4 Projekt. Sie gewährleistet Konsistenz, Barrierefreiheit und Wartbarkeit.

## Allgemeine Komponent-Anforderungen

### ✅ Code-Qualität

#### TypeScript-Integration
- [ ] **TypeScript-Typen**: Alle Props sind vollständig typisiert
- [ ] **Interface-Dokumentation**: JSDoc-Kommentare für alle öffentlichen Props
- [ ] **Export-Konsistenz**: Named Export + Default Export verfügbar
- [ ] **Generic-Support**: Wo sinnvoll, Generic-Types verwenden

```typescript
// ✅ Beispiel: Vollständig typisierte Component
interface EnergyMeterProps {
  /**
   * Aktueller Energiewert in kWh
   */
  value: number
  /**
   * Anzeigeformat für den Wert
   * @default 'standard'
   */
  format?: 'standard' | 'compact' | 'detailed'
  /**
   * Callback beim Erreichen eines Schwellenwerts
   */
  onThresholdReached?: (threshold: number) => void
  /**
   * Zusätzliche CSS-Klassen
   */
  className?: string
}

export const EnergyMeter: React.FC<EnergyMeterProps> = ({ ... }) => { ... }
export default EnergyMeter
```

#### Code-Standards
- [ ] **ESLint-Clean**: Keine ESLint-Warnungen oder -Fehler
- [ ] **Prettier-Formatiert**: Code ist konsistent formatiert
- [ ] **Naming-Konventionen**: PascalCase für Komponenten, camelCase für Props
- [ ] **File-Struktur**: Komponent + Stories + Tests in logischer Struktur

### ✅ Functionality & Performance

#### React-Best Practices
- [ ] **Funktionale Komponente**: Verwende React.FC oder Function Declaration
- [ ] **Hook-Regeln**: Hooks korrekt und in richtiger Reihenfolge verwendet
- [ ] **Memoization**: React.memo bei Pure Components, useMemo/useCallback wo angebracht
- [ ] **Key-Props**: Eindeutige Keys bei Listen und dynamischen Elementen

```typescript
// ✅ Beispiel: Performance-optimierte Component
export const EnergyChart = React.memo<EnergyChartProps>(({ data, onDataPointClick }) => {
  const processedData = useMemo(() => 
    data.map(point => ({
      ...point,
      co2Equivalent: point.value * CO2_CONVERSION_FACTOR
    }))
  , [data])
  
  const handleDataPointClick = useCallback((point: DataPoint) => {
    onDataPointClick?.(point)
  }, [onDataPointClick])
  
  return (
    <div className="energy-chart">
      {processedData.map(point => (
        <ChartPoint 
          key={`${point.id}-${point.timestamp}`}
          data={point}
          onClick={handleDataPointClick}
        />
      ))}
    </div>
  )
})
```

#### Error Handling
- [ ] **Error Boundaries**: Kritische Komponenten mit Error Boundary geschützt
- [ ] **PropTypes-Validation**: Runtime-Validierung für kritische Props
- [ ] **Graceful Degradation**: Komponente funktioniert auch bei fehlenden optionalen Props
- [ ] **Loading States**: Entsprechende Zustände für asynchrone Operationen

### ✅ Accessibility (A11y)

#### Semantic HTML
- [ ] **Korrekte HTML-Semantik**: Verwendung semantischer HTML-Elemente
- [ ] **ARIA-Labels**: Beschreibende Labels für Screen Reader
- [ ] **ARIA-Roles**: Korrekte Rollen für interaktive Elemente
- [ ] **Landmark-Regions**: Navigation und Content-Bereiche klar abgegrenzt

```typescript
// ✅ Beispiel: Accessibility-konforme Component
export const EnergyDialog: React.FC<EnergyDialogProps> = ({ 
  isOpen, 
  title, 
  children, 
  onClose 
}) => {
  const titleId = useId()
  
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
      // Focus-Trap Implementation
    }
    return () => {
      document.body.style.overflow = ''
    }
  }, [isOpen])
  
  if (!isOpen) return null
  
  return (
    <div 
      className="dialog-backdrop"
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      onKeyDown={(e) => e.key === 'Escape' && onClose()}
    >
      <div role="document" className="dialog-content">
        <header className="dialog-header">
          <h2 id={titleId}>{title}</h2>
          <button 
            onClick={onClose}
            aria-label="Dialog schließen"
            className="dialog-close"
          >
            <CloseIcon />
          </button>
        </header>
        <main className="dialog-body">
          {children}
        </main>
      </div>
    </div>
  )
}
```

#### Keyboard Navigation
- [ ] **Tab-Order**: Logische Tab-Reihenfolge durch interaktive Elemente
- [ ] **Focus-Management**: Sichtbare Focus-Indikatoren
- [ ] **Keyboard-Shortcuts**: Standard-Shortcuts (Escape, Enter, Arrow Keys)
- [ ] **Focus-Trap**: In Modals und Dialogen Focus gefangen

#### Color & Contrast
- [ ] **Farbkontrast**: Mindestens WCAG AA (4.5:1 für Normal-Text)
- [ ] **Color-Independence**: Information nicht nur über Farbe vermittelt
- [ ] **High-Contrast Mode**: Komponente funktioniert im High-Contrast Modus
- [ ] **Dark-Mode Support**: Angepasste Farben für Dark Theme

### ✅ Testing

#### Unit Tests
- [ ] **Component-Rendering**: Grundlegendes Rendering ohne Fehler
- [ ] **Props-Handling**: Alle Props werden korrekt verarbeitet
- [ ] **User-Interactions**: Klicks, Eingaben, Hover-States getestet
- [ ] **Edge-Cases**: Grenzwerte und Fehlerzustände abgedeckt

```typescript
// ✅ Beispiel: Comprehensive Component Tests
describe('EnergyMeter', () => {
  it('should render with basic props', () => {
    render(<EnergyMeter value={100} />)
    expect(screen.getByText('100 kWh')).toBeInTheDocument()
  })
  
  it('should handle different formats', () => {
    const { rerender } = render(<EnergyMeter value={1500} format="compact" />)
    expect(screen.getByText('1.5k kWh')).toBeInTheDocument()
    
    rerender(<EnergyMeter value={1500} format="detailed" />)
    expect(screen.getByText('1,500.00 kWh')).toBeInTheDocument()
  })
  
  it('should call onThresholdReached when threshold is exceeded', () => {
    const mockCallback = vi.fn()
    render(<EnergyMeter value={1000} onThresholdReached={mockCallback} />)
    
    // Simulate threshold condition
    fireEvent.click(screen.getByRole('button', { name: /check threshold/i }))
    expect(mockCallback).toHaveBeenCalledWith(1000)
  })
  
  it('should handle invalid values gracefully', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    
    render(<EnergyMeter value={-100} />)
    expect(screen.getByText('Ungültiger Wert')).toBeInTheDocument()
    
    consoleSpy.mockRestore()
  })
})
```

#### Accessibility Tests
- [ ] **jest-axe Tests**: Automatisierte A11y-Validierung
- [ ] **Keyboard-Tests**: Tastaturnavigation funktional getestet
- [ ] **Screen-Reader Tests**: ARIA-Labels und -Descriptions validiert
- [ ] **Focus-Management**: Focus-States getestet

```typescript
// ✅ Beispiel: A11y Tests
describe('EnergyMeter Accessibility', () => {
  it('should not have accessibility violations', async () => {
    const { container } = render(<EnergyMeter value={100} />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
  
  it('should support keyboard navigation', async () => {
    const user = userEvent.setup()
    render(<EnergyMeter value={100} />)
    
    const meter = screen.getByRole('meter')
    await user.tab()
    expect(meter).toHaveFocus()
    
    await user.keyboard('{Enter}')
    // Test interaction via keyboard
  })
})
```

### ✅ Storybook Integration

#### Story Coverage
- [ ] **Default Story**: Grundkonfiguration mit typischen Props
- [ ] **Variant Stories**: Alle wichtigen Varianten und Zustände
- [ ] **Interactive Stories**: Demos für User-Interaktionen
- [ ] **Documentation**: Beschreibende Texte und Verwendungshinweise

```typescript
// ✅ Beispiel: Comprehensive Storybook Stories
const meta: Meta<typeof EnergyMeter> = {
  title: 'Components/EnergyMeter',
  component: EnergyMeter,
  parameters: {
    docs: {
      description: {
        component: 'Zeigt Energieverbrauch mit CO2-Berechnungen an. Unterstützt verschiedene Anzeigeformate und Schwellenwert-Benachrichtigungen.'
      }
    }
  },
  argTypes: {
    value: { control: { type: 'number', min: 0, max: 10000, step: 10 } },
    format: { control: { type: 'select', options: ['standard', 'compact', 'detailed'] } },
    onThresholdReached: { action: 'threshold-reached' }
  }
}

export const Default: Story = {
  args: {
    value: 150,
    format: 'standard'
  }
}

export const HighConsumption: Story = {
  args: {
    value: 850,
    format: 'detailed'
  },
  parameters: {
    docs: {
      description: {
        story: 'Zeigt das Verhalten bei hohem Energieverbrauch mit Warnstufen.'
      }
    }
  }
}

export const CompactFormat: Story = {
  args: {
    value: 1200,
    format: 'compact'
  }
}

export const Interactive: Story = {
  args: {
    value: 500
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const incrementBtn = canvas.getByRole('button', { name: /erhöhen/i })
    
    await userEvent.click(incrementBtn)
    await expect(canvas.getByText('510 kWh')).toBeInTheDocument()
  }
}
```

#### Controls & Documentation
- [ ] **ArgTypes**: Sinnvolle Controls für alle Props
- [ ] **Actions**: Event-Handler als Actions konfiguriert
- [ ] **Docs-Page**: Automatische Dokumentation aktiviert
- [ ] **Examples**: Praktische Verwendungsbeispiele

### ✅ CSS & Styling

#### Styling-Architektur
- [ ] **CSS-Modules oder Styled-Components**: Isolierte Styles
- [ ] **Responsive Design**: Mobile-First Ansatz
- [ ] **CSS Custom Properties**: Für Themes und Varianten
- [ ] **BEM-Methodology**: Klare CSS-Klassennamen

```css
/* ✅ Beispiel: Strukturierte Component Styles */
.energy-meter {
  --meter-primary-color: var(--color-primary, #0d6efd);
  --meter-warning-color: var(--color-warning, #ffc107);
  --meter-danger-color: var(--color-danger, #dc3545);
  
  display: flex;
  flex-direction: column;
  gap: var(--spacing-unit);
  padding: calc(var(--spacing-unit) * 3);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--background-color);
  transition: all 0.2s ease-in-out;
}

.energy-meter__value {
  font-size: 2rem;
  font-weight: 600;
  color: var(--meter-primary-color);
}

.energy-meter__unit {
  font-size: 0.875rem;
  color: var(--text-muted);
  text-transform: uppercase;
}

.energy-meter--warning .energy-meter__value {
  color: var(--meter-warning-color);
}

.energy-meter--danger .energy-meter__value {
  color: var(--meter-danger-color);
}

/* Responsive Design */
@media (max-width: 768px) {
  .energy-meter {
    padding: calc(var(--spacing-unit) * 2);
  }
  
  .energy-meter__value {
    font-size: 1.5rem;
  }
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  .energy-meter {
    --background-color: var(--dark-background);
    --border-color: var(--dark-border);
    --text-muted: var(--dark-text-muted);
  }
}
```

#### Theme-Integration
- [ ] **Design-Tokens**: Verwendung von Design-System Variablen
- [ ] **Dark-Mode**: Explizite Dark-Mode Styles
- [ ] **High-Contrast**: Anpassung für High-Contrast Modus
- [ ] **Print-Styles**: Optimierung für Druckausgabe

### ✅ Documentation

#### Code-Dokumentation
- [ ] **JSDoc-Comments**: Alle öffentlichen APIs dokumentiert
- [ ] **README-Updates**: Komponent in Hauptdokumentation erwähnt
- [ ] **Verwendungsbeispiele**: Praktische Code-Beispiele
- [ ] **Migration-Guide**: Bei Breaking Changes

```typescript
/**
 * EnergyMeter Component
 * 
 * Zeigt Energieverbrauchsdaten mit konfigurierbaren Anzeigeoptionen.
 * Unterstützt Schwellenwert-Benachrichtigungen und verschiedene Formate.
 * 
 * @example
 * ```tsx
 * <EnergyMeter 
 *   value={150} 
 *   format="detailed"
 *   onThresholdReached={(threshold) => console.log(`Schwellenwert erreicht: ${threshold}`)}
 * />
 * ```
 * 
 * @see {@link https://storybook.terra-nature.com/energy-meter} Storybook
 */
export const EnergyMeter: React.FC<EnergyMeterProps> = ({ ... }) => { ... }
```

## Spezielle Checklisten

### ✅ Form-Komponenten

#### Input-Handling
- [ ] **Controlled Components**: State wird von Parent verwaltet
- [ ] **Input-Validation**: Client-seitige Validierung implementiert
- [ ] **Error-Display**: Benutzerfreundliche Fehlermeldungen
- [ ] **Label-Association**: Labels korrekt mit Inputs verknüpft

```typescript
// ✅ Beispiel: Accessible Form Component
export const EnergyInput: React.FC<EnergyInputProps> = ({
  value,
  onChange,
  onBlur,
  error,
  label,
  required = false,
  ...props
}) => {
  const inputId = useId()
  const errorId = useId()
  
  return (
    <div className="energy-input">
      <label htmlFor={inputId} className="energy-input__label">
        {label}
        {required && <span aria-label="Pflichtfeld">*</span>}
      </label>
      
      <input
        id={inputId}
        type="number"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
        onBlur={onBlur}
        aria-invalid={!!error}
        aria-describedby={error ? errorId : undefined}
        className={`energy-input__field ${error ? 'energy-input__field--error' : ''}`}
        {...props}
      />
      
      {error && (
        <div id={errorId} className="energy-input__error" role="alert">
          {error}
        </div>
      )}
    </div>
  )
}
```

### ✅ Chart/Visualization-Komponenten

#### Data-Handling
- [ ] **Data-Validation**: Eingabedaten auf Konsistenz prüfen
- [ ] **Loading-States**: Ladezustände für asynchrone Daten
- [ ] **Empty-States**: Anzeige bei fehlenden Daten
- [ ] **Performance**: Virtualisierung bei großen Datensätzen

#### Accessibility für Charts
- [ ] **Alternative Darstellung**: Tabelle oder Text für Screen Reader
- [ ] **Farbblindheit**: Muster oder Icons zusätzlich zu Farben
- [ ] **Keyboard-Navigation**: Datenpunkte per Tastatur erreichbar
- [ ] **ARIA-Descriptions**: Beschreibung des Chart-Inhalts

### ✅ Modal/Dialog-Komponenten

#### Focus-Management
- [ ] **Focus-Trap**: Focus bleibt im Modal gefangen
- [ ] **Initial-Focus**: Erstes focussierbares Element wird fokussiert
- [ ] **Return-Focus**: Focus kehrt zu auslösendem Element zurück
- [ ] **Escape-Handling**: ESC-Taste schließt Modal

#### Modal-Behavior
- [ ] **Backdrop-Click**: Klick außerhalb schließt Modal (optional)
- [ ] **Scroll-Lock**: Body-Scroll während Modal-Anzeige gesperrt
- [ ] **Z-Index-Management**: Korrekte Stapel-Reihenfolge
- [ ] **Animation-Performance**: Smooth Open/Close-Animationen

## Review-Prozess

### Code-Review Checkliste

#### Reviewer-Aufgaben
- [ ] **Funktionalität**: Komponent erfüllt Anforderungen vollständig
- [ ] **Performance**: Keine Performance-Regressionen
- [ ] **Accessibility**: A11y-Standards eingehalten
- [ ] **Browser-Kompatibilität**: Tests in verschiedenen Browsern
- [ ] **Mobile-Responsiveness**: Funktioniert auf verschiedenen Bildschirmgrößen

#### Automatisierte Checks
- [ ] **CI-Pipeline**: Alle automatisierten Tests bestanden
- [ ] **Coverage**: Test-Coverage über definiertem Schwellenwert
- [ ] **Bundle-Size**: Keine signifikante Vergrößerung des Bundles
- [ ] **Lighthouse-Score**: Accessibility-Score mindestens 95

### Deployment-Checkliste

#### Pre-Deployment
- [ ] **Storybook-Update**: Stories funktionieren in Storybook-Build
- [ ] **Documentation**: Alle Docs sind aktuell
- [ ] **Breaking-Changes**: Migration-Guide bei Breaking Changes
- [ ] **Changelog**: Änderungen dokumentiert

#### Post-Deployment
- [ ] **Monitoring**: Performance-Metriken überwachen
- [ ] **User-Feedback**: Community-Feedback sammeln
- [ ] **Bug-Reports**: Issue-Tracking für neue Probleme
- [ ] **Follow-up**: Iterative Verbesserungen basierend auf Nutzung

---

## Template für neue Komponenten

```bash
# Komponent-Struktur generieren
mkdir -p src/components/NewComponent
cd src/components/NewComponent

# Dateien erstellen
touch NewComponent.tsx
touch NewComponent.stories.tsx  
touch NewComponent.test.tsx
touch NewComponent.module.css
touch index.ts
```

```typescript
// NewComponent.tsx Template
import React from 'react'
import styles from './NewComponent.module.css'

export interface NewComponentProps {
  /**
   * Beschreibung der Prop
   */
  children: React.ReactNode
  /**
   * Zusätzliche CSS-Klassen
   */
  className?: string
}

/**
 * NewComponent - Kurze Beschreibung
 * 
 * Längere Beschreibung der Funktionalität und Verwendung.
 */
export const NewComponent: React.FC<NewComponentProps> = ({
  children,
  className = '',
  ...props
}) => {
  return (
    <div 
      className={`${styles.newComponent} ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}

export default NewComponent
```

---

**Letzte Aktualisierung**: 2024-12-10  
**Version**: 1.0.0  
**Maintainer**: Terra Nature Development Team