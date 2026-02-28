import time

from django.db import connection
from django.http import JsonResponse


def health_check(request):
    """Lightweight health check that returns JSON.
    Used by the Docker HEALTHCHECK and load-balancer probes.
    """
    checks = {}
    healthy = True

    # Database check
    try:
        start = time.monotonic()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = {
            "status": "ok",
            "latency_ms": round((time.monotonic() - start) * 1000, 2),
        }
    except Exception as exc:
        checks["database"] = {"status": "error", "detail": str(exc)}
        healthy = False

    status_code = 200 if healthy else 503
    return JsonResponse({"status": "healthy" if healthy else "unhealthy", "checks": checks}, status=status_code)
