# Frontend-Guidelines v2.1

## Commit-Konvention
- Commitlint + Husky/Lint-Staged sind Pflicht in CI.

## A11y {#a11y}
- `:focus-visible`
- `aria-live` für Toasts
- `prefers-reduced-motion`

## Performance
- Web-Vitals-Ziele: LCP, CLS, INP.
- RUM-Telemetrie einplanen.

## Tests {#tests}
- API-Contract-Tests (MSW).

## Security
- CSP-Baseline.
- Dependabot/npm audit.
- Secret-Scanning.

## Design-Tokens
- Mindestens Light/Dark-Theming via CSS-Variablen.

## Branch-Strategie
- Optionales `release/x.y.z` wie im Workflow-Dokument.

## Review-Erwartungen
- Max. Diff-Scope ≤ 400 LOC (außer Migrations), sonst aufteilen.
