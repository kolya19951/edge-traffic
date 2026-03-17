import numpy as np

from edge_traffic.domain.frame import Frame
from edge_traffic.storage.latest_snapshot import LatestSnapshotStore


def test_latest_snapshot_store_save_and_load(tmp_path) -> None:
    store = LatestSnapshotStore(str(tmp_path))
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    frame = Frame.create(source="test", image=image)
    frame_id = frame.frame_id

    store.save(frame)

    metadata = store.load_metadata()
    assert metadata is not None
    assert metadata["frame_id"] == frame_id
    assert metadata["source"] == "test"
    assert store.image_exists()
