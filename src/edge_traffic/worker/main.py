import logging

from edge_traffic.capture.factory import build_frame_provider
from edge_traffic.config import get_settings
from edge_traffic.logging import setup_logging
from edge_traffic.storage.latest_snapshot import LatestSnapshotStore


def main() -> None:
    settings = get_settings()
    setup_logging(settings)

    logger = logging.getLogger(__name__)
    provider = build_frame_provider(settings)
    snapshot_store = LatestSnapshotStore(settings.latest_snapshot_dir)

    logger.info(
        "worker started frame_source=%s camera_url=%s",
        settings.frame_source,
        settings.camera_url,
    )

    for frame in provider.frames():
        snapshot_store.save(frame)
        logger.info(
            "frame received id=%s source=%s shape=(%s, %s, %s)",
            frame.frame_id,
            frame.source,
            frame.height,
            frame.width,
            frame.channels
        )


if __name__ == "__main__":
    main()
