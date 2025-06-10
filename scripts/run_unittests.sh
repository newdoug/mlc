#!/usr/bin/env bash

[ "$DEBUG" = "1" ] && set -x

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
TESTDIR="$(readlink -f "$SCRIPTDIR/../tests")"
TESTSCRIPT="$TESTDIR/run.sh"

"$TESTSCRIPT" "$@"
