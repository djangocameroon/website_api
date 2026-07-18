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
    APP_HOME=/app \
    GUNICORN_WORKERS=4 \
    GUNICORN_THREADS=2 \
    GUNICORN_TIMEOUT=120 \
    GUNICORN_MODULE=website_api.wsgi:application

WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

COPY . $APP_HOME/

RUN mkdir -p $APP_HOME/static $APP_HOME/media $APP_HOME/logs $APP_HOME/staticfiles

COPY docker/entrypoints/web.sh /entrypoint.sh
COPY docker/scripts/wait-for-services.sh /wait-for-services.sh
RUN chmod +x /entrypoint.sh /wait-for-services.sh

RUN groupadd -r django && useradd -r -g django -d $APP_HOME -s /sbin/nologin django \
    && chown -R django:django $APP_HOME
USER django

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health/?format=json || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn"]
