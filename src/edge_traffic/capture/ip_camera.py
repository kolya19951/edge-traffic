import time
from typing import Iterator

import cv2
import numpy as np

from edge_traffic.capture.base import FrameProvider


class IPCameraFrameProvider(FrameProvider):
    def __init__(
        self,
        url: str,
        width: int | None = None,
        height: int | None = None,
        fps: float | None = None,
        reconnect_delay: float = 2.0,
    ) -> None:
        self.url = url
        self.width = width
        self.height = height
        self.fps = fps
        self.reconnect_delay = reconnect_delay

    def _open(self) -> cv2.VideoCapture:
        cap = cv2.VideoCapture(self.url)
        if self.width is not None:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        if self.height is not None:
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if self.fps is not None:
            cap.set(cv2.CAP_PROP_FPS, self.fps)
        return cap

    def frames(self) -> Iterator[np.ndarray]:
        cap = self._open()

        try:
            while True:
                if not cap.isOpened():
                    cap.release()
                    time.sleep(self.reconnect_delay)
                    cap = self._open()
                    continue

                ok, frame = cap.read()
                if not ok or frame is None:
                    cap.release()
                    time.sleep(self.reconnect_delay)
                    cap = self._open()
                    continue

                yield frame
        finally:
            cap.release()
