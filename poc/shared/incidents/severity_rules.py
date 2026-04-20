from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


SEVERITY_LEVELS = ("low", "medium", "high", "critical")


@dataclass
class IncidentSeverityResult:
    severity: str
    reasons: List[str]
    recommended_actions: List[str]


class SeverityRulesError(ValueError):
    """Raised when incident severity inputs are invalid."""


def validate_severity(severity: str) -> None:
    if severity not in SEVERITY_LEVELS:
        raise SeverityRulesError(f"Unsupported severity level: {severity}")


def classify_incident(context: Dict[str, Any]) -> IncidentSeverityResult:
    """
    Classify incident severity from a governance context snapshot.

    Expected keys may include:
    - series_id: str
    - risk_tier: str
    - event_type: str
    - safety_critical: bool
    - rights_affecting: bool
    - customer_facing: bool
    - external_effect: bool
    - data_breach: bool
    - confidentiality_breach: bool
    - regulator_attention: bool
    - repeated_incident_count: int
    - unauthorized_operation: bool
    - boundary_violation: bool
    - production_drift: bool
    """

    risk_tier = str(context.get("risk_tier", "minimal"))
    event_type = str(context.get("event_type", ""))
    repeated_incident_count = int(context.get("repeated_incident_count", 0))

    safety_critical = bool(context.get("safety_critical", False))
    rights_affecting = bool(context.get("rights_affecting", False))
    customer_facing = bool(context.get("customer_facing", False))
    external_effect = bool(context.get("external_effect", False))
    data_breach = bool(context.get("data_breach", False))
    confidentiality_breach = bool(context.get("confidentiality_breach", False))
    regulator_attention = bool(context.get("regulator_attention", False))
    unauthorized_operation = bool(context.get("unauthorized_operation", False))
    boundary_violation = bool(context.get("boundary_violation", False))
    production_drift = bool(context.get("production_drift", False))

    reasons: List[str] = []

    if safety_critical:
        reasons.append("safety_critical_condition_detected")
    if rights_affecting:
        reasons.append("rights_affecting_effect_detected")
    if customer_facing:
        reasons.append("customer_facing_effect_detected")
    if external_effect:
        reasons.append("material_external_effect_detected")
    if data_breach:
        reasons.append("data_breach_detected")
    if confidentiality_breach:
        reasons.append("confidentiality_breach_detected")
    if regulator_attention:
        reasons.append("regulator_attention_detected")
    if unauthorized_operation:
        reasons.append("unauthorized_operation_detected")
    if boundary_violation:
        reasons.append("approved_boundary_violation_detected")
    if production_drift:
        reasons.append("production_drift_detected")
    if repeated_incident_count >= 3:
        reasons.append("repeated_incidents_exceed_threshold")

    severity = "low"

    if risk_tier == "high":
        severity = "medium"

    if customer_facing or external_effect or repeated_incident_count >= 3:
        severity = max_severity(severity, "medium")

    if rights_affecting or data_breach or confidentiality_breach or boundary_violation:
        severity = max_severity(severity, "high")

    if safety_critical or regulator_attention or unauthorized_operation:
        severity = max_severity(severity, "critical")

    if event_type in {"TRIGGER_EVENT_CONFIRMED", "INCIDENT_REPORTED"} and risk_tier == "high" and safety_critical:
        severity = "critical"

    recommended_actions = build_recommended_actions(
        severity=severity,
        risk_tier=risk_tier,
        context=context,
    )

    validate_severity(severity)
    return IncidentSeverityResult(
        severity=severity,
        reasons=reasons,
        recommended_actions=recommended_actions,
    )


def max_severity(current: str, proposed: str) -> str:
    order = {
        "low": 0,
        "medium": 1,
        "high": 2,
        "critical": 3,
    }
    return proposed if order[proposed] > order[current] else current


def build_recommended_actions(
    *,
    severity: str,
    risk_tier: str,
    context: Dict[str, Any],
) -> List[str]:
    actions: List[str] = ["log_incident", "notify_responsible_personnel"]

    if severity in {"medium", "high", "critical"}:
        actions.append("open_review")

    if bool(context.get("boundary_violation", False)):
        actions.append("check_boundary_controls")

    if severity == "high":
        actions.extend([
            "consider_scope_narrowing",
            "collect_supporting_evidence",
        ])

    if severity == "critical":
        actions.extend([
            "suspend_operation",
            "escalate_immediately",
            "preserve_evidence_bundle",
        ])

    if risk_tier == "high":
        if "collect_supporting_evidence" not in actions:
            actions.append("collect_supporting_evidence")
        if bool(context.get("safety_critical", False)):
            if "preserve_evidence_bundle" not in actions:
                actions.append("preserve_evidence_bundle")

    if bool(context.get("production_drift", False)):
        actions.append("start_reclassification_review")

    # Deduplicate while preserving order
    seen = set()
    deduped: List[str] = []
    for action in actions:
        if action not in seen:
            deduped.append(action)
            seen.add(action)
    return deduped


if __name__ == "__main__":
    example_context = {
        "series_id": "SeriesA",
        "risk_tier": "high",
        "event_type": "INCIDENT_REPORTED",
        "safety_critical": True,
        "rights_affecting": False,
        "customer_facing": True,
        "external_effect": True,
        "data_breach": False,
        "confidentiality_breach": False,
        "regulator_attention": False,
        "repeated_incident_count": 1,
        "unauthorized_operation": False,
        "boundary_violation": False,
        "production_drift": False,
    }

    result = classify_incident(example_context)
    print(result)
