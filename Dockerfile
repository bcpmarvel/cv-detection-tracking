# Multi-stage build for minimal production image
FROM python:3.12-slim AS base

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files and source (needed for package build)
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

# Install dependencies (no dev)
RUN uv sync --no-dev --frozen

# Create models directory
RUN mkdir -p models

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health')" || exit 1

# Run API server
CMD ["uv", "run", "uvicorn", "sentinel.api.app:app", "--host", "0.0.0.0", "--port", "8000"]


# Development stage with dev dependencies
FROM base AS dev

# Install dev dependencies
RUN uv sync --frozen

# Override entrypoint for development
CMD ["uv", "run", "uvicorn", "sentinel.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
