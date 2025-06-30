# shellcheck disable=SC2034,SC2148
# This is just an example containing possible fields. You should change these to be your own values and ensure the
# credentials are safely stored somewhere (not in the repo) and with appropriate ACLs.
# This file is expected to be sourced by the postgres database setup script. That script will then write these values
# to a YAML file containing the same information that is meant for the Python code.
export DB_NAME=mlc_data
export DB_USER=user
export DB_PASS=password
