from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np

from edge_traffic.domain.frame import Frame
from edge_traffic.processing.base import ProcessingStage


@dataclass
class MotionDetectionConfig:
    enable: bool = True
    resize_width: int = 320
    blur_kernel_size: int = 5
    diff_threshold: int = 25
    min_area: int = 500
    dilation_iterations: int = 2


class MotionDetectionStage(ProcessingStage):

    def __init__(self, config: MotionDetectionConfig) -> None:
        self._config = config
        self._previous_gray: np.ndarray | None = None

    def process(self, frame: Frame, metadata: dict[str, Any]) -> dict[str, Any]:
        if not self._config.enable:
            metadata["motion"] = {
                "enabled": False,
                "detected": False,
                "regions": [],
                "pixel_ratio": 0.0,
            }
            return metadata

        image = frame.image

        original_height, original_width = image.shape[:2]

        scale = self._config.resize_width / float(original_width)
        resized_height = max(1, int(original_height * scale))

        small = cv2.resize(
            image,
            (self._config.resize_width, resized_height),
            interpolation=cv2.INTER_LINEAR,
        )

        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        kernel = self._config.blur_kernel_size
        if kernel % 2 == 0:
            kernel += 1

        gray = cv2.GaussianBlur(gray, (kernel, kernel), 0)

        if self._previous_gray is None:
            self._previous_gray = gray
            metadata["motion"] = {
                "enabled": True,
                "detected": False,
                "regions": [],
                "pixel_ratio": 0.0,
                "warmup": True,
            }
            return metadata

        if self._previous_gray.shape != gray.shape:
            self._previous_gray = gray
            metadata["motion"] = {
                "enabled": True,
                "detected": False,
                "regions": [],
                "pixel_ratio": 0.0,
                "warmup": True,
            }
            return metadata

        frame_delta = cv2.absdiff(self._previous_gray, gray)
        _, thresh = cv2.threshold(
            frame_delta,
            self._config.diff_threshold,
            255,
            cv2.THRESH_BINARY,
        )

        thresh = cv2.dilate(
            thresh,
            None,
            iterations=self._config.dilation_iterations,
        )

        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        regions: list[dict[str, int]] = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self._config.min_area:
                continue

            x, y, w, h = cv2.boundingRect(contour)

            # Map back to original image coordinates
            x1 = int(x / scale)
            y1 = int(y / scale)
            x2 = int((x + w) / scale)
            y2 = int((y + h) / scale)

            regions.append(
                {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "area": int(area),
                }
            )

        motion_pixels = int(np.count_nonzero(thresh))
        total_pixels = int(thresh.shape[0] * thresh.shape[1])
        pixel_ratio = motion_pixels / total_pixels if total_pixels else 0.0

        metadata["motion"] = {
            "enabled": True,
            "detected": len(regions) > 0,
            "regions": regions,
            "pixel_ratio": round(pixel_ratio, 6),
            "warmup": False,
        }

        self._previous_gray = gray
        return metadata
