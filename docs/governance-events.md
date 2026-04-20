# Governance Events

## Purpose

This document defines the governance event model for the modular rider architecture.  
The goal is to describe the event types that drive the executable governance layer, including deployment decisions, material changes, incidents, overrides, reclassification triggers, audit exports, and related actions.

The governance event model supports the clause architecture as follows:

- `Cbase` requires baseline event capture for approvals, changes, incidents, overrides, and tier review
- `Chigh` requires enhanced event capture for trigger-action-evidence workflows, gatekeeping, suspension, and reactivation
- `Ctransparency` requires event capture for user notice, documentation changes, and workflow-dependence monitoring

Accordingly, the event layer should support:

- consistent event capture across all series
- risk-tier-specific escalation logic
- structured linkage between events, state transitions, and evidence objects

---

## 1. Core Event Principles

The governance event model should satisfy the following principles:

(a) **Series attribution**: every event must be attributable to a defined series;  
(b) **Type clarity**: event types should be explicit and machine-readable;  
(c) **Boundary relevance**: events should be linkable to the approved use case boundary;  
(d) **Actor traceability**: the initiating human or system actor should be identifiable;  
(e) **State relevance**: events should be usable to drive or explain state transitions; and  
(f) **Evidence linkage**: events should be capable of linking to evidence objects and artifacts.

---

## 2. Baseline Event Object

All governance events should conform to a common baseline structure.

### 2.1 Baseline Schema

```json
{
  "event_id": "evt_000001",
  "event_type": "DEPLOYMENT_REQUESTED",
  "series_id": "SeriesA",
  "risk_tier": "high",
  "timestamp": "2026-04-20T12:00:00Z",
  "actor_type": "human",
  "actor_id": "ops_manager_01",
  "system_id": "autonomy_stack",
  "system_version": "5.1.0",
  "approved_boundary_reference": "registry/series_a.json",
  "related_state": "draft",
  "status": "open",
  "linked_evidence_ids": [],
  "notes": "Initial deployment request submitted."
}
```

### 2.2 Required Fields

| Field | Purpose |
|---|---|
| `event_id` | Unique identifier for the governance event |
| `event_type` | Machine-readable event classification |
| `series_id` | Identifies the responsible series |
| `risk_tier` | Identifies the governance tier |
| `timestamp` | Preserves event order |
| `actor_type` / `actor_id` | Identifies initiating human or system actor |
| `system_id` / `system_version` | Identifies relevant system context |
| `approved_boundary_reference` | Links event to approved scope |
| `related_state` | Indicates governance state context |
| `status` | Indicates whether the event is open, closed, resolved, or pending |
| `linked_evidence_ids` | Connects the event to evidence objects |
| `notes` | Human-readable summary |

---

## 3. Core Event Taxonomy

The PoC should support a minimum common governance event taxonomy.

### 3.1 Approval and Deployment Events

| Event Type | Description |
|---|---|
| `DEPLOYMENT_REQUESTED` | Initial request to activate a deployment |
| `DEPLOYMENT_APPROVED` | Approval of a deployment |
| `DEPLOYMENT_DENIED` | Rejection of a deployment request |
| `DEPLOYMENT_ACTIVATED` | Deployment entered active state |
| `DEPLOYMENT_SUSPENDED` | Deployment suspended |
| `DEPLOYMENT_TERMINATED` | Deployment ended |

### 3.2 Change Control Events

| Event Type | Description |
|---|---|
| `MATERIAL_CHANGE_SUBMITTED` | Material change request submitted |
| `MATERIAL_CHANGE_APPROVED` | Material change approved |
| `MATERIAL_CHANGE_REJECTED` | Material change rejected |
| `MATERIAL_CHANGE_DEPLOYED` | Approved material change implemented |
| `EXPANSION_REQUESTED` | Scope or boundary expansion requested |
| `EXPANSION_APPROVED` | Scope or boundary expansion approved |

### 3.3 Incident and Escalation Events

| Event Type | Description |
|---|---|
| `INCIDENT_REPORTED` | Incident or anomaly reported |
| `INCIDENT_CLASSIFIED` | Incident severity or class assigned |
| `INCIDENT_ESCALATED` | Incident escalated to responsible personnel |
| `INCIDENT_RESOLVED` | Incident closed or resolved |
| `OVERRIDE_EXECUTED` | Human override executed |
| `SUSPENSION_EXECUTED` | Human or system suspension action executed |

### 3.4 Tier and Review Events

| Event Type | Description |
|---|---|
| `RECLASSIFICATION_TRIGGERED` | Event suggesting tier mismatch |
| `RECLASSIFICATION_REVIEW_STARTED` | Formal review begun |
| `RECLASSIFICATION_APPROVED` | Use case reassigned or tier revised |
| `RECLASSIFICATION_REJECTED` | Review concluded without reassignment |
| `AUDIT_EXPORT_REQUESTED` | Review or audit packet requested |
| `INDEPENDENT_REVIEW_REQUESTED` | Independent review initiated |

### 3.5 Transparency Events

| Event Type | Description |
|---|---|
| `USER_NOTICE_DELIVERED` | User informed of AI-assisted operation |
| `SCOPE_DOCUMENT_UPDATED` | Scope or limitations document updated |
| `WORKFLOW_DEPENDENCE_ALERT` | Overreliance or dependence threshold reached |
| `LIMITATION_NOTICE_ACKNOWLEDGED` | User acknowledges system limitation notice |

---

## 4. Series-Specific Event Profiles

## 4.1 Series A Event Profile
## Urban Ride-Hailing (`Cbase ∪ Chigh`)

Series A requires the richest event profile because it is high-risk and incident-sensitive.

### Priority Event Types for Series A

- `DEPLOYMENT_REQUESTED`
- `DEPLOYMENT_APPROVED`
- `EXPANSION_REQUESTED`
- `INCIDENT_REPORTED`
- `INCIDENT_CLASSIFIED`
- `SUSPENSION_EXECUTED`
- `OVERRIDE_EXECUTED`
- `AUDIT_EXPORT_REQUESTED`
- `INDEPENDENT_REVIEW_REQUESTED`
- `REACTIVATION_REQUESTED`
- `REACTIVATION_APPROVED`

### Series A Example Event

```json
{
  "event_id": "evt_a_000077",
  "event_type": "INCIDENT_REPORTED",
  "series_id": "SeriesA",
  "risk_tier": "high",
  "timestamp": "2026-04-20T12:01:00Z",
  "actor_type": "system",
  "actor_id": "trigger_detector",
  "system_id": "autonomy_stack",
  "system_version": "5.1.0",
  "approved_boundary_reference": "registry/series_a.json",
  "related_state": "active",
  "status": "open",
  "linked_evidence_ids": [
    "tae_000077"
  ],
  "notes": "Near-collision detected and escalation initiated."
}
```

## 4.2 Series B Event Profile
## Executive Fleet Leasing (`Cbase ∪ Ctransparency`)

Series B requires baseline governance events plus transparency and dependence events.

### Priority Event Types for Series B

- `DEPLOYMENT_REQUESTED`
- `DEPLOYMENT_APPROVED`
- `MATERIAL_CHANGE_SUBMITTED`
- `USER_NOTICE_DELIVERED`
- `SCOPE_DOCUMENT_UPDATED`
- `WORKFLOW_DEPENDENCE_ALERT`
- `RECLASSIFICATION_TRIGGERED`
- `RECLASSIFICATION_REVIEW_STARTED`

### Series B Example Event

```json
{
  "event_id": "evt_b_000021",
  "event_type": "WORKFLOW_DEPENDENCE_ALERT",
  "series_id": "SeriesB",
  "risk_tier": "limited",
  "timestamp": "2026-04-20T13:15:00Z",
  "actor_type": "system",
  "actor_id": "workflow_dependence_monitor",
  "system_id": "fleet_router_v2",
  "system_version": "2.4.1",
  "approved_boundary_reference": "registry/series_b.json",
  "related_state": "active",
  "status": "open",
  "linked_evidence_ids": [
    "dep_000021"
  ],
  "notes": "Operational dependence threshold exceeded."
}
```

## 4.3 Series C Event Profile
## Predictive Maintenance (`Cbase only`)

Series C requires the lightest event profile, but still needs enough structure to support escalation and transfer.

### Priority Event Types for Series C

- `DEPLOYMENT_REQUESTED`
- `DEPLOYMENT_APPROVED`
- `MATERIAL_CHANGE_SUBMITTED`
- `INCIDENT_REPORTED`
- `RECLASSIFICATION_TRIGGERED`

### Series C Example Event

```json
{
  "event_id": "evt_c_000004",
  "event_type": "RECLASSIFICATION_TRIGGERED",
  "series_id": "SeriesC",
  "risk_tier": "minimal",
  "timestamp": "2026-04-20T14:30:00Z",
  "actor_type": "system",
  "actor_id": "tier_review_service",
  "system_id": "maint_predictor_v1",
  "system_version": "1.8.0",
  "approved_boundary_reference": "registry/series_c.json",
  "related_state": "active",
  "status": "open",
  "linked_evidence_ids": [
    "promo_000004"
  ],
  "notes": "Customer-facing promotion attempt detected."
}
```

---

## 5. Event-to-State Mapping

Events should drive or explain governance state transitions.

| Event Type | Typical State Effect |
|---|---|
| `DEPLOYMENT_REQUESTED` | `draft -> gated` or `draft -> approved` |
| `DEPLOYMENT_APPROVED` | `gated -> active` or `approved -> active` |
| `MATERIAL_CHANGE_SUBMITTED` | `active -> material_change_review` |
| `INCIDENT_REPORTED` | `active -> trigger_event` or `active -> review` |
| `SUSPENSION_EXECUTED` | `active -> suspended` |
| `OVERRIDE_EXECUTED` | `active -> narrowed` or `active -> suspended` |
| `RECLASSIFICATION_TRIGGERED` | `active -> tier_review` or `active -> transferred` |
| `AUDIT_EXPORT_REQUESTED` | usually no immediate state change, but may accompany `review` |

---

## 6. Event-to-Evidence Mapping

Each governance event should be capable of linking to evidence objects.

| Event Type | Typical Evidence Link |
|---|---|
| `DEPLOYMENT_REQUESTED` | deployment request record |
| `DEPLOYMENT_APPROVED` | approval memo or gate record |
| `MATERIAL_CHANGE_SUBMITTED` | change request object |
| `INCIDENT_REPORTED` | incident ticket |
| `OVERRIDE_EXECUTED` | override record |
| `USER_NOTICE_DELIVERED` | notice delivery log |
| `WORKFLOW_DEPENDENCE_ALERT` | dependence review memo |
| `RECLASSIFICATION_TRIGGERED` | tier review packet |
| `TRIGGER_EVENT_CONFIRMED` | trigger-action-evidence record |

---

## 7. Event Lifecycle

Each event should move through a basic lifecycle.

### 7.1 Event Status Values

- `open`
- `pending_review`
- `in_progress`
- `resolved`
- `closed`
- `escalated`

### 7.2 Example Lifecycle

```text
open -> pending_review -> in_progress -> resolved -> closed
                       \
                        -> escalated
```

### 7.3 Governance Meaning

This lifecycle allows the PoC to distinguish between mere detection, active handling, escalation, and final closure.

---

## 8. Event Storage Model

A PoC implementation should preserve events as first-class governance objects.

### 8.1 Suggested Layout

```text
/events
  /series_a
    evt_a_000001.json
    evt_a_000002.json
  /series_b
    evt_b_000001.json
  /series_c
    evt_c_000001.json
  /indexes
    by_type.json
    by_series.json
    by_state.json
```

### 8.2 Recommended Indexes

- by event type
- by series
- by status
- by timestamp
- by related system version
- by linked evidence object

---

## 9. Recommended PoC Services

Recommended implementation files:

```text
governance_events/
  schemas/
    event.schema.json
  writers/
    event_writer.py
  routers/
    event_router.py
  handlers/
    deployment_handler.py
    change_handler.py
    incident_handler.py
    transparency_handler.py
    reclassification_handler.py
  indexes/
    event_index.py
```

Recommended functions:

- `create_event()`
- `update_event_status()`
- `link_event_to_evidence()`
- `route_event()`
- `query_events_by_series()`
- `query_events_by_type()`

---

## 10. Design Principles for the PoC

The event model should be designed so that:

(a) every material governance action is eventable;  
(b) event types are stable enough for audit and replay;  
(c) higher-risk series naturally produce denser event trails;  
(d) lower-risk series preserve lighter but still reviewable event histories; and  
(e) events can be replayed to demonstrate the operation of the rider architecture.

---

## 11. Interpretation

The governance event model is intended to serve as the operational heartbeat of the modular rider architecture.

In this formulation:

- `Cbase` defines the shared event vocabulary required for baseline accountability
- `Chigh` adds denser and more safety-critical event paths
- `Ctransparency` adds user-facing and documentation-related event paths

The event layer therefore links the clause-to-control matrix, the state-machine model, and the evidence model into a single executable governance structure.
