#!/usr/bin/bash

set -e

envsubst < "config/temp.yaml" > "config/config.yaml"

export PYTHONPATH=.

alembic upgrade head

python3 main.py

exec "$@"