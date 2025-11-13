#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${REPO_ROOT}/src:${PYTHONPATH:-}"
cd "${REPO_ROOT}"

if ! command -v jupyter >/dev/null 2>&1; then
  echo "Error: jupyter command not found. Did you install the requirements?" >&2
  exit 1
fi

NOTEBOOK_DIR="${REPO_ROOT}/notebooks"
mkdir -p "${NOTEBOOK_DIR}"

exec jupyter lab --notebook-dir="${NOTEBOOK_DIR}" "$@"
