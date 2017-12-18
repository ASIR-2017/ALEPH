#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER dca with password 'dca';
    CREATE DATABASE museo;
    GRANT ALL PRIVILEGES ON DATABASE museo TO dca;
EOSQL
