from dataclasses import dataclass
from datetime import datetime, UTC

from uuid import uuid4

import numpy as np


@dataclass(slots=True)
class Frame:
    frame_id: str
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
    def create(cls, source: str, image: np.ndarray) -> "Frame":
        return cls(
            frame_id=str(uuid4()),
            source=source,
            captured_at=datetime.now(UTC),
            image=image,
        )
