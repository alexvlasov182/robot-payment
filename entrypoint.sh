#!/bin/sh
set -e

echo "🔄 Running Alembic migrations..."
alembic upgrade head >/dev/null 2>&1 || alembic stamp head >/dev/null 2>&1

echo "🚀 Starting Gunicorn..."
exec gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
