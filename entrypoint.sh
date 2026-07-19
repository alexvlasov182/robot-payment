#!/bin/sh
set -e

echo "🔄 Running Alembic migrations..."
alembic upgrade head 2>/dev/null || alembic stamp head

echo "🚀 Starting Gunicorn..."
exec gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000