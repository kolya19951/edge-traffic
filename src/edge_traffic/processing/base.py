from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from edge_traffic.domain.frame import Frame


class ProcessingStage(ABC):
    @abstractmethod
    def process(self, frame: Frame, metadata: dict[str, Any]) -> dict[str, Any]:
        """Process one frame and return updated metadata."""
        raise NotImplementedError
