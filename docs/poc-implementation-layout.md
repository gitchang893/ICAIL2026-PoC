# PoC Implementation Layout

## Overview

This document outlines a proof-of-concept (PoC) implementation layout for the modular rider architecture.  
The goal is to translate the clause sets (`Cbase`, `Chigh`, and `Ctransparency`) into an executable governance layer that can be used to test deployment gates, change control, incident escalation, evidence preservation, transparency duties, and tier reclassification.

The legal formulas are:

- `OAride = Cbase ∪ Chigh`
- `OAfleet = Cbase ∪ Ctransparency`
- `OAmaint = Cbase only`

The PoC layout below is designed to mirror that structure.

---

## Directory Structure

```text
/poc
  /shared
    series_registry/
      series_a.json
      series_b.json
      series_c.json
    policy_engine/
      boundary_check.py
      tier_policy.py
    change_control/
      change_request.py
      approval_flow.py
    incidents/
      incident_service.py
      severity_rules.py
    events/
      event_store.py
      schemas.py
    overrides/
      override_service.py
    documents/
      document_store.py
    vendors/
      vendor_registry.py
    tier_review/
      tier_review_service.py

  /series_a
    deployment_gatekeeper.py
    odd_expansion_review.py
    trigger_detector.py
    incident_response_orchestrator.py
    evidence_bundle_service.py
    reactivation_gate.py
    audit_readiness_monitor.py
    review_export_service.py

  /series_b
    user_notice_service.py
    ui_guardrails.py
    workflow_dependence_monitor.py
    reclassification_review.py

  /series_c
    minimal_logging_profile.py
    promotion_blocker.py

  /scenarios
    series_a_near_collision.json
    series_a_odd_expansion_request.json
    series_b_routing_dependence_drift.json
    series_b_reclassification_trigger.json
    series_c_customer_facing_promotion_attempt.json

  /docs
    clause-to-control-matrix.md
    state-machines.md
    evidence-model.md
    governance-events.md
