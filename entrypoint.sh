#!/bin/sh
set -e

# Додаємо PYTHONPATH
export PYTHONPATH=/app:$PYTHONPATH

echo "🔄 Running Alembic migrations..."
cd /app && alembic upgrade head

echo "🚀 Starting Gunicorn..."
exec gunicorn app.main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
