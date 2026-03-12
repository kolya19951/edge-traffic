from fastapi import FastAPI

from edge_traffic.config import get_settings


settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
