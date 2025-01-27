#!/usr/bin/env bash

set -e

if [ "$DEBUG" = "1" ]; then
  set -x
fi

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
TESTDIR="$SCRIPTDIR"
SRCDIR="$(readlink -f "$SCRIPTDIR/../src")"
# cd "$SCRIPTDIR/.."

PYTHONPATH="$PYTHONPATH:$SRCDIR" python3 -m unittest "$@"
