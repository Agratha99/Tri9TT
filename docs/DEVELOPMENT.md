# Development Guide

## Workflow

Development follows a milestone-based approach.

Each milestone should:

1. Implement only its assigned scope.
2. Keep changes isolated.
3. Pass all verification commands.
4. Maintain Ruff compliance.

---

# Code Quality

Before completing work:

```bash
uv run ruff check .
```

Auto-fix formatting issues:

```bash
uv run ruff check . --fix
```

---

# Testing

Run the full test suite:

```bash
uv run pytest -q
```

All tests should pass before merging changes.

---

# Alembic Workflow

Check migration status:

```bash
uv run alembic current
```

Create a revision:

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

Migration commands are executed outside the pytest suite.

---

# Local Verification

Before considering a milestone complete, run:

```bash
uv run pytest -q
uv run ruff check .
uv run alembic current
uv run python -c "from app.main import app; print('Import OK')"
```

---

# Phase-Based Strategy

Development is incremental.

Each milestone builds on the previous one.

Avoid implementing functionality assigned to future phases.

---

# Commit Policy

Each milestone should produce a focused commit.

Avoid combining unrelated work in a single commit.

Suggested commit message format:

```
type(scope): summary
```

Example:

```
docs(phase1): add infrastructure documentation
```

---

# Troubleshooting

## Module import errors

Run:

```bash
uv sync --dev
```

from the repository root.

---

## Ruff failures

Run:

```bash
uv run ruff check . --fix
```

Review remaining issues manually.

---

## Alembic cannot locate configuration

Run Alembic from the repository root so `alembic.ini` is discoverable.

---

## Health endpoint not responding

Verify the application imports successfully:

```bash
uv run python -c "from app.main import app; print('Import OK')"
```