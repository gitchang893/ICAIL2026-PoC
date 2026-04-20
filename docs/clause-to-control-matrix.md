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

```text id="53169"
draft -> gated -> active -> trigger_event -> suspended -> reviewed -> reactivated
                                                \-> terminated
