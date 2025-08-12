# Git-Workflow für Terra Nature v2.4

## Übersicht

Dieses Dokument beschreibt erweiterte Git-Befehle und Szenarien für die effektive Zusammenarbeit im Terra Nature v2.4 Projekt.

## Inhaltsverzeichnis

1. [Grundlegende Workflow-Einrichtung](#grundlegende-workflow-einrichtung)
2. [Feature-Entwicklung](#feature-entwicklung)
3. [Code-Review Prozess](#code-review-prozess)
4. [Hotfix-Workflow](#hotfix-workflow)
5. [Release-Management](#release-management)
6. [Erweiterte Git-Befehle](#erweiterte-git-befehle)
7. [Konfliktlösung](#konfliktlösung)
8. [Git-Hooks und Automatisierung](#git-hooks-und-automatisierung)

## Grundlegende Workflow-Einrichtung

### Repository-Setup

```bash
# Repository klonen
git clone https://github.com/Terra-Nature-powered-by-terraloft/terra-nature-v2.4.git
cd terra-nature-v2.4

# Development-Branch als Standard setzen
git checkout develop
git branch --set-upstream-to=origin/develop develop

# Git-Konfiguration für das Projekt
git config user.name "Ihr Name"
git config user.email "ihre.email@domain.de"

# Hilfreiches Alias für commit mit conventional format
git config alias.cz '!npx cz'
```

### Branch-Konfiguration

```bash
# Feature-Branch Prefixes definieren
git config --local feature.prefix "feature/"
git config --local bugfix.prefix "fix/"
git config --local hotfix.prefix "hotfix/"

# Auto-Setup für Remote-Tracking
git config --local push.autoSetupRemote true
```

## Feature-Entwicklung

### Standard Feature-Workflow

```bash
# 1. Aktuellen develop-Branch holen
git checkout develop
git pull origin develop

# 2. Feature-Branch erstellen
git checkout -b feature/energy-nft-integration

# 3. Entwicklung mit atomic commits
git add src/components/NFTMinter.tsx
git commit -m "feat(nft): add basic NFT minter component

- Implement energy-to-NFT conversion interface
- Add form validation for energy inputs
- Include CO2 calculation display"

# 4. Regelmäßige Updates vom develop-Branch
git fetch origin develop
git rebase origin/develop

# 5. Feature-Branch pushen
git push origin feature/energy-nft-integration

# 6. Pull Request erstellen (über GitHub UI)
# 7. Nach Review: Branch löschen
git checkout develop
git pull origin develop
git branch -d feature/energy-nft-integration
```

### Interactive Rebase für Clean History

```bash
# Letzte 3 Commits interaktiv bearbeiten
git rebase -i HEAD~3

# In der Rebase-Datei:
# pick abc1234 feat(nft): add NFT component  
# squash def5678 fix typo in component
# squash ghi9012 update documentation

# Commit-Message für squashed commits bearbeiten
# Resultat: Ein sauberer Commit statt drei
```

### Stashing für Unterbrechungen

```bash
# Aktuellen Arbeitsstand temporär sichern
git stash push -m "WIP: NFT integration half done"

# Dringenden Bugfix bearbeiten
git checkout develop
git checkout -b fix/websocket-timeout
# ... Bugfix implementieren ...
git add . && git commit -m "fix(ws): resolve timeout in energy monitoring"

# Zurück zur Feature-Entwicklung
git checkout feature/energy-nft-integration
git stash pop

# Stash-Liste verwalten
git stash list
git stash show stash@{0}
git stash drop stash@{0}
```

## Code-Review Prozess

### Pull Request Vorbereitung

```bash
# 1. Selbst-Review durchführen
git diff develop...feature/energy-nft-integration

# 2. Tests sicherstellen
npm run test
npm run lint
npm run type-check

# 3. Interaktives Staging für Partial Commits
git add -p src/components/EnergyChart.tsx
# Auswahl: y(es), n(o), s(plit), e(dit)

# 4. Commit-Messages überprüfen
git log --oneline develop..HEAD
```

### Review-Feedback Integration

```bash
# Reviewer-Kommentare als fixup commits
git add src/components/NFTMinter.tsx
git commit --fixup abc1234  # abc1234 = ursprünglicher Commit

# Alle fixup commits automatisch squashen
git rebase -i --autosquash develop

# Force-Push mit Sicherheit
git push origin feature/energy-nft-integration --force-with-lease
```

### Draft Pull Requests

```bash
# Work-in-Progress als Draft markieren
gh pr create --draft --title "WIP: Energy NFT Integration" \
  --body "Noch in Entwicklung - Feedback willkommen"

# Draft in Ready for Review ändern
gh pr ready 123
```

## Hotfix-Workflow

### Kritische Bugs in Production

```bash
# 1. Hotfix-Branch von main erstellen
git checkout main
git pull origin main
git checkout -b hotfix/critical-websocket-memory-leak

# 2. Problem isolieren und fixen
git add tools/ws_demo_server.py
git commit -m "fix(ws): resolve memory leak in WebSocket connections

- Clear intervals on connection close
- Add connection timeout handling
- Prevent accumulation of dead connections

Fixes #456"

# 3. Hotfix testen
npm run test
npm run test:py

# 4. In main und develop mergen
git checkout main
git merge --no-ff hotfix/critical-websocket-memory-leak
git tag -a v2.4.1 -m "Hotfix: WebSocket memory leak"
git push origin main --tags

git checkout develop
git merge --no-ff hotfix/critical-websocket-memory-leak
git push origin develop

# 5. Hotfix-Branch löschen
git branch -d hotfix/critical-websocket-memory-leak
git push origin --delete hotfix/critical-websocket-memory-leak
```

## Release-Management

### Release-Branch Workflow

```bash
# 1. Release-Branch erstellen
git checkout develop
git pull origin develop
git checkout -b release/v2.4.0

# 2. Version-Bump und Metadaten
npm version minor --no-git-tag-version
git add package.json package-lock.json
git commit -m "chore(release): bump version to 2.4.0"

# 3. Release Notes vorbereiten
git log --oneline v2.3.0..HEAD > CHANGELOG-v2.4.0.md

# 4. Final Testing
npm run build
npm run test:all
npm run storybook:build

# 5. Release finalisieren
git checkout main
git merge --no-ff release/v2.4.0
git tag -a v2.4.0 -m "Release v2.4.0: Energy NFT Integration"

git checkout develop  
git merge --no-ff release/v2.4.0

# 6. Deploy und cleanup
git push origin main develop --tags
git branch -d release/v2.4.0
```

### Semantic Versioning

```bash
# Major Release (Breaking Changes)
npm version major    # 2.4.0 -> 3.0.0

# Minor Release (New Features)  
npm version minor    # 2.4.0 -> 2.5.0

# Patch Release (Bug Fixes)
npm version patch    # 2.4.0 -> 2.4.1

# Pre-Release Versionen
npm version prerelease --preid=beta  # 2.4.0 -> 2.4.1-beta.0
```

## Erweiterte Git-Befehle

### Commit-History Analyse

```bash
# Commits pro Autor
git shortlog -sn --since="2024-01-01"

# Dateien mit den meisten Änderungen
git log --name-only --pretty=format: | sort | uniq -c | sort -nr

# Commit-Aktivität Timeline
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --since="2 weeks ago"

# Zeige alle Commits die eine Datei geändert haben
git log --follow -p -- src/components/EnergyChart.tsx

# Finde Commit der einen Bug eingeführt hat
git bisect start
git bisect bad HEAD
git bisect good v2.3.0
# Git führt durch binäre Suche...
```

### Cherry-Picking und Backports

```bash
# Einzelnen Commit in anderen Branch übernehmen
git cherry-pick abc1234

# Mehrere Commits übernehmen
git cherry-pick abc1234^..def5678

# Cherry-pick mit Edit-Option
git cherry-pick -e abc1234

# Backport zu älteren Release-Branch
git checkout release/v2.3-maintenance
git cherry-pick -x abc1234  # -x fügt "cherry picked from" hinzu
```

### Worktree für parallele Entwicklung

```bash
# Separates Arbeitsverzeichnis für Hotfix
git worktree add ../terra-nature-hotfix main
cd ../terra-nature-hotfix
# ... Hotfix implementieren ...
cd ../terra-nature-v2.4

# Worktrees verwalten
git worktree list
git worktree remove ../terra-nature-hotfix
```

## Konfliktlösung

### Merge-Konflikte lösen

```bash
# Bei Merge-Konflikt
git status  # Zeigt konfliktbehaftete Dateien

# Konflikt manuell lösen
code src/components/EnergyChart.tsx  # In Editor öffnen

# Nach Lösung:
git add src/components/EnergyChart.tsx
git commit  # Automatische Merge-Commit Message

# Alternative: Merge Tool verwenden
git mergetool
```

### Rebase-Konflikte

```bash
# Während interaktivem Rebase
git rebase --continue  # Nach Konfliktlösung fortfahren
git rebase --abort     # Rebase abbrechen
git rebase --skip      # Aktuellen Commit überspringen

# Konflikte vermeiden mit Merge-Strategie
git rebase -X theirs develop    # Bei Konflikten: deren Version nehmen
git rebase -X ours develop      # Bei Konflikten: unsere Version nehmen
```

### Reflog für Wiederherstellung

```bash
# Alle Git-Operationen anzeigen
git reflog

# Verlorene Commits wiederherstellen
git checkout abc1234  # Hash aus reflog
git branch recovery-branch

# Reflog für bestimmten Branch
git reflog show feature/energy-nft-integration

# Reset rückgängig machen
git reset --hard HEAD@{5}  # Zustand von vor 5 Operationen
```

## Git-Hooks und Automatisierung

### Husky-Setup Validierung

```bash
# Pre-commit Hook testen
git add .
git commit -m "test: trigger pre-commit hook"
# Sollte Linting und Formatierung ausführen

# Commit-msg Hook testen  
git commit -m "invalid commit message"
# Sollte bei ungültiger Conventional Commit Syntax fehlschlagen

# Hook-Bypass für Notfälle (vorsichtig verwenden!)
git commit -m "emergency fix" --no-verify
```

### Custom Hooks

```bash
# .husky/pre-push Hook hinzufügen
cat > .husky/pre-push << 'EOF'
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Verhindere versehentliches Pushen zu main
protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ $protected_branch = $current_branch ]; then
    echo "Direktes Pushen zu main ist nicht erlaubt. Verwende Pull Requests."
    exit 1
fi
EOF

chmod +x .husky/pre-push
```

### Automatische Changelog-Generierung

```bash
# Conventional Changelog installieren
npm install -D conventional-changelog-cli

# Package.json Script hinzufügen
"scripts": {
  "changelog": "conventional-changelog -p angular -i CHANGELOG.md -s -r 0"
}

# Changelog generieren
npm run changelog
```

## Branch-Schutz und Policies

### GitHub Branch Protection Setup

```bash
# Via GitHub CLI
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci/build","ci/test"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":2}' \
  --field restrictions=null
```

### Git Attributs für Repository

```bash
# .gitattributes erstellen
cat > .gitattributes << 'EOF'
# Line ending normalization
* text=auto

# Language detection
*.ts linguist-language=TypeScript
*.tsx linguist-language=TypeScript

# Binary files
*.png binary
*.jpg binary
*.ico binary

# Export ignore (für git archive)
.gitignore export-ignore
.gitattributes export-ignore
*.md export-ignore
tests/ export-ignore
EOF
```

## Troubleshooting

### Häufige Git-Probleme

```bash
# "Detached HEAD" State reparieren
git checkout -b temp-branch
git checkout develop
git merge temp-branch

# Große Dateien aus History entfernen
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/large/file' \
  --prune-empty --tag-name-filter cat -- --all

# Remote-Tracking reparieren
git branch --set-upstream-to=origin/develop develop

# Staging Area zurücksetzen
git reset HEAD src/components/  # Spezifische Dateien
git reset HEAD                  # Alle staged Änderungen

# Letzte Commits rückgängig machen
git reset --soft HEAD~1   # Änderungen bleiben staged
git reset --mixed HEAD~1  # Änderungen bleiben im Working Directory
git reset --hard HEAD~1   # Änderungen werden verworfen (VORSICHT!)
```

### Performance-Optimierung

```bash
# Repository Cleanup
git gc --aggressive --prune=now

# Große Repository analysieren
git count-objects -vH

# Unreferenzierte Objekte löschen
git reflog expire --expire=now --all
git gc --prune=now

# Shallow Clone für CI/CD
git clone --depth 1 https://github.com/Terra-Nature-powered-by-terraloft/terra-nature-v2.4.git
```

## Best Practices Zusammenfassung

### Do's ✅

- Regelmäßig kleine, atomare Commits
- Aussagekräftige Commit-Messages mit Conventional Commits
- Feature-Branches für jede neue Funktionalität
- Code-Review für alle Änderungen
- Tests vor jedem Push ausführen
- Rebase verwenden für saubere History

### Don'ts ❌

- Direkt auf main/develop pushen
- Force-Push ohne --force-with-lease
- Merge-Commits in Feature-Branches
- Große binäre Dateien committen
- Secrets in Git-History
- Commit-Messages wie "fix", "wip", "test"

---

**Letzte Aktualisierung**: 2024-12-10  
**Version**: 1.0.0  
**Autor**: Terra Nature Development Team