#!/usr/bin/env bash

if [ "$DEBUG" = "1" ]; then
  set -x
fi

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
DST="$1"
if [ -z "$DST" ]; then
  DST="$SCRIPTDIR"
else
  if [ ! -d "$DST" ]; then
    printf "Input path wasn't a directory: '%s'\\n" "$DST" >&2
    exit 1
  fi
fi


find_pylint_cmd() {
  readonly CMD_OPTIONS=(
    pylint
    pylint3
  )
  for CMD_OPTION in "${CMD_OPTIONS[@]}"; do
    if command -v "${CMD_OPTION}" >/dev/null 2>&1; then
      printf "%s\\n" "${CMD_OPTION}"
      return 0
    fi
  done
  return 1
}

PYLINT_CMD="$(find_pylint_cmd)"
ALL_PASSED=1
NUM_FILES=0
FAILED_FILENAMES=()

while read -r FILENAME; do
  if ! "${PYLINT_CMD}" "$FILENAME"; then
    FAILED_FILENAMES+=("$FILENAME")
    ALL_PASSED=0
  fi
  NUM_FILES=$((NUM_FILES+1))
done <<< "$(find "$DST" -type f -iname "*.py")"

if [ "${ALL_PASSED}" = "1" ]; then
  printf "All %d files passed '%s'\\n" "${NUM_FILES}" "${PYLINT_CMD}"
  exit 0
fi

printf "%d files failed lint check\\n" "${#FAILED_FILENAMES[@]}"
for FAILED_FILENAME in "${FAILED_FILENAMES[@]}"; do
  printf "\t%s\n" "${FAILED_FILENAME}"
done
exit 1
