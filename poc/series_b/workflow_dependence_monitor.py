from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from poc.shared.events.event_writer import EventWriter, EventWriterConfig


@dataclass
class WorkflowDependenceMonitorConfig:
    output_dir: Path
    events_base_dir: Optional[Path] = None
    event_schema_path: Optional[Path] = None
    pretty: bool = True
    default_acceptance_threshold: float = 0.90
    default_review_window_days: int = 14


class WorkflowDependenceMonitorError(Exception):
    """Raised when dependence monitoring fails."""


class WorkflowDependenceMonitor:
    """
    Series B monitor for operational overreliance on AI-assisted outputs.
    """

    def __init__(self, config: WorkflowDependenceMonitorConfig) -> None:
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        self.event_writer: Optional[EventWriter] = None
        if self.config.events_base_dir is not None:
            self.event_writer = EventWriter(
                EventWriterConfig(
                    base_dir=self.config.events_base_dir,
                    schema_path=self.config.event_schema_path,
                    pretty=self.config.pretty,
                )
            )

    def evaluate(
        self,
        *,
        system_id: str,
        system_version: str,
        acceptance_rate_without_edit: float,
        review_window_days: Optional[int] = None,
        volume_count: int,
        external_effect: bool = True,
        notes: str = "",
    ) -> Dict[str, Any]:
        threshold = self.config.default_acceptance_threshold
        window_days = review_window_days or self.config.default_review_window_days

        triggered = acceptance_rate_without_edit >= threshold

        record = {
            "dependence_id": f"dep_{uuid4().hex[:10]}",
            "series_id": "SeriesB",
            "series_name": "Executive Fleet Leasing",
            "risk_tier": "limited",
            "system_id": system_id,
            "system_version": system_version,
            "review_window_days": window_days,
            "acceptance_rate_without_edit": acceptance_rate_without_edit,
            "acceptance_threshold": threshold,
            "volume_count": volume_count,
            "external_effect": external_effect,
            "status": "review_required" if triggered else "within_threshold",
            "triggered": triggered,
            "approved_boundary_reference": "registry/series_b.json",
            "created_at": self._utc_now(),
            "notes": notes,
        }
        return record

    def write_record(self, record: Dict[str, Any]) -> Path:
        path = self.config.output_dir / f'{record["dependence_id"]}.json'
        with path.open("w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

        if record["triggered"] and self.event_writer is not None:
            event = self.event_writer.create_event(
                event_type="WORKFLOW_DEPENDENCE_ALERT",
                series_id="SeriesB",
                risk_tier="limited",
                actor_type="system",
                actor_id="workflow_dependence_monitor",
                system_id=record["system_id"],
                system_version=record["system_version"],
                approved_boundary_reference=record["approved_boundary_reference"],
                related_state="active",
                status="open",
                notes="Operational dependence threshold exceeded.",
                metadata={
                    "dependence_id": record["dependence_id"],
                    "acceptance_rate_without_edit": record["acceptance_rate_without_edit"],
                    "acceptance_threshold": record["acceptance_threshold"],
                    "review_window_days": record["review_window_days"],
                    "volume_count": record["volume_count"],
                },
            )
            self.event_writer.write_event(event)

        return path

    def summarize_recent(
        self,
        *,
        days: int = 30,
    ) -> Dict[str, Any]:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        total = 0
        triggered = 0
        rates: List[float] = []

        for file_path in self.config.output_dir.glob("dep_*.json"):
            with file_path.open("r", encoding="utf-8") as f:
                record = json.load(f)

            created_at = datetime.fromisoformat(record["created_at"])
            if created_at < cutoff:
                continue

            total += 1
            rates.append(float(record["acceptance_rate_without_edit"]))
            if record["triggered"]:
                triggered += 1

        avg_rate = sum(rates) / len(rates) if rates else 0.0
        return {
            "window_days": days,
            "records_evaluated": total,
            "alerts_triggered": triggered,
            "average_acceptance_rate_without_edit": round(avg_rate, 4),
        }

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


if __name__ == "__main__":
    monitor = WorkflowDependenceMonitor(
        WorkflowDependenceMonitorConfig(
            output_dir=Path("poc/series_b/dependence"),
            events_base_dir=Path("poc/shared"),
            event_schema_path=Path("poc/shared/events/event.schema.json"),
        )
    )

    record = monitor.evaluate(
        system_id="fleet_router_v2",
        system_version="2.4.1",
        acceptance_rate_without_edit=0.94,
        volume_count=482,
        notes="Dispatch team is accepting AI-assisted routes with minimal edits."
    )
    path = monitor.write_record(record)
    print(f"Wrote dependence record to {path}")
