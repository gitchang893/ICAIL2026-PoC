from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


RISK_TIERS = ("minimal", "limited", "high")


@dataclass
class TierReviewResult:
    current_tier: str
    recommended_tier: str
    triggered: bool
    reasons: List[str]


class TierPolicyError(ValueError):
    """Raised when the tier policy receives invalid inputs."""


def validate_tier(tier: str) -> None:
    if tier not in RISK_TIERS:
        raise TierPolicyError(f"Unsupported risk tier: {tier}")


def infer_recommended_tier(context: Dict[str, Any]) -> str:
    """
    Infer the recommended risk tier from observed context.

    Expected keys in `context` may include:
    - customer_facing: bool
    - rights_affecting: bool
    - external_effects_allowed: bool
    - safety_critical: bool
    - workflow_dependence_score: float
    - repeated_incident_count: int
    - regulator_attention: bool
    """

    customer_facing = bool(context.get("customer_facing", False))
    rights_affecting = bool(context.get("rights_affecting", False))
    external_effects_allowed = bool(context.get("external_effects_allowed", False))
    safety_critical = bool(context.get("safety_critical", False))
    regulator_attention = bool(context.get("regulator_attention", False))
    workflow_dependence_score = float(context.get("workflow_dependence_score", 0.0))
    repeated_incident_count = int(context.get("repeated_incident_count", 0))

    if safety_critical or rights_affecting or regulator_attention:
        return "high"

    if customer_facing or external_effects_allowed:
        return "limited"

    if workflow_dependence_score >= 0.90 or repeated_incident_count >= 3:
        return "limited"

    return "minimal"


def review_tier(
    current_tier: str,
    context: Dict[str, Any],
) -> TierReviewResult:
    """
    Review whether the current series tier remains appropriate.

    Returns a TierReviewResult with:
    - current_tier
    - recommended_tier
    - triggered
    - reasons
    """
    validate_tier(current_tier)
    recommended_tier = infer_recommended_tier(context)

    reasons: List[str] = []

    if bool(context.get("safety_critical", False)):
        reasons.append("safety_critical_condition_detected")

    if bool(context.get("rights_affecting", False)):
        reasons.append("rights_affecting_use_detected")

    if bool(context.get("customer_facing", False)):
        reasons.append("customer_facing_use_detected")

    if bool(context.get("external_effects_allowed", False)):
        reasons.append("external_effects_detected")

    if bool(context.get("regulator_attention", False)):
        reasons.append("regulator_attention_detected")

    if float(context.get("workflow_dependence_score", 0.0)) >= 0.90:
        reasons.append("material_workflow_dependence_detected")

    if int(context.get("repeated_incident_count", 0)) >= 3:
        reasons.append("repeated_incidents_exceed_threshold")

    triggered = recommended_tier != current_tier

    return TierReviewResult(
        current_tier=current_tier,
        recommended_tier=recommended_tier,
        triggered=triggered,
        reasons=reasons,
    )


def can_operate_within_tier(
    current_tier: str,
    proposed_context: Dict[str, Any],
) -> bool:
    """
    Return True if the proposed context is compatible with the current tier.
    """
    validate_tier(current_tier)
    recommended_tier = infer_recommended_tier(proposed_context)

    tier_order = {
        "minimal": 0,
        "limited": 1,
        "high": 2,
    }
    return tier_order[recommended_tier] <= tier_order[current_tier]


def build_reclassification_record(
    series_id: str,
    current_tier: str,
    context: Dict[str, Any],
    actor_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a simple record object for use by tier_review_service.
    """
    result = review_tier(current_tier=current_tier, context=context)

    return {
        "series_id": series_id,
        "current_tier": result.current_tier,
        "recommended_tier": result.recommended_tier,
        "triggered": result.triggered,
        "reasons": result.reasons,
        "actor_id": actor_id,
        "context_snapshot": context,
    }


if __name__ == "__main__":
    example_context = {
        "customer_facing": True,
        "rights_affecting": False,
        "external_effects_allowed": True,
        "safety_critical": False,
        "workflow_dependence_score": 0.92,
        "repeated_incident_count": 1,
        "regulator_attention": False,
    }

    record = build_reclassification_record(
        series_id="SeriesB",
        current_tier="limited",
        context=example_context,
        actor_id="tier_review_service",
    )
    print(record)
