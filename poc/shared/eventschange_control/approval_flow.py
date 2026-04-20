from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from poc.shared.change_control.change_request import ChangeRequestService, ChangeRequestConfig


@dataclass
class ApprovalFlowConfig:
    base_dir: Path
    pretty: bool = True

    @property
    def approvals_dir(self) -> Path:
        return self.base_dir / "approvals"


class ApprovalFlowError(Exception):
    """Raised when approval flow operations fail."""


class ApprovalFlowService:
    """
    Adds approval and decision workflow on top of change requests.

    The service:
    - records approvers
    - records approve/reject/defer decisions
    - updates request status
    """

    def __init__(self, config: ApprovalFlowConfig) -> None:
        self.config = config
        self.config.approvals_dir.mkdir(parents=True, exist_ok=True)
        self.change_requests = ChangeRequestService(
            ChangeRequestConfig(base_dir=self.config.base_dir, pretty=config.pretty)
        )

    def add_approver(
        self,
        request_id: str,
        *,
        approver_id: str,
        approver_role: str,
    ) -> Dict[str, Any]:
        req = self.change_requests.get_request(request_id)
        req.setdefault("approvals", [])

        exists = any(
            a["approver_id"] == approver_id
            for a in req["approvals"]
        )
        if not exists:
            req["approvals"].append({
                "approver_id": approver_id,
                "approver_role": approver_role,
                "decision": "pending",
                "decision_at": None,
                "decision_note": None,
            })
            req["updated_at"] = self._utc_now()
            self._write_request(req)

        return req

    def record_decision(
        self,
        request_id: str,
        *,
        approver_id: str,
        decision: str,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        if decision not in {"approved", "rejected", "deferred"}:
            raise ApprovalFlowError(f"Unsupported decision: {decision}")

        req = self.change_requests.get_request(request_id)
        found = False

        for approval in req.get("approvals", []):
            if approval["approver_id"] == approver_id:
                approval["decision"] = decision
                approval["decision_at"] = self._utc_now()
                approval["decision_note"] = note
                found = True
                break

        if not found:
            raise ApprovalFlowError(f"Approver not assigned to request: {approver_id}")

        req["updated_at"] = self._utc_now()
        req.setdefault("decision_notes", []).append({
            "timestamp": self._utc_now(),
            "approver_id": approver_id,
            "decision": decision,
            "note": note,
        })

        req["status"] = self._derive_request_status(req)
        self._write_request(req)
        self._write_approval_record(req, approver_id, decision, note)
        return req

    def summarize_request(self, request_id: str) -> Dict[str, Any]:
        req = self.change_requests.get_request(request_id)
        approvals = req.get("approvals", [])

        return {
            "request_id": req["request_id"],
            "series_id": req["series_id"],
            "title": req["title"],
            "status": req["status"],
            "total_approvers": len(approvals),
            "approved": sum(1 for a in approvals if a["decision"] == "approved"),
            "rejected": sum(1 for a in approvals if a["decision"] == "rejected"),
            "deferred": sum(1 for a in approvals if a["decision"] == "deferred"),
            "pending": sum(1 for a in approvals if a["decision"] == "pending"),
        }

    def _derive_request_status(self, req: Dict[str, Any]) -> str:
        approvals = req.get("approvals", [])
        if not approvals:
            return "submitted"

        decisions = {a["decision"] for a in approvals}
        if "rejected" in decisions:
            return "rejected"
        if all(dec == "approved" for dec in decisions):
            return "approved"
        if "deferred" in decisions:
            return "deferred"
        return "pending_review"

    def _write_request(self, req: Dict[str, Any]) -> None:
        series_dir = self.config.base_dir / "change_requests" / req["series_id"].lower()
        series_dir.mkdir(parents=True, exist_ok=True)
        path = series_dir / f'{req["request_id"]}.json'
        with path.open("w", encoding="utf-8") as f:
            json.dump(req, f, ensure_ascii=False, indent=2 if self.config.pretty else None)
        self.change_requests.rebuild_indexes()

    def _write_approval_record(
        self,
        req: Dict[str, Any],
        approver_id: str,
        decision: str,
        note: Optional[str],
    ) -> None:
        record = {
            "request_id": req["request_id"],
            "series_id": req["series_id"],
            "approver_id": approver_id,
            "decision": decision,
            "decision_at": self._utc_now(),
            "note": note,
            "request_status_after_decision": req["status"],
        }
        path = self.config.approvals_dir / f'{req["request_id"]}_{approver_id}.json'
        with path.open("w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


if __name__ == "__main__":
    service = ApprovalFlowService(ApprovalFlowConfig(base_dir=Path("poc/shared/change_control")))

    # Assumes a request already exists
    request_id = "cr_b_demo1234"

    try:
        service.add_approver(
            request_id,
            approver_id="compliance_liaison_01",
            approver_role="Compliance Liaison",
        )
        service.record_decision(
            request_id,
            approver_id="compliance_liaison_01",
            decision="approved",
            note="No additional legal issues identified."
        )
        print(service.summarize_request(request_id))
    except Exception as exc:
        print(f"Demo skipped: {exc}")
