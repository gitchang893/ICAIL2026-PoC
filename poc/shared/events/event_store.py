from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class EventStoreConfig:
    base_dir: Path
    pretty: bool = True

    @property
    def events_dir(self) -> Path:
        return self.base_dir / "events"

    @property
    def index_dir(self) -> Path:
        return self.events_dir / "indexes"


class EventStoreError(Exception):
    """Raised when event storage operations fail."""


class EventStore:
    """
    Query and maintenance layer for governance events written by EventWriter.

    Expected layout:
        base_dir/
          events/
            seriesa/
            seriesb/
            seriesc/
            indexes/
              by_series.json
              by_type.json
              by_status.json
    """

    def __init__(self, config: EventStoreConfig) -> None:
        self.config = config
        self.config.events_dir.mkdir(parents=True, exist_ok=True)
        self.config.index_dir.mkdir(parents=True, exist_ok=True)

    def get_event(self, event_path: Path) -> Dict[str, Any]:
        if not event_path.exists():
            raise EventStoreError(f"Event file not found: {event_path}")
        return self._load_json(event_path)

    def get_event_by_id(self, event_id: str) -> Dict[str, Any]:
        path = self._find_event_path(event_id)
        if path is None:
            raise EventStoreError(f"Event not found: {event_id}")
        return self._load_json(path)

    def query_by_series(self, series_id: str) -> List[Dict[str, Any]]:
        return self._query_index("by_series.json", series_id)

    def query_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        return self._query_index("by_type.json", event_type)

    def query_by_status(self, status: str) -> List[Dict[str, Any]]:
        return self._query_index("by_status.json", status)

    def append_note(self, event_id: str, note: str) -> Dict[str, Any]:
        path = self._require_event_path(event_id)
        event = self._load_json(path)
        existing = event.get("notes", "")
        event["notes"] = f"{existing}\n{note}".strip()
        self._write_json(path, event)
        return event

    def set_status(self, event_id: str, new_status: str) -> Dict[str, Any]:
        path = self._require_event_path(event_id)
        event = self._load_json(path)
        old_status = event.get("status")
        event["status"] = new_status
        event.setdefault("metadata", {})
        event["metadata"]["previous_status"] = old_status
        self._write_json(path, event)
        self.rebuild_indexes()
        return event

    def link_evidence(self, event_id: str, evidence_id: str) -> Dict[str, Any]:
        path = self._require_event_path(event_id)
        event = self._load_json(path)
        event.setdefault("linked_evidence_ids", [])
        if evidence_id not in event["linked_evidence_ids"]:
            event["linked_evidence_ids"].append(evidence_id)
        self._write_json(path, event)
        return event

    def rebuild_indexes(self) -> None:
        by_series: Dict[str, Dict[str, str]] = {}
        by_type: Dict[str, Dict[str, str]] = {}
        by_status: Dict[str, Dict[str, str]] = {}

        for event_path in self._iter_event_files():
            event = self._load_json(event_path)
            event_id = event["event_id"]
            event_ref = str(event_path)

            by_series.setdefault(event["series_id"], {})[event_id] = event_ref
            by_type.setdefault(event["event_type"], {})[event_id] = event_ref
            by_status.setdefault(event["status"], {})[event_id] = event_ref

        self._write_json(self.config.index_dir / "by_series.json", by_series)
        self._write_json(self.config.index_dir / "by_type.json", by_type)
        self._write_json(self.config.index_dir / "by_status.json", by_status)

    def summarize(self) -> Dict[str, Any]:
        summary = {
            "series_counts": {},
            "type_counts": {},
            "status_counts": {},
            "total_events": 0,
        }

        for index_name, key in [
            ("by_series.json", "series_counts"),
            ("by_type.json", "type_counts"),
            ("by_status.json", "status_counts"),
        ]:
            path = self.config.index_dir / index_name
            if path.exists():
                index_data = self._load_json(path)
                summary[key] = {k: len(v) for k, v in index_data.items()}

        summary["total_events"] = sum(summary["series_counts"].values())
        return summary

    def _query_index(self, filename: str, bucket: str) -> List[Dict[str, Any]]:
        index_path = self.config.index_dir / filename
        if not index_path.exists():
            return []

        index = self._load_json(index_path)
        results: List[Dict[str, Any]] = []

        for _, file_ref in index.get(bucket, {}).items():
            event_path = Path(file_ref)
            if event_path.exists():
                results.append(self._load_json(event_path))

        results.sort(key=lambda e: e.get("timestamp", ""))
        return results

    def _find_event_path(self, event_id: str) -> Optional[Path]:
        for index_file in ["by_series.json", "by_type.json", "by_status.json"]:
            index_path = self.config.index_dir / index_file
            if not index_path.exists():
                continue
            index = self._load_json(index_path)
            for _, bucket in index.items():
                if event_id in bucket:
                    return Path(bucket[event_id])
        return None

    def _require_event_path(self, event_id: str) -> Path:
        path = self._find_event_path(event_id)
        if path is None:
            raise EventStoreError(f"Event not found: {event_id}")
        return path

    def _iter_event_files(self):
        for series_dir in self.config.events_dir.iterdir():
            if not series_dir.is_dir() or series_dir.name == "indexes":
                continue
            for event_file in series_dir.glob("*.json"):
                yield event_file

    def _load_json(self, path: Path) -> Dict[str, Any]:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2 if self.config.pretty else None)


if __name__ == "__main__":
    store = EventStore(EventStoreConfig(base_dir=Path("poc/shared")))
    store.rebuild_indexes()
    print(store.summarize())
