#!/usr/bin/env bash

[ "$DEBUG" = "1" ] && set -x

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
SRCDIR="$(readlink -f "$SCRIPTDIR/../src")"

cd "$SRCDIR" || exit 1
PYMOD="$1"
shift

find_py_command() {
  local CMDS=(
    python3
    python3.10
    python3.9
    python3.8
    python3.7
    python3.6
  )
  for CMD in "${CMDS[@]}"; do
    if command -v "$CMD" >/dev/null 2>&1; then
      printf "%s\\n" "$CMD"
      return 0
    fi
  done
  return 1
}

PYCMD="$(find_py_command)"
if [ -z "$PYCMD" ]; then
  printf "No valid python command found: ensure Python3 is installed\\n" >&2
  exit 1
fi

"$PYCMD" -m "$PYMOD" "$@"
