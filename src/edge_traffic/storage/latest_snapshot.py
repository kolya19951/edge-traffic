import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import cv2

from edge_traffic.domain.frame import Frame


class LatestSnapshotStore:
    def __init__(self, base_dir: str) -> None:
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.image_path = self.base_path / "snapshot.jpg"
        self.meta_path = self.base_path / "snapshot.json"

    def save(self, frame: Frame, extra_metadata: dict[str, Any] | None = None) -> None:
        metadata = {
            "frame_id": frame.frame_id,
            "source": frame.source,
            "captured_at": frame.captured_at.isoformat(),
            "width": frame.width,
            "height": frame.height,
            "channels": frame.channels,
        }

        if extra_metadata:
            metadata.update(extra_metadata)

        self._write_image_atomic(frame)
        self._write_json_atomic(metadata)

    def load_metadata(self) -> dict[str, Any] | None:
        if not self.meta_path.exists():
            return None

        with self.meta_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def image_exists(self) -> bool:
        return self.image_path.exists()

    def _write_image_atomic(self, frame: Frame) -> None:
        self.base_path.mkdir(parents=True, exist_ok=True)

        with NamedTemporaryFile(
                mode="wb",
                suffix=".jpg",
                dir=self.base_path,
                delete=False,
        ) as tmp:
            tmp_path = Path(tmp.name)

        try:
            ok = cv2.imwrite(str(tmp_path), frame.image)
            if not ok:
                raise RuntimeError("Failed to write snapshot image")
            tmp_path.replace(self.image_path)
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except FileNotFoundError:
                    pass

    def _write_json_atomic(self, data: dict[str, Any]) -> None:
        self.base_path.mkdir(parents=True, exist_ok=True)

        with NamedTemporaryFile(
                mode="w",
                suffix=".json",
                dir=self.base_path,
                delete=False,
                encoding="utf-8",
        ) as tmp:
            json.dump(data, tmp)
            tmp.flush()
            tmp_path = Path(tmp.name)

        tmp_path.replace(self.meta_path)
