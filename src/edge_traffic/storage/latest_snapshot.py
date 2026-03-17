import json
import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import cv2

from edge_traffic.domain.frame import Frame


@dataclass(frozen=True, slots=True)
class LatestSnapshotRef:
    snapshot_id: str
    dir_path: Path
    image_path: Path
    motion_image_path: Path | None
    meta_path: Path


class LatestSnapshotStore:
    def __init__(self, base_dir: str) -> None:
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.latest_manifest_path = self.base_path / "latest.json"
        self.snapshots_path = self.base_path / "snapshots"
        self.snapshots_path.mkdir(parents=True, exist_ok=True)

    def save(self, frame: Frame, extra_metadata: dict[str, Any] | None = None) -> str:
        snapshot_id = self._new_snapshot_id(frame)

        tmp_dir = self.snapshots_path / f".tmp-{snapshot_id}"
        final_dir = self.snapshots_path / snapshot_id
        tmp_dir.mkdir(parents=True, exist_ok=False)

        image_path = tmp_dir / "snapshot.jpg"
        meta_path = tmp_dir / "snapshot.json"

        metadata = {
            "snapshot_id": snapshot_id,
            "frame_id": frame.frame_id,
            "source": frame.source,
            "captured_at": frame.captured_at.isoformat(),
            "width": frame.width,
            "height": frame.height,
            "channels": frame.channels,
        }

        if extra_metadata:
            metadata.update(extra_metadata)

            motion = metadata.get("motion")
            regions = motion.get("regions", []) if isinstance(motion, dict) else []
            if regions:
                img_move = frame.image.copy()
                for region in regions:
                    cv2.rectangle(
                        img_move,
                        (region["x1"], region["y1"]),
                        (region["x2"], region["y2"]),
                        (0, 255, 0),
                        2,
                    )

                image_move_path = tmp_dir / "snapshot_motion.jpg"
                move_ok = cv2.imwrite(str(image_move_path), img_move)
                if not move_ok:
                    raise RuntimeError("Failed to write motion snapshot image")

        ok = cv2.imwrite(str(image_path), frame.image)

        if not ok:
            raise RuntimeError("Failed to write snapshot image")

        with meta_path.open("w", encoding="utf-8") as f:
            json.dump(metadata, f)
            f.flush()
            os.fsync(f.fileno())

        tmp_dir.replace(final_dir)
        manifest = {"snapshot_id": snapshot_id}
        self._write_json_atomic(manifest, self.latest_manifest_path)
        return snapshot_id

    def load_metadata(self) -> dict[str, Any] | None:
        ref = self.resolve_latest()

        if not ref:
            return None

        with ref.meta_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def image_exists(self) -> bool:
        return self.get_latest_image_path() is not None

    def get_latest_image_path(self) -> Path | None:
        ref = self.resolve_latest()
        return None if ref is None else ref.image_path

    def get_latest_motion_image_path(self) -> Path | None:
        ref = self.resolve_latest()
        return None if ref is None else ref.motion_image_path

    def resolve_latest(self) -> LatestSnapshotRef | None:
        if not self.latest_manifest_path.exists():
            return None

        try:
            with self.latest_manifest_path.open("r", encoding="utf-8") as f:
                manifest = json.load(f)
        except json.JSONDecodeError:
            return None

        snapshot_id = manifest.get("snapshot_id")
        if not snapshot_id:
            return None

        dir_path = self.snapshots_path / str(snapshot_id)
        image_path = dir_path / "snapshot.jpg"
        motion_image_path = dir_path / "snapshot_motion.jpg"
        meta_path = dir_path / "snapshot.json"

        if not (dir_path.exists() and image_path.exists() and meta_path.exists()):
            return None

        return LatestSnapshotRef(
            snapshot_id=str(snapshot_id),
            dir_path=dir_path,
            image_path=image_path,
            motion_image_path=motion_image_path if motion_image_path.exists() else None,
            meta_path=meta_path,
        )

    def _new_snapshot_id(self, frame: Frame) -> str:
        return f"f{frame.frame_id}-{uuid.uuid4().hex}"

    def _write_json_atomic(self, data: dict[str, Any], dest_path: Path) -> None:
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

        tmp_path.replace(dest_path)
