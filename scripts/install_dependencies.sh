#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root relative to this script so pip can always find requirements.txt
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$repo_root"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
