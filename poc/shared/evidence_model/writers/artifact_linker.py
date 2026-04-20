from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class ArtifactLinkerConfig:
    base_dir: Path
    pretty: bool = True

    @property
    def artifacts_dir(self) -> Path:
        return self.base_dir / "artifacts"

    @property
    def evidence_dir(self) -> Path:
        return self.base_dir / "records"


class ArtifactLinkerError(Exception):
    """Raised when artifacts or evidence records cannot be linked."""


class ArtifactLinker:
    """
    Copies or references artifacts and links them to evidence objects.

    Expected layout:
        base_dir/
          artifacts/
          records/
    """

    def __init__(self, config: ArtifactLinkerConfig) -> None:
        self.config = config
        self.config.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.config.evidence_dir.mkdir(parents=True, exist_ok=True)

    def compute_sha256(self, file_path: Path) -> str:
        if not file_path.exists():
            raise ArtifactLinkerError(f"Artifact file not found: {file_path}")

        digest = hashlib.sha256()
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                digest.update(chunk)
        return f"sha256:{digest.hexdigest()}"

    def import_artifact(
        self,
        source_path: Path,
        *,
        copy: bool = True,
        target_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not source_path.exists():
            raise ArtifactLinkerError(f"Source artifact not found: {source_path}")

        target_name = target_name or source_path.name
        target_path = self.config.artifacts_dir / target_name

        if copy:
            shutil.copy2(source_path, target_path)
        else:
            target_path = source_path

        return {
            "artifact_name": target_name,
            "artifact_path": str(target_path),
            "artifact_hash": self.compute_sha256(target_path),
            "imported_at": self._utc_now(),
        }

    def link_artifact_to_evidence(
        self,
        evidence_path: Path,
        artifact_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        evidence = self._load_json(evidence_path)

        evidence.setdefault("artifacts", [])
        evidence["artifacts"].append(artifact_info["artifact_name"])

        evidence.setdefault("integrity", {})
        evidence["integrity"].setdefault("artifact_hashes", [])
        evidence["integrity"]["artifact_hashes"].append(artifact_info["artifact_hash"])
        evidence["integrity"]["created_at"] = evidence["integrity"].get("created_at") or self._utc_now()

        evidence.setdefault("metadata", {})
        evidence["metadata"].setdefault("artifact_links", [])
        evidence["metadata"]["artifact_links"].append({
            "artifact_name": artifact_info["artifact_name"],
            "artifact_path": artifact_info["artifact_path"],
            "artifact_hash": artifact_info["artifact_hash"],
            "linked_at": self._utc_now(),
        })

        self._write_json(evidence_path, evidence)
        return evidence

    def create_evidence_record(
        self,
        *,
        evidence_id: str,
        series_id: str,
        series_name: str,
        risk_tier: str,
        event_type: str,
        actor_type: str,
        actor_id: str,
        system_id: str,
        system_version: str,
        approved_boundary_reference: str,
        decision_status: str,
        notes: str = "",
    ) -> Path:
        record = {
            "evidence_id": evidence_id,
            "series_id": series_id,
            "series_name": series_name,
            "risk_tier": risk_tier,
            "event_type": event_type,
            "timestamp": self._utc_now(),
            "actor_type": actor_type,
            "actor_id": actor_id,
            "system_id": system_id,
            "system_version": system_version,
            "approved_boundary_reference": approved_boundary_reference,
            "decision_status": decision_status,
            "artifacts": [],
            "notes": notes,
            "integrity": {
                "created_at": self._utc_now(),
                "created_by": actor_id,
                "artifact_hashes": [],
                "previous_evidence": None,
            },
            "metadata": {},
        }

        path = self.config.evidence_dir / f"{evidence_id}.json"
        self._write_json(path, record)
        return path

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            raise ArtifactLinkerError(f"JSON record not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


if __name__ == "__main__":
    base_dir = Path("poc/shared/evidence_model")
    linker = ArtifactLinker(ArtifactLinkerConfig(base_dir=base_dir))

    evidence_path = linker.create_evidence_record(
        evidence_id="ev_demo_001",
        series_id="SeriesB",
        series_name="Executive Fleet Leasing",
        risk_tier="limited",
        event_type="WORKFLOW_DEPENDENCE_ALERT",
        actor_type="system",
        actor_id="workflow_dependence_monitor",
        system_id="fleet_router_v2",
        system_version="2.4.1",
        approved_boundary_reference="registry/series_b.json",
        decision_status="review_required",
        notes="Demo evidence record."
    )

    print(f"Created evidence record: {evidence_path}")
