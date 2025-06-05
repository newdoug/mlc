#!/usr/bin/env bash

[ "$DEBUG" = "1" ] && set -x

# Config things to update. Can be changed by setting them for this script.
# Something to note that confused me for a little bit: username passed to DB is typically 'elastic' while the system
# user that this script makes and sets permissions on and runs the service as is 'elasticsearch'.
# TODO: sort this out properly maybe
DISABLE_SSL=1
if [ -z "${ES_HOST}" ]; then
  ES_HOST="localhost"
fi
if [ -z "${ES_PORT}" ]; then
  ES_PORT="9200"
fi

INSTALLDIR="$1"
CONFIG_FILE="$INSTALLDIR/config/elasticsearch.yml"
AUTOGEN_CONFIG="$INSTALLDIR/auto_config_vars.sh"
PIDFILE="$INSTALLDIR/set_up.pid"
if [ -z "${INSTALLDIR}" ]; then
  printf "Usage: %s <INSTALLDIR>\\n" "$0" >&2
  exit 1
fi
if [ ! -d "${INSTALLDIR}" ]; then
  printf "Install dir '%s' must already exist\\n" "$INSTALLDIR" >&2
  exit 1
fi

if [ "${DISABLE_SSL}" = "1" ]; then
  # TODO: This is dangerous and not very good: do it in python instead or something,
  #       but right now, the only properties that match this pattern are the 2 SSL ones we care about.
  sed -i 's/  enabled: true/  enabled: false/' "${CONFIG_FILE}"
fi
sed -E -i "s/^\#.?\\s*http.port:\\s*.*/http.port: ${ES_PORT}/" "${CONFIG_FILE}"
sed -E -i "s/^\#.?\\s*network.host:\\s*.*/network.host: ${ES_HOST}/" "${CONFIG_FILE}"

# Start elasticsearch in background so we can set other things up like credentials
"$INSTALLDIR/bin/elasticsearch" -d -p "$PIDFILE" || exit 1

# Auto-generate a new password
if ! PW="$(echo y | "$INSTALLDIR/bin/elasticsearch-reset-password" -u elastic -a | grep "^New value: " | grep -o ":\s.*[a-zA-Z0-9_\-\+\=\*].*$" | tr -d ':[:space:]')" || [ -z "$PW" ]; then
  printf "Failed to auto-generate a new password\\n" >&1
  pkill -F "$PIDFILE"
  rm -f "$PIDFILE"
  exit 1
fi

TOKEN="$("$INSTALLDIR/bin/elasticsearch-create-enrollment-token" -s node)"

SERVICE_FILE="/etc/systemd/system/elasticsearch.service"
SERVICE_CONTENTS="[Unit]
Description=Elasticsearch
Documentation=https://www.elastic.co
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=elasticsearch
Group=elasticsearch
ExecStart=$INSTALLDIR/bin/elasticsearch
Restart=on-failure
LimitNOFILE=65536
LimitMEMLOCK=infinity
TimeoutStopSec=20
TimeoutStartSec=60

[Install]
WantedBy=multi-user.target"

# Stop running our process before we start service so it doesn't collide or whatever
pkill -F "$PIDFILE"
rm -f "$PIDFILE"

printf "Creating elasticsearch user\\n"
sudo useradd -r -s /bin/false elasticsearch
# Required because systemd service will run as elasticsearch user and will need exec permissions on binaries in here
sudo chown -R elasticsearch:elasticsearch "$INSTALLDIR"
ls -lrt "$INSTALLDIR"
ls -lrt "$INSTALLDIR/bin/elasticsearch"*
printf "Writing service file for elasticsearch.\\n"
printf "%s" "${SERVICE_CONTENTS}" | sudo tee "${SERVICE_FILE}" >/dev/null
printf "Starting new service"
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
systemctl status elasticsearch

# Not used by anything, just putting stuff here so it's not lost be user
printf "TOKEN=%s\\nUSERNAME=elastic\\nPASSWORD=%s\\nES_HOME=%s" "$TOKEN" "$PW" "$INSTALLDIR" | sudo tee "${AUTOGEN_CONFIG}" >/dev/null
sudo chown elasticsearch:elasticsearch "${AUTOGEN_CONFIG}"
sudo chmod 640 "${AUTOGEN_CONFIG}"

printf "Elasticsearch password auto-generated: '%s'\\n" "$PW"
printf "Use this command to test the elastic server: curl -X GET -k https://localhost:9200 -u 'elastic:%s'\\n" "$PW"
printf "Important information saved to '%s'\\n" "${AUTOGEN_CONFIG}"
