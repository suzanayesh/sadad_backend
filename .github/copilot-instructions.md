## Quick context for AI coding agents

- Project type: Django (5.x) API backed by Django REST Framework. Main code lives under `apps/` and the active settings module is `config.settings` (see `manage.py`).
- Database: PostgreSQL. Connection settings are hard-coded in `config/settings.py` (NAME: `sadad_db25`, USER: `postgres`, PASSWORD present in file). Treat these as local-dev only.

## Big-picture architecture

- Single Django monolith with small purpose-built apps: `apps.root_users`, `apps.admin_info`, `apps.creditors`, `apps.debts`, `apps.payments`, `apps.calculations`, `apps.admin_users`.
- Each app follows the typical Django app layout (models, views, migrations). Models explicitly set `Meta.db_table` (snake_case table names matching app names).
- REST endpoints are mounted under `config/urls.py` at `path("api/", include("apps.root_users.urls"))`. Note: there is a second `sadad_backend/urls.py` that includes `root_users.urls` without the `apps.` prefix and contains an inline Arabic comment — prefer `config/` as the canonical settings/urls used by `manage.py`.
- Data flow example: Creditor -> Debt (FK) -> Payment (FK), Calculation is OneToOne with Debt. Admin approvals link to `RootUser` via `approved_by_root`.

## Project-specific conventions and patterns

- Tables: every Model sets `Meta.db_table` to the explicit table name (e.g. `db_table = "debts"`). When creating or referencing tables, follow this naming.
- Apps are small and often scaffolded; many `views.py` files are placeholders. Implementations that exist use DRF generic views (example: `apps/root_users/views.py` uses `generics.CreateAPIView`).
- Passwords: the `RootUser` model stores a `password_hash` field. Serializers call `make_password` in `create()` — follow this pattern when creating or updating root/admin passwords (see `apps/root_users/serializers.py`).
- API patterns: use DRF serializers and generics where present. Responses may return raw strings (see CreateRootUserView returns a success string) rather than JSON objects — keep consistency with local files when adding endpoints.

## Integration points & gotchas

- Settings: `manage.py` uses `config.settings`. Edit or read configuration from `config/settings.py`. There is another settings file at `sadad_backend/settings.py` but it is not used by `manage.py`.
- Database credentials and SECRET_KEY are checked in repo files — these are development placeholders. Don't commit real secrets; treat them as local-only and prefer environment variables if adding configuration.
- URL mounting: `config/urls.py` includes `apps.root_users.urls` at `/api/`. Adding new apps should follow the `apps.` dotted path convention.

## Useful concrete examples (copy-paste friendly)

- Run dev server (from repo root):

  python manage.py runserver

- Make migrations and apply (local dev):

  python manage.py makemigrations
  python manage.py migrate

- Example API: create a root user

  POST /api/createrootuser/
  Content-Type: application/json
  Body: { "username": "alice", "password_hash": "plain-text-password" }

  Note: serializer will hash `password_hash` before saving (see `apps/root_users/serializers.py`).

## Where to look when changing the data model

- Model table names: `apps/*/models.py` (each file sets `Meta.db_table`). Update migrations after changing models.
- Migration history: `apps/*/migrations/` contains generated migration files — follow these when reasoning about schema changes.

## Tests & developer workflows

- There are no tests implemented yet (many `tests.py` files contain placeholders). Use `python manage.py test` to run tests if added.
- Pipenv is used (`Pipfile` exists) and requires Python 3.13 in the Pipfile. Local dev typically uses a virtualenv or pipenv; repository does not include Docker files.

## Safety & style notes for AI changes

- Respect existing naming: DB tables are explicitly defined; do not change table names without also generating migrations.
- Preserve existing response styles for endpoints you modify (e.g., string messages vs JSON) unless an API-wide change is requested.
- Avoid committing secrets. If you add config changes, prefer reading values from environment variables and document the change.

## Quick file references (start here)

- Entrypoint: `manage.py` (points to `config.settings`)
- Active settings: `config/settings.py`
- URL router: `config/urls.py`
- Example app + API: `apps/root_users/{models.py,serializers.py,views.py,urls.py}`
- Data models: `apps/{creditors,debts,payments,calculations,admin_info}`

If any section is unclear or you'd like more examples (e.g., how to add a new endpoint, how to run with a local Postgres container), tell me which area to expand and I'll iterate.
