## Books API (FastAPI + SQLModel)

Asynchronous FastAPI service for managing books with user authentication, JWT-based access/refresh tokens, and role-protected endpoints. Uses SQLModel with PostgreSQL, Alembic for migrations, and Redis for token blocklisting.

### Features
- User signup/login with hashed passwords and JWT access/refresh tokens (PyJWT, Passlib).
- Role enforcement via dependencies, plus logout with Redis JTI blocklist.
- Book CRUD endpoints; each book is linked to a user (`user_uid`).
- Async data layer powered by SQLModel + PostgreSQL (`asyncpg`).

### Tech Stack
- FastAPI (+ Starlette utilities) with async endpoints.
- SQLModel over PostgreSQL; Alembic for schema migrations.
- Redis for token revocation; Pydantic for validation/settings.
- Python 3.10+.

### Getting Started
1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
2. **Configure environment**
   - Copy `src/.env` and adjust values:
     - `DATABASE_URL=postgresql+asyncpg://<user>:<pass>@localhost:5432/<db>`
     - `JWT_SECRET_KEY`, `ALGORITHM`, `REFRESH_TOKRN_EXPIRE_DAYS`
     - `REDIS_HOST`, `REDIS_PORT`
   - Ensure PostgreSQL database and Redis are running.
3. **Run migrations**
   ```bash
   alembic upgrade head
   ```
   (Uses the existing `alembic.ini` and `mirgrations/` setup.)
4. **Start the API**
   ```bash
   uvicorn src:app --reload
   ```
   - Docs: `http://localhost:8000/docs`
   - Books routes are under `/api/v1.0.0/books`
   - Auth routes are under `/api/v1.0.0/auth`

### API Notes
- **Auth**: `POST /api/v1.0.0/auth/signup`, `POST /api/v1.0.0/auth/login`, `GET /api/v1.0.0/auth/refresh-token`, `POST /api/v1.0.0/auth/logout`, `GET /api/v1.0.0/auth/me`.
- **Books**: `GET /api/v1.0.0/books/`, `POST /api/v1.0.0/books/`, `GET /api/v1.0.0/books/{book_id}`, `PATCH /api/v1.0.0/books/{book_id}`, `DELETE /api/v1.0.0/books/{book_id}`, `GET /api/v1.0.0/books/user/{user_id}`.
- Include `Authorization: Bearer <access_token>` for protected routes; created books return the owning `user_uid`.

### Development Tips
- Database models live in `src/books/models.py` and `src/auth/models.py`.
- Dependency-injected async sessions come from `src/db/main.py#get_session`.
- Lifespan initialization in `src/__init__.py` calls `init_db()` to create tables when the app starts.
