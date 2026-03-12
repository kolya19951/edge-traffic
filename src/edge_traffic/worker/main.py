import logging

from edge_traffic.capture.factory import build_frame_provider
from edge_traffic.config import get_settings
from edge_traffic.logging import setup_logging


def main() -> None:
    settings = get_settings()
    setup_logging(settings)

    logger = logging.getLogger(__name__)

    provider = build_frame_provider(settings)

    logger.info(
        "worker started frame_source=%s camera_url=%s",
        settings.frame_source,
        settings.camera_url,
    )

    for frame in provider.frames():
        logger.info("frame received shape=%s", frame.shape)


if __name__ == "__main__":
    main()
