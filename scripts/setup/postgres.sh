#!/usr/bin/env bash

[ "$DEBUG" = "1" ] && set -x

if ! command -v psql >/dev/null 2>&1; then
  printf "Please install psql first\\n" >&2
  printf "E.g.: 'apt install -y postgresql'\\n" >&2
  exit 1
fi

DB_NAME="$1"
DB_USER="$2"
DB_PASS="$3"
if [ -z "${DB_PORT}" ]; then
  # The usual default for postgresql
  DB_PORT=5432
fi


SQLFILE="$(mktemp --suffix='.sql')"
trap "rm -f '$SQLFILE'" EXIT

cat <<'EOF' >"$SQLFILE"
# Create a user and database
CREATE USER '${DB_USER}' WITH PASSWORD '${DB_PASS}';
CREATE DATABASE '${DB_NAME}' OWNER '${DB_USER}';
GRANT ALL PRIVILEGES ON DATABASE '${DB_NAME}' TO '${DB_USER}';
EOF

printf "SQLFILE: '%s'\\n" "$SQLFILE"
cat "$SQLFILE"

# Initial database setup
sudo su -U postgres psql -U postgres -f "$SQLFILE" "${DB_NAME}"
