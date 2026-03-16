from abc import ABC, abstractmethod
from typing import Iterator

from edge_traffic.domain.frame import Frame


class FrameProvider(ABC):
    """
    Abstract frame source.
    """

    @abstractmethod
    def frames(self) -> Iterator[Frame]:
        """
        Yield frames indefinitely.
        """
        raise NotImplementedError
