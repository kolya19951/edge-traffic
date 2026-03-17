import logging

from edge_traffic.capture.factory import build_frame_provider
from edge_traffic.config import get_settings
from edge_traffic.logging import setup_logging
from edge_traffic.storage.latest_snapshot import LatestSnapshotStore
from edge_traffic.processing.pipeline import ProcessingPipeline
from edge_traffic.processing.motion import MotionDetectionConfig, MotionDetectionStage


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

    pipeline = ProcessingPipeline(
        stages=[
            MotionDetectionStage(
                MotionDetectionConfig(
                    enable=settings.motion_enabled,
                    resize_width=settings.motion_resize_width,
                    blur_kernel_size=settings.motion_blur_kernel_size,
                    diff_threshold=settings.motion_diff_threshold,
                    min_area=settings.motion_min_area,
                    dilation_iterations=settings.motion_dilation_iterations
                )
            )
        ]
    )

    for frame in provider.frames():
        processing_metadata = pipeline.process(frame)

        snapshot_store.save(frame, extra_metadata=processing_metadata)
        logger.info(
            "frame received id=%s source=%s shape=(%s, %s, %s)",
            frame.frame_id,
            frame.source,
            frame.height,
            frame.width,
            frame.channels,
            extra={"processing_metadata": processing_metadata},
        )


if __name__ == "__main__":
    main()
