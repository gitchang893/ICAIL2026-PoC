from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class ChangeRequestConfig:
    base_dir: Path
    pretty: bool = True

    @property
    def requests_dir(self) -> Path:
        return self.base_dir / "change_requests"

    @property
    def index_dir(self) -> Path:
        return self.requests_dir / "indexes"


class ChangeRequestError(Exception):
    """Raised when change request operations fail."""


class ChangeRequestService:
    """
    Manages material change requests for the PoC governance layer.

    Expected layout:
        base_dir/
          change_requests/
            seriesa/
            seriesb/
            seriesc/
            indexes/
              by_series.json
              by_status.json
    """

    def __init__(self, config: ChangeRequestConfig) -> None:
        self.config = config
        self.config.requests_dir.mkdir(parents=True, exist_ok=True)
        self.config.index_dir.mkdir(parents=True, exist_ok=True)

    def create_request(
        self,
        *,
        series_id: str,
        requested_by: str,
        title: str,
        description: str,
        change_type: str,
        target_system_id: str,
        current_version: Optional[str] = None,
        proposed_version: Optional[str] = None,
        risk_notes: Optional[List[str]] = None,
        request_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        req = {
            "request_id": request_id or self._generate_request_id(series_id),
            "series_id": series_id,
            "requested_by": requested_by,
            "created_at": self._utc_now(),
            "updated_at": self._utc_now(),
            "title": title,
            "description": description,
            "change_type": change_type,
            "target_system_id": target_system_id,
            "current_version": current_version,
            "proposed_version": proposed_version,
            "risk_notes": risk_notes or [],
            "status": "submitted",
            "approvals": [],
            "decision_notes": [],
            "artifacts": [],
        }
        self._validate_request(req)
        return req

    def write_request(self, request: Dict[str, Any]) -> Path:
        self._validate_request(request)
        series_dir = self._series_dir(request["series_id"])
        series_dir.mkdir(parents=True, exist_ok=True)

        path = series_dir / f'{request["request_id"]}.json'
        self._write_json(path, request)
        self.rebuild_indexes()
        return path

    def get_request(self, request_id: str) -> Dict[str, Any]:
        path = self._require_request_path(request_id)
        return self._load_json(path)

    def update_status(
        self,
        request_id: str,
        *,
        new_status: str,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        path = self._require_request_path(request_id)
        req = self._load_json(path)
        req["status"] = new_status
        req["updated_at"] = self._utc_now()
        if note:
            req.setdefault("decision_notes", []).append({
                "timestamp": self._utc_now(),
                "note": note,
            })
        self._validate_request(req)
        self._write_json(path, req)
        self.rebuild_indexes()
        return req

    def attach_artifact(
        self,
        request_id: str,
        artifact_ref: str,
    ) -> Dict[str, Any]:
        path = self._require_request_path(request_id)
        req = self._load_json(path)
        req.setdefault("artifacts", [])
        if artifact_ref not in req["artifacts"]:
            req["artifacts"].append(artifact_ref)
        req["updated_at"] = self._utc_now()
        self._write_json(path, req)
        return req

    def list_by_series(self, series_id: str) -> List[Dict[str, Any]]:
        return self._query_index("by_series.json", series_id)

    def list_by_status(self, status: str) -> List[Dict[str, Any]]:
        return self._query_index("by_status.json", status)

    def rebuild_indexes(self) -> None:
        by_series: Dict[str, Dict[str, str]] = {}
        by_status: Dict[str, Dict[str, str]] = {}

        for req_path in self._iter_request_files():
            req = self._load_json(req_path)
            req_id = req["request_id"]
            req_ref = str(req_path)
            by_series.setdefault(req["series_id"], {})[req_id] = req_ref
            by_status.setdefault(req["status"], {})[req_id] = req_ref

        self._write_json(self.config.index_dir / "by_series.json", by_series)
        self._write_json(self.config.index_dir / "by_status.json", by_status)

    def _validate_request(self, req: Dict[str, Any]) -> None:
        required = {
            "request_id",
            "series_id",
            "requested_by",
            "created_at",
            "updated_at",
            "title",
            "description",
            "change_type",
            "target_system_id",
            "status",
            "approvals",
            "decision_notes",
            "artifacts",
        }
        missing = required - set(req.keys())
        if missing:
            raise ChangeRequestError(f"Missing required fields: {sorted(missing)}")

    def _generate_request_id(self, series_id: str) -> str:
        prefix = series_id.lower().replace("series", "cr_")
        return f"{prefix}_{uuid4().hex[:8]}"

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    def _series_dir(self, series_id: str) -> Path:
        return self.config.requests_dir / series_id.lower()

    def _iter_request_files(self):
        for series_dir in self.config.requests_dir.iterdir():
            if not series_dir.is_dir() or series_dir.name == "indexes":
                continue
            for req_file in series_dir.glob("*.json"):
                yield req_file

    def _find_request_path(self, request_id: str) -> Optional[Path]:
        by_status_path = self.config.index_dir / "by_status.json"
        by_series_path = self.config.index_dir / "by_series.json"

        for index_path in [by_status_path, by_series_path]:
            if not index_path.exists():
                continue
            index = self._load_json(index_path)
            for _, bucket in index.items():
                if request_id in bucket:
                    return Path(bucket[request_id])
        return None

    def _require_request_path(self, request_id: str) -> Path:
        path = self._find_request_path(request_id)
        if path is None:
            raise ChangeRequestError(f"Change request not found: {request_id}")
        return path

    def _query_index(self, filename: str, bucket: str) -> List[Dict[str, Any]]:
        index_path = self.config.index_dir / filename
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

    def _load_json(self, path: Path) -> Dict[str, Any]:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2 if self.config.pretty else None)


if __name__ == "__main__":
    service = ChangeRequestService(ChangeRequestConfig(base_dir=Path("poc/shared/change_control")))
    req = service.create_request(
        series_id="SeriesB",
        requested_by="fleet_ops_manager_01",
        title="Update routing logic weights",
        description="Adjust weights for congestion-aware routing.",
        change_type="routing_logic_update",
        target_system_id="fleet_router_v2",
        current_version="2.4.1",
        proposed_version="2.5.0",
        risk_notes=["May affect dispatch timing and routing outcomes."]
    )
    path = service.write_request(req)
    print(f"Wrote change request to {path}")
