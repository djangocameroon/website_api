#!/bin/sh
set -e

RETRIES=${WAIT_RETRIES:-30}
INTERVAL=${WAIT_INTERVAL:-2}

if [ -z "$REDIS_HOST" ]; then
    REDIS_URL_TO_PARSE="${REDIS_URL:-$CELERY_BROKER_URL}"
    if [ -n "$REDIS_URL_TO_PARSE" ]; then
        REDIS_HOST=$(python3 -c "
from urllib.parse import urlparse
u = urlparse('$REDIS_URL_TO_PARSE')
print(u.hostname or 'localhost')
")
        REDIS_PORT=$(python3 -c "
from urllib.parse import urlparse
u = urlparse('$REDIS_URL_TO_PARSE')
print(u.port or 6379)
")
    else
        REDIS_HOST="localhost"
        REDIS_PORT="6379"
    fi
fi
REDIS_PORT=${REDIS_PORT:-6379}

PG_HOST=${DB_HOST:-localhost}
PG_PORT=${DB_PORT:-5432}

wait_for() {
    SERVICE=$1
    HOST=$2
    PORT=$3
    attempt=0

    echo "  Waiting for $SERVICE at $HOST:$PORT ..."
    while [ $attempt -lt "$RETRIES" ]; do
        if python3 -c "
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
    s.connect(('$HOST', $PORT))
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
"; then
            echo "  $SERVICE is ready."
            return 0
        fi
        attempt=$((attempt + 1))
        echo "  $SERVICE not ready (attempt $attempt/$RETRIES) — retrying in ${INTERVAL}s..."
        sleep "$INTERVAL"
    done

    echo "  ERROR: $SERVICE at $HOST:$PORT did not become ready after $RETRIES attempts."
    exit 1
}

wait_for "PostgreSQL" "$PG_HOST" "$PG_PORT"
wait_for "Redis"      "$REDIS_HOST" "$REDIS_PORT"

echo "All services are ready."
