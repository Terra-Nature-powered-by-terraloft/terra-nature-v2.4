# Storybook-Setup für Terra Nature v2.4

## Übersicht

Storybook ist unser Tool für die isolierte Entwicklung und Dokumentation von React-Komponenten im Terra Nature v2.4 Projekt. Diese Anleitung führt durch Setup, Konfiguration und Best Practices.

## Inhaltsverzeichnis

1. [Quick Start](#quick-start)
2. [Grundlegende Konfiguration](#grundlegende-konfiguration)
3. [Stories erstellen](#stories-erstellen)
4. [Addons und Erweiterungen](#addons-und-erweiterungen)
5. [Testing mit Storybook](#testing-mit-storybook)
6. [Deployment und CI/CD](#deployment-und-cicd)
7. [Troubleshooting](#troubleshooting)

## Quick Start

### Installation und erste Schritte

```bash
# Repository klonen und Dependencies installieren
git clone https://github.com/Terra-Nature-powered-by-terraloft/terra-nature-v2.4.git
cd terra-nature-v2.4
npm install

# Storybook starten
npm run storybook

# Öffnet automatisch: http://localhost:6006
```

### Erste Story erstellen

```typescript
// src/components/EnergyWidget/EnergyWidget.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { EnergyWidget } from './EnergyWidget'

const meta: Meta<typeof EnergyWidget> = {
  title: 'Dashboard/EnergyWidget',
  component: EnergyWidget,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Widget zur Anzeige von Energieverbrauchsdaten mit CO2-Berechnungen.'
      }
    }
  },
  argTypes: {
    value: { control: 'number' },
    unit: { control: { type: 'select', options: ['kWh', 'MWh'] } }
  }
}

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    value: 150,
    unit: 'kWh'
  }
}
```

## Grundlegende Konfiguration

### .storybook/main.ts Erklärung

```typescript
import type { StorybookConfig } from '@storybook/react-vite'

const config: StorybookConfig = {
  // Story-Dateien Pattern
  stories: ['../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  
  // Aktivierte Addons
  addons: [
    '@storybook/addon-links',         // Komponenten verlinken
    '@storybook/addon-essentials',    // Standard-Addons Bundle
    '@storybook/addon-interactions',  // User-Interaction Testing
    '@storybook/addon-a11y',         // Accessibility Testing
  ],
  
  // Framework-Konfiguration
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  
  // Automatische Dokumentation
  docs: {
    autodocs: 'tag',
  },
  
  // TypeScript-Konfiguration
  typescript: {
    check: false,
    reactDocgen: 'react-docgen-typescript',
    reactDocgenTypescriptOptions: {
      shouldExtractLiteralValuesFromEnum: true,
      propFilter: (prop) => (prop.parent ? !/node_modules/.test(prop.parent.fileName) : true),
    },
  },
}

export default config
```

### .storybook/preview.ts Konfiguration

```typescript
import type { Preview } from '@storybook/react'
import '../src/globals.css' // Globale Styles laden

const preview: Preview = {
  parameters: {
    // Actions-Konfiguration
    actions: { argTypesRegex: '^on[A-Z].*' },
    
    // Controls-Konfiguration
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
    
    // A11y-Addon Konfiguration
    a11y: {
      element: '#storybook-root',
      config: {},
      options: {},
      manual: true,
    },
    
    // Viewport-Konfiguration für Responsive Testing
    viewport: {
      viewports: {
        mobile: {
          name: 'Mobile',
          styles: { width: '375px', height: '667px' },
        },
        tablet: {
          name: 'Tablet',
          styles: { width: '768px', height: '1024px' },
        },
        desktop: {
          name: 'Desktop',
          styles: { width: '1920px', height: '1080px' },
        },
      },
    },
  },
  
  // Globale Decorators
  decorators: [
    (Story) => (
      <div style={{ padding: '2rem' }}>
        <Story />
      </div>
    ),
  ],
}

export default preview
```

## Stories erstellen

### Story-Anatomie

```typescript
// Vollständiges Beispiel einer Story-Datei
import type { Meta, StoryObj } from '@storybook/react'
import { fn } from '@storybook/testing-library'
import { EnergyDashboard } from './EnergyDashboard'

// Meta-Konfiguration definiert grundlegende Story-Eigenschaften
const meta: Meta<typeof EnergyDashboard> = {
  // Hierarchie im Storybook-Navigator
  title: 'Pages/EnergyDashboard',
  
  // React-Komponente
  component: EnergyDashboard,
  
  // Story-Parameter
  parameters: {
    layout: 'fullscreen', // 'centered', 'fullscreen', 'padded'
    
    // Dokumentation
    docs: {
      description: {
        component: `
          Das Energy Dashboard ist die Hauptansicht für CO2-Tracking und Energiemonitoring.
          Es zeigt Real-Time Daten von WebSocket-Verbindungen an.
        `
      }
    },
    
    // Background-Farben zum Testen
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
        { name: 'earth', value: '#2d5016' },
      ],
    },
  },
  
  // Control-Konfiguration für Props
  argTypes: {
    initialData: {
      description: 'Anfangsdaten für das Dashboard',
      control: 'object',
    },
    
    theme: {
      description: 'Dashboard-Theme',
      control: { type: 'select' },
      options: ['light', 'dark', 'earth'],
    },
    
    showDebugInfo: {
      description: 'Debug-Informationen anzeigen',
      control: 'boolean',
    },
    
    onDataUpdate: {
      description: 'Callback bei Datenaktualisierung',
      action: 'data-updated', // Erscheint im Actions-Panel
    },
  },
  
  // Standard-Args für alle Stories
  args: {
    onDataUpdate: fn(),
  },
}

export default meta
type Story = StoryObj<typeof meta>

// Standard-Story
export const Default: Story = {
  args: {
    initialData: [
      { type: 'NRG', value: 150, id: '1', timestamp: new Date() },
      { type: 'NRG', value: 200, id: '2', timestamp: new Date() },
    ],
    theme: 'light',
  },
}

// Dark Mode Variante
export const DarkMode: Story = {
  args: {
    ...Default.args,
    theme: 'dark',
  },
  parameters: {
    backgrounds: { default: 'dark' },
    docs: {
      description: {
        story: 'Dashboard im Dark Mode für bessere Lesbarkeit bei schwachem Licht.'
      }
    }
  }
}

// High Energy Consumption Scenario
export const HighConsumption: Story = {
  args: {
    ...Default.args,
    initialData: [
      { type: 'NRG', value: 850, id: '1', timestamp: new Date() },
      { type: 'NRG', value: 920, id: '2', timestamp: new Date() },
      { type: 'NRG', value: 1100, id: '3', timestamp: new Date() },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Zeigt das Dashboard-Verhalten bei hohem Energieverbrauch mit Warnindikatoren.'
      }
    }
  }
}

// Loading State
export const Loading: Story = {
  args: {
    initialData: [],
    isLoading: true,
  },
}

// Error State
export const Error: Story = {
  args: {
    error: 'WebSocket-Verbindung fehlgeschlagen. Bitte versuchen Sie es erneut.',
  },
}
```

### Interaktive Stories mit Play Functions

```typescript
import { userEvent, within } from '@storybook/testing-library'
import { expect } from '@storybook/test'

export const UserInteraction: Story = {
  args: {
    ...Default.args,
  },
  
  // Automatisierte User-Interaktionen
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    
    // Energie-Eingabefeld finden und Wert eingeben
    const energyInput = canvas.getByLabelText(/energie eingeben/i)
    await userEvent.clear(energyInput)
    await userEvent.type(energyInput, '500')
    
    // Submit-Button klicken
    const submitButton = canvas.getByRole('button', { name: /hinzufügen/i })
    await userEvent.click(submitButton)
    
    // Erwartetes Ergebnis prüfen
    await expect(canvas.getByText('500 kWh')).toBeInTheDocument()
    
    // Filter-Interaktion
    const filterSelect = canvas.getByLabelText(/zeitraum filter/i)
    await userEvent.selectOptions(filterSelect, 'last-week')
    
    // Prüfen ob Filter angewendet wurde
    await expect(canvas.getByText(/letzte woche/i)).toBeInTheDocument()
  },
}
```

## Addons und Erweiterungen

### Accessibility-Testing mit A11y Addon

```typescript
// Story mit spezifischen A11y-Tests
export const AccessibilityTest: Story = {
  args: {
    ...Default.args,
  },
  parameters: {
    a11y: {
      // Spezifische A11y-Regeln konfigurieren
      config: {
        rules: [
          {
            id: 'color-contrast',
            enabled: true,
          },
          {
            id: 'label',
            enabled: true,
          },
        ],
      },
      // Bestimmte Elemente von Tests ausschließen
      options: {
        exclude: '.chart-tooltip', // Tooltips oft problematisch
      },
    },
  },
}
```

### Controls-Addon erweitert nutzen

```typescript
// Erweiterte Control-Konfigurationen
argTypes: {
  energyData: {
    description: 'Array von Energiemessungen',
    control: {
      type: 'object',
    },
    table: {
      type: { summary: 'EnergyReading[]' },
      defaultValue: { summary: '[]' },
    },
  },
  
  co2Factor: {
    description: 'CO2-Umrechnungsfaktor (kg CO2 / kWh)',
    control: {
      type: 'number',
      min: 0,
      max: 1,
      step: 0.01,
    },
    table: {
      type: { summary: 'number' },
      defaultValue: { summary: '0.42' },
    },
  },
  
  chartType: {
    description: 'Art der Diagramm-Darstellung',
    control: {
      type: 'select',
      options: ['line', 'bar', 'area'],
    },
    mapping: {
      line: 'line-chart',
      bar: 'bar-chart',
      area: 'area-chart',
    },
  },
  
  theme: {
    description: 'Visuelle Theme-Variante',
    control: {
      type: 'radio',
      options: ['light', 'dark', 'earth'],
    },
  },
  
  onEnergyUpdate: {
    description: 'Callback bei neuen Energiedaten',
    action: 'energy-updated',
  },
}
```

### Viewport-Addon für Responsive Testing

```typescript
// .storybook/preview.ts - Erweiterte Viewport-Konfiguration
viewport: {
  viewports: {
    // Terra Nature spezifische Viewports
    mobileTerra: {
      name: 'Terra Mobile (iPhone 12)',
      styles: { width: '390px', height: '844px' },
      type: 'mobile',
    },
    tabletTerra: {
      name: 'Terra Tablet (iPad)',
      styles: { width: '768px', height: '1024px' },
      type: 'tablet',
    },
    dashboardMonitor: {
      name: 'Dashboard Monitor (1440p)',
      styles: { width: '2560px', height: '1440px' },
      type: 'desktop',
    },
  },
  defaultViewport: 'dashboardMonitor',
},

// Story mit spezifischen Viewport-Tests
export const ResponsiveBreakpoints: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobileTerra',
    },
    chromatic: {
      // Screenshots für verschiedene Viewports in Chromatic
      viewports: [390, 768, 1440, 2560],
    },
  },
}
```

## Testing mit Storybook

### Test Runner Setup

```bash
# Test Runner installieren
npm install -D @storybook/test-runner

# Package.json Script hinzufügen
"scripts": {
  "test-storybook": "test-storybook",
  "test-storybook:ci": "concurrently -k -s first -n \"SB,TEST\" -c \"magenta,blue\" \"npm run storybook:ci\" \"wait-on tcp:6006 && npm run test-storybook\""
}
```

```typescript
// .storybook/test-runner.ts - Erweiterte Test-Konfiguration
import { injectAxe, checkA11y, configureAxe } from 'axe-playwright'

module.exports = {
  async preRender(page) {
    await injectAxe(page)
  },
  
  async postRender(page) {
    // A11y-Tests für jede Story
    await configureAxe(page, {
      rules: [
        {
          id: 'color-contrast',
          enabled: true,
        },
      ],
    })
    await checkA11y(page, '#storybook-root', {
      detailedReport: true,
      detailedReportOptions: {
        html: true,
      },
    })
  },
}
```

### Visual Regression Tests

```typescript
// .storybook/preview.ts - Chromatic-Konfiguration
parameters: {
  chromatic: {
    // Animationen pausieren für konsistente Screenshots
    pauseAnimationAtEnd: true,
    
    // Bestimmte Stories von Visual Tests ausschließen
    disableSnapshot: false,
    
    // Verzögerung vor Screenshot
    delay: 1000,
  },
}

// Einzelne Story von Visual Tests ausschließen
export const InteractiveDemo: Story = {
  parameters: {
    chromatic: { disableSnapshot: true },
  },
}
```

## Deployment und CI/CD

### Storybook Build für Production

```bash
# Static Storybook Build
npm run build-storybook

# Output in storybook-static/ Verzeichnis
# Kann auf beliebigem Webserver gehostet werden
```

### GitHub Actions Workflow

```yaml
# .github/workflows/storybook.yml
name: Storybook Tests
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - run: npm ci
      
      - name: Run Storybook tests
        run: npm run test-storybook:ci
      
      - name: Build Storybook
        run: npm run build-storybook
      
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./storybook-static
```

### Chromatic Integration

```bash
# Chromatic installieren
npm install -D chromatic

# Package.json Script
"scripts": {
  "chromatic": "chromatic --project-token=<YOUR_PROJECT_TOKEN>"
}
```

```yaml
# GitHub Actions für Chromatic
- name: Publish to Chromatic
  uses: chromaui/action@v1
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    buildScriptName: build-storybook
```

## Troubleshooting

### Häufige Probleme und Lösungen

#### Storybook startet nicht

```bash
# Dependency-Konflikte lösen
rm -rf node_modules package-lock.json
npm install

# Storybook-Cache löschen
npx storybook@latest automigrate
```

#### TypeScript-Fehler in Stories

```typescript
// Häufiger Fehler: Controls funktionieren nicht mit TypeScript

// ❌ Schlecht: Fehlende Typisierung
export const Example: Story = {
  args: {
    unknownProp: 'value' // TypeScript-Fehler
  }
}

// ✅ Besser: Korrekte Typisierung
export const Example: Story = {
  args: {
    knownProp: 'value'
  } satisfies ComponentProps<typeof MyComponent>
}
```

#### Import-Probleme mit CSS/Assets

```typescript
// .storybook/main.ts - Webpack-Alias konfigurieren
viteFinal: async (config) => {
  config.resolve.alias = {
    ...config.resolve.alias,
    '@': path.resolve(__dirname, '../src'),
    '@assets': path.resolve(__dirname, '../src/assets'),
  }
  return config
}
```

#### Performance-Probleme

```typescript
// Große Datasets in Stories handhaben
export const LargeDataset: Story = {
  args: {
    data: Array.from({ length: 1000 }, (_, i) => ({
      id: i,
      value: Math.random() * 1000,
    })),
  },
  parameters: {
    // Chromatic Screenshots überspringen
    chromatic: { disableSnapshot: true },
  },
}
```

### Debug-Modus

```bash
# Storybook im Debug-Modus starten
npm run storybook -- --debug-webpack

# Ausführliche Logs aktivieren
DEBUG=storybook:* npm run storybook
```

## Advanced Features

### Custom Decorators

```typescript
// .storybook/preview.ts - Theme-Provider Decorator
import { ThemeProvider } from '../src/contexts/ThemeContext'

export const decorators = [
  (Story, context) => {
    const theme = context.globals.theme || 'light'
    
    return (
      <ThemeProvider theme={theme}>
        <div className={`theme-${theme}`}>
          <Story />
        </div>
      </ThemeProvider>
    )
  },
]

// Global Controls für Theme
export const globalTypes = {
  theme: {
    description: 'Global theme for components',
    defaultValue: 'light',
    toolbar: {
      title: 'Theme',
      icon: 'paintbrush',
      items: [
        { value: 'light', title: 'Light', icon: 'sun' },
        { value: 'dark', title: 'Dark', icon: 'moon' },
        { value: 'earth', title: 'Earth', icon: 'leaf' },
      ],
      dynamicTitle: true,
    },
  },
}
```

### Custom Addon Development

```typescript
// .storybook/addons/energy-monitor/register.ts
import { addons, types } from '@storybook/addons'
import { ADDON_ID, PANEL_ID } from './constants'
import { EnergyPanel } from './Panel'

addons.register(ADDON_ID, () => {
  addons.add(PANEL_ID, {
    type: types.PANEL,
    title: 'Energy Monitor',
    render: ({ active, key }) => (
      <EnergyPanel active={active} key={key} />
    ),
  })
})
```

## Best Practices Zusammenfassung

### Do's ✅

- **Aussagekräftige Story-Namen**: Beschreiben den Zustand/Anwendungsfall
- **Umfassende Args**: Alle wichtigen Props als Controls verfügbar
- **Documentation**: Komponenten und Stories gut dokumentieren
- **A11y-Tests**: Accessibility-Addon für alle interaktiven Komponenten
- **Visual Tests**: Chromatic oder ähnliche Tools für Visual Regression
- **Responsive Stories**: Verschiedene Viewports testen

### Don'ts ❌

- **Echte API-Calls**: Keine echten Backend-Aufrufe in Stories
- **Seiteneffekte**: Stories sollten keine persistenten Änderungen verursachen
- **Überkomplexe Stories**: Einfache, fokussierte Beispiele bevorzugen
- **Fehlende Dokumentation**: Komponenten ohne Beschreibung vermeiden
- **Hard-coded Daten**: Mocking und Fixtures für realistische Daten

---

**Letzte Aktualisierung**: 2024-12-10  
**Version**: 1.0.0  
**Maintainer**: Terra Nature Development Team