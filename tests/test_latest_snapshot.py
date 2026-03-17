import numpy as np

from edge_traffic.domain.frame import Frame
from edge_traffic.storage.latest_snapshot import LatestSnapshotStore


def test_latest_snapshot_store_save_and_load(tmp_path) -> None:
    store = LatestSnapshotStore(str(tmp_path))
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    frame = Frame.create(source="test", image=image)
    frame_id = frame.frame_id

    snapshot_id = store.save(frame)

    metadata = store.load_metadata()
    assert metadata is not None
    assert metadata["frame_id"] == frame_id
    assert metadata["snapshot_id"] == snapshot_id
    assert metadata["source"] == "test"
    assert store.image_exists()
    image_path = store.get_latest_image_path()
    assert image_path is not None
    assert image_path.parent.name == snapshot_id


def test_latest_snapshot_store_exposes_latest_motion_image(tmp_path) -> None:
    store = LatestSnapshotStore(str(tmp_path))
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    frame = Frame.create(source="test", image=image)

    snapshot_id = store.save(
        frame,
        extra_metadata={
            "motion": {
                "regions": [
                    {"x1": 10, "y1": 20, "x2": 30, "y2": 40},
                ]
            }
        },
    )

    ref = store.resolve_latest()
    motion_image_path = store.get_latest_motion_image_path()

    assert ref is not None
    assert ref.snapshot_id == snapshot_id
    assert motion_image_path is not None
    assert motion_image_path.exists()
    assert motion_image_path.parent.name == snapshot_id
