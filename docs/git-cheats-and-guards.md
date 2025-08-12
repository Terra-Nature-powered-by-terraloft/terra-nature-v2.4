# Git Cheats & Guards

## Top 12
1. `git switch -c <branch>`
2. `git fetch --prune`
3. `git pull --rebase`
4. `git commit -m "msg"`
5. `git cherry-pick -x <commit>`
6. `git revert --no-commit <old>^..<new>`
7. `git merge --no-ff <branch>`
8. `git reset --hard HEAD@{1}`
9. `git reflog`
10. `git stash push -u`
11. `git push --force-with-lease`
12. `git tag -s vX.Y.Z`

## Do / Don't für main
- **Do:** PRs, Reviews, Branch-Protection.
- **Don't:** `git push --force`, direkter Commit.
