#!/bin/bash
set -e
# Beat has no worker to answer `celery inspect ping`, so just confirm a
# celery beat process is still running. Scans /proc instead of assuming
# PID 1, in case the container runtime wraps the entrypoint with an init.
python3 -c "
import os
for pid in os.listdir('/proc'):
    if not pid.isdigit():
        continue
    try:
        with open(f'/proc/{pid}/cmdline', 'rb') as f:
            cmdline = f.read()
    except OSError:
        continue
    if b'beat' in cmdline:
        raise SystemExit(0)
raise SystemExit(1)
"
