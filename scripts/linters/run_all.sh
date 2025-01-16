#!/usr/bin/env bash

if [ "$DEBUG" = "1" ]; then
  set -x
fi

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
LINT_SCRIPTS=(
  run_pylint.sh
  run_shellcheck.sh
)

ALL_PASSED=1
NUM_SCRIPTS=0
FAILED_SCRIPTS=()

for LINT_SCRIPT in "${LINT_SCRIPTS[@]}"; do
  LINT_SCRIPT="$SCRIPTDIR/${LINT_SCRIPT}"
  NUM_SCRIPTS=$((NUM_SCRIPTS+1))
  if ! "${LINT_SCRIPT}"; then
    ALL_PASSED=0
    FAILED_SCRIPTS+=("${LINT_SCRIPT}")
  fi
done

if [ "${ALL_PASSED}" = "1" ]; then
  printf "All %d lint scripts succeeded\\n" "${NUM_SCRIPTS}"
  exit 0
fi

printf "%d lint scripts failed\\n" "${#FAILED_SCRIPTS[@]}"
for FAILED_SCRIPT in "${FAILED_SCRIPTS[@]}"; do
  printf "\t%s\n" "${FAILED_SCRIPT}"
done
exit 1
