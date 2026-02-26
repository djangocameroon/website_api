# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    APP_HOME=/app

# Set work directory
WORKDIR $APP_HOME

# Install system dependencies and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock /app/

# Install Python dependencies using uv
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache -r pyproject.toml

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    POSTGRES_DB=${DB_NAME} \
    POSTGRES_USER=${DB_USER} \
    POSTGRES_PASSWORD=${DB_PASSWORD}

# Copy project files 
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/logs

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD pg_isready -U ${DB_USER:-postgres} -h ${DB_HOST:-localhost}

# Expose port
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]