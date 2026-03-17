import time
from typing import Iterator


import numpy as np

from edge_traffic.capture.base import FrameProvider
from edge_traffic.domain.frame import Frame


class FakeFrameProvider(FrameProvider):
    """
    Generates synthetic frames for testing.
    """

    def __init__(
            self,
            width: int = 640,
            height: int = 480,
            fps: float = 5.0,
            source: str = "fake") -> None:
        self.width = width
        self.height = height
        self.delay = 1.0 / fps
        self.source = source

    def frames(self) -> Iterator[Frame]:
        while True:
            image = np.random.randint(
                0, 255, (self.height, self.width, 3), dtype=np.uint8
            )

            yield Frame.create(
                source=self.source,
                image=image
            )
            time.sleep(self.delay)
