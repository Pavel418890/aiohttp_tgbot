cat config/heroku_config.yaml | envsubst > config/config.yaml

export PYTHONPATH=.

alembic upgrade head

python3 main.py

exec "$@"