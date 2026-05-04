FROM python:3.12-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development tools
RUN pip install --no-cache-dir ruff mypy pytest pytest-cov httpx

# Copy application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]