from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="edge-traffic")
    environment: str = Field(default="dev")
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    log_level: str = Field(default="INFO")

    frame_source: Literal["fake", "ip"] = Field(default="fake")
    camera_url: str | None = Field(default=None)
    camera_width: int = Field(default=640)
    camera_height: int = Field(default=480)
    camera_fps: float = Field(default=5.0)

    data_dir: str = Field(default="data")
    latest_snapshot_dir: str = Field(default="data/latest")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
