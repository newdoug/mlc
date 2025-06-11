#!/usr/bin/env bash

[ "$DEBUG" = "1" ] && set -x

DEFAULT_DB_PORT=5432

if ! command -v psql >/dev/null 2>&1; then
  printf "Please install psql first\\n" >&2
  printf "E.g.: 'apt install -y postgresql'\\n" >&2
  exit 1
fi

DB_CONFIG="$1"
# shellcheck disable=SC1090
if [ -z "${DB_CONFIG}" ] || ! source "${DB_CONFIG}" > /dev/null; then
  printf "Failed to source DB config file '%s'\\n" "${DB_CONFIG}" >&2
  printf "Usage: %s DB_CONFIG_FILE\\n" "$0" >&2
  exit 1
fi

if [ -z "${DB_USER}" ] || [ -z "${DB_PASS}" ] || [ -z "${DB_NAME}" ]; then
  printf "DB_CONFIG_FILE '%s' must contain definitions for DB_USER and DB_PASS environment variables\\n" "${DB_CONFIG}" >&2
  exit 1
fi

if [ -z "${DB_PORT}" ]; then
  printf "Warning: no DB_PORT in DB_CONFIG_FILE found: default value '%d' will be used\\n" "${DEFAULT_DB_PORT}"
  # The usual default for postgresql
  DB_PORT="${DEFAULT_DB_PORT}"
fi


SQLFILE="$(mktemp --suffix='.sql')"
# shellcheck disable=SC2064
trap "rm -f '$SQLFILE'" EXIT

cat <<EOF >"$SQLFILE"
-- Create a user and database
CREATE USER "${DB_USER}" WITH PASSWORD '${DB_PASS}';
CREATE DATABASE "${DB_NAME}" OWNER "${DB_USER}";
GRANT ALL PRIVILEGES ON DATABASE "${DB_NAME}" TO "${DB_USER}";
EOF

# Make sure postgres user can read it
sudo chown postgres:postgres "$SQLFILE"
sudo chmod 700 "$SQLFILE"

# Initial database setup
sudo -u postgres psql -U postgres -f "$SQLFILE"
# Truncate before we open permissions to try to delete
echo | sudo -u postgres tee "$SQLFILE"
sudo chmod 777 "$SQLFILE"
# Change back
sudo chown "$USER:$USER" "$SQLFILE"
printf "Successfully created DB '%s' and user '%s'. Remember to give these as configuration to any applications that will need to connect to this DB\\n" "${DB_NAME}" "${DB_USER}"
