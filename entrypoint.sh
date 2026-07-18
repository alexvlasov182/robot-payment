#!/bin/sh
set -e

if [ -f "alembic.ini" ]; then
  echo "Running Alembic migrations..."
  python -m alembic upgrade head
else
  echo "No alembic.ini found, skipping migrations."
fi

echo "Starting Gunicorn (2 workers, uvicorn worker class)..."
exec gunicorn app.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
