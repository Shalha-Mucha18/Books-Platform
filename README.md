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

## Project Structure (high level)
- `src/__init__.py`: FastAPI app, lifespan, router registration.
- `src/auth/`: auth routes, JWT utilities, dependencies.
- `src/books/`: book routes/services/schemas.
- `src/reviews/`: review routes/services/schemas.
- `src/db/`: SQLModel models and session management.
- `mirgrations/`: Alembic migration env.

## Setup
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
