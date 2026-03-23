#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$HERE/install_skills.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found; install Python 3." >&2
  exit 1
fi

exec python3 "$PY" "$@"
