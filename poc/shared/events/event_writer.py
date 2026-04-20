from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

try:
    import jsonschema  # type: ignore
except ImportError:  # pragma: no cover
    jsonschema = None


@dataclass
class EventWriterConfig:
    base_dir: Path
    schema_path: Optional[Path] = None
    pretty: bool = True

    @property
    def events_dir(self) -> Path:
        return self.base_dir / "events"

    @property
    def index_dir(self) -> Path:
        return self.events_dir / "indexes"


class EventWriterError(Exception):
    """Raised when an event cannot be validated or written."""


class EventWriter:
    """
    Writes governance events to disk and maintains simple JSON indexes.

    Expected layout:
        base_dir/
          events/
            series_a/
            series_b/
            series_c/
            indexes/
              by_series.json
              by_type.json
              by_status.json
    """

    def __init__(self, config: EventWriterConfig) -> None:
        self.config = config
        self.config.events_dir.mkdir(parents=True, exist_ok=True)
        self.config.index_dir.mkdir(parents=True, exist_ok=True)

    def create_event(
        self,
        *,
        event_type: str,
        series_id: str,
        risk_tier: str,
        actor_type: str,
        actor_id: str,
        system_id: str,
        system_version: str,
        approved_boundary_reference: str,
        related_state: str,
        status: str = "open",
        notes: str = "",
        linked_evidence_ids: Optional[list[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        event_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        event = {
            "event_id": event_id or self._generate_event_id(series_id),
            "event_type": event_type,
            "series_id": series_id,
            "risk_tier": risk_tier,
            "timestamp": timestamp or self._utc_now(),
            "actor_type": actor_type,
            "actor_id": actor_id,
            "system_id": system_id,
            "system_version": system_version,
            "approved_boundary_reference": approved_boundary_reference,
            "related_state": related_state,
            "status": status,
            "linked_evidence_ids": linked_evidence_ids or [],
            "notes": notes,
            "metadata": metadata or {},
        }
        self._validate_event(event)
        return event

    def write_event(self, event: Dict[str, Any]) -> Path:
        self._validate_event(event)

        series_path = self._series_dir(event["series_id"])
        series_path.mkdir(parents=True, exist_ok=True)

        file_path = series_path / f'{event["event_id"]}.json'
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(event, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

        self._update_indexes(event, file_path)
        return file_path

    def update_event_status(
        self,
        event_path: Path,
        *,
        new_status: str,
        notes_append: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not event_path.exists():
            raise EventWriterError(f"Event file not found: {event_path}")

        with event_path.open("r", encoding="utf-8") as f:
            event = json.load(f)

        old_status = event.get("status")
        event["status"] = new_status
        event.setdefault("metadata", {})
        event["metadata"]["updated_at"] = self._utc_now()
        event["metadata"]["previous_status"] = old_status

        if notes_append:
            existing = event.get("notes", "")
            event["notes"] = f"{existing}\n{notes_append}".strip()

        self._validate_event(event)

        with event_path.open("w", encoding="utf-8") as f:
            json.dump(event, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

        self._rebuild_indexes_for_event(event, event_path, old_status=old_status)
        return event

    def link_evidence(
        self,
        event_path: Path,
        evidence_id: str,
    ) -> Dict[str, Any]:
        if not event_path.exists():
            raise EventWriterError(f"Event file not found: {event_path}")

        with event_path.open("r", encoding="utf-8") as f:
            event = json.load(f)

        event.setdefault("linked_evidence_ids", [])
        if evidence_id not in event["linked_evidence_ids"]:
            event["linked_evidence_ids"].append(evidence_id)

        self._validate_event(event)

        with event_path.open("w", encoding="utf-8") as f:
            json.dump(event, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

        self._update_indexes(event, event_path)
        return event

    def _validate_event(self, event: Dict[str, Any]) -> None:
        required_fields = {
            "event_id",
            "event_type",
            "series_id",
            "risk_tier",
            "timestamp",
            "actor_type",
            "actor_id",
            "system_id",
            "system_version",
            "approved_boundary_reference",
            "related_state",
            "status",
            "linked_evidence_ids",
            "notes",
        }
        missing = required_fields - set(event.keys())
        if missing:
            raise EventWriterError(f"Missing required event fields: {sorted(missing)}")

        if self.config.schema_path and self.config.schema_path.exists() and jsonschema is not None:
            with self.config.schema_path.open("r", encoding="utf-8") as f:
                schema = json.load(f)
            try:
                jsonschema.validate(instance=event, schema=schema)
            except jsonschema.ValidationError as e:  # type: ignore[attr-defined]
                raise EventWriterError(f"Event schema validation failed: {e.message}") from e

    def _series_dir(self, series_id: str) -> Path:
        return self.config.events_dir / series_id.lower()

    def _generate_event_id(self, series_id: str) -> str:
        prefix = series_id.lower().replace("series", "evt_")
        return f"{prefix}_{uuid4().hex[:8]}"

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    def _update_indexes(self, event: Dict[str, Any], path: Path) -> None:
        self._update_index("by_series.json", event["series_id"], event["event_id"], str(path))
        self._update_index("by_type.json", event["event_type"], event["event_id"], str(path))
        self._update_index("by_status.json", event["status"], event["event_id"], str(path))

    def _rebuild_indexes_for_event(
        self,
        event: Dict[str, Any],
        path: Path,
        *,
        old_status: Optional[str],
    ) -> None:
        if old_status and old_status != event["status"]:
            by_status_path = self.config.index_dir / "by_status.json"
            if by_status_path.exists():
                with by_status_path.open("r", encoding="utf-8") as f:
                    index = json.load(f)
                if old_status in index:
                    index[old_status].pop(event["event_id"], None)
                with by_status_path.open("w", encoding="utf-8") as f:
                    json.dump(index, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

        self._update_indexes(event, path)

    def _update_index(self, filename: str, bucket: str, event_id: str, file_path: str) -> None:
        index_path = self.config.index_dir / filename
        if index_path.exists():
            with index_path.open("r", encoding="utf-8") as f:
                index = json.load(f)
        else:
            index = {}

        index.setdefault(bucket, {})
        index[bucket][event_id] = file_path

        with index_path.open("w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2 if self.config.pretty else None)


if __name__ == "__main__":
    base_dir = Path("poc/shared")
    writer = EventWriter(
        EventWriterConfig(
            base_dir=base_dir,
            schema_path=base_dir / "events" / "event.schema.json",
        )
    )

    event = writer.create_event(
        event_type="DEPLOYMENT_REQUESTED",
        series_id="SeriesA",
        risk_tier="high",
        actor_type="human",
        actor_id="ops_manager_01",
        system_id="autonomy_stack",
        system_version="5.1.0",
        approved_boundary_reference="registry/series_a.json",
        related_state="draft",
        notes="Initial deployment request submitted."
    )
    path = writer.write_event(event)
    print(f"Wrote event to {path}")
