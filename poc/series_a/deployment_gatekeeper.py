from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from poc.shared.events.event_writer import EventWriter, EventWriterConfig


@dataclass
class DeploymentGatekeeperConfig:
    registry_dir: Path
    output_dir: Path
    events_base_dir: Optional[Path] = None
    event_schema_path: Optional[Path] = None
    pretty: bool = True


class DeploymentGatekeeperError(Exception):
    """Raised when deployment gate evaluation fails."""


class DeploymentGatekeeper:
    """
    Series A deployment gate for high-risk autonomous ride-hailing.

    Evaluates whether a deployment or redeployment request satisfies
    the minimum Chigh gate conditions.
    """

    def __init__(self, config: DeploymentGatekeeperConfig) -> None:
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

    def load_series_record(self, series_id: str = "SeriesA") -> Dict[str, Any]:
        path = self.config.registry_dir / f"{series_id.lower()}.json"
        if not path.exists():
            raise DeploymentGatekeeperError(f"Series registry not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate_gate(
        self,
        *,
        requested_by: str,
        system_version: str,
        odd_snapshot: Dict[str, Any],
        responsible_personnel: Dict[str, Optional[str]],
        legal_checks: Dict[str, bool],
        emergency_controls_ready: bool,
        evidence_readiness: bool,
        deployment_mode: str = "deployment",
        notes: str = "",
    ) -> Dict[str, Any]:
        series_record = self.load_series_record("SeriesA")

        failures: List[str] = []

        required_roles = [
            "operations_manager",
            "safety_officer",
            "human_oversight_officer",
            "incident_response_lead",
        ]
        for role in required_roles:
            if not responsible_personnel.get(role):
                failures.append(f"missing_required_personnel:{role}")

        if not odd_snapshot:
            failures.append("missing_odd_snapshot")

        for check_name, passed in legal_checks.items():
            if not passed:
                failures.append(f"legal_check_failed:{check_name}")

        if not emergency_controls_ready:
            failures.append("emergency_controls_not_ready")

        if not evidence_readiness:
            failures.append("evidence_readiness_not_confirmed")

        approved = len(failures) == 0

        gate_record = {
            "gate_id": f"gate_{uuid4().hex[:10]}",
            "series_id": "SeriesA",
            "series_name": series_record["series_name"],
            "risk_tier": "high",
            "deployment_mode": deployment_mode,
            "requested_by": requested_by,
            "system_id": series_record["system_context"]["system_id"],
            "system_version": system_version,
            "approved_boundary_reference": "registry/series_a.json",
            "odd_snapshot": odd_snapshot,
            "responsible_personnel": responsible_personnel,
            "legal_checks": legal_checks,
            "emergency_controls_ready": emergency_controls_ready,
            "evidence_readiness": evidence_readiness,
            "status": "approved" if approved else "denied",
            "failures": failures,
            "created_at": self._utc_now(),
            "notes": notes,
        }
        return gate_record

    def write_gate_record(self, record: Dict[str, Any]) -> Path:
        path = self.config.output_dir / f'{record["gate_id"]}.json'
        with path.open("w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

        if self.event_writer is not None:
            request_event = self.event_writer.create_event(
                event_type="DEPLOYMENT_REQUESTED",
                series_id="SeriesA",
                risk_tier="high",
                actor_type="human",
                actor_id=record["requested_by"],
                system_id=record["system_id"],
                system_version=record["system_version"],
                approved_boundary_reference=record["approved_boundary_reference"],
                related_state="draft",
                status="open",
                notes=f'{record["deployment_mode"]} gate requested',
                metadata={"gate_id": record["gate_id"]},
            )
            self.event_writer.write_event(request_event)

            result_event_type = "DEPLOYMENT_APPROVED" if record["status"] == "approved" else "DEPLOYMENT_DENIED"
            result_event = self.event_writer.create_event(
                event_type=result_event_type,
                series_id="SeriesA",
                risk_tier="high",
                actor_type="human",
                actor_id=record["requested_by"],
                system_id=record["system_id"],
                system_version=record["system_version"],
                approved_boundary_reference=record["approved_boundary_reference"],
                related_state="gated" if record["status"] == "approved" else "draft",
                status="resolved",
                notes=f'Gate result: {record["status"]}',
                metadata={"gate_id": record["gate_id"], "failures": record["failures"]},
            )
            self.event_writer.write_event(result_event)

        return path

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


if __name__ == "__main__":
    gatekeeper = DeploymentGatekeeper(
        DeploymentGatekeeperConfig(
            registry_dir=Path("poc/shared/series_registry"),
            output_dir=Path("poc/series_a/gates"),
            events_base_dir=Path("poc/shared"),
            event_schema_path=Path("poc/shared/events/event.schema.json"),
        )
    )

    record = gatekeeper.evaluate_gate(
        requested_by="ops_manager_01",
        system_version="5.1.0",
        odd_snapshot={
            "geography": ["urban_core_zone_1"],
            "service_hours": ["06:00-23:00"],
            "weather_conditions": ["clear", "light_rain"],
            "road_types": ["city_streets"],
            "speed_constraints": ["<=45mph"],
            "traffic_conditions": ["dense_urban"]
        },
        responsible_personnel={
            "operations_manager": "ops_manager_01",
            "safety_officer": "safety_officer_01",
            "human_oversight_officer": "oversight_01",
            "incident_response_lead": "incident_lead_01",
        },
        legal_checks={
            "city_permit_valid": True,
            "insurance_valid": True,
            "service_zone_authorized": True,
        },
        emergency_controls_ready=True,
        evidence_readiness=True,
        notes="Initial go-live request.",
    )
    path = gatekeeper.write_gate_record(record)
    print(f"Wrote gate record to {path}")
