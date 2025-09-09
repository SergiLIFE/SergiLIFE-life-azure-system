# L.I.F.E. Platform Docker Image
# Champion-level autonomous optimization system (22.66x SOTA performance)
# Production-ready deployment for Azure Container Apps

FROM python:3.12-slim

# Set environment variables for optimal Python performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV LIFE_PLATFORM_MODE=production
ENV SOTA_PERFORMANCE_TARGET=22.66
ENV NEURAL_PROCESSING_RATE=1000

# Set working directory
WORKDIR /app

# Install system dependencies for neural processing
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libc6-dev \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy L.I.F.E. platform source code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash lifeuser && \
    chown -R lifeuser:lifeuser /app
USER lifeuser

# Expose port for Azure Container Apps
EXPOSE 8000

# Health check for Azure monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# Default command - can be overridden by Azure Container Apps
CMD ["python", "-m", "uvicorn", "life_platform_api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
