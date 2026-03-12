from edge_traffic.capture.base import FrameProvider
from edge_traffic.capture.fake import FakeFrameProvider
from edge_traffic.capture.ip_camera import IPCameraFrameProvider
from edge_traffic.config import Settings


def build_frame_provider(settings: Settings) -> FrameProvider:
    if settings.frame_source == "fake":
        return FakeFrameProvider(
            width=settings.camera_width,
            height=settings.camera_height,
            fps=settings.camera_fps,
        )

    if settings.frame_source == "ip":
        if not settings.camera_url:
            raise ValueError("CAMERA_URL must be set when FRAME_SOURCE=ip")

        return IPCameraFrameProvider(
            url=settings.camera_url,
            width=settings.camera_width,
            height=settings.camera_height,
            fps=settings.camera_fps,
        )

    raise ValueError(f"Unsupported frame source: {settings.frame_source}")
