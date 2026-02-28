#!/bin/bash
set -e
celery -A website_api inspect ping --timeout 10 > /dev/null 2>&1
