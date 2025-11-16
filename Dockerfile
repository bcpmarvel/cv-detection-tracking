FROM python:3.12-slim AS base

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

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

RUN uv sync --no-dev --frozen

RUN mkdir -p models

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health')" || exit 1

CMD ["uv", "run", "uvicorn", "sentinel.api.app:app", "--host", "0.0.0.0", "--port", "8000"]


FROM base AS dev

RUN uv sync --frozen

CMD ["uv", "run", "uvicorn", "sentinel.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
