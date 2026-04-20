# Evidence Model

## Purpose

This document defines the evidence model for the modular rider architecture.  
The goal is to specify how governance-relevant events, decisions, approvals, incidents, overrides, and reclassification actions are preserved in a structured and reviewable form.

The evidence model supports the clause architecture as follows:

- `Cbase` requires baseline logging, documentation, and incident preservation
- `Chigh` requires enhanced evidence preservation, especially through trigger-action-evidence records
- `Ctransparency` requires notice, documentation, and workflow-dependence records

Accordingly, the evidence layer should support:

- baseline accountability for all series
- enhanced reviewability for high-risk series
- transparency-oriented documentation for limited-risk series

---

## 1. Core Evidence Principles

The evidence model should satisfy the following principles:

(a) **Series specificity**: evidence must be attributable to a defined series;  
(b) **Boundary linkage**: evidence must be linked to the approved use case boundary;  
(c) **Actor traceability**: state-changing actions must identify the responsible human or system actor;  
(d) **Temporal integrity**: evidence objects must preserve timestamps and event order;  
(e) **Governance relevance**: evidence should preserve the facts necessary for review, audit, escalation, or transfer; and  
(f) **Tier sensitivity**: evidence burden should scale with the risk tier of the use case.

---

## 2. Baseline Evidence Object

All series should produce at least a baseline evidence object for governance-relevant events.

### 2.1 Baseline Schema

```json
{
  "evidence_id": "ev_000001",
  "series_id": "SeriesB",
  "series_name": "Executive Fleet Leasing",
  "risk_tier": "limited",
  "event_type": "MATERIAL_CHANGE_SUBMITTED",
  "timestamp": "2026-04-20T12:00:00Z",
  "actor_type": "human",
  "actor_id": "fleet_ops_manager_01",
  "system_id": "fleet_router_v2",
  "system_version": "2.4.1",
  "approved_boundary_reference": "registry/series_b.json",
  "decision_status": "pending_review",
  "artifacts": [],
  "notes": "Routing logic update submitted for review."
}
```

### 2.2 Required Fields

| Field | Purpose |
|---|---|
| `evidence_id` | Unique identifier for the evidence object |
| `series_id` | Identifies the responsible series |
| `risk_tier` | Identifies the governance tier |
| `event_type` | Identifies the governance-relevant event |
| `timestamp` | Preserves temporal order |
| `actor_type` / `actor_id` | Identifies responsible human or system actor |
| `system_id` / `system_version` | Identifies the relevant system state |
| `approved_boundary_reference` | Links the event to the approved use case |
| `decision_status` | Indicates current governance status |
| `artifacts` | Links attached evidence materials |
| `notes` | Human-readable summary |

---

## 3. Evidence Categories by Clause Set

### 3.1 `Cbase` Evidence

The baseline clause set should produce evidence for:

- series designation
- responsible personnel assignment
- deployment approval
- material changes
- incident creation and escalation
- overrides and suspensions
- tier review or reclassification triggers
- vendor/provider changes

### 3.2 `Chigh` Evidence

The high-risk clause set should produce additional evidence for:

- deployment gates
- expansion gates
- reactivation gates
- trigger events
- required responsive actions
- evidence preservation bundles
- audit readiness status
- independent review exports

### 3.3 `Ctransparency` Evidence

The transparency clause set should produce additional evidence for:

- user notice delivery
- scope documentation
- documentation of material changes
- workflow-dependence alerts
- reclassification reviews arising from limited-risk drift

---

## 4. Series-Specific Evidence Requirements

## 4.1 Series A Evidence
## Urban Ride-Hailing (`Cbase ∪ Chigh`)

Series A requires the most robust evidence model.

### Required Series A Evidence Types

- deployment gate record
- operational design domain approval record
- trigger event record
- trigger-action-evidence record
- reactivation clearance record
- audit readiness record
- independent review packet

### Series A Example: Trigger-Action-Evidence Record

```json
{
  "tae_id": "tae_000077",
  "series_id": "SeriesA",
  "risk_tier": "high",
  "trigger": {
    "type": "SAFETY_CRITICAL_EVENT",
    "timestamp": "2026-04-20T12:01:00Z",
    "description": "Near-collision detected at urban intersection."
  },
  "action": {
    "timestamp": "2026-04-20T12:01:05Z",
    "steps": [
      "vehicle_safe_stop",
      "service_suspension",
      "notify_safety_officer",
      "open_incident_case"
    ]
  },
  "evidence": {
    "telemetry_log": "hash_tel_001",
    "route_history": "hash_route_002",
    "software_version": "autonomy_stack_5.1.0",
    "intervention_record": "hash_remote_003",
    "review_record": "hash_review_004"
  },
  "review_status": "pending_reactivation_review"
}
```

## 4.2 Series B Evidence
## Executive Fleet Leasing (`Cbase ∪ Ctransparency`)

Series B requires baseline governance evidence plus transparency-oriented documentation.

### Required Series B Evidence Types

- user notice log
- scope documentation record
- material change documentation
- workflow-dependence alert
- reclassification review record

### Series B Example: Workflow Dependence Record

```json
{
  "evidence_id": "dep_000021",
  "series_id": "SeriesB",
  "risk_tier": "limited",
  "event_type": "WORKFLOW_DEPENDENCE_ALERT",
  "timestamp": "2026-04-20T13:15:00Z",
  "actor_type": "system",
  "actor_id": "workflow_dependence_monitor",
  "system_id": "fleet_router_v2",
  "system_version": "2.4.1",
  "approved_boundary_reference": "registry/series_b.json",
  "decision_status": "review_required",
  "metrics": {
    "acceptance_rate_without_edit": 0.94,
    "review_window_days": 14
  },
  "artifacts": [
    "dependence_report_hash_001"
  ],
  "notes": "Operational reliance threshold exceeded."
}
```

## 4.3 Series C Evidence
## Predictive Maintenance (`Cbase only`)

Series C requires a lighter evidence burden, while preserving baseline accountability.

### Required Series C Evidence Types

- material change record
- material incident record
- baseline version record
- tier review trigger record

### Series C Example: Promotion Block Record

```json
{
  "evidence_id": "promo_000004",
  "series_id": "SeriesC",
  "risk_tier": "minimal",
  "event_type": "RECLASSIFICATION_TRIGGERED",
  "timestamp": "2026-04-20T14:30:00Z",
  "actor_type": "system",
  "actor_id": "tier_review_service",
  "system_id": "maint_predictor_v1",
  "system_version": "1.8.0",
  "approved_boundary_reference": "registry/series_c.json",
  "decision_status": "blocked_pending_transfer",
  "artifacts": [
    "proposal_hash_001",
    "tier_review_hash_002"
  ],
  "notes": "Attempted customer-facing deployment exceeds minimal-risk boundary."
}
```

---

## 5. Event-to-Evidence Mapping

The following table maps common governance events to expected evidence outputs.

| Event | Minimum Evidence Output |
|---|---|
| `DEPLOYMENT_REQUESTED` | deployment approval record |
| `MATERIAL_CHANGE_SUBMITTED` | change request record |
| `INCIDENT_REPORTED` | incident ticket |
| `OVERRIDE_EXECUTED` | override record |
| `RECLASSIFICATION_TRIGGERED` | tier review record |
| `AUDIT_EXPORT_REQUESTED` | audit/export record |
| `USER_NOTICE_DELIVERED` | notice log |
| `TRIGGER_EVENT_CONFIRMED` | trigger-action-evidence record for Series A |

---

## 6. Evidence Storage Model

A PoC implementation should separate logical evidence structure from physical storage.

### 6.1 Logical Layers

- **event layer**  
  Stores timestamped governance events.

- **decision layer**  
  Stores approvals, overrides, suspensions, narrowing decisions, and review outcomes.

- **artifact layer**  
  Stores linked files, logs, hashes, reports, and supporting objects.

- **series metadata layer**  
  Stores use case boundary, responsible personnel, and risk tier references.

### 6.2 Suggested Layout

```text
/evidence
  /events
    2026-04-20-event-0001.json
    2026-04-20-event-0002.json
  /decisions
    2026-04-20-decision-0001.json
  /artifacts
    telemetry_hash_001.bin
    dependence_report_hash_001.pdf
  /series_refs
    series_a.json
    series_b.json
    series_c.json
```

---

## 7. Chain-of-Custody and Integrity

The PoC should preserve basic evidentiary integrity, especially for Series A.

### 7.1 Minimum Integrity Controls

- unique evidence identifiers
- immutable timestamps where practicable
- actor attribution
- linked artifact hashes
- append-only event history where practicable
- review and export logs

### 7.2 Suggested Integrity Metadata

```json
{
  "evidence_id": "ev_000001",
  "created_at": "2026-04-20T12:00:00Z",
  "created_by": "incident_service",
  "artifact_hashes": [
    "sha256:abc123",
    "sha256:def456"
  ],
  "previous_evidence": "ev_000000",
  "export_history": [
    {
      "timestamp": "2026-04-21T09:00:00Z",
      "recipient": "internal_audit",
      "purpose": "incident_review"
    }
  ]
}
```

### 7.3 Governance Meaning

These controls do not necessarily make the evidence legally conclusive in all contexts, but they make the governance layer reviewable, traceable, and more defensible.

---

## 8. Export and Review Profiles

Different series may require different evidence export profiles.

### 8.1 Series A Export Profile

Series A exports may include:

- trigger-action-evidence record
- incident packet
- audit packet
- regulator-ready review materials

### 8.2 Series B Export Profile

Series B exports may include:

- user notice record
- scope documentation
- workflow-dependence review memo
- change history

### 8.3 Series C Export Profile

Series C exports may include:

- baseline incident record
- material change record
- transfer or promotion block record

---

## 9. PoC Implementation Notes

Recommended implementation files:

```text
evidence_model/
  schemas/
    baseline_event.schema.json
    tae_record.schema.json
    review_record.schema.json
  writers/
    event_writer.py
    decision_writer.py
    artifact_linker.py
  exports/
    audit_export.py
    regulator_export.py
    internal_review_export.py
  integrity/
    hash_util.py
    chain_index.py
```

Recommended functions:

- `create_evidence_object()`
- `link_artifact()`
- `write_decision_record()`
- `build_trigger_action_evidence_record()`
- `export_review_packet()`

---

## 10. Interpretation

The evidence model is intended to operationalize the reviewability and accountability assumptions embedded in the rider architecture.

In this formulation:

- `Cbase` yields baseline governance evidence
- `Chigh` yields enhanced high-risk evidentiary records
- `Ctransparency` yields limited-risk notice and documentation evidence

The evidence layer therefore functions as the documentary counterpart to the clause-to-control matrix and the state-machine model.  
It shows how the legal architecture can be translated into structured governance records suitable for internal review, audit, escalation, and, where necessary, external examination.
