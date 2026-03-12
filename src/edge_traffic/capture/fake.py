import time
from typing import Iterator

import numpy as np

from edge_traffic.capture.base import FrameProvider


class FakeFrameProvider(FrameProvider):
    """
    Generates synthetic frames for testing.
    """

    def __init__(self, width: int = 640, height: int = 480, fps: float = 5.0):
        self.width = width
        self.height = height
        self.delay = 1.0 / fps

    def frames(self) -> Iterator[np.ndarray]:
        while True:
            frame = np.random.randint(
                0, 255, (self.height, self.width, 3), dtype=np.uint8
            )
            yield frame
            time.sleep(self.delay)
