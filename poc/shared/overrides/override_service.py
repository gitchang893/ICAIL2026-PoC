from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from poc.shared.events.event_writer import EventWriter, EventWriterConfig


@dataclass
class OverrideServiceConfig:
    base_dir: Path
    events_base_dir: Optional[Path] = None
    event_schema_path: Optional[Path] = None
    pretty: bool = True

    @property
    def overrides_dir(self) -> Path:
        return self.base_dir / "overrides"

    @property
    def records_dir(self) -> Path:
        return self.overrides_dir / "records"

    @property
    def indexes_dir(self) -> Path:
        return self.overrides_dir / "indexes"


class OverrideServiceError(Exception):
    """Raised when override operations fail."""


class OverrideService:
    """
    Records human override, narrowing, suspension, and termination actions.

    Expected layout:
        base_dir/
          overrides/
            records/
            indexes/
              by_series.json
              by_action.json
              by_status.json
    """

    def __init__(self, config: OverrideServiceConfig) -> None:
        self.config = config
        self.config.records_dir.mkdir(parents=True, exist_ok=True)
        self.config.indexes_dir.mkdir(parents=True, exist_ok=True)

        self.event_writer: Optional[EventWriter] = None
        if self.config.events_base_dir is not None:
            self.event_writer = EventWriter(
                EventWriterConfig(
                    base_dir=self.config.events_base_dir,
                    schema_path=self.config.event_schema_path,
                    pretty=self.config.pretty,
                )
            )

    def create_override(
        self,
        *,
        series_id: str,
        risk_tier: str,
        actor_id: str,
        system_id: str,
        system_version: str,
        approved_boundary_reference: str,
        action_type: str,
        reason: str,
        target: Optional[str] = None,
        notes: str = "",
        override_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        if action_type not in {
            "override_output",
            "narrow_scope",
            "suspend_operation",
            "terminate_use",
            "disable_tool",
            "disable_integration",
        }:
            raise OverrideServiceError(f"Unsupported override action: {action_type}")

        record = {
            "override_id": override_id or self._generate_override_id(series_id),
            "series_id": series_id,
            "risk_tier": risk_tier,
            "actor_id": actor_id,
            "system_id": system_id,
            "system_version": system_version,
            "approved_boundary_reference": approved_boundary_reference,
            "action_type": action_type,
            "target": target,
            "reason": reason,
            "notes": notes,
            "status": "executed",
            "created_at": self._utc_now(),
            "updated_at": self._utc_now(),
            "linked_event_ids": [],
        }
        self._validate_override(record)
        return record

    def write_override(self, record: Dict[str, Any]) -> Path:
        self._validate_override(record)

        path = self.config.records_dir / f'{record["override_id"]}.json'
        self._write_json(path, record)
        self.rebuild_indexes()

        if self.event_writer is not None:
            event_type = (
                "SUSPENSION_EXECUTED"
                if record["action_type"] == "suspend_operation"
                else "OVERRIDE_EXECUTED"
            )
            related_state = (
                "suspended"
                if record["action_type"] == "suspend_operation"
                else "review"
            )
            event = self.event_writer.create_event(
                event_type=event_type,
                series_id=record["series_id"],
                risk_tier=record["risk_tier"],
                actor_type="human",
                actor_id=record["actor_id"],
                system_id=record["system_id"],
                system_version=record["system_version"],
                approved_boundary_reference=record["approved_boundary_reference"],
                related_state=related_state,
                status="resolved",
                notes=record["reason"],
                metadata={
                    "override_id": record["override_id"],
                    "action_type": record["action_type"],
                    "target": record["target"],
                },
            )
            self.event_writer.write_event(event)
            record["linked_event_ids"].append(event["event_id"])
            self._write_json(path, record)
            self.rebuild_indexes()

        return path

    def get_override(self, override_id: str) -> Dict[str, Any]:
        path = self._require_override_path(override_id)
        return self._load_json(path)

    def list_by_series(self, series_id: str) -> List[Dict[str, Any]]:
        return self._query_index("by_series.json", series_id)

    def list_by_action(self, action_type: str) -> List[Dict[str, Any]]:
        return self._query_index("by_action.json", action_type)

    def list_by_status(self, status: str) -> List[Dict[str, Any]]:
        return self._query_index("by_status.json", status)

    def rebuild_indexes(self) -> None:
        by_series: Dict[str, Dict[str, str]] = {}
        by_action: Dict[str, Dict[str, str]] = {}
        by_status: Dict[str, Dict[str, str]] = {}

        for record_path in self.config.records_dir.glob("*.json"):
            record = self._load_json(record_path)
            record_id = record["override_id"]
            record_ref = str(record_path)

            by_series.setdefault(record["series_id"], {})[record_id] = record_ref
            by_action.setdefault(record["action_type"], {})[record_id] = record_ref
            by_status.setdefault(record["status"], {})[record_id] = record_ref

        self._write_json(self.config.indexes_dir / "by_series.json", by_series)
        self._write_json(self.config.indexes_dir / "by_action.json", by_action)
        self._write_json(self.config.indexes_dir / "by_status.json", by_status)

    def _validate_override(self, record: Dict[str, Any]) -> None:
        required = {
            "override_id",
            "series_id",
            "risk_tier",
            "actor_id",
            "system_id",
            "system_version",
            "approved_boundary_reference",
            "action_type",
            "reason",
            "notes",
            "status",
            "created_at",
            "updated_at",
            "linked_event_ids",
        }
        missing = required - set(record.keys())
        if missing:
            raise OverrideServiceError(f"Missing required override fields: {sorted(missing)}")

    def _generate_override_id(self, series_id: str) -> str:
        prefix = series_id.lower().replace("series", "ovr_")
        return f"{prefix}_{uuid4().hex[:8]}"

    def _require_override_path(self, override_id: str) -> Path:
        path = self.config.records_dir / f"{override_id}.json"
        if not path.exists():
            raise OverrideServiceError(f"Override record not found: {override_id}")
        return path

    def _query_index(self, filename: str, bucket: str) -> List[Dict[str, Any]]:
        index_path = self.config.indexes_dir / filename
        if not index_path.exists():
            return []

        index = self._load_json(index_path)
        results: List[Dict[str, Any]] = []

        for _, file_ref in index.get(bucket, {}).items():
            path = Path(file_ref)
            if path.exists():
                results.append(self._load_json(path))

        results.sort(key=lambda r: r.get("created_at", ""))
        return results

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    def _load_json(self, path: Path) -> Dict[str, Any]:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2 if self.config.pretty else None)


if __name__ == "__main__":
    service = OverrideService(
        OverrideServiceConfig(
            base_dir=Path("poc/shared"),
            events_base_dir=Path("poc/shared"),
            event_schema_path=Path("poc/shared/events/event.schema.json"),
        )
    )

    record = service.create_override(
        series_id="SeriesB",
        risk_tier="limited",
        actor_id="human_supervisory_officer_01",
        system_id="fleet_router_v2",
        system_version="2.4.1",
        approved_boundary_reference="registry/series_b.json",
        action_type="narrow_scope",
        reason="Routing dependence exceeded acceptable threshold.",
        target="downtown_dispatch_scope",
        notes="Restricting use pending review.",
    )
    path = service.write_override(record)
    print(f"Wrote override record to {path}")
