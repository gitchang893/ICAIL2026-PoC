# Clause-to-Control Matrix

## Purpose

This document maps the modular rider architecture to an executable proof-of-concept (PoC) governance layer.  
The objective is to show how each contractual clause set can be operationalized as a control object, event handler, state transition, approval gate, or evidence bundle within a software system.

The clause architecture is defined as follows:

- `Cbase` = baseline governance clauses applicable to all AI-related series
- `Chigh` = supplemental clauses for high-risk AI use cases
- `Ctransparency` = supplemental clauses for limited-risk AI use cases

Accordingly:

- `OAride = Cbase ∪ Chigh`
- `OAfleet = Cbase ∪ Ctransparency`
- `OAmaint = Cbase only`

---

## 1. Shared PoC Components

The following PoC components are shared across all series unless otherwise stated.

| Component | Function | Notes |
|---|---|---|
| `series_registry` | Stores approved use case, risk tier, responsible personnel, and boundary metadata for each series | Core source of truth |
| `policy_engine` | Checks whether a requested action or deployment falls within the approved boundary | Used by all series |
| `change_control_service` | Registers, reviews, and approves material changes | Required by `Cbase` |
| `incident_service` | Receives, classifies, escalates, and tracks incidents | Required by `Cbase`; extended for Series A |
| `event_store` | Stores baseline logs, approvals, version references, and incident history | Baseline evidence layer |
| `override_service` | Allows authorized human actors to revise, suspend, narrow, or terminate use | Used by all series |
| `tier_review_service` | Determines whether a series remains correctly classified by risk tier | Especially relevant for Series B and C |
| `document_store` | Stores internal scope documentation, notices, and governance records | Especially relevant for Series B |
| `evidence_bundle_service` | Produces structured incident or audit bundles | Especially relevant for Series A |

---

## 2. Cbase Clause-to-Control Mapping

The following controls implement the baseline clause set (`Cbase`) across all series.

| Clause | Legal Function | Control Object / Service | Trigger | Output / Evidence |
|---|---|---|---|---|
| `Cbase §3.1 Purpose Limitation` | Restricts use to approved boundary | `policy_engine` + `series_registry` | Any deployment, action, or configuration change | boundary check result; allow/deny log |
| `Cbase §3.2 Human Responsibility` | Assigns responsible natural persons | `series_registry` | Series creation or amendment | personnel designation record |
| `Cbase §3.3 No Delegation of Ultimate Responsibility` | Prevents responsibility from being shifted to the model | `governance_policy.yaml` + approval workflow | Any use of automated output in decision flow | human accountability record |
| `Cbase §3.4 Supervisory Authority` | Allows human override, narrowing, suspension, termination | `override_service` | manual intervention, incident, drift review | override event log |
| `Cbase §3.5 Change Control` | Requires review for material changes | `change_control_service` | model/provider/tool/data/workflow change | change request, approver, disposition |
| `Cbase §3.6 Baseline Logging` | Preserves minimal governance record | `event_store` | deployment, approval, incident, change | event record with timestamp and actor |
| `Cbase §3.7 Incident Escalation` | Ensures incidents are surfaced to supervisors | `incident_service` | incident report or anomaly threshold | incident ticket, severity, assignee |
| `Cbase §3.8 No Unapproved Higher-Risk Migration` | Prevents silent drift into higher-risk use | `tier_review_service` | repeated incidents, boundary expansion, new external effect | tier review record |
| `Cbase §3.9 Vendor and Provider Baseline` | Preserves governance duties despite outsourcing | `vendor_registry` + contract metadata | onboarding or material provider change | vendor profile, contractual controls checklist |
| `Cbase §3.10 Baseline Documentation` | Requires written description of use case and tier | `document_store` | series activation or update | use case memo, governance summary |

---

## 3. Series A (Urban Ride-Hailing) = `Cbase ∪ Chigh`

Series A is the high-risk tier use case.  
Its PoC layer must implement all `Cbase` controls plus the `Chigh` controls below.

### 3.1 Chigh Clause-to-Control Mapping

| Clause | Legal Function | Control Object / Service | Trigger | Output / Evidence |
|---|---|---|---|---|
| `Chigh §2.1 Deployment Gate` | Blocks deployment until required approvals are complete | `deployment_gatekeeper` | new deployment or redeployment request | gate decision record |
| `Chigh §2.2 Expansion Gate` | Requires approval for ODD expansion | `odd_expansion_review` | geography/time/weather/service expansion request | expansion approval packet |
| `Chigh §2.3 Reactivation Gate` | Blocks reactivation after safety suspension until clearance | `reactivation_gate` | request to resume suspended vehicle/system | clearance log |
| `Chigh §3.1 Trigger Events` | Defines when heightened response is mandatory | `trigger_detector` | collision, near miss, law-enforcement stop, ODD deviation, regulator request | trigger classification record |
| `Chigh §3.2 Required Actions` | Enforces response steps after trigger | `incident_response_orchestrator` | confirmed trigger event | action sequence log |
| `Chigh §3.3 Required Evidence` | Preserves event-linked evidence | `evidence_bundle_service` | trigger event | structured evidence bundle hash |
| `Chigh §4.1 Audit Readiness` | Keeps series in auditable condition | `audit_readiness_monitor` | periodic check or regulator request | readiness status report |
| `Chigh §4.2 Independent Review` | Supports third-party or internal independent review | `review_export_service` | major incident, repeated anomalies, ODD change | exportable review packet |
| `Chigh §4.3 No Evasion by Internal Reallocation` | Prevents control avoidance by moving functions elsewhere | `series_transfer_validator` | transfer/reallocation request | reallocation compliance check |

### 3.2 Series A Representative PoC Workflow

**Scenario:** Near collision occurs during autonomous ride.

1. `trigger_detector` classifies event as `SAFETY_CRITICAL`
2. `incident_response_orchestrator` initiates:
   - vehicle safe-stop flag
   - service suspension
   - notification to Safety Officer and Incident Response Lead
3. `evidence_bundle_service` collects:
   - telemetry log
   - software/model version
   - route and dispatch history
   - intervention records
4. `reactivation_gate` blocks return to service
5. authorized human clears vehicle only after review
6. `audit_readiness_monitor` updates incident exposure status

### 3.3 Series A State Machine

```text
draft -> gated -> active -> trigger_event -> suspended -> reviewed -> reactivated
                                                \-> terminated
```

---

## 4. Series B (Executive Fleet Leasing) = `Cbase ∪ Ctransparency`

Series B is the limited-risk tier use case.  
Its PoC layer must implement all `Cbase` controls plus the `Ctransparency` controls below.

### 4.1 Ctransparency Clause-to-Control Mapping

| Clause | Legal Function | Control Object / Service | Trigger | Output / Evidence |
|---|---|---|---|---|
| `Ctransparency §2.1 User Notice` | Informs users that outputs are AI-assisted | `user_notice_service` | user login, dashboard load, workflow entry | notice delivery log |
| `Ctransparency §2.2 No Implied Finality` | Prevents users from treating outputs as self-authorizing | `ui_guardrails` + workflow flags | schedule/route acceptance event | human review confirmation |
| `Ctransparency §3.1 Scope Documentation` | Documents approved purpose and limits | `document_store` | series activation or update | scope documentation record |
| `Ctransparency §3.2 Documentation of Material Changes` | Records changes affecting transparency and operation | `change_control_service` + `document_store` | approved material change | updated change log |
| `Ctransparency §3.3 Workflow Dependence Documentation` | Tracks increasing operational dependence on AI outputs | `workflow_dependence_monitor` | repeated reliance threshold reached | dependence review memo |
| `Ctransparency §4.1 No High-Risk Drift` | Prevents migration into rights-affecting use | `tier_review_service` | new decision scope or external effect | reclassification ticket |
| `Ctransparency §4.2 Reclassification Review` | Requires review if limited-risk use becomes high-impact | `reclassification_review` | trigger from monitor or management | review decision |
| `Ctransparency §4.3 No Full High-Risk Gatekeeping by Reason of Limited-Risk Status Alone` | Preserves lighter burden unless escalation justified | `tier_policy` | control selection step | applied control profile |

### 4.2 Series B Representative PoC Workflow

**Scenario:** Routing tool becomes heavily relied upon by dispatch staff.

1. `workflow_dependence_monitor` observes increasing acceptance rate without edits  
2. threshold crossed -> generate `DEPENDENCE_ALERT`  
3. `incident_service` or `tier_review_service` opens review ticket  
4. `document_store` updates operational dependence memo  
5. responsible manager decides:  
   - remain limited-risk with extra training  
   - narrow use  
   - trigger reclassification review  

### 4.3 Series B State Machine

```text
draft -> approved -> active -> dependence_alert -> review
                                 |                 |
                                 |                 -> remain_B
                                 |                 -> narrowed
                                 \-> reclassification_trigger -> transferred
```

---

## 5. Series C (Predictive Maintenance) = `Cbase only`

Series C is the minimal-risk tier use case.  
Its PoC layer implements `Cbase` only, with no `Chigh` or `Ctransparency` supplements unless separately adopted.

### 5.1 Series C Cbase Emphasis

| Clause | Operational Emphasis for Series C | Control Object / Service | Output / Evidence |
|---|---|---|---|
| `Cbase §3.1 Purpose Limitation` | Internal predictive maintenance only | `policy_engine` | boundary compliance log |
| `Cbase §3.5 Change Control` | Model/provider/sensor-input changes tracked | `change_control_service` | change record |
| `Cbase §3.6 Baseline Logging` | Minimal logging burden preserved | `event_store` | version/incident log |
| `Cbase §3.7 Incident Escalation` | Significant false-signal patterns escalated | `incident_service` | incident ticket |
| `Cbase §3.8 No Unapproved Higher-Risk Migration` | Prevents customer-facing or rights-affecting repurposing | `tier_review_service` | promotion review |

### 5.2 Series C Representative PoC Workflow

**Scenario:** Internal predictive-maintenance model is proposed for customer-facing service guarantees.

1. business owner submits scope change  
2. `policy_engine` flags request as outside approved use case  
3. `tier_review_service` classifies as possible migration beyond minimal-risk  
4. system blocks direct promotion inside Series C  
5. Company must either:  
   - reject  
   - narrow proposal  
   - transfer use case to Series B or Series A structure  

### 5.3 Series C State Machine

```text
draft -> approved -> active -> material_change_review -> remain_C
                                              \
                                               -> tier_review -> transferred
```

---

## 6. Cross-Series Event Model

The PoC should treat the following as shared governance events:

| Event | Description | Typical Consumer |
|---|---|---|
| `DEPLOYMENT_REQUESTED` | Initial deployment or go-live request | gatekeeper / approval service |
| `MATERIAL_CHANGE_SUBMITTED` | Change to model, provider, tools, workflow, or scope | change control service |
| `INCIDENT_REPORTED` | Incident or anomaly requiring attention | incident service |
| `OVERRIDE_EXECUTED` | Human override, narrowing, suspension, or termination | event store / audit layer |
| `RECLASSIFICATION_TRIGGERED` | Possible mismatch between current tier and observed use | tier review service |
| `AUDIT_EXPORT_REQUESTED` | Export for internal audit, litigation, or regulator review | evidence or review export service |

---

## 7. Evidence Model

All series should produce at least a baseline evidence object:

```json
{
  "series_id": "SeriesA",
  "risk_tier": "high",
  "event_type": "INCIDENT_REPORTED",
  "timestamp": "2026-04-20T12:00:00Z",
  "actor": "incident_service",
  "system_version": "v3.4.1",
  "approved_boundary_reference": "registry/series_a.json",
  "decision": "suspended",
  "reviewer": "Safety Officer",
  "artifacts": [
    "telemetry_hash_1",
    "route_log_hash_2",
    "approval_record_hash_3"
  ]
}
```

For Series A, this baseline evidence object should expand into a formal **Trigger-Action-Evidence Record**.

---

## 8. Minimal PoC Implementation Roadmap

### Phase 1: Shared Cbase Layer

Implement:

- `series_registry`
- `policy_engine`
- `change_control_service`
- `incident_service`
- `event_store`
- `tier_review_service`

### Phase 2: Series-Specific Modules

Implement:

- Series A: `deployment_gatekeeper`, `trigger_detector`, `evidence_bundle_service`, `reactivation_gate`
- Series B: `user_notice_service`, `workflow_dependence_monitor`, `reclassification_review`
- Series C: `minimal logging profile`, `promotion blocker`

### Phase 3: Scenario Replay

Implement replayable test scenarios:

- Series A: near-collision and suspension
- Series B: routing dependence drift
- Series C: attempted promotion to customer-facing use

---

## 9. Interpretation

This matrix is intended to show that the rider architecture can be translated into an executable governance layer.  
The PoC is therefore not merely a technical implementation of isolated controls, but an operational expression of the series-level legal architecture itself.

In this formulation:

- `Cbase` becomes the shared governance runtime
- `Chigh` becomes the high-risk control overlay
- `Ctransparency` becomes the limited-risk transparency overlay

The result is a programmable governance structure aligned with the clause-set formulas used in the paper.
