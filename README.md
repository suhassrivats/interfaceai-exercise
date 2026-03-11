# Todo Application

A Todo app with full CRUD operations, PostgreSQL storage, and a simple UI, running in Docker with CI/CD via GitHub Actions.

## Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Containers:** Docker, Docker Compose
- **CI/CD:** GitHub Actions (lint, tests, Docker build)

## Quick start with Docker

```bash
docker compose up --build
```

- **UI:** http://localhost:8000  
- **API docs:** http://localhost:8000/docs  

The app waits for Postgres to be healthy before starting.

## Run locally (no Docker)

1. Start PostgreSQL (e.g. local install or a Postgres container) and create a database.

2. Set the database URL and run the app:

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/todo_db"
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

3. Open http://localhost:8000

## Run tests

Tests expect a running Postgres instance (e.g. `docker compose up -d db`).

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/todo_test"
pip install -r requirements.txt pytest httpx
pytest tests/ -v
```

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/todos` | List todos (optional `?completed=true|false`) |
| POST | `/api/todos` | Create todo |
| GET | `/api/todos/{id}` | Get one todo |
| PATCH | `/api/todos/{id}` | Update todo |
| DELETE | `/api/todos/{id}` | Delete todo |
| GET | `/api/health` | Health check |

## Docker Images

Two separate images are built and pushed to Docker Hub:

| Image | Docker Hub |
|-------|------------|
| Database (Postgres + schema) | `DOCKERHUB_USERNAME/interfaceai-exercise-db` |
| Application (FastAPI) | `DOCKERHUB_USERNAME/interfaceai-exercise-app` |

Use `docker compose up --build` to build locally. To pull from Docker Hub, set `DOCKERHUB_USERNAME` in a `.env` file (e.g. `DOCKERHUB_USERNAME=yourusername`) or export it, then run `docker compose up`.

**Required GitHub secrets** (Settings → Secrets and variables → Actions): `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (create at [hub.docker.com/settings/security](https://hub.docker.com/settings/security)).

## CI/CD

On push/PR to `main` or `master`, GitHub Actions:

1. **lint-and-test:** Ruff lint on Python 3.11 and 3.12  
2. **test-postgres:** Pytest against a Postgres service  
3. **build-database-image:** Build and push the database image to Docker Hub  
4. **build-app-image:** Build and push the application image to Docker Hub  

Images are pushed only on push to `main`/`master` (not on pull requests).
