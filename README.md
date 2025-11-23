<div align="center">
  <h1>Books Platform</h1>
  <p>
    <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/SQLModel-4B8BBE?logo=python&logoColor=white" alt="SQLModel" />
    <img src="https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white" alt="Redis" />
    <img src="https://img.shields.io/badge/Alembic-E07A5F?logo=alembic&logoColor=white" alt="Alembic" />
    <img src="https://img.shields.io/badge/Pydantic-4B8BBE?logo=pydantic&logoColor=white" alt="Pydantic" />
    <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  </p>
</div>

An asynchronous FastAPI service for managing books with user authentication, JWT-based access/refresh tokens, and role-protected endpoints. Built for reliability (typed SQLModel models, async DB sessions), security (hashed passwords, JWT with Redis blocklist), and operability (Alembic migrations, structured logging).

## Overview
- **Backend**: FastAPI with async SQLModel + PostgreSQL; Alembic migrations ensure schema parity across environments; Redis backs token blacklisting and cache-friendly lookups.
- **Auth**: Email/password signup + login with hashed credentials; short-lived access tokens and longer refresh tokens; role claims (`user`, `admin`) are injected into dependency guards for RBAC.
- **Data model**: Users own Books; Books can have Reviews; timestamps and ownership fields baked into models for auditing.
- **Ops & DX**: Project wired for `.env` configuration, typed services, and consistent router patterns; ready-made logging commands for demos; Next.js frontend consumes the same versioned API paths used in docs.

**Project impact**
- Demonstrates a production-style FastAPI stack: layered architecture (routers/services/models), async DB access, and JWT/role-based auth.
- Shows how to integrate Redis for token revocation and PostgreSQL for relational data with clean migrations.
- Ready for interviews/demos with clear API docs, logging, and reproducible setup.

**Use cases**
- Personal or team book catalog with per-user ownership and role-restricted admin actions.
- Starter template for any CRUD + auth FastAPI service needing JWT, refresh tokens, and RBAC.
- Reference implementation for async SQLModel patterns with PostgreSQL and Alembic migrations.

## Features
- Secure auth: hashed passwords, JWT access/refresh tokens, Redis-backed token revocation.
- Role-based access control for protected routes.
- Book CRUD with per-user ownership, timestamps, and review support.
- Async data layer with SQLModel + PostgreSQL (`asyncpg`) and Alembic migrations.
- Ready-to-run OpenAPI/Swagger UI for fast onboarding and demos.
- Next.js 14 marketing site that consumes the Books API, with curated fallback data for demos.
- Dedicated `/dashboard` operations view highlighting live catalog metrics, tables, and activity feeds.

## Project Structure (high level)
- `src/__init__.py`: FastAPI app, lifespan, router registration.
- `src/auth/`: auth routes, JWT utilities, dependencies.
- `src/books/`: book routes/services/schemas.
- `src/reviews/`: review routes/services/schemas.
- `src/db/`: SQLModel models and session management.
- `mirgrations/`: Alembic migration env.
- `frontend/`: Next.js 14 App Router workspace (marketing + dashboard).

## Backend Setup
1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
2. **Configure environment**
   - Copy or create `src/.env` and set:
     - `DATABASE_URL=postgresql+asyncpg://<user>:<pass>@localhost:5432/<db>`
     - `JWT_SECRET_KEY`, `ALGORITHM`, `REFRESH_TOKRN_EXPIRE_DAYS`
     - `REDIS_HOST`, `REDIS_PORT`
   - Ensure PostgreSQL and Redis are running.
3. **Run migrations**
   ```bash
   alembic upgrade head
   ```
4. **Start the API**
   ```bash
   uvicorn src:app --reload
   ```
   - Docs: `http://localhost:8000/docs`
   - Books: `/api/v1.0.0/books`
   - Auth: `/api/v1.0.0/auth`

## Frontend (Next.js 14 + React 18)
1. **Install Node modules**
   ```bash
   cd frontend
   npm install
   ```
2. **Create `frontend/.env.local`**
   ```ini
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1.0.0
   # Optional – short-lived JWT access token for SSR previews
   NEXT_PUBLIC_API_ACCESS_TOKEN=<your_access_token>
   ```
   The UI automatically falls back to curated demo data when the API/token is unavailable and surfaces an alert.
3. **Run the Next.js dev server**
   ```bash
   npm run dev
   ```
   - Marketing site: `http://localhost:3000`
   - Operations dashboard: `http://localhost:3000/dashboard`
4. **Production build preview**
   ```bash
   npm run build
   npm run start
   ```

### Run both services together
```bash
# Terminal 1 – FastAPI backend
source .venv/bin/activate
uvicorn src:app --reload

# Terminal 2 – Next.js frontend
cd frontend
npm run dev
```
Keep `NEXT_PUBLIC_API_BASE_URL`/`NEXT_PUBLIC_API_ACCESS_TOKEN` in sync with the backend host and freshly issued JWT tokens to see live catalog data (otherwise the UI shows the demo collection).

## Logging
- Enable structured app logs via Uvicorn:
  ```bash
  uvicorn src:app --reload --log-level info
  ```
- Include SQL echo for debugging (optional):
  ```bash
  SQLALCHEMY_SILENCE_UBER_WARNING=1 DATABASE_URL=... uvicorn src:app --reload --log-level debug --env-file src/.env
  ```
- FastAPI/Starlette request logs and error traces will appear in the console; pipe to a file for interviews/demos:
  ```bash
  uvicorn src:app --log-level info 2>&1 | tee api.log
  ```

## API Surface (quick ref)
- **Auth**: `POST /api/v1.0.0/auth/signup`, `POST /api/v1.0.0/auth/login`, `GET /api/v1.0.0/auth/refresh-token`, `POST /api/v1.0.0/auth/logout`, `GET /api/v1.0.0/auth/me`
- **Books**: `GET /api/v1.0.0/books/`, `POST /api/v1.0.0/books/`, `GET /api/v1.0.0/books/{book_id}`, `PATCH /api/v1.0.0/books/{book_id}`, `DELETE /api/v1.0.0/books/{book_id}`, `GET /api/v1.0.0/books/user/{user_id}`
- **Reviews**: `POST /api/v1.0.0/reviews/book/{book_uid}`
- Protected routes require `Authorization: Bearer <access_token>`.

## Development Notes
- Async DB sessions are injected via `src/db/main.py#get_session`.
- SQLModel entities (User, Book, Review) live in `src/db/models.py`.
- Lifespan startup calls `init_db()` to ensure tables exist before serving requests.
