#!/usr/bin/env bash
set -euo pipefail
REPO='https://github.com/xioxii/V2demo.git'
BRANCH='main'
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
command -v git >/dev/null || { echo 'ERROR: git tidak dijumpai.' >&2; exit 1; }
if [ ! -d .git ]; then
  git init
  git remote add origin "$REPO"
else
  git remote set-url origin "$REPO"
fi
git fetch origin "$BRANCH" || true
if git show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
  git checkout -B "$BRANCH" "origin/$BRANCH"
else
  git checkout -B "$BRANCH"
fi
git add -A
git commit -m 'Import MT6890 Phase 1 target device source' || echo 'Tiada perubahan baru untuk commit.'
git push -u origin "$BRANCH"
echo 'DONE: pushed to xioxii/V2demo'
