#!/bin/bash
set -e

echo "[beat] Waiting for external services..."
/wait-for-services.sh

echo "[beat] Starting Celery beat scheduler..."
exec celery -A website_api beat \
    --loglevel="${CELERY_LOG_LEVEL:-info}" \
    --scheduler django_celery_beat.schedulers:DatabaseScheduler
