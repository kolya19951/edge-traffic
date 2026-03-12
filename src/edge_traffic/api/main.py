import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from edge_traffic.config import get_settings
from edge_traffic.logging import setup_logging

settings = get_settings()
setup_logging(settings)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(
        "starting api app_name=%s env=%s host=%s port=%s",
        settings.app_name,
        settings.environment,
        settings.api_host,
        settings.api_port,
    )
    yield
    logger.info("stopping api")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/info")
def info() -> dict[str, str | int]:
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "api_port": settings.api_port,
        "log_level": settings.log_level,
    }
