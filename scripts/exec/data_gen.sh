#!/usr/bin/env bash

[ "$DEBUG" = "1" ] && set -x

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
"$SCRIPTDIR/run_mlc_module.sh" "mlc.data_gen" "$@"
