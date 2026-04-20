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
    /series_registry
      series_a.json
      series_b.json
      series_c.json
    /policy_engine
      boundary_check.py
      tier_policy.py
    /change_control
      change_request.py
      approval_flow.py
    /incidents
      incident_service.py
      severity_rules.py
    /events
      event_store.py
      schemas.py
    /overrides
      override_service.py
    /documents
      document_store.py
    /vendors
      vendor_registry.py
    /tier_review
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
```

---

## 1. Shared Layer (`Cbase` Runtime)

The `/shared` directory implements the common baseline governance layer corresponding to `Cbase`.

### `series_registry/`

Stores the approved use case boundary, risk tier, responsible personnel, and governance metadata for each series.

Example responsibilities:

- approved scope
- responsible humans
- risk-tier assignment
- boundary metadata

### `policy_engine/`

Validates whether a deployment, action, or change request falls within the approved boundary.

Key functions:

- `check_boundary()`
- `check_risk_tier()`
- `deny_unapproved_use()`

### `change_control/`

Implements documented review of material changes.

Key functions:

- register a change request
- assign reviewer
- approve / reject / defer
- preserve change history

### `incidents/`

Handles Material Incidents and escalation.

Key functions:

- create incident ticket
- classify severity
- notify responsible personnel
- link incident to evidence and actions

### `events/`

Provides baseline event logging and evidence support.

Key functions:

- log approvals
- log overrides
- log incidents
- log reclassification triggers
- preserve timestamped event objects

### `overrides/`

Supports human override, narrowing, suspension, and termination.

Key functions:

- suspend deployment
- narrow approved scope
- override AI-assisted outputs
- terminate use

### `documents/`

Stores governance memos, documentation, scope notices, and internal transparency records.

### `vendors/`

Tracks third-party providers and associated governance metadata.

### `tier_review/`

Determines whether the current use case still fits the assigned series and risk tier.

---

## 2. Series A Module (`Chigh` Overlay)

The `/series_a` directory implements the high-risk control overlay corresponding to `Chigh`.

### `deployment_gatekeeper.py`

Implements deployment gate logic before go-live or redeployment.

### `odd_expansion_review.py`

Implements gate review for expansion of the operational design domain.

### `trigger_detector.py`

Detects trigger events such as:

- collision
- near-collision
- emergency stop
- ODD deviation
- regulator inquiry

### `incident_response_orchestrator.py`

Runs the required action sequence after a trigger event.

### `evidence_bundle_service.py`

Builds a formal Trigger-Action-Evidence bundle for safety and audit use.

### `reactivation_gate.py`

Blocks return to service after suspension until formal clearance.

### `audit_readiness_monitor.py`

Tracks whether Series A is in a state of audit readiness.

### `review_export_service.py`

Exports structured materials for audit, independent review, litigation, or regulator response.

---

## 3. Series B Module (`Ctransparency` Overlay)

The `/series_b` directory implements the limited-risk transparency overlay corresponding to `Ctransparency`.

### `user_notice_service.py`

Provides notices to internal users that outputs are AI-assisted.

### `ui_guardrails.py`

Prevents outputs from being treated as final or self-authorizing in workflows requiring human review.

### `workflow_dependence_monitor.py`

Tracks operational dependence on AI outputs and flags overreliance.

### `reclassification_review.py`

Supports review if the system begins to function like a higher-risk use case.

---

## 4. Series C Module (`Cbase only`)

The `/series_c` directory implements a light-weight minimal-risk profile using `Cbase` only.

### `minimal_logging_profile.py`

Applies baseline logging without the additional overhead of `Chigh` or `Ctransparency`.

### `promotion_blocker.py`

Blocks attempts to migrate Series C directly into customer-facing, rights-affecting, or high-risk functions without reclassification.

---

## 5. Scenario Replay Files

The `/scenarios` directory stores replayable governance scenarios.

These scenarios are useful for demonstrating that the rider architecture can be executed as a governance runtime, rather than remaining purely descriptive.

Illustrative scenarios include:

- Series A near-collision leading to suspension and evidence capture
- Series A ODD expansion request requiring gate review
- Series B routing dependence drift requiring reassessment
- Series B reclassification trigger into a higher-risk profile
- Series C attempted promotion into customer-facing use, blocked pending transition

---

## 6. Documentation Layer

The `/docs` directory stores architecture-facing and legal-facing explanation files.

Recommended documents:

- `clause-to-control-matrix.md`
- `state-machines.md`
- `evidence-model.md`
- `governance-events.md`

These files help map the legal structure to the implementation structure.

---

## 7. Design Principles

This PoC should follow the following principles:

(a) **Clause fidelity**: each control should map back to an identifiable clause or clause set;  
(b) **Series separation**: each series should retain its own scope, tier logic, and escalation path;  
(c) **Human accountability**: no control should imply that final responsibility has shifted to the AI System;  
(d) **Reclassification awareness**: the PoC should detect drift into a higher-risk governance tier; and  
(e) **Evidence preservation**: event logs, approvals, overrides, and incidents should be recorded in a reviewable form.

---

## 8. Suggested Next Build Order

A practical implementation order is:

### Phase 1

Build the shared `Cbase` runtime:

- `series_registry`
- `policy_engine`
- `change_control`
- `incidents`
- `events`
- `tier_review`

### Phase 2

Add the series-specific overlays:

- Series A `Chigh`
- Series B `Ctransparency`
- Series C minimal-risk constraints

### Phase 3

Add scenario replay and exported evidence packets.

---

## 9. Interpretation

This layout is intended to show that the rider architecture can be implemented as a modular governance runtime.  
It is not merely a software layout; it is a structural translation of the legal clause architecture into an executable proof-of-concept.

Under this approach:

- `Cbase` becomes the shared governance runtime
- `Chigh` becomes a high-risk overlay
- `Ctransparency` becomes a limited-risk transparency overlay

The PoC therefore mirrors the same modular structure used in the paper and in the rider drafts.
