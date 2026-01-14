SHELL := /bin/bash

UV ?= uv run
PY ?= $(UV) python
CELERY ?= $(UV) celery

HOST ?= 127.0.0.1
PORT ?= 8912
RUNSERVER ?= $(HOST):$(PORT)

PID_DIR ?= .pids
LOG_DIR ?= logs

WEB_PID := $(PID_DIR)/web.pid
WORKER_PID := $(PID_DIR)/celery_worker.pid
BEAT_PID := $(PID_DIR)/celery_beat.pid

.DEFAULT_GOAL := help
.PHONY: help start stop migrations migrate _start_web _start_worker _start_beat

## Show this help (scraped from comments above targets)
help:
	@awk 'BEGIN {FS=":"} /^##/ {sub(/^##[ ]?/, ""); help=$$0; next} /^[a-zA-Z0-9_\-]+:/ {target=$$1; if (help != "") {printf "%-15s %s\n", target, help; help=""}}' $(MAKEFILE_LIST)

## Start Django + Celery worker + Celery beat (background)
start:
	@mkdir -p $(PID_DIR) $(LOG_DIR)
	@$(MAKE) _start_web _start_worker _start_beat

## Stop Django + Celery worker + Celery beat
stop:
	@bash -lc 'set -e; \
		stop_one() { \
			name="$$1"; pidfile="$$2"; \
			if [[ -f "$$pidfile" ]]; then \
				pid=$$(cat "$$pidfile" || true); \
				if [[ -n "$$pid" ]] && kill -0 "$$pid" 2>/dev/null; then \
					echo "Stopping $$name (pid $$pid)"; \
					kill "$$pid" || true; \
					for i in {1..20}; do kill -0 "$$pid" 2>/dev/null || break; sleep 0.2; done; \
					kill -9 "$$pid" 2>/dev/null || true; \
				else \
					echo "$$name not running"; \
				fi; \
				rm -f "$$pidfile"; \
			else \
				echo "$$name pidfile not found"; \
			fi; \
		}; \
		stop_one "celery_beat" "$(BEAT_PID)"; \
		stop_one "celery_worker" "$(WORKER_PID)"; \
		stop_one "web" "$(WEB_PID)";'

## Create new Django migrations
migrations:
	@$(PY) manage.py makemigrations

## Apply Django migrations
migrate:
	@$(PY) manage.py migrate

## Internal: start Django dev server
_start_web:
	@bash -lc 'set -e; \
		if [[ -f "$(WEB_PID)" ]] && kill -0 "$$(cat "$(WEB_PID)")" 2>/dev/null; then \
			echo "web already running (pid $$(cat "$(WEB_PID)"))"; \
		else \
			echo "Starting web on $(RUNSERVER)"; \
			nohup $(PY) manage.py runserver $(RUNSERVER) > "$(LOG_DIR)/web.log" 2>&1 & echo $$! > "$(WEB_PID)"; \
			echo "web started (pid $$(cat "$(WEB_PID)"))"; \
		fi'

## Internal: start Celery worker
_start_worker:
	@bash -lc 'set -e; \
		if [[ -f "$(WORKER_PID)" ]] && kill -0 "$$(cat "$(WORKER_PID)")" 2>/dev/null; then \
			echo "celery_worker already running (pid $$(cat "$(WORKER_PID)"))"; \
		else \
			echo "Starting celery worker"; \
			nohup $(CELERY) -A website_api worker --loglevel=info --concurrency=2 > "$(LOG_DIR)/celery_worker.log" 2>&1 & echo $$! > "$(WORKER_PID)"; \
			echo "celery_worker started (pid $$(cat "$(WORKER_PID)"))"; \
		fi'

## Internal: start Celery beat
_start_beat:
	@bash -lc 'set -e; \
		if [[ -f "$(BEAT_PID)" ]] && kill -0 "$$(cat "$(BEAT_PID)")" 2>/dev/null; then \
			echo "celery_beat already running (pid $$(cat "$(BEAT_PID)"))"; \
		else \
			echo "Starting celery beat"; \
			nohup $(CELERY) -A website_api beat --loglevel=info > "$(LOG_DIR)/celery_beat.log" 2>&1 & echo $$! > "$(BEAT_PID)"; \
			echo "celery_beat started (pid $$(cat "$(BEAT_PID)"))"; \
		fi'
