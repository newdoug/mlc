#!/usr/bin/env bash

set -e

if [ "$DEBUG" = "1" ]; then
  set -x
fi

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
TESTDIR="$SCRIPTDIR"

cd "$TESTDIR/.." || exit 1

# Old (before poetry), but kept for reference in case it's useful
# SRCDIR="$(readlink -f "$SCRIPTDIR/../src")"
# PYTHONPATH="$PYTHONPATH:$SRCDIR" python3 -m pytest "$@"

poetry run pytest
