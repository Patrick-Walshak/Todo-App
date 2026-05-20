# Todo API

Production-grade MVP Todo API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, and JWT authentication.

## Features

- **Authenticated User System** — register, login, and manage private todos via JWT
- **Guest System** — public, unauthenticated todo creation and listing
- Clean modular architecture with strict separation of concerns
- Alembic migrations for schema versioning
- Docker + Docker Compose for containerised deployment
- Gunicorn + Uvicorn workers for production serving

---

## Project Structure

```
todo-api/
├── app/
│   ├── auth/
│   │   ├── dependencies.py   # JWT bearer extraction, current user resolution
│   │   ├── models.py         # User SQLAlchemy model
│   │   ├── router.py         # /auth/register, /auth/login
│   │   ├── schemas.py        # Pydantic request/response schemas
│   │   └── service.py        # Register and login business logic
│   ├── core/
│   │   ├── config.py         # Pydantic Settings — reads from .env
│   │   ├── exceptions.py     # Centralised HTTP exception helpers
│   │   └── security.py       # bcrypt hashing, JWT encode/decode
│   ├── db/
│   │   └── session.py        # SQLAlchemy engine, session, Base, get_db
│   ├── guest/
│   │   ├── models.py         # GuestTodo SQLAlchemy model
│   │   ├── router.py         # /guest/todos (public)
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── service.py        # Create/list guest todos
│   ├── todos/
│   │   ├── models.py         # Todo SQLAlchemy model + TodoStatus enum
│   │   ├── router.py         # /todos CRUD (protected)
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── service.py        # CRUD with owner enforcement
│   └── main.py               # FastAPI app, router registration, error handlers
├── migrations/
│   ├── versions/
│   │   └── 0001_initial.py   # Initial schema migration
│   ├── env.py                # Alembic environment config
│   └── script.py.mako
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set a strong `JWT_SECRET_KEY`:

```env
POSTGRES_USER=todouser
POSTGRES_PASSWORD=todopassword
POSTGRES_DB=tododb
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgresql://todouser:todopassword@db:5432/tododb

JWT_SECRET_KEY=your-strong-random-secret-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 2. Start with Docker Compose

```bash
docker compose up --build
```

This will:
1. Start the PostgreSQL container and wait for it to be healthy
2. Run `alembic upgrade head` to apply migrations
3. Start the API server on port `8000`

### 3. Access the API

- **API Base:** `http://localhost:8000/api/v1`
- **Interactive Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`

---

## API Reference

All routes are prefixed with `/api/v1`.

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | None | Register a new user |
| POST | `/auth/login` | None | Login and receive JWT token |

#### Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "password": "securepassword"
  }'
```

**Response `201`:**
```json
{
  "message": "Account created successfully.",
  "user": {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "securepassword"
  }'
```

**Response `200`:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

### User Todos (Protected)

All endpoints require `Authorization: Bearer <token>`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/todos` | Create a todo |
| GET | `/todos` | List your todos |
| PUT | `/todos/{id}` | Update a todo |
| DELETE | `/todos/{id}` | Delete a todo |

#### Create Todo

```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish report", "body": "Complete Q4 summary"}'
```

#### Update Todo

```bash
curl -X PUT http://localhost:8000/api/v1/todos/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "COMPLETED"}'
```

Allowed status values: `PENDING`, `COMPLETED`

---

### Guest Todos (Public)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/guest/todos` | Create a guest todo |
| GET | `/guest/todos` | List all guest todos |

---

## Development (Without Docker)

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://user:password@localhost:5432/tododb
export JWT_SECRET_KEY=your-dev-secret

# Run migrations
alembic upgrade head

# Start dev server
uvicorn app.main:app --reload --port 8000
```

---

## Security Notes

- Passwords are hashed with **bcrypt** and never stored or returned in plaintext
- JWT tokens expire after **60 minutes**
- Users can only read, update, or delete **their own todos** — enforced at the service layer
- All secrets are loaded from environment variables — never hardcoded
- `pool_pre_ping=True` ensures stale DB connections are detected before use

---

## Error Response Format

All errors return consistent JSON:

```json
{ "detail": "Human-readable error message." }
```

Validation errors (`422`) return a list of field-level issues:

```json
{
  "detail": [
    { "field": "body -> password", "message": "Password must be at least 8 characters long." }
  ]
}
```
