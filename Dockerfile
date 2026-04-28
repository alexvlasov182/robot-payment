FROM python:3.12-slim
WORKDIR /app

# Install only essential system packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development tools (optional, for quality checks)
RUN pip install --no-cache-dir ruff mypy pytest pytest-cov httpx

COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
