#!/usr/bin/env bash

[ "$DEBUG" = "1" ] && set -x

SCRIPTDIR="$(readlink -f "$(dirname "$0")")"

BASE_DIR="/opt"
if [ ! -d "${BASE_DIR}" ]; then
  if ! mkdir -p "${BASE_DIR}" >/dev/null 2>&1; then
    if ! sudo mkdir -p "${BASE_DIR}" >/dev/null 2>&1; then
      printf "Please make directory '%s'\\n" "${BASE_DIR}"
      exit 1
    else
      sudo chmod 755 "${BASE_DIR}"
    fi
  else
    chmod 755 "${BASE_DIR}"
  fi
fi

DESTDIR="${BASE_DIR}/elasticsearch"
OLDDIR="$DESTDIR.old.$(date +%s)"
rm -rf "$OLDDIR" >/dev/null
[ -e "$DESTDIR" ] && mv "$DESTDIR" "$OLDDIR"
sudo mkdir -p "$DESTDIR" >/dev/null
# So we can work more easily within it
sudo chown "$USER:$USER" "$DESTDIR"

if ! "$SCRIPTDIR/download.sh" "$DESTDIR"; then
  rm -r "$DESTDIR" && mv "$OLDDIR" "$DESTDIR"
  exit 1
fi
if ! "$SCRIPTDIR/set_up.sh" "$DESTDIR"; then
  rm -r "$DESTDIR" && mv "$OLDDIR" "$DESTDIR"
  exit 1
fi
sudo rm -rf "$OLDDIR" >/dev/null
