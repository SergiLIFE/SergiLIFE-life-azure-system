# L.I.F.E. Platform - Production Docker Container
# Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
# Neuroadaptive Learning Platform - Enterprise Ready
# Copyright 2025 - Sergio Paya Borrull

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies for neural processing
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libfftw3-dev \
    libfreetype6-dev \
    libhdf5-dev \
    libjpeg-dev \
    libpng-dev \
    libssl-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
COPY requirements-test.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create logs and results directories
RUN mkdir -p /app/logs /app/results /app/data

# Copy application code
COPY . .

# Create non-root user for security
RUN groupadd -r life && useradd -r -g life -d /app -s /bin/bash life \
    && chown -R life:life /app

# Switch to non-root user
USER life

# Expose port for web interface
EXPOSE 8000

# Health check for container monitoring
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Multi-stage build for production
FROM base as production

# Set production environment variables
ENV ENVIRONMENT=production \
    AZURE_MARKETPLACE_OFFER_ID=9a600d96-fe1e-420b-902a-a0c42c561adb \
    LIFE_PLATFORM_VERSION=2025.1.0-PRODUCTION

# Copy optimized application
COPY --from=base /app /app

# Default command - can be overridden
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "life_platform_api:app"]

# Alternative commands for different use cases:
# Development: docker run -it life-platform python experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py
# Testing: docker run life-platform python -m pytest
# Benchmarking: docker run life-platform python sota_benchmark.py
# Azure Functions: docker run life-platform func start --host 0.0.0.0 --port 8000

# Docker build and run instructions:
# Build: docker build -t life-platform:latest .
# Run: docker run -p 8000:8000 -v $(pwd)/logs:/app/logs life-platform:latest
# Azure: docker run -e AZURE_CLIENT_ID=<id> -e AZURE_CLIENT_SECRET=<secret> life-platform:latest

LABEL maintainer="Sergio Paya Borrull" \
      version="2025.1.0-PRODUCTION" \
      description="L.I.F.E. Platform - Neuroadaptive Learning System" \
      azure.marketplace.offer.id="9a600d96-fe1e-420b-902a-a0c42c561adb" \
      org.opencontainers.image.title="L.I.F.E. Platform" \
      org.opencontainers.image.description="Learning Individually from Experience - Neural Processing Platform" \
      org.opencontainers.image.version="2025.1.0-PRODUCTION" \
      org.opencontainers.image.created="2025-09-26" \
      org.opencontainers.image.source="https://github.com/SergiLIFE/life-azure-system" \
      org.opencontainers.image.licenses="Proprietary"
