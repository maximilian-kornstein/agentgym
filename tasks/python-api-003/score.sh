#!/usr/bin/env bash
set -euo pipefail

TASK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$TASK_DIR"

if [[ ! -x "repo/.venv/bin/python" ]]; then
  echo "Missing virtual environment. Run ./setup.sh first." >&2
  exit 2
fi

echo "Running public tests..."
repo/.venv/bin/python -m pytest tests

echo "Running hidden tests..."
repo/.venv/bin/python -m pytest hidden_tests

echo "Score: pass"
