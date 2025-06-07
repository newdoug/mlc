#!/usr/bin/env bash

if [ "$DEBUG" = "1" ]; then
  set -x
fi

DST="$1"
if [ -z "$DST" ]; then
  printf "No destination dir entered, using current dir by default\\n"
  DST="$(pwd)"
else
  if [ ! -d "$DST" ]; then
    printf "Input path wasn't a directory: '%s'\\n" "$DST" >&2
    exit 1
  fi
fi

SHELLCHECK_CMD="shellcheck"
# Boolean
ALL_PASSED=1
# Integer
NUM_FILES=0
FAILED_FILENAMES=()

while read -r FILENAME; do
  if ! "${SHELLCHECK_CMD}" "$FILENAME"; then
    FAILED_FILENAMES+=("$FILENAME")
    ALL_PASSED=0
  fi
  NUM_FILES=$((NUM_FILES+1))
done <<< "$(find "$DST" -type f -iname "*.sh")"

if [ "${ALL_PASSED}" = "1" ]; then
  printf "All %d files passed '%s'\\n" "${NUM_FILES}" "${SHELLCHECK_CMD}"
  exit 0
fi

printf "%d out of %d files failed lint check:\\n" "${#FAILED_FILENAMES[@]}" "${NUM_FILES}"
for FAILED_FILENAME in "${FAILED_FILENAMES[@]}"; do
  printf "\t%s\n" "${FAILED_FILENAME}"
done
exit 1
