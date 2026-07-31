# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Django REST Framework API backing the Django Cameroon website (blog, events, subscriptions, users). Python 3.12+, managed with `uv`.

## Working Guidelines

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## Commands

Setup:
```bash
uv venv
cp .env.example .env   # fill in DB/Redis/etc credentials
make migrate
mkdir -p static
```

Run (Django dev server + Celery worker + Celery beat, backgrounded via PID files in `.pids/`, logs in `logs/`):
```bash
make start   # HOST=localhost PORT=8912 by default
make stop
```

To run just the Django dev server directly (e.g. for foreground debugging):
```bash
uv run python manage.py runserver localhost:8912
```

Migrations:
```bash
make migrations   # makemigrations
make migrate      # migrate
```

Tests (Django test runner, not pytest):
```bash
uv run python manage.py test                              # all tests
uv run python manage.py test apps.events                  # one app
uv run python manage.py test apps.events.test.test_views   # one module
uv run python manage.py test apps.events.test.test_views.EventViewSetTests.test_list  # one test
```

Lint/format (flake8 config in `.flake8`: max-line-length 120, ignores F401/F403/F405/W503; isort config in `.isort.cfg`: black profile, line_length 120):
```bash
uv run flake8
uv run black .
uv run isort .
```

API docs are served at `/redoc/` (drf-spectacular) when the server is running.

**Query the graph before grepping. Refresh it after editing.**

If `graphify-out/graph.json` exists (local-only, session-scoped — it's gitignored and not shared across clones):
- Before searching the codebase (finding symbols, callers, file locations), query it: `graphify query graphify-out/graph.json <name>`. Prefer this over Glob/Grep for structural lookups.
- After editing files, if you'll query the graph again this session, refresh it: `graphify update graphify-out/graph.json <files...>` or `graphify auto-update`.
- If the graph looks stale or a query comes up empty for something you expect to exist, fall back to Grep/Glob rather than trusting stale results.

## Architecture

**Django apps** live under `apps/` (`users`, `events`, `blog`, `subs`), each following the same internal layout: `models/`, `serializers/`, `views/`, `routes/` (URL routing split into `api.py` for the router-based CRUD endpoints and sometimes `extra.py` for extra non-router routes), `permissions.py`, `signals.py`/`signals/`, `tasks.py` (Celery tasks), `test/`. `apps/subs` is simpler and keeps `models.py`/`serializers.py`/`views.py` as flat files instead of packages.

Root URLconf is `website_api/routes/main.py`, which mounts each app's `routes/api.py` (and `routes/extra.py` where present) under `api/v1/`, plus `/health/`, `/admin/`, `/__debug__/`, Prometheus metrics, and Swagger/Redoc (`website_api/routes/swagger.py`).

Settings are split under `website_api/settings/`: `base.py` (Django core config, DB, i18n, middleware assembly), `apps.py` (`INSTALLED_APPS`/`MIDDLEWARE` lists and CORS config), `extra.py` (DRF/drf-spectacular config, Unfold admin theme, S3/Whitenoise static & media storage switch based on `DEBUG`, Redis cache, Celery beat schedule, debug toolbar), `celery.py` (Celery app bootstrap). `manage.py` and `celery.py` both point at `website_api.settings` as the settings package.

**Shared cross-app infrastructure** (top-level packages, not part of any single Django app):
- `mixins/api_response_mixin.py` — `APIResponseMixin` standardizes all API responses (`success()`, `error()`, `paginated_response()` with a consistent `{status, message, data, ...}` envelope and pagination metadata). Nearly every viewset mixes this in alongside DRF's `ModelViewSet`.
- `exceptions/rest_exception.py` — `rest_exception_handler`, wired as `REST_FRAMEWORK["EXCEPTION_HANDLER"]`, normalizes all DRF/Django exceptions (404, permission, validation, throttling, etc.) into the same response envelope as `APIResponseMixin`, including flattening nested serializer error dicts into a flat error list.
- `middlewares/` — custom middleware (e.g. `translator.py`).
- `services/` — cross-cutting integrations: email (`mail_service.py`), SMS/Twilio (`sms_service.py`), calendar (`calendar_service.py`), notifications (`notification_service.py`, `notification_preferences.py`).
- `utils/` — `auth.py` (custom auth backend `EmailOrUsernameBackend`, registered in `AUTHENTICATION_BACKENDS`), `main.py` (helpers used by settings, e.g. `load_documentation` for the Spectacular description and `add_tag_groups` postprocessing hook), `uploads/`.

**View conventions**: viewsets extend `ModelViewSet, APIResponseMixin`; permissions are usually set dynamically via `get_permissions()` based on `self.action`; every endpoint is documented with drf-spectacular's `@extend_schema` (summary, operation_id, description, responses, tags); list endpoints return via `self.paginated_response(...)`, others via `self.success(...)`/`self.error(...)`. Auth uses OAuth2 (`django-oauth-toolkit`) as the default DRF authentication class.

**Async work**: Celery (`website_api/settings/celery.py` bootstraps the app, tasks live in each app's `tasks.py`), with `django-celery-beat` for the DB-backed schedule plus a hardcoded `CELERY_BEAT_SCHEDULE` in `settings/extra.py` for event reminders/digests. Broker/result backend is Redis (`REDIS_URL`, falls back to `CELERY_BROKER_URL`).

**Storage**: static files always served via Whitenoise; media files are local in `DEBUG=True`, S3-compatible storage (`django-storages`) when `DEBUG=False`, configured via `AWS_*` env vars in `settings/extra.py`.

**Deployment**: Dockerfiles per process type under `docker/` (`web.Dockerfile`, `celery.Dockerfile`, `beat.Dockerfile`), with `entrypoints/` and `scripts/`. Monitoring stack (Prometheus/Grafana) config under `monitoring/`.

## Keeping this file current

If a change alters commands, architecture, or file layout described above, update the relevant section of this file in the same change. Don't rewrite it for routine code changes that don't affect what's documented here.
