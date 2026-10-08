# Egg Distribution Management System

Status: **Phase 1 of 10** (setup, database, login, base screens, Docker).

## Run it

1. Install Docker Desktop.
2. In this folder:
   ```
   cp .env.example .env
   ```
   Open `.env` and change the three CHANGE_ME values.
3. Start everything:
   ```
   docker compose up --build
   ```
4. Open `http://localhost:5173` and log in with `FIRST_ADMIN_EMAIL` / `FIRST_ADMIN_PASSWORD` from `.env`.
5. API docs: `http://localhost:8000/docs`

**On your Android phone** (same Wi-Fi as the PC): open `http://<PC-IP-address>:5173`.

## Run the backend tests
```
docker compose exec backend pip install pytest httpx   # only if not already installed
docker compose exec backend python -m pytest -q
```
Tests use a temporary in-memory database, so they never touch your real data.

## Check the frontend types
```
docker compose exec frontend npm run typecheck
```

## What exists in Phase 1
- `POST /api/v1/auth/login`, `GET /api/v1/auth/me`, `GET /api/v1/settings`, `GET /api/v1/health`
- Tables: `users`, `settings` (migration `0001`)
- Login screen, desktop sidebar, phone bottom bar, placeholder pages for every module

See `docs/assumptions.md` for decisions and `docs/ARCHITECTURE.md` for the full plan.
