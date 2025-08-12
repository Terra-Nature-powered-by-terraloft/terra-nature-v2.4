# Git-Workflow v2.1

## Start-Flow
- Verwende `git switch -c <branch>` statt `git checkout -b`.

## Range-Reverts
- Sicheres Pattern: `git revert --no-commit <ältester>^..<neuester> && git commit -m "revert: <range>"`.

## Pull-Policy
- Standard: `git config pull.rebase true`.
- Alternative: `git config pull.ff only`.

## Force-with-lease
- `git push --force-with-lease` **nie** auf `main` oder `release/*`.
- Setze Branch-Protection-Regeln.

## Merge-Strategie
- `git merge --no-ff` verpflichtend für Merges in `main`.

## Backports
- Verwende `git cherry-pick -x <a>^..<b>`.
- Konfliktlösung mit `-X theirs` nur im Ausnahmefall.

## Recovery
- Reflog-Sicherheitsnetz: z.B. `git reset --hard HEAD@{1}`.

## PR-Checkliste
- Siehe [A11y](Guidelines.de_Version2.1.md#a11y) und [Tests](Guidelines.de_Version2.1.md#tests).
