#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error
set -x   # print what we are doing

cd /app/

set

python models.py --drop
psql -U $DATABASE_USER -h $DATABASE_HOST $DATABASE_NAME < /deploy/db/dump.sql
