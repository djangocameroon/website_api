FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache -r pyproject.toml

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOME=/app

WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

COPY . $APP_HOME/

RUN mkdir -p $APP_HOME/logs

COPY docker/entrypoints/beat.sh /entrypoint.sh
COPY docker/scripts/wait-for-services.sh /wait-for-services.sh
COPY docker/scripts/healthcheck-beat.sh /healthcheck.sh
RUN chmod +x /entrypoint.sh /wait-for-services.sh /healthcheck.sh

RUN groupadd -r celery && useradd -r -g celery -d $APP_HOME -s /sbin/nologin celery \
    && chown -R celery:celery $APP_HOME
USER celery

HEALTHCHECK --interval=30s --timeout=15s --start-period=30s --retries=3 \
    CMD /healthcheck.sh

ENTRYPOINT ["/entrypoint.sh"]
