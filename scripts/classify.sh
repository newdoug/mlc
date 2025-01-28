#!/usr/bin/env bash

if [ "$DEBUG" = "1" ]; then
  set -x
fi

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
"$SCRIPTDIR/run_mlc_module.sh" "models.classify" "$@" || exit 1
