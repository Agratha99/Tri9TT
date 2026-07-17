from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Application startup and shutdown lifecycle.

    Reserved for initialization tasks in future milestones.
    """
    settings = get_settings()
    print(f"Starting {settings.app_name}")
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}