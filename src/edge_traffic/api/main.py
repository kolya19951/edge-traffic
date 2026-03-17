import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from edge_traffic.config import get_settings
from edge_traffic.logging import setup_logging
from edge_traffic.storage.latest_snapshot import LatestSnapshotStore

settings = get_settings()
setup_logging(settings)
logger = logging.getLogger(__name__)
snapshot_store = LatestSnapshotStore(settings.latest_snapshot_dir)


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


@app.get("/snapshot/meta")
def snapshot_meta() -> dict[str, str | int | dict]:
    metadata = snapshot_store.load_metadata()
    if metadata is None:
        raise HTTPException(status_code=404, detail="No snapshot available")
    return metadata


@app.get("/snapshot.jpg")
def snapshot_image() -> FileResponse:
    image_path = snapshot_store.get_latest_image_path()
    if not image_path:
        raise HTTPException(status_code=404, detail="No snapshot image available")
    return FileResponse(image_path, media_type="image/jpeg")


@app.get("/snapshot_motion.jpg")
def snapshot_image_motion() -> FileResponse:
    image_path = snapshot_store.get_latest_motion_image_path()
    if not image_path:
        raise HTTPException(status_code=404, detail="No snapshot image available")
    return FileResponse(image_path, media_type="image/jpeg")
