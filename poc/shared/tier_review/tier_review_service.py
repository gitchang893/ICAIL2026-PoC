from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from poc.shared.policy_engine.tier_policy import (
    TierReviewResult,
    build_reclassification_record,
    can_operate_within_tier,
    review_tier,
)


@dataclass
class TierReviewServiceConfig:
    registry_dir: Path
    output_dir: Path
    pretty: bool = True


class TierReviewServiceError(Exception):
    """Raised when the tier review workflow fails."""


class TierReviewService:
    """
    Reviews whether a series remains appropriately classified by risk tier.

    Expected usage:
    - load series registry metadata
    - evaluate proposed or observed context
    - write a tier review record
    - optionally recommend transfer or suspension
    """

    def __init__(self, config: TierReviewServiceConfig) -> None:
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

    def load_series_record(self, series_id: str) -> Dict[str, Any]:
        path = self.config.registry_dir / f"{series_id.lower()}.json"
        if not path.exists():
            raise TierReviewServiceError(f"Series registry not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate(
        self,
        *,
        series_id: str,
        observed_context: Dict[str, Any],
        actor_id: str = "tier_review_service",
    ) -> Dict[str, Any]:
        series_record = self.load_series_record(series_id)
        current_tier = series_record["risk_tier"]

        review: TierReviewResult = review_tier(
            current_tier=current_tier,
            context=observed_context,
        )

        record = build_reclassification_record(
            series_id=series_id,
            current_tier=current_tier,
            context=observed_context,
            actor_id=actor_id,
        )
        record["timestamp"] = self._utc_now()
        record["series_name"] = series_record.get("series_name")
        record["clause_formula"] = series_record.get("clause_formula")
        record["status"] = self._status_from_review(review)
        record["transfer_required"] = review.triggered and review.recommended_tier != current_tier
        record["can_operate_within_current_tier"] = can_operate_within_tier(
            current_tier=current_tier,
            proposed_context=observed_context,
        )
        record["recommended_action"] = self._recommended_action(review, current_tier)
        return record

    def write_review_record(self, record: Dict[str, Any]) -> Path:
        series_id = record["series_id"].lower()
        timestamp = record["timestamp"].replace(":", "-")
        path = self.config.output_dir / f"{series_id}_tier_review_{timestamp}.json"

        with path.open("w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

        return path

    def evaluate_and_write(
        self,
        *,
        series_id: str,
        observed_context: Dict[str, Any],
        actor_id: str = "tier_review_service",
    ) -> Path:
        record = self.evaluate(
            series_id=series_id,
            observed_context=observed_context,
            actor_id=actor_id,
        )
        return self.write_review_record(record)

    def _status_from_review(self, review: TierReviewResult) -> str:
        if review.triggered:
            return "reclassification_review_required"
        return "tier_confirmed"

    def _recommended_action(self, review: TierReviewResult, current_tier: str) -> str:
        if not review.triggered:
            return "remain_in_current_series"

        if current_tier == "minimal" and review.recommended_tier == "limited":
            return "transfer_to_limited_risk_structure"

        if current_tier == "minimal" and review.recommended_tier == "high":
            return "transfer_to_high_risk_structure"

        if current_tier == "limited" and review.recommended_tier == "high":
            return "transfer_to_high_risk_structure"

        if current_tier == "high" and review.recommended_tier in {"limited", "minimal"}:
            return "formal_downward_review_required"

        return "formal_governance_review_required"

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


if __name__ == "__main__":
    service = TierReviewService(
        TierReviewServiceConfig(
            registry_dir=Path("poc/shared/series_registry"),
            output_dir=Path("poc/shared/tier_review/reviews"),
        )
    )

    example = {
        "customer_facing": True,
        "rights_affecting": False,
        "external_effects_allowed": True,
        "safety_critical": False,
        "workflow_dependence_score": 0.94,
        "repeated_incident_count": 1,
        "regulator_attention": False,
    }

    output = service.evaluate_and_write(
        series_id="SeriesB",
        observed_context=example,
    )
    print(f"Wrote tier review record to {output}")
