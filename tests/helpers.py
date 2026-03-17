from __future__ import annotations

import cv2
import numpy as np

from edge_traffic.domain.frame import Frame


def make_frame(
        image: np.ndarray,
        source: str = "test",
) -> Frame:
    return Frame.create(
        source=source,
        image=image,
    )


def black_image(width: int = 640, height: int = 480) -> np.ndarray:
    return np.zeros((height, width, 3), dtype=np.uint8)


def image_with_rectangle(
        width: int = 640,
        height: int = 480,
        x1: int = 100,
        y1: int = 100,
        x2: int = 200,
        y2: int = 180,
) -> np.ndarray:
    image = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), thickness=-1)
    return image
