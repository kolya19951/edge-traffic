from dataclasses import dataclass
from datetime import datetime, UTC

import numpy as np


@dataclass(slots=True)
class Frame:
    frame_id: int
    source: str
    captured_at: datetime
    image: np.ndarray

    @property
    def height(self) -> int:
        return int(self.image.shape[0])

    @property
    def width(self) -> int:
        return int(self.image.shape[1])

    @property
    def channels(self) -> int:
        return int(self.image.shape[2]) if self.image.ndim == 3 else 1

    @classmethod
    def create(cls, frame_id: int, source: str, image: np.ndarray) -> "Frame":
        return cls(
            frame_id=frame_id,
            source=source,
            captured_at=datetime.now(UTC),
            image=image,
        )
