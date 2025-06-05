#!/usr/bin/env bash

[ "$DEBUG" = "1" ] && set -x

# TODO: take INSTALL_DIR as argument for where to put the downloaded ES.
# TODO: automatically set up ES user and systemd service

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"
TOML_FILE="$(readlink -f "$SCRIPTDIR/../../pyproject.toml")"

DESTDIR="$1"
if [ -z "$DESTDIR" ]; then
  printf "Usage: %s <DESTDIR>\\n" "$0" >&2
  exit 1
fi
mkdir -p "$DESTDIR" >/dev/null || exit 1

if [ ! -f "${TOML_FILE}" ]; then
  printf "TOML file doesn't exist where we expected it to ('%s')\\n" "${TOML_FILE}" >&2
  exit 1
fi

# Get the version that python code will use, try to match it
VERS="$(grep "elasticsearch\s*=\s*\".*\"$" "${TOML_FILE}" | grep -o "[0-9]*\.[0-9]*\.[0-9]*")"
if [ -z "$VERS" ]; then
  printf "Failed to parse version out of TOML file '%s'\\n" "${TOML_FILE}" >&2
  exit 1
fi

BASE="elasticsearch-$VERS"
DIRNAME="$BASE"
ES_FILE_TGZ="$BASE-linux-x86_64.tar.gz"
ES_FILE_SHA="${ES_FILE_TGZ}.sha512"
TGZ_URL="https://artifacts.elastic.co/downloads/elasticsearch/${ES_FILE_TGZ}"
SHAURL="${TGZ_URL}.sha512"

if ! TMPDIR="$(mktemp -d)"; then
  printf "Failed to make a temp dir\\n" >&2
  exit 1
fi

_cleanup() {
  [ -n "$TMPDIR" ] && [ -e "$TMPDIR" ] && rm -r "$TMPDIR"
}

# Sub-shell so we don't have to worry by getting by to original dir
(
  cd "$TMPDIR" || exit 1

  if ! wget "${TGZ_URL}" >/dev/null || [ ! -f "${ES_FILE_TGZ}" ]; then
    printf "Failed to download Elasticsearch TGZ '%s' from URL '%s'\\n" "${ES_FILE_TGZ}" "${TGZ_URL}" >&2
    _cleanup
    exit 1
  fi
  if ! wget "$SHAURL" >/dev/null || [ ! -f "${ES_FILE_SHA}" ]; then
    printf "Failed to download Elasticsearch TGZ SHA file '%s' from URL '%s'\\n" "${ES_FILE_SHA}" "$SHAURL" >&2
    _cleanup
    exit 1
  fi
  if ! sha512sum -c "${ES_FILE_SHA}" >/dev/null; then
    printf "WARNING: sha512 file '%s' didn't match actual sha512 of download\\n" "${ES_FILE_SHA}" >&2
  else
    printf "SHA512 verified!\\n"
  fi

  if ! tar -xzf "${ES_FILE_TGZ}" >/dev/null; then
    printf "Downloaded Elasticsearch package file from URL '%s' wasn't in expected format?\\n" "${TGZ_URL}" >&2
    _cleanup
    exit 1
  fi
  if [ "$DEBUG" = "1" ]; then
    ls -lrt
    pwd
  fi

  if ! mv "$DIRNAME"/* "$DESTDIR"; then
    printf "Failed to move downloaded elasticsearch contents to dir '%s'\\n" "$DESTDIR" >&2
    _cleanup
    exit 1
  fi
  printf "Downloaded Elasticsearch successfully into directory '%s'\\n" "$DESTDIR"
)
_cleanup
