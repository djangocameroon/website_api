#!/bin/bash
set -e

echo "[celery] Waiting for external services..."
/wait-for-services.sh

CONCURRENCY=${CELERY_CONCURRENCY:-2}
LOG_LEVEL=${CELERY_LOG_LEVEL:-info}
QUEUES=${CELERY_QUEUES:-celery}
MAX_TASKS_PER_CHILD=${CELERY_MAX_TASKS_PER_CHILD:-100}

echo "[celery] Starting worker (concurrency=$CONCURRENCY, queues=$QUEUES)..."
exec celery -A website_api worker \
    --loglevel="$LOG_LEVEL" \
    --concurrency="$CONCURRENCY" \
    --queues="$QUEUES" \
    --max-tasks-per-child="$MAX_TASKS_PER_CHILD" \
    --without-heartbeat \
    --without-mingle \
    --without-gossip
