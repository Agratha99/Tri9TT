# Architecture

## Overview

Tri9T currently follows a lightweight modular monolith architecture.

Only the infrastructure layer has been implemented.

No domain modules, repositories, services, or business logic currently exist.

---

# Directory Structure

```text
app/
    core/
        config.py

    db/
        base.py
        session.py

    main.py
```

---

# Configuration Flow

Application startup:

```
FastAPI
      │
      ▼
get_settings()
      │
      ▼
Settings
      │
      ▼
Environment variables /.env
```

Configuration is cached using `functools.lru_cache`.

---

# FastAPI Startup Flow

```
Application import
        │
        ▼
Settings loaded
        │
        ▼
FastAPI created
        │
        ▼
lifespan()
        │
        ▼
Application ready
```

The application currently exposes one endpoint:

```
GET /health
```

---

# SQLAlchemy Flow

```
Settings
    │
    ▼
database_url
    │
    ▼
create_engine()
    │
    ▼
SessionLocal
    │
    ▼
Application sessions
```

The declarative `Base` provides shared metadata for future ORM models.

No models currently inherit from `Base`.

---

# Alembic Integration

Alembic is configured using:

- alembic.ini
- alembic/env.py

`Base.metadata` is exposed to Alembic for migration generation.

No application schema currently exists.

---

# Public API

## GET /health

Returns:

```json
{
  "status": "ok"
}
```

---

# Current Limitations

Current implementation intentionally excludes:

- ORM models
- business logic
- repositories
- services
- parser
- document processing
- authentication
- authorization

---

# Phase 1 Design Principles

- Keep infrastructure isolated.
- Maintain deterministic configuration.
- Separate configuration from application logic.
- Centralize database initialization.
- Keep testing focused on public behavior.
- Avoid introducing unused abstractions.