#!/bin/bash
set -e

echo "[web] Waiting for external services..."
/wait-for-services.sh

echo "[web] Running database migrations..."
python manage.py migrate --noinput

echo "[web] Collecting static files..."
python manage.py collectstatic --noinput

# Optional: create superuser from env vars (only when explicitly requested)
if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "[web] Creating superuser if not exists..."
    python manage.py shell <<END
from django.contrib.auth import get_user_model
import os
User = get_user_model()
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@djangocameroon.com")
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password, username=username)
    print(f"Superuser {email} created.")
else:
    print(f"Superuser {email} already exists.")
END
fi

# Gunicorn configuration via environment variables
WORKERS=${GUNICORN_WORKERS:-4}
THREADS=${GUNICORN_THREADS:-2}
TIMEOUT=${GUNICORN_TIMEOUT:-120}
GRACEFUL_TIMEOUT=${GUNICORN_GRACEFUL_TIMEOUT:-30}
KEEP_ALIVE=${GUNICORN_KEEP_ALIVE:-5}
MAX_REQUESTS=${GUNICORN_MAX_REQUESTS:-1000}
MAX_REQUESTS_JITTER=${GUNICORN_MAX_REQUESTS_JITTER:-50}
BIND=${GUNICORN_BIND:-0.0.0.0:8000}
LOG_LEVEL=${GUNICORN_LOG_LEVEL:-info}

echo "[web] Starting Gunicorn (workers=$WORKERS, threads=$THREADS)..."
exec gunicorn website_api.wsgi:application \
    --bind "$BIND" \
    --workers "$WORKERS" \
    --threads "$THREADS" \
    --worker-class gthread \
    --timeout "$TIMEOUT" \
    --graceful-timeout "$GRACEFUL_TIMEOUT" \
    --keep-alive "$KEEP_ALIVE" \
    --max-requests "$MAX_REQUESTS" \
    --max-requests-jitter "$MAX_REQUESTS_JITTER" \
    --log-level "$LOG_LEVEL" \
    --access-logfile - \
    --error-logfile -
