#!/usr/bin/env bash

if [ "$DEBUG" = "1" ]; then
  set -x
fi

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
SRCDIR="$(readlink -f "$SCRIPTDIR/../src")"

cd "$SRCDIR" || exit 1
python3 -m data_gen "$@"
