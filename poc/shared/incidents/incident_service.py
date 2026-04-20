from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from poc.shared.events.event_writer import EventWriter, EventWriterConfig
from poc.shared.incidents.severity_rules import classify_incident


@dataclass
class IncidentServiceConfig:
    base_dir: Path
    events_base_dir: Optional[Path] = None
    event_schema_path: Optional[Path] = None
    pretty: bool = True

    @property
    def incidents_dir(self) -> Path:
        return self.base_dir / "incidents"

    @property
    def cases_dir(self) -> Path:
        return self.incidents_dir / "cases"

    @property
    def indexes_dir(self) -> Path:
        return self.incidents_dir / "indexes"


class IncidentServiceError(Exception):
    """Raised when incident operations fail."""


class IncidentService:
    """
    Incident management layer for the governance PoC.

    Expected layout:
        base_dir/
          incidents/
            cases/
            indexes/
              by_series.json
              by_status.json
              by_severity.json
    """

    def __init__(self, config: IncidentServiceConfig) -> None:
        self.config = config
        self.config.cases_dir.mkdir(parents=True, exist_ok=True)
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

    def create_incident(
        self,
        *,
        series_id: str,
        series_name: str,
        risk_tier: str,
        reported_by: str,
        title: str,
        description: str,
        system_id: str,
        system_version: str,
        approved_boundary_reference: str,
        context: Optional[Dict[str, Any]] = None,
        incident_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        ctx = dict(context or {})
        ctx.setdefault("series_id", series_id)
        ctx.setdefault("risk_tier", risk_tier)
        ctx.setdefault("event_type", "INCIDENT_REPORTED")

        severity_result = classify_incident(ctx)

        incident = {
            "incident_id": incident_id or self._generate_incident_id(series_id),
            "series_id": series_id,
            "series_name": series_name,
            "risk_tier": risk_tier,
            "reported_by": reported_by,
            "title": title,
            "description": description,
            "system_id": system_id,
            "system_version": system_version,
            "approved_boundary_reference": approved_boundary_reference,
            "severity": severity_result.severity,
            "severity_reasons": severity_result.reasons,
            "recommended_actions": severity_result.recommended_actions,
            "status": "open",
            "context": ctx,
            "linked_evidence_ids": [],
            "linked_event_ids": [],
            "response_actions": [],
            "created_at": self._utc_now(),
            "updated_at": self._utc_now(),
        }

        self._validate_incident(incident)
        return incident

    def write_incident(self, incident: Dict[str, Any]) -> Path:
        self._validate_incident(incident)

        path = self.config.cases_dir / f'{incident["incident_id"]}.json'
        self._write_json(path, incident)
        self.rebuild_indexes()

        if self.event_writer is not None:
            incident_event = self.event_writer.create_event(
                event_type="INCIDENT_REPORTED",
                series_id=incident["series_id"],
                risk_tier=incident["risk_tier"],
                actor_type="human",
                actor_id=incident["reported_by"],
                system_id=incident["system_id"],
                system_version=incident["system_version"],
                approved_boundary_reference=incident["approved_boundary_reference"],
                related_state="active",
                status="open",
                notes=incident["title"],
                metadata={
                    "incident_id": incident["incident_id"],
                    "severity": incident["severity"],
                },
            )
            event_path = self.event_writer.write_event(incident_event)
            incident["linked_event_ids"].append(incident_event["event_id"])
            self._write_json(path, incident)
            self.rebuild_indexes()

        return path

    def get_incident(self, incident_id: str) -> Dict[str, Any]:
        path = self._require_incident_path(incident_id)
        return self._load_json(path)

    def escalate_incident(
        self,
        incident_id: str,
        *,
        escalated_by: str,
        escalation_note: str,
    ) -> Dict[str, Any]:
        path = self._require_incident_path(incident_id)
        incident = self._load_json(path)

        incident["status"] = "escalated"
        incident["updated_at"] = self._utc_now()
        incident.setdefault("response_actions", []).append({
            "timestamp": self._utc_now(),
            "actor_id": escalated_by,
            "action": "incident_escalated",
            "note": escalation_note,
        })

        if self.event_writer is not None:
            event = self.event_writer.create_event(
                event_type="INCIDENT_ESCALATED",
                series_id=incident["series_id"],
                risk_tier=incident["risk_tier"],
                actor_type="human",
                actor_id=escalated_by,
                system_id=incident["system_id"],
                system_version=incident["system_version"],
                approved_boundary_reference=incident["approved_boundary_reference"],
                related_state="review",
                status="escalated",
                notes=escalation_note,
                linked_evidence_ids=incident.get("linked_evidence_ids", []),
                metadata={"incident_id": incident_id},
            )
            self.event_writer.write_event(event)
            incident.setdefault("linked_event_ids", []).append(event["event_id"])

        self._write_json(path, incident)
        self.rebuild_indexes()
        return incident

    def resolve_incident(
        self,
        incident_id: str,
        *,
        resolved_by: str,
        resolution_note: str,
    ) -> Dict[str, Any]:
        path = self._require_incident_path(incident_id)
        incident = self._load_json(path)

        incident["status"] = "resolved"
        incident["updated_at"] = self._utc_now()
        incident.setdefault("response_actions", []).append({
            "timestamp": self._utc_now(),
            "actor_id": resolved_by,
            "action": "incident_resolved",
            "note": resolution_note,
        })

        if self.event_writer is not None:
            event = self.event_writer.create_event(
                event_type="INCIDENT_RESOLVED",
                series_id=incident["series_id"],
                risk_tier=incident["risk_tier"],
                actor_type="human",
                actor_id=resolved_by,
                system_id=incident["system_id"],
                system_version=incident["system_version"],
                approved_boundary_reference=incident["approved_boundary_reference"],
                related_state="review",
                status="resolved",
                notes=resolution_note,
                linked_evidence_ids=incident.get("linked_evidence_ids", []),
                metadata={"incident_id": incident_id},
            )
            self.event_writer.write_event(event)
            incident.setdefault("linked_event_ids", []).append(event["event_id"])

        self._write_json(path, incident)
        self.rebuild_indexes()
        return incident

    def link_evidence(
        self,
        incident_id: str,
        evidence_id: str,
    ) -> Dict[str, Any]:
        path = self._require_incident_path(incident_id)
        incident = self._load_json(path)

        incident.setdefault("linked_evidence_ids", [])
        if evidence_id not in incident["linked_evidence_ids"]:
            incident["linked_evidence_ids"].append(evidence_id)
            incident["updated_at"] = self._utc_now()

        self._write_json(path, incident)
        return incident

    def list_by_series(self, series_id: str) -> List[Dict[str, Any]]:
        return self._query_index("by_series.json", series_id)

    def list_by_status(self, status: str) -> List[Dict[str, Any]]:
        return self._query_index("by_status.json", status)

    def list_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        return self._query_index("by_severity.json", severity)

    def rebuild_indexes(self) -> None:
        by_series: Dict[str, Dict[str, str]] = {}
        by_status: Dict[str, Dict[str, str]] = {}
        by_severity: Dict[str, Dict[str, str]] = {}

        for case_path in self.config.cases_dir.glob("*.json"):
            incident = self._load_json(case_path)
            inc_id = incident["incident_id"]
            inc_ref = str(case_path)

            by_series.setdefault(incident["series_id"], {})[inc_id] = inc_ref
            by_status.setdefault(incident["status"], {})[inc_id] = inc_ref
            by_severity.setdefault(incident["severity"], {})[inc_id] = inc_ref

        self._write_json(self.config.indexes_dir / "by_series.json", by_series)
        self._write_json(self.config.indexes_dir / "by_status.json", by_status)
        self._write_json(self.config.indexes_dir / "by_severity.json", by_severity)

    def _validate_incident(self, incident: Dict[str, Any]) -> None:
        required = {
            "incident_id",
            "series_id",
            "series_name",
            "risk_tier",
            "reported_by",
            "title",
            "description",
            "system_id",
            "system_version",
            "approved_boundary_reference",
            "severity",
            "severity_reasons",
            "recommended_actions",
            "status",
            "context",
            "linked_evidence_ids",
            "linked_event_ids",
            "response_actions",
            "created_at",
            "updated_at",
        }
        missing = required - set(incident.keys())
        if missing:
            raise IncidentServiceError(f"Missing required incident fields: {sorted(missing)}")

    def _generate_incident_id(self, series_id: str) -> str:
        prefix = series_id.lower().replace("series", "inc_")
        return f"{prefix}_{uuid4().hex[:8]}"

    def _require_incident_path(self, incident_id: str) -> Path:
        path = self.config.cases_dir / f"{incident_id}.json"
        if not path.exists():
            raise IncidentServiceError(f"Incident not found: {incident_id}")
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

        results.sort(key=lambda i: i.get("created_at", ""))
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
    service = IncidentService(
        IncidentServiceConfig(
            base_dir=Path("poc/shared"),
            events_base_dir=Path("poc/shared"),
            event_schema_path=Path("poc/shared/events/event.schema.json"),
        )
    )

    incident = service.create_incident(
        series_id="SeriesA",
        series_name="Urban Ride-Hailing",
        risk_tier="high",
        reported_by="safety_officer_01",
        title="Near collision detected",
        description="Autonomous vehicle executed emergency stop at intersection.",
        system_id="autonomy_stack",
        system_version="5.1.0",
        approved_boundary_reference="registry/series_a.json",
        context={
            "safety_critical": True,
            "customer_facing": True,
            "external_effect": True
        },
    )
    path = service.write_incident(incident)
    print(f"Wrote incident to {path}")
