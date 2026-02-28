# ============================================================
# Celery Beat Dockerfile — fully self-contained
# ============================================================
# Build:  docker build -f docker/beat.Dockerfile -t celery-beat .
# Run:    docker run --env-file .env celery-beat
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

# Runtime-only: just the Postgres client lib
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . $APP_HOME/

# Create log directory
RUN mkdir -p $APP_HOME/logs

# Copy entrypoint & scripts, make executable
COPY docker/entrypoints/beat.sh /entrypoint.sh
COPY docker/scripts/wait-for-services.sh /wait-for-services.sh
COPY docker/scripts/healthcheck-beat.sh /healthcheck.sh
RUN chmod +x /entrypoint.sh /wait-for-services.sh /healthcheck.sh

# Non-root user
RUN groupadd -r celery && useradd -r -g celery -d $APP_HOME -s /sbin/nologin celery \
    && chown -R celery:celery $APP_HOME
USER celery

HEALTHCHECK --interval=30s --timeout=15s --start-period=30s --retries=3 \
    CMD /healthcheck.sh

ENTRYPOINT ["/entrypoint.sh"]
