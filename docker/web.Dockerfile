# ============================================================
# Web Dockerfile — fully self-contained, zero-downtime ready
# ============================================================
# Build:  docker build -f docker/web.Dockerfile -t web .
# Run:    docker run --env-file .env -p 8000:8000 web
# ============================================================

# ---------- Stage 1: builder ----------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files and install into a venv
COPY pyproject.toml uv.lock ./
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache -r pyproject.toml

# ---------- Stage 2: runtime ----------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOME=/app

WORKDIR $APP_HOME

# Runtime-only system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . $APP_HOME/

# Create necessary directories
RUN mkdir -p $APP_HOME/static $APP_HOME/media $APP_HOME/logs $APP_HOME/staticfiles

# Copy entrypoint & scripts, make executable
COPY docker/entrypoints/web.sh /entrypoint.sh
COPY docker/scripts/wait-for-services.sh /wait-for-services.sh
RUN chmod +x /entrypoint.sh /wait-for-services.sh

# Non-root user
RUN groupadd -r django && useradd -r -g django -d $APP_HOME -s /sbin/nologin django \
    && chown -R django:django $APP_HOME
USER django

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health/?format=json || exit 1

ENTRYPOINT ["/entrypoint.sh"]
