#!/usr/bin/env bash

if [ "$DEBUG" = "1" ]; then
  set -x
fi

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
TESTDIR="$(readlink -f "$SCRIPTDIR/../tests")"
TESTSCRIPT="$TESTDIR/run.sh"

"$TESTSCRIPT" "$@"
