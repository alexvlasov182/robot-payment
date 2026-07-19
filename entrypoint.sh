#!/bin/sh
set -e

# Завантажуємо змінні з .env, якщо файл існує
if [ -f ".env" ]; then
  export $(cat .env | grep -v '^#' | xargs)
fi

# Перевіряємо, чи задана DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
  echo "❌ ERROR: DATABASE_URL is not set!"
  exit 1
fi

echo "🔄 Running Alembic migrations..."
python -m alembic upgrade head

echo "🚀 Starting Gunicorn..."
exec gunicorn app.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -