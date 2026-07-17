from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.db.base import Base
from app.db.session import SessionLocal
from app.main import app


def test_app_imports_and_health_endpoint_returns_expected_payload() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_settings_load_deterministically() -> None:
    settings_one = get_settings()
    settings_two = get_settings()

    assert isinstance(settings_one, Settings)
    assert settings_one is settings_two
    assert settings_one.app_name == "Tri9T CT-200 Backend"
    assert settings_one.database_url == "sqlite:///./tri9t.db"


def test_sqlalchemy_base_metadata_is_available() -> None:
    assert Base.metadata is not None
    assert len(Base.metadata.tables) == 0


def test_session_factory_creates_and_closes_session() -> None:
    session = SessionLocal()
    try:
        assert session.is_active is True
    finally:
        session.close()



def test_project_manually_supplied_ct200_files_exist() -> None:
    data_dir = Path("data")
    assert (data_dir / "ct200_manual.md").is_file()
    assert (data_dir / "ct200_manual_v2.md").is_file()


def test_alembic_configuration_file_exists() -> None:
    assert Path("alembic.ini").is_file()
    assert Path("alembic").is_dir()
    assert Path("alembic") / "env.py"