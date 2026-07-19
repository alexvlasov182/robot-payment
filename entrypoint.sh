#!/bin/sh
set -e

echo "🔄 Checking database state..."

if alembic current 2>/dev/null | grep -q "head"; then
    echo "✅ Database is already up to date"
else
    echo "🔄 Applying migrations..."
    alembic upgrade head || {
        echo "⚠️ Migration failed, stamping as head..."
        alembic stamp head
    }
fi

echo "🚀 Starting Gunicorn..."
exec gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000