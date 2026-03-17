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

    motion_enabled: bool = Field(default=True)
    motion_resize_width: int = Field(default=320)
    motion_blur_kernel_size: int = Field(default=5)
    motion_diff_threshold: int = Field(default=25)
    motion_min_area: int = Field(default=500)
    motion_dilation_iterations: int = Field(default=2)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
