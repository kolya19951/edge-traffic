import numpy as np

from edge_traffic.domain.frame import Frame


def test_frame_properties() -> None:
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    frame = Frame.create(source="test", image=image)
    frame_id = frame.frame_id

    assert frame.frame_id == frame_id
    assert frame.source == "test"
    assert frame.width == 640
    assert frame.height == 480
    assert frame.channels == 3
