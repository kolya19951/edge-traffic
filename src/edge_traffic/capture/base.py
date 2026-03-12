from abc import ABC, abstractmethod
from typing import Iterator

import numpy as np


class FrameProvider(ABC):
    """
    Abstract frame source.
    """

    @abstractmethod
    def frames(self) -> Iterator[np.ndarray]:
        """
        Yield frames indefinitely.
        """
        raise NotImplementedError
