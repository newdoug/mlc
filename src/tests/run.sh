#!/usr/bin/env bash

set -e

if [ "$DEBUG" = "1" ]; then
  set -x
fi

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
cd "$SCRIPTDIR/.."

python3 -m unittest "$@"
