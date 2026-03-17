from __future__ import annotations

from typing import Any, Iterable

from edge_traffic.domain.frame import Frame
from edge_traffic.processing.base import ProcessingStage


class ProcessingPipeline:
    def __init__(self, stages: Iterable[ProcessingStage]) -> None:
        self._stages = list(stages)

    def process(self, frame: Frame) -> dict[str, Any]:
        metadata: dict[str, Any] = {}

        for stage in self._stages:
            metadata = stage.process(frame, metadata)

        return metadata
