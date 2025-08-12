# Testing-Setup für Terra Nature v2.4

## Übersicht

Dieses Dokument beschreibt die Testing-Architektur und Setup-Prozesse für das Terra Nature v2.4 Projekt. Wir verwenden eine Kombination aus Vitest, React Testing Library, jest-axe und Storybook für umfassende Test-Coverage.

## Inhaltsverzeichnis

1. [Testing-Stack Übersicht](#testing-stack-übersicht)
2. [Vitest-Setup](#vitest-setup)
3. [React Component Testing](#react-component-testing)
4. [Accessibility Testing](#accessibility-testing)
5. [Integration Testing](#integration-testing)
6. [E2E Testing mit Storybook](#e2e-testing-mit-storybook)
7. [Performance Testing](#performance-testing)
8. [CI/CD Integration](#cicd-integration)

## Testing-Stack Übersicht

### Technologie-Stack

```typescript
// Test-Framework
"vitest": "^1.0.4"              // Schneller Test-Runner
"jsdom": "^23.0.1"              // DOM-Simulation

// React Testing
"@testing-library/react": "^13.4.0"        // Component Testing
"@testing-library/user-event": "^14.5.1"   // User Interactions
"@testing-library/jest-dom": "^6.1.5"      // DOM-Assertions

// Accessibility Testing
"jest-axe": "^8.0.0"            // A11y-Validierung

// Mocking & Fixtures
// Vitest-native Mocking
```

### Test-Kategorien

```bash
# Unit Tests
npm run test:unit           # Einzelne Funktionen/Hooks

# Component Tests  
npm run test:components     # React-Komponenten

# Integration Tests
npm run test:integration    # Mehrere Komponenten zusammen

# A11y Tests
npm run test:a11y          # Accessibility-Validierung

# All Tests
npm test                   # Vollständige Test-Suite
```

## Vitest-Setup

### Konfiguration (vitest.config.ts)

```typescript
/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    // Test-Environment
    environment: 'jsdom',
    
    // Setup-Dateien
    setupFiles: ['./tests/setup.ts'],
    
    // Global verfügbare Test-Utilities
    globals: true,
    
    // CSS-Support für styled-components
    css: true,
    
    // Coverage-Konfiguration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/setup.ts',
        '**/*.stories.tsx',
        '**/*.config.ts',
        'dist/',
        '.storybook/',
      ],
      thresholds: {
        global: {
          branches: 75,
          functions: 80,
          lines: 80,
          statements: 80,
        },
      },
    },
    
    // Test-Timeouts
    testTimeout: 10000,
    hookTimeout: 10000,
    
    // Test-Pattern
    include: [
      'tests/**/*.{test,spec}.{js,ts,tsx}',
      'src/**/__tests__/**/*.{js,ts,tsx}',
    ],
    
    // Watch-Mode für Development
    watch: false,
    
    // Reporter für bessere Output
    reporter: ['verbose', 'json'],
  },
})
```

### Setup-Datei (tests/setup.ts)

```typescript
import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach, beforeAll, vi } from 'vitest'

// Cleanup nach jedem Test
afterEach(() => {
  cleanup()
})

// Global Mocks
beforeAll(() => {
  // ResizeObserver Mock (für Chart-Komponenten)
  global.ResizeObserver = class ResizeObserver {
    constructor(_callback: ResizeObserverCallback) {}
    observe(_target: Element): void {}
    unobserve(_target: Element): void {}
    disconnect(): void {}
  }

  // IntersectionObserver Mock (für Lazy Loading)
  global.IntersectionObserver = class IntersectionObserver {
    constructor(_callback: IntersectionObserverCallback) {}
    observe(_target: Element): void {}
    unobserve(_target: Element): void {}
    disconnect(): void {}
  }

  // matchMedia Mock (für responsive Tests)
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation(query => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  })

  // WebSocket Mock für Energy-Monitoring
  global.WebSocket = class WebSocket extends EventTarget {
    static CONNECTING = 0
    static OPEN = 1
    static CLOSING = 2
    static CLOSED = 3

    readyState = WebSocket.CONNECTING
    url: string

    constructor(url: string) {
      super()
      this.url = url
      setTimeout(() => {
        this.readyState = WebSocket.OPEN
        this.dispatchEvent(new Event('open'))
      }, 100)
    }

    send(_data: string) {
      // Mock implementation
    }

    close() {
      this.readyState = WebSocket.CLOSED
      this.dispatchEvent(new Event('close'))
    }
  }

  // Console-Spies für Error-Testing
  vi.spyOn(console, 'error').mockImplementation(() => {})
  vi.spyOn(console, 'warn').mockImplementation(() => {})
})
```

## React Component Testing

### Basis Component Test

```typescript
// tests/components/EnergyMeter.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { EnergyMeter } from '../../src/components/EnergyMeter'

describe('EnergyMeter', () => {
  const defaultProps = {
    value: 150,
    unit: 'kWh' as const,
    onThresholdReached: vi.fn(),
  }

  it('should render energy value correctly', () => {
    render(<EnergyMeter {...defaultProps} />)
    
    expect(screen.getByText('150')).toBeInTheDocument()
    expect(screen.getByText('kWh')).toBeInTheDocument()
  })

  it('should format large values correctly', () => {
    render(<EnergyMeter {...defaultProps} value={1500} format="compact" />)
    
    expect(screen.getByText('1.5k')).toBeInTheDocument()
  })

  it('should call onThresholdReached when limit exceeded', async () => {
    const user = userEvent.setup()
    const mockCallback = vi.fn()
    
    render(
      <EnergyMeter 
        {...defaultProps} 
        value={900} 
        threshold={800}
        onThresholdReached={mockCallback} 
      />
    )
    
    // Threshold-Check auslösen
    const checkButton = screen.getByRole('button', { name: /check threshold/i })
    await user.click(checkButton)
    
    expect(mockCallback).toHaveBeenCalledWith(900)
  })

  it('should handle invalid values gracefully', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    
    render(<EnergyMeter {...defaultProps} value={-100} />)
    
    expect(screen.getByText(/invalid value/i)).toBeInTheDocument()
    expect(consoleSpy).toHaveBeenCalled()
    
    consoleSpy.mockRestore()
  })

  it('should update display when props change', () => {
    const { rerender } = render(<EnergyMeter {...defaultProps} value={100} />)
    
    expect(screen.getByText('100')).toBeInTheDocument()
    
    rerender(<EnergyMeter {...defaultProps} value={200} />)
    
    expect(screen.getByText('200')).toBeInTheDocument()
    expect(screen.queryByText('100')).not.toBeInTheDocument()
  })
})
```

### Komplexe Component Tests mit Context

```typescript
// tests/components/EnergyDashboard.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { EnergyContext, EnergyProvider } from '../../src/contexts/EnergyContext'
import { EnergyDashboard } from '../../src/components/EnergyDashboard'

// Custom Render mit Context
const renderWithEnergyContext = (
  ui: React.ReactElement,
  contextValue?: Partial<EnergyContextType>
) => {
  const defaultValue: EnergyContextType = {
    energyData: [],
    isConnected: true,
    error: null,
    addEnergyReading: vi.fn(),
    clearData: vi.fn(),
    ...contextValue,
  }

  return render(
    <EnergyContext.Provider value={defaultValue}>
      {ui}
    </EnergyContext.Provider>
  )
}

describe('EnergyDashboard', () => {
  it('should display energy data from context', () => {
    const mockData = [
      { id: '1', type: 'NRG', value: 150, timestamp: new Date() },
      { id: '2', type: 'NRG', value: 200, timestamp: new Date() },
    ]

    renderWithEnergyContext(<EnergyDashboard />, {
      energyData: mockData,
    })

    expect(screen.getByText('150 kWh')).toBeInTheDocument()
    expect(screen.getByText('200 kWh')).toBeInTheDocument()
  })

  it('should show error message when connection fails', () => {
    renderWithEnergyContext(<EnergyDashboard />, {
      isConnected: false,
      error: 'WebSocket connection failed',
    })

    expect(screen.getByText(/connection failed/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument()
  })

  it('should add new energy reading via form', async () => {
    const user = userEvent.setup()
    const mockAddReading = vi.fn()

    renderWithEnergyContext(<EnergyDashboard />, {
      addEnergyReading: mockAddReading,
    })

    const input = screen.getByLabelText(/energy value/i)
    const submitButton = screen.getByRole('button', { name: /add reading/i })

    await user.type(input, '300')
    await user.click(submitButton)

    expect(mockAddReading).toHaveBeenCalledWith(300)
  })
})
```

### Custom Hooks Testing

```typescript
// tests/hooks/useEnergyCalculations.test.ts
import { renderHook } from '@testing-library/react'
import { useEnergyCalculations } from '../../src/hooks/useEnergyCalculations'

describe('useEnergyCalculations', () => {
  it('should calculate CO2 equivalent correctly', () => {
    const { result } = renderHook(() => 
      useEnergyCalculations([
        { id: '1', type: 'NRG', value: 100, timestamp: new Date() }
      ])
    )

    expect(result.current.totalCO2).toBe(42) // 100 * 0.42
  })

  it('should update calculations when data changes', () => {
    const initialData = [
      { id: '1', type: 'NRG', value: 100, timestamp: new Date() }
    ]

    const { result, rerender } = renderHook(
      ({ data }) => useEnergyCalculations(data),
      { initialProps: { data: initialData } }
    )

    expect(result.current.totalEnergy).toBe(100)

    const newData = [
      ...initialData,
      { id: '2', type: 'NRG', value: 200, timestamp: new Date() }
    ]

    rerender({ data: newData })

    expect(result.current.totalEnergy).toBe(300)
    expect(result.current.totalCO2).toBe(126) // 300 * 0.42
  })
})
```

## Accessibility Testing

### jest-axe Integration

```typescript
// tests/a11y/EnergyDialog.a11y.test.tsx
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { EnergyDialog } from '../../src/components/EnergyDialog'

// Erweitere expect mit jest-axe Matchers
expect.extend(toHaveNoViolations)

describe('EnergyDialog Accessibility', () => {
  it('should not have accessibility violations when open', async () => {
    const { container } = render(
      <EnergyDialog 
        isOpen={true} 
        title="Energy Settings" 
        onClose={() => {}}
      >
        <p>Dialog content with form elements.</p>
        <button>Action Button</button>
      </EnergyDialog>
    )

    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('should have proper ARIA attributes', () => {
    const { getByRole, getByLabelText } = render(
      <EnergyDialog 
        isOpen={true} 
        title="Energy Configuration" 
        onClose={() => {}}
      >
        <form>
          <label htmlFor="energy-input">Energy Value</label>
          <input id="energy-input" type="number" />
        </form>
      </EnergyDialog>
    )

    const dialog = getByRole('dialog')
    expect(dialog).toHaveAttribute('aria-modal', 'true')
    expect(dialog).toHaveAttribute('aria-labelledby')

    const closeButton = getByLabelText(/close dialog/i)
    expect(closeButton).toBeInTheDocument()
  })

  it('should maintain focus within dialog', async () => {
    const user = userEvent.setup()
    
    render(
      <div>
        <button>Outside Button</button>
        <EnergyDialog 
          isOpen={true} 
          title="Focus Test" 
          onClose={() => {}}
        >
          <input type="text" placeholder="First input" />
          <button>Middle Button</button>
          <input type="text" placeholder="Last input" />
        </EnergyDialog>
      </div>
    )

    const firstInput = screen.getByPlaceholderText('First input')
    const lastInput = screen.getByPlaceholderText('Last input')

    // Focus sollte initial auf erstem Element sein
    expect(firstInput).toHaveFocus()

    // Tab zum letzten Element
    await user.tab()
    await user.tab()
    expect(lastInput).toHaveFocus()

    // Ein weiterer Tab sollte zum ersten Element zurückführen
    await user.tab()
    expect(firstInput).toHaveFocus()
  })

  it('should close on Escape key', async () => {
    const user = userEvent.setup()
    const mockClose = vi.fn()

    render(
      <EnergyDialog 
        isOpen={true} 
        title="Escape Test" 
        onClose={mockClose}
      >
        <p>Press Escape to close</p>
      </EnergyDialog>
    )

    await user.keyboard('{Escape}')
    expect(mockClose).toHaveBeenCalled()
  })
})
```

### Farbkontrast Testing

```typescript
// tests/a11y/colorContrast.test.tsx
import { render } from '@testing-library/react'
import { axe } from 'jest-axe'

describe('Color Contrast Compliance', () => {
  it('should meet WCAG AA contrast requirements', async () => {
    const { container } = render(
      <div>
        <h1 style={{ color: '#333', backgroundColor: '#fff' }}>
          Terra Nature Dashboard
        </h1>
        <button style={{ 
          backgroundColor: '#0d6efd', 
          color: '#fff',
          border: 'none',
          padding: '0.5rem 1rem' 
        }}>
          Primary Action
        </button>
        <p style={{ color: '#6c757d', backgroundColor: '#f8f9fa' }}>
          Secondary text content
        </p>
      </div>
    )

    const results = await axe(container, {
      rules: {
        'color-contrast': { enabled: true },
      },
    })

    expect(results).toHaveNoViolations()
  })
})
```

## Integration Testing

### Multi-Component Integration

```typescript
// tests/integration/EnergyMonitoring.integration.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { EnergyMonitoringApp } from '../../src/EnergyMonitoringApp'

// Mock WebSocket für Integration Tests
const mockWebSocket = {
  send: vi.fn(),
  close: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
}

vi.mock('../../src/hooks/useWebSocket', () => ({
  useWebSocket: () => ({
    isConnected: true,
    error: null,
    sendMessage: mockWebSocket.send,
    disconnect: mockWebSocket.close,
  }),
}))

describe('Energy Monitoring Integration', () => {
  it('should handle complete energy reading workflow', async () => {
    const user = userEvent.setup()
    
    render(<EnergyMonitoringApp />)

    // 1. Überprüfen dass Dashboard geladen ist
    expect(screen.getByText(/energy dashboard/i)).toBeInTheDocument()

    // 2. Neue Energie-Messung hinzufügen
    const energyInput = screen.getByLabelText(/energy value/i)
    const addButton = screen.getByRole('button', { name: /add reading/i })

    await user.type(energyInput, '250')
    await user.click(addButton)

    // 3. Überprüfen dass Wert in Dashboard angezeigt wird
    await waitFor(() => {
      expect(screen.getByText('250 kWh')).toBeInTheDocument()
    })

    // 4. CO2-Berechnung überprüfen
    expect(screen.getByText(/105\.0 kg co2/i)).toBeInTheDocument() // 250 * 0.42

    // 5. Filter anwenden
    const filterSelect = screen.getByLabelText(/time period/i)
    await user.selectOptions(filterSelect, 'today')

    // 6. Chart-Interaktion
    const chartElement = screen.getByRole('img', { name: /energy chart/i })
    await user.hover(chartElement)

    await waitFor(() => {
      expect(screen.getByText(/tooltip/i)).toBeInTheDocument()
    })
  })

  it('should handle WebSocket connection errors gracefully', async () => {
    const user = userEvent.setup()

    // Mock WebSocket error
    vi.mocked(useWebSocket).mockReturnValue({
      isConnected: false,
      error: 'Connection failed',
      sendMessage: vi.fn(),
      disconnect: vi.fn(),
    })

    render(<EnergyMonitoringApp />)

    // Error message sollte angezeigt werden
    expect(screen.getByText(/connection failed/i)).toBeInTheDocument()

    // Retry-Button sollte verfügbar sein
    const retryButton = screen.getByRole('button', { name: /retry/i })
    expect(retryButton).toBeInTheDocument()

    await user.click(retryButton)

    // Reconnect-Versuch sollte ausgelöst werden
    expect(mockWebSocket.connect).toHaveBeenCalled()
  })
})
```

## E2E Testing mit Storybook

### Storybook Test Runner

```typescript
// .storybook/test-runner.ts
import { injectAxe, checkA11y } from 'axe-playwright'

module.exports = {
  async preRender(page) {
    await injectAxe(page)
  },
  
  async postRender(page, context) {
    // A11y-Tests für jede Story
    await checkA11y(page, '#storybook-root', {
      detailedReport: true,
      detailedReportOptions: {
        html: true,
      },
    })

    // Custom Tests für spezifische Stories
    if (context.name.includes('Interactive')) {
      // Interaktive Tests für Interactive Stories
      await page.click('[data-testid="increment-button"]')
      await page.waitForSelector('[data-testid="updated-value"]')
    }
  },
}
```

### Story-basierte Tests

```typescript
// src/components/EnergyChart.stories.tsx
import { expect } from '@storybook/test'
import { within, userEvent } from '@storybook/testing-library'

export const InteractiveChart: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    
    // Chart-Interaktionen testen
    const chart = canvas.getByRole('img')
    await userEvent.hover(chart)
    
    // Tooltip sollte erscheinen
    await expect(canvas.getByRole('tooltip')).toBeInTheDocument()
    
    // Datenpunkt klicken
    const dataPoint = canvas.getByTestId('data-point-1')
    await userEvent.click(dataPoint)
    
    // Detail-View sollte geöffnet werden
    await expect(canvas.getByRole('dialog')).toBeInTheDocument()
  },
}
```

## Performance Testing

### Performance Metrics

```typescript
// tests/performance/EnergyChart.perf.test.tsx
import { render } from '@testing-library/react'
import { performance } from 'perf_hooks'
import { EnergyChart } from '../../src/components/EnergyChart'

describe('EnergyChart Performance', () => {
  it('should render large datasets efficiently', () => {
    const largeDataset = Array.from({ length: 10000 }, (_, i) => ({
      id: i.toString(),
      value: Math.random() * 1000,
      timestamp: new Date(Date.now() - i * 60000),
    }))

    const startTime = performance.now()
    
    render(<EnergyChart data={largeDataset} />)
    
    const endTime = performance.now()
    const renderTime = endTime - startTime

    // Render sollte unter 100ms dauern
    expect(renderTime).toBeLessThan(100)
  })

  it('should handle frequent updates without memory leaks', () => {
    const { rerender } = render(<EnergyChart data={[]} />)
    
    const initialMemory = (performance as any).memory?.usedJSHeapSize || 0

    // 100 Updates simulieren
    for (let i = 0; i < 100; i++) {
      const data = Array.from({ length: 100 }, (_, j) => ({
        id: `${i}-${j}`,
        value: Math.random() * 1000,
        timestamp: new Date(),
      }))
      
      rerender(<EnergyChart data={data} />)
    }

    const finalMemory = (performance as any).memory?.usedJSHeapSize || 0
    const memoryIncrease = finalMemory - initialMemory

    // Memory-Increase sollte unter 10MB bleiben
    expect(memoryIncrease).toBeLessThan(10 * 1024 * 1024)
  })
})
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite
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
      
      - name: Run TypeScript checks
        run: npm run type-check
      
      - name: Run linting
        run: npm run lint
      
      - name: Run unit tests
        run: npm run test:coverage
      
      - name: Run Storybook tests
        run: npm run test-storybook:ci
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: |
            coverage/
            test-results.xml
```

### Test-Skripte (package.json)

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui",
    "test:components": "vitest run src/components",
    "test:a11y": "vitest run tests/a11y",
    "test:integration": "vitest run tests/integration",
    "test-storybook": "test-storybook",
    "test-storybook:ci": "concurrently -k -s first -n \"SB,TEST\" \"npm run storybook:ci\" \"wait-on tcp:6006 && npm run test-storybook\"",
    "type-check": "tsc --noEmit"
  }
}
```

## Best Practices Zusammenfassung

### Do's ✅

- **Isolierte Tests**: Jeder Test sollte unabhängig laufen können
- **Beschreibende Namen**: Tests als lebende Dokumentation
- **AAA-Pattern**: Arrange, Act, Assert struktur
- **Mock External Dependencies**: APIs, WebSockets, Browser-APIs
- **Test User Behavior**: Nicht Implementation-Details
- **Accessibility Testing**: A11y als Standard-Requirement

### Don'ts ❌

- **Implementationsdetails testen**: Nur öffentliche APIs testen
- **Snapshot-Tests überstrapazieren**: Nur bei stabilen UI-Komponenten
- **Zu viele Mocks**: Balance zwischen Isolation und Realitätsnähe
- **Flaky Tests ignorieren**: Instabile Tests sofort reparieren
- **Coverage-Zahlen-Jagd**: Qualität vor Quantität

---

**Letzte Aktualisierung**: 2024-12-10  
**Version**: 1.0.0  
**Maintainer**: Terra Nature Development Team