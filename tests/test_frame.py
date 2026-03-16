import numpy as np

from edge_traffic.domain.frame import Frame


def test_frame_properties() -> None:
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    frame = Frame.create(frame_id=1, source="test", image=image)

    assert frame.frame_id == 1
    assert frame.source == "test"
    assert frame.width == 640
    assert frame.height == 480
    assert frame.channels == 3
