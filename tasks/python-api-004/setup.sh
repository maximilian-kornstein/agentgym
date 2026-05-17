#!/usr/bin/env bash
set -euo pipefail

TASK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$TASK_DIR/repo"

VENV_ROOT="${TMPDIR:-/tmp}/agentgym-venvs"
VENV_PATH="$VENV_ROOT/python-api-004"

mkdir -p "$VENV_ROOT"
rm -rf "$VENV_PATH"
python3 -m venv "$VENV_PATH"
rm -f .venv
ln -s "$VENV_PATH" .venv

.venv/bin/python -m pip install --upgrade pip >/dev/null
.venv/bin/python -m pip install -e . pytest >/dev/null

echo "Setup complete for python-api-004."
