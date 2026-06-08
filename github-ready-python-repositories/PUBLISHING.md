# Publishing These Repositories

Three polished Python repositories are ready locally:

- `signal-scout`: CSV data-quality profiler with Markdown reports
- `workflow-weaver`: dependency-aware workflow runner with retries
- `receipt-radar`: private expense analyzer and anomaly detector

This environment could not publish them directly because `git`, `gh`, and `winget` are not available on PATH, and the connected GitHub app currently has no writable repositories installed.

## Option A: GitHub CLI

After installing Git and GitHub CLI, run:

```powershell
cd C:\Users\bnall\Documents\Codex\2026-06-07\make-my-github-cleaner-make-repositories\outputs\signal-scout
git init
git add .
git commit -m "Initial polished Python project"
gh repo create signal-scout --public --source . --remote origin --push

cd ..\workflow-weaver
git init
git add .
git commit -m "Initial polished Python project"
gh repo create workflow-weaver --public --source . --remote origin --push

cd ..\receipt-radar
git init
git add .
git commit -m "Initial polished Python project"
gh repo create receipt-radar --public --source . --remote origin --push
```

## Option B: Existing Empty GitHub Repos

If you create empty repositories on GitHub first, use:

```powershell
cd C:\Users\bnall\Documents\Codex\2026-06-07\make-my-github-cleaner-make-repositories\outputs\signal-scout
git init
git add .
git commit -m "Initial polished Python project"
git branch -M main
git remote add origin https://github.com/BhuvaneshN09/signal-scout.git
git push -u origin main
```

Repeat with `workflow-weaver` and `receipt-radar`.

## Suggested Profile Pins

Pin these in this order:

1. `signal-scout`
2. `workflow-weaver`
3. `receipt-radar`

Together they show CLI design, data handling, packaging, tests, CI, algorithms, and clear documentation.
