from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from poc.shared.events.event_writer import EventWriter, EventWriterConfig
from poc.shared.tier_review.tier_review_service import (
    TierReviewService,
    TierReviewServiceConfig,
)


@dataclass
class PromotionBlockerConfig:
    registry_dir: Path
    output_dir: Path
    tier_review_output_dir: Path
    events_base_dir: Optional[Path] = None
    event_schema_path: Optional[Path] = None
    pretty: bool = True


class PromotionBlockerError(Exception):
    """Raised when promotion-blocking logic fails."""


class PromotionBlocker:
    """
    Series C guard against direct migration into customer-facing or higher-risk use.
    """

    def __init__(self, config: PromotionBlockerConfig) -> None:
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        self.tier_review_service = TierReviewService(
            TierReviewServiceConfig(
                registry_dir=self.config.registry_dir,
                output_dir=self.config.tier_review_output_dir,
                pretty=self.config.pretty,
            )
        )

        self.event_writer: Optional[EventWriter] = None
        if self.config.events_base_dir is not None:
            self.event_writer = EventWriter(
                EventWriterConfig(
                    base_dir=self.config.events_base_dir,
                    schema_path=self.config.event_schema_path,
                    pretty=self.config.pretty,
                )
            )

    def evaluate_promotion_attempt(
        self,
        *,
        proposed_use_case: str,
        actor_id: str,
        system_id: str,
        system_version: str,
        customer_facing: bool,
        rights_affecting: bool,
        external_effects_allowed: bool,
        notes: str = "",
    ) -> Dict[str, Any]:
        observed_context = {
            "customer_facing": customer_facing,
            "rights_affecting": rights_affecting,
            "external_effects_allowed": external_effects_allowed,
            "safety_critical": False,
            "workflow_dependence_score": 0.0,
            "repeated_incident_count": 0,
            "regulator_attention": False,
        }

        tier_review = self.tier_review_service.evaluate(
            series_id="SeriesC",
            observed_context=observed_context,
            actor_id=actor_id,
        )

        blocked = tier_review["triggered"]
        record = {
            "promotion_block_id": f"promo_{uuid4().hex[:10]}",
            "series_id": "SeriesC",
            "series_name": "Predictive Maintenance",
            "risk_tier": "minimal",
            "actor_id": actor_id,
            "system_id": system_id,
            "system_version": system_version,
            "proposed_use_case": proposed_use_case,
            "customer_facing": customer_facing,
            "rights_affecting": rights_affecting,
            "external_effects_allowed": external_effects_allowed,
            "approved_boundary_reference": "registry/series_c.json",
            "blocked": blocked,
            "status": "blocked_pending_transfer" if blocked else "within_minimal_boundary",
            "tier_review": tier_review,
            "created_at": self._utc_now(),
            "notes": notes,
        }
        return record

    def write_block_record(self, record: Dict[str, Any]) -> Path:
        path = self.config.output_dir / f'{record["promotion_block_id"]}.json'
        with path.open("w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2 if self.config.pretty else None)

        if record["blocked"]:
            review_path = self.tier_review_service.write_review_record(record["tier_review"])
            if self.event_writer is not None:
                event = self.event_writer.create_event(
                    event_type="RECLASSIFICATION_TRIGGERED",
                    series_id="SeriesC",
                    risk_tier="minimal",
                    actor_type="system",
                    actor_id="promotion_blocker",
                    system_id=record["system_id"],
                    system_version=record["system_version"],
                    approved_boundary_reference=record["approved_boundary_reference"],
                    related_state="active",
                    status="open",
                    notes="Promotion attempt exceeds Series C minimal-risk boundary.",
                    metadata={
                        "promotion_block_id": record["promotion_block_id"],
                        "tier_review_path": str(review_path),
                        "recommended_tier": record["tier_review"]["recommended_tier"],
                    },
                )
                self.event_writer.write_event(event)

        return path

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


if __name__ == "__main__":
    blocker = PromotionBlocker(
        PromotionBlockerConfig(
            registry_dir=Path("poc/shared/series_registry"),
            output_dir=Path("poc/series_c/promotion_blocks"),
            tier_review_output_dir=Path("poc/shared/tier_review/reviews"),
            events_base_dir=Path("poc/shared"),
            event_schema_path=Path("poc/shared/events/event.schema.json"),
        )
    )

    record = blocker.evaluate_promotion_attempt(
        proposed_use_case="customer-facing maintenance guarantee service",
        actor_id="product_owner_01",
        system_id="maint_predictor_v1",
        system_version="1.8.0",
        customer_facing=True,
        rights_affecting=False,
        external_effects_allowed=True,
        notes="Attempted direct use of Series C model in customer-facing workflow.",
    )
    path = blocker.write_block_record(record)
    print(f"Wrote promotion block record to {path}")
