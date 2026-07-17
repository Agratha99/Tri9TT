# Tri9T

Tri9T is the backend implementation for the CT-200 AI Engineering Internship assignment.

The project is being developed incrementally using a strict milestone-based approach. At the current stage, the repository contains only the infrastructure required to support future development.

---

## Phase 1 Objectives

Phase 1 establishes the project foundation by providing:

- FastAPI application setup
- Centralized configuration
- SQLAlchemy initialization
- Alembic migration configuration
- Infrastructure verification tests
- Development tooling
- Project documentation

No domain models, repositories, services, parser logic, or business functionality have been implemented yet.

---

# Technology Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- pydantic-settings
- Uvicorn
- Pytest
- Ruff

---

# Project Structure

```text
.
├── alembic/
├── app/
│   ├── core/
│   ├── db/
│   └── main.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── DEVELOPMENT.md
├── tests/
├── pyproject.toml
├── alembic.ini
└── README.md
```

---

# Installation

Clone the repository.

Create the virtual environment.

```bash
uv sync
```

Install development dependencies.

```bash
uv sync --dev
```

---

# Environment Configuration

The application loads configuration using `pydantic-settings`.

Current configuration values:

| Variable | Default |
|-----------|----------|
| DATABASE_URL | sqlite:///./tri9t.db |

A local `.env` file may be used.

Example:

```env
DATABASE_URL=sqlite:///./tri9t.db
```

---

# Running the Application

```bash
uv run uvicorn app.main:app --reload
```

The application starts on the default Uvicorn port.

Health endpoint:

```
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# Alembic

Current migration state:

```bash
uv run alembic current
```

Generate a migration:

```bash
uv run alembic revision -m "message"
```

Upgrade:

```bash
uv run alembic upgrade head
```

Downgrade:

```bash
uv run alembic downgrade -1
```

---

# Running Tests

```bash
uv run pytest -q
```

---

# Ruff

Check:

```bash
uv run ruff check .
```

Auto-fix:

```bash
uv run ruff check . --fix
```

---

# Current Project Status

Completed:

- Phase 1 – Milestone 1: Project Foundation
- Phase 1 – Milestone 2: Alembic Configuration
- Phase 1 – Milestone 3: Foundation Tests
- Phase 1 – Milestone 4: Project Documentation

---

# Repository Layout

Current repository responsibilities:

- `app/` – application source
- `app/core/` – configuration
- `app/db/` – SQLAlchemy infrastructure
- `alembic/` – migration environment
- `tests/` – infrastructure tests
- `docs/` – project documentation

Only infrastructure exists at this stage.