# ==============================================================================
# SmartFeed AI - Production Multi-Architecture Dockerfile
# ==============================================================================
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    SMARTFEED_DB_PATH=/app/data/smartfeed.db

# Set working directory
WORKDIR /app

# Install essential system dependencies for OpenCV and pyzbar (QR decoding)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libzbar0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code and assets
COPY . .

# Ensure data directories exist
RUN mkdir -p /app/data /app/data/qr_codes /app/exports

# Expose production port
EXPOSE 8000

# Health check to ensure zero-downtime rolling deployments
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/healthz || exit 1

# Production command using Uvicorn
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT} --workers 2"]
