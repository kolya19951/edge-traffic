from typing import Any
from tests.helpers import black_image, make_frame

from edge_traffic.domain.frame import Frame
from edge_traffic.processing.base import ProcessingStage
from edge_traffic.processing.pipeline import ProcessingPipeline


class AppendStage(ProcessingStage):
    def __init__(self, name: str) -> None:
        self.name = name

    def process(self, frame: Frame, metadata: dict[str, Any]) -> dict[str, Any]:
        order = metadata.setdefault("order", [])
        order.append(self.name)
        metadata[self.name] = True
        return metadata


class ReadPreviousStage(ProcessingStage):
    def process(self, frame: Frame, metadata: dict[str, Any]) -> dict[str, Any]:
        metadata["saw_previous"] = metadata.get("first") == "ok"
        return metadata


class FirstStage(ProcessingStage):
    def process(self, frame: Frame, metadata: dict[str, Any]) -> dict[str, Any]:
        metadata["first"] = "ok"
        return metadata


def test_pipeline_runs_stages_in_order() -> None:
    frame = make_frame(black_image())

    pipeline = ProcessingPipeline(
        stages=[
            AppendStage("stage_a"),
            AppendStage("stage_b"),
            AppendStage("stage_c"),
        ]
    )

    metadata = pipeline.process(frame)

    assert metadata["order"] == ["stage_a", "stage_b", "stage_c"]
    assert metadata["stage_a"] is True
    assert metadata["stage_b"] is True
    assert metadata["stage_c"] is True


def test_pipeline_allows_later_stage_to_read_previous_output() -> None:
    frame = make_frame(black_image())

    pipeline = ProcessingPipeline(
        stages=[FirstStage(), ReadPreviousStage()]
    )

    metadata = pipeline.process(frame)

    assert metadata["first"] == "ok"
    assert metadata["saw_previous"] is True
