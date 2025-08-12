# Husky Hooks Setup für Terra Nature v2.4

## Übersicht

Husky Git-Hooks automatisieren Qualitätssicherung und Code-Standards im Terra Nature v2.4 Projekt. Diese Anleitung beschreibt Setup, Konfiguration und Verwendung der Git-Hooks.

## Inhaltsverzeichnis

1. [Quick Setup](#quick-setup)
2. [Hook-Konfiguration](#hook-konfiguration)
3. [Pre-Commit Hooks](#pre-commit-hooks)
4. [Commit-Message Validation](#commit-message-validation)
5. [Pre-Push Hooks](#pre-push-hooks)
6. [Lint-Staged Integration](#lint-staged-integration)
7. [Troubleshooting](#troubleshooting)

## Quick Setup

### Installation und Aktivierung

```bash
# Repository klonen
git clone https://github.com/Terra-Nature-powered-by-terraloft/terra-nature-v2.4.git
cd terra-nature-v2.4

# Dependencies installieren (aktiviert Husky automatisch)
npm install

# Husky-Hooks sind jetzt aktiv!
# Test mit einem Commit:
git add .
git commit -m "test: husky hooks functionality"
```

### Manuelle Husky-Aktivierung (falls nötig)

```bash
# Husky initialisieren
npx husky install

# Git-Hook-Pfad setzen
git config core.hooksPath .husky

# Hooks ausführbar machen
chmod +x .husky/*
```

## Hook-Konfiguration

### Verfügbare Hooks

```bash
# Aktuelle Hook-Struktur
.husky/
├── _/                    # Husky-interne Dateien
├── pre-commit           # Code-Qualität vor Commit
├── commit-msg          # Commit-Message Validierung
└── pre-push            # Tests vor Push (optional)
```

### Husky-Konfiguration (package.json)

```json
{
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{js,json,md}": [
      "prettier --write"
    ],
    "*.{ts,tsx,js}": [
      "vitest related --run"
    ]
  }
}
```

## Pre-Commit Hooks

### .husky/pre-commit Konfiguration

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "🔍 Running pre-commit checks..."

# 1. Lint-Staged für Code-Qualität
echo "📝 Linting and formatting staged files..."
npx lint-staged

# 2. TypeScript Type-Check
echo "🔍 Running TypeScript checks..."
npm run type-check

# 3. Unit Tests für geänderte Dateien
echo "🧪 Running tests for changed files..."
npm run test:changed

echo "✅ Pre-commit checks completed!"
```

### Erweiterte Pre-Commit Validierung

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Farben für bessere Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 ${YELLOW}Terra Nature v2.4 Pre-Commit Hooks${NC}"

# Funktionen für einzelne Checks
run_linting() {
  echo "📝 ${YELLOW}Linting and formatting...${NC}"
  if npx lint-staged; then
    echo "✅ ${GREEN}Linting passed${NC}"
  else
    echo "❌ ${RED}Linting failed${NC}"
    exit 1
  fi
}

run_type_check() {
  echo "🔍 ${YELLOW}TypeScript type checking...${NC}"
  if npm run type-check; then
    echo "✅ ${GREEN}Type check passed${NC}"
  else
    echo "❌ ${RED}Type check failed${NC}"
    exit 1
  fi
}

run_tests() {
  echo "🧪 ${YELLOW}Running unit tests...${NC}"
  if npm run test:staged; then
    echo "✅ ${GREEN}Tests passed${NC}"
  else
    echo "❌ ${RED}Tests failed${NC}"
    exit 1
  fi
}

check_file_sizes() {
  echo "📊 ${YELLOW}Checking file sizes...${NC}"
  
  # Große Dateien finden (> 500KB)
  large_files=$(find . -type f -size +500k -not -path "./node_modules/*" -not -path "./.git/*")
  
  if [ -n "$large_files" ]; then
    echo "⚠️  ${YELLOW}Large files detected:${NC}"
    echo "$large_files"
    echo "Consider optimizing or adding to .gitignore"
  else
    echo "✅ ${GREEN}File sizes OK${NC}"
  fi
}

check_secrets() {
  echo "🔐 ${YELLOW}Checking for secrets...${NC}"
  
  # Einfache Regex-Patterns für Secrets
  secrets_pattern="(api[_-]?key|password|secret|token|auth)"
  
  if git diff --cached --name-only | xargs grep -i "$secrets_pattern" 2>/dev/null; then
    echo "⚠️  ${RED}Potential secrets detected in staged files!${NC}"
    echo "Please review and remove sensitive information"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      exit 1
    fi
  else
    echo "✅ ${GREEN}No secrets detected${NC}"
  fi
}

# Haupt-Execution
run_linting
run_type_check
run_tests
check_file_sizes
check_secrets

echo "🎉 ${GREEN}All pre-commit checks passed!${NC}"
```

### Package.json Scripts für Pre-Commit

```json
{
  "scripts": {
    "type-check": "tsc --noEmit",
    "test:staged": "vitest related --run",
    "test:changed": "vitest related --run --passWithNoTests",
    "lint:staged": "lint-staged"
  }
}
```

## Commit-Message Validation

### .husky/commit-msg Hook

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Conventional Commits Validierung
npx --no-install commitlint --edit "$1"
```

### Commitlint Konfiguration (commitlint.config.cjs)

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  
  rules: {
    // Typ ist Pflicht
    'type-enum': [
      2,
      'always',
      [
        'feat',     // Neue Funktionalität
        'fix',      // Bugfix
        'docs',     // Dokumentation
        'style',    // Code-Formatierung
        'refactor', // Refactoring
        'perf',     // Performance-Verbesserung
        'test',     // Tests
        'build',    // Build-System
        'ci',       // CI/CD
        'chore',    // Wartung
        'revert',   // Revert
      ],
    ],
    
    // Message-Format Regeln
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100],
    
    // Terra Nature spezifische Regeln
    'scope-enum': [
      1,
      'always',
      [
        'energy',     // Energie-bezogene Features
        'nft',        // NFT/Blockchain Features
        'dashboard',  // Dashboard-Komponenten
        'websocket',  // WebSocket-Funktionalität
        'api',        // API-Integration
        'ui',         // UI-Komponenten
        'docs',       // Dokumentation
        'test',       // Testing
        'config',     // Konfiguration
      ],
    ],
  },
  
  // Custom Plugins für Terra Nature
  plugins: [
    {
      rules: {
        'energy-feature-format': (parsed) => {
          const { scope, subject } = parsed
          
          if (scope === 'energy' && !subject.includes('kWh') && !subject.includes('CO2')) {
            return [
              false,
              'Energy-related commits should mention kWh or CO2 in subject'
            ]
          }
          
          return [true]
        },
      },
    },
  ],
}
```

### Erweiterte Commit-Message Validierung

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

commit_file=$1
commit_msg=$(cat "$commit_file")

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "📝 ${YELLOW}Validating commit message...${NC}"

# 1. Conventional Commits Check
echo "🔍 Checking conventional commit format..."
if npx --no-install commitlint --edit "$1"; then
  echo "✅ ${GREEN}Commit format valid${NC}"
else
  echo "❌ ${RED}Commit format invalid${NC}"
  echo ""
  echo "📖 ${YELLOW}Correct format examples:${NC}"
  echo "  feat(energy): add real-time CO2 calculation"
  echo "  fix(websocket): resolve connection timeout"
  echo "  docs(readme): update installation instructions"
  echo "  test(dashboard): add integration tests"
  echo ""
  exit 1
fi

# 2. Ticket-Reference Check (optional)
if [[ $commit_msg =~ \#[0-9]+ ]]; then
  echo "✅ ${GREEN}Ticket reference found${NC}"
else
  echo "ℹ️  ${YELLOW}No ticket reference found (optional)${NC}"
fi

# 3. Breaking Changes Check
if [[ $commit_msg =~ "BREAKING CHANGE" ]]; then
  echo "⚠️  ${YELLOW}Breaking change detected${NC}"
  echo "Please ensure:"
  echo "  - Migration guide is included"
  echo "  - Version bump is planned"
  echo "  - Team is notified"
fi

echo "✅ ${GREEN}Commit message validation passed${NC}"
```

## Pre-Push Hooks

### .husky/pre-push (Optional)

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Nur bei Push zu main/develop ausführen
protected_branches="main develop"
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if echo "$protected_branches" | grep -q "$current_branch"; then
  echo "🛡️  Pushing to protected branch: $current_branch"
  
  # Vollständige Test-Suite
  echo "🧪 Running full test suite..."
  npm run test:all
  
  # Build-Test
  echo "🏗️  Testing production build..."
  npm run build
  
  # Bundle-Size Check
  echo "📦 Checking bundle size..."
  npm run bundlesize
  
  echo "✅ Pre-push checks completed!"
fi
```

### Branch-Protection

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Verhindere direktes Pushen zu main
protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ "$protected_branch" = "$current_branch" ]; then
  echo "❌ Direct push to main branch is not allowed!"
  echo "Please create a pull request instead."
  echo ""
  echo "To push anyway (emergency only):"
  echo "  git push --no-verify"
  exit 1
fi

# Prüfe ob Branch up-to-date ist
git fetch origin "$current_branch"
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "@{u}" 2>/dev/null)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "⚠️  Your branch is not up-to-date with remote."
  echo "Please pull the latest changes first:"
  echo "  git pull origin $current_branch"
  exit 1
fi
```

## Lint-Staged Integration

### Erweiterte Lint-Staged Konfiguration

```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix --max-warnings 0",
      "prettier --write",
      "vitest related --run --passWithNoTests"
    ],
    
    "*.{js,jsx}": [
      "eslint --fix --max-warnings 0", 
      "prettier --write"
    ],
    
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ],
    
    "*.css": [
      "stylelint --fix",
      "prettier --write"
    ],
    
    "package.json": [
      "npm audit --audit-level moderate",
      "sort-package-json"
    ],
    
    "*.{png,jpg,jpeg,gif,svg}": [
      "imagemin-lint-staged"
    ]
  }
}
```

### Custom Lint-Staged Funktionen

```javascript
// .lintstagedrc.js
const path = require('path')

module.exports = {
  '*.{ts,tsx}': (filenames) => [
    `eslint --fix --max-warnings 0 ${filenames.join(' ')}`,
    `prettier --write ${filenames.join(' ')}`,
    
    // Tests nur für geänderte Dateien
    `vitest related ${filenames.join(' ')} --run --passWithNoTests`,
    
    // Type-Check nur für geänderte Dateien
    filenames.length > 10 
      ? 'npm run type-check' // Bei vielen Dateien: Full Check
      : `tsc --noEmit ${filenames.join(' ')}`, // Bei wenigen: nur diese Dateien
  ],
  
  '*.{js,jsx}': (filenames) => [
    `eslint --fix --max-warnings 0 ${filenames.join(' ')}`,
    `prettier --write ${filenames.join(' ')}`,
  ],
  
  // Component-spezifische Checks
  'src/components/**/*.{ts,tsx}': (filenames) => {
    const componentFiles = filenames.filter(f => 
      !f.includes('.test.') && !f.includes('.stories.')
    )
    
    if (componentFiles.length === 0) return []
    
    return [
      // Standard Checks
      `eslint --fix --max-warnings 0 ${componentFiles.join(' ')}`,
      `prettier --write ${componentFiles.join(' ')}`,
      
      // Storybook Stories Check
      () => {
        const storiesExist = componentFiles.every(file => {
          const storyFile = file.replace(/\.tsx?$/, '.stories.tsx')
          return require('fs').existsSync(storyFile)
        })
        
        if (!storiesExist) {
          throw new Error('All components must have corresponding .stories.tsx files')
        }
        
        return 'echo "✅ All components have stories"'
      },
      
      // Test Coverage Check
      `vitest related ${componentFiles.join(' ')} --run --coverage`,
    ]
  },
}
```

## Hook-Bypass und Notfälle

### Temporärer Hook-Bypass

```bash
# Alle Hooks überspringen (Notfall)
git commit -m "emergency: critical fix" --no-verify
git push --no-verify

# Nur Pre-Commit überspringen
HUSKY=0 git commit -m "wip: work in progress"

# Nur Commit-Message Validation überspringen
git commit -m "quick fix" --no-verify
```

### Hook-Debugging

```bash
# Husky-Debug aktivieren
HUSKY_DEBUG=1 git commit -m "test commit"

# Einzelnen Hook manuell testen
.husky/pre-commit

# Hook-Execution verfolgen
set -x  # Am Anfang des Hook-Scripts
```

### Hook-Deaktivierung

```bash
# Husky komplett deaktivieren
git config core.hooksPath ""

# Husky wieder aktivieren
npx husky install
```

## Troubleshooting

### Häufige Probleme

#### "Command not found" Errors

```bash
# Problem: npx/npm nicht gefunden
# Lösung: PATH in Hook-Script setzen
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# PATH erweitern
export PATH="$PATH:/usr/local/bin:$HOME/.npm-global/bin"

# Oder absolute Pfade verwenden
/usr/local/bin/npx lint-staged
```

#### Windows-Kompatibilität

```bash
# .husky/pre-commit für Windows
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Windows-spezifische PATH-Behandlung
if [ -n "$WINDIR" ]; then
  export PATH="$PATH:/c/Program Files/nodejs"
fi

npx lint-staged
```

#### Performance-Probleme

```javascript
// .lintstagedrc.js - Performance-Optimierung
module.exports = {
  // Parallel Processing begrenzen
  '*.{ts,tsx}': {
    commands: [
      'eslint --fix --max-warnings 0',
      'prettier --write',
    ],
    parallel: 2, // Nur 2 parallel
  },
  
  // Große Dateien ausschließen
  '*.{ts,tsx}': (filenames) => {
    const smallFiles = filenames.filter(f => {
      const stats = require('fs').statSync(f)
      return stats.size < 100000 // < 100KB
    })
    
    return [
      `eslint --fix ${smallFiles.join(' ')}`,
      `prettier --write ${smallFiles.join(' ')}`,
    ]
  },
}
```

### Hook-Performance Monitoring

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Performance-Tracking
start_time=$(date +%s)

echo "🚀 Starting pre-commit hooks..."

# Hook-Operationen...
npx lint-staged

end_time=$(date +%s)
execution_time=$((end_time - start_time))

echo "⏱️  Pre-commit completed in ${execution_time}s"

# Warnung bei langsamen Hooks
if [ $execution_time -gt 30 ]; then
  echo "⚠️  Hook execution took longer than 30s"
  echo "Consider optimizing hook performance"
fi
```

## Best Practices

### Do's ✅

- **Schnelle Hooks**: Hooks sollten unter 30 Sekunden dauern
- **Klare Fehlermeldungen**: Hilfreiche Ausgaben bei Fehlern
- **Inkrementelle Checks**: Nur geänderte Dateien prüfen
- **Bypass-Option**: Notfall-Bypass dokumentieren
- **Performance-Monitoring**: Hook-Zeiten überwachen

### Don'ts ❌

- **Langsame Operationen**: Keine kompletten Builds in Pre-Commit
- **Externe Abhängigkeiten**: Keine Netzwerk-Calls in Hooks
- **Zu strenge Regeln**: Entwicklung nicht blockieren
- **Unklare Errors**: Kryptische Fehlermeldungen vermeiden
- **Hook-Ketten**: Zu komplexe Hook-Abhängigkeiten

---

**Letzte Aktualisierung**: 2024-12-10  
**Version**: 1.0.0  
**Maintainer**: Terra Nature Development Team