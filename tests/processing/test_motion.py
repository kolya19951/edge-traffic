from tests.helpers import black_image, make_frame, image_with_rectangle
from edge_traffic.processing.motion import MotionDetectionStage, MotionDetectionConfig


def test_motion_stage_first_frame_is_warmup() -> None:
    image = black_image()
    frame = make_frame(image)

    stage = MotionDetectionStage(MotionDetectionConfig())
    metadata = stage.process(frame, {})

    assert "motion" in metadata
    assert metadata["motion"]["enabled"] is True
    assert metadata["motion"]["detected"] is False
    assert metadata["motion"]["regions"] == []
    assert metadata["motion"]["pixel_ratio"] == 0.0
    assert metadata["motion"]["warmup"] is True


def test_motion_stage_no_change_detects_no_motion() -> None:
    image = black_image()
    frame1 = make_frame(image)
    frame2 = make_frame(image.copy())

    stage = MotionDetectionStage(MotionDetectionConfig())

    stage.process(frame1, {})
    metadata = stage.process(frame2, {})

    assert metadata["motion"]["enabled"] is True
    assert metadata["motion"]["warmup"] is False
    assert metadata["motion"]["detected"] is False
    assert metadata["motion"]["regions"] == []
    assert metadata["motion"]["pixel_ratio"] == 0.0


def test_motion_stage_detects_simple_rectangle_motion() -> None:
    frame1 = make_frame(black_image())
    frame2 = make_frame(
        image_with_rectangle(x1=120, y1=140, x2=220, y2=220)
    )

    stage = MotionDetectionStage(
        MotionDetectionConfig(
            resize_width=320,
            diff_threshold=25,
            min_area=200,
        )
    )

    stage.process(frame1, {})
    metadata = stage.process(frame2, {})

    motion = metadata["motion"]

    assert motion["warmup"] is False
    assert motion["detected"] is True
    assert motion["pixel_ratio"] > 0.0
    assert len(motion["regions"]) >= 1

    region = motion["regions"][0]
    assert region["x1"] < 220
    assert region["x2"] > 120
    assert region["y1"] < 220
    assert region["y2"] > 140


def test_motion_stage_ignores_small_regions_below_min_area() -> None:
    base = black_image()
    changed = black_image()
    changed[10:15, 10:15] = 255  # tiny white patch

    frame1 = make_frame(base)
    frame2 = make_frame(changed)

    stage = MotionDetectionStage(
        MotionDetectionConfig(
            resize_width=320,
            diff_threshold=25,
            min_area=1000,
        )
    )

    stage.process(frame1, {})
    metadata = stage.process(frame2, {})

    motion = metadata["motion"]
    assert motion["detected"] is False
    assert motion["regions"] == []


def test_motion_stage_disabled_returns_disabled_metadata() -> None:
    frame = make_frame(black_image())

    stage = MotionDetectionStage(
        MotionDetectionConfig(enable=False)
    )
    metadata = stage.process(frame, {})

    assert metadata["motion"]["enabled"] is False
    assert metadata["motion"]["detected"] is False
    assert metadata["motion"]["regions"] == []
    assert metadata["motion"]["pixel_ratio"] == 0.0


def test_motion_stage_shape_change_resets_warmup_before_diff() -> None:
    frame1 = make_frame(black_image(width=640, height=480))
    frame2 = make_frame(black_image(width=800, height=480))

    stage = MotionDetectionStage(MotionDetectionConfig(resize_width=320))

    warmup = stage.process(frame1, {})
    reset = stage.process(frame2, {})
    steady = stage.process(frame2, {})

    assert warmup["motion"]["warmup"] is True
    assert reset["motion"]["warmup"] is True
    assert reset["motion"]["detected"] is False
    assert steady["motion"]["warmup"] is False
    assert steady["motion"]["detected"] is False
