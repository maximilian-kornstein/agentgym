#!/usr/bin/env bash
set -euo pipefail

TASK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$TASK_DIR"

if [ ! -x repo/.venv/bin/python ]; then
  echo "Virtualenv not found. Run ./setup.sh first." >&2
  exit 2
fi

rm -f .venv
ln -s repo/.venv .venv

echo "Running public tests..."
.venv/bin/python -m pytest tests

echo "Running hidden tests..."
.venv/bin/python -m pytest hidden_tests
