# State Machines

## Purpose

This document describes the state machines for the modular rider architecture.  
The objective is to show how each series can be modeled as a governed operational lifecycle, with transitions triggered by deployment, incidents, review, override, suspension, reclassification, or termination.

The structure follows the clause-set model:

- `Series A = Cbase ∪ Chigh`
- `Series B = Cbase ∪ Ctransparency`
- `Series C = Cbase only`

Each state machine is therefore designed to reflect the governance burden associated with the relevant risk tier.

---

## 1. Shared State Concepts

Across all series, the following state categories may appear:

- `draft`  
  The series or use case exists in design or registration form only.

- `approved`  
  The use case has been approved for operation under the applicable governance tier.

- `gated`  
  Additional gatekeeping conditions must be satisfied before operation may begin or resume.

- `active`  
  The use case is currently in operation within its approved boundary.

- `review`  
  The use case is under structured governance review due to dependence, drift, incident, or change.

- `suspended`  
  Operation is paused pending clearance, remediation, or review.

- `narrowed`  
  Operation continues, but only within a reduced scope.

- `transferred`  
  The use case has been reassigned to another governance structure or series.

- `terminated`  
  The use case or deployment has been ended.

These states do not need to appear identically in every implementation, but the PoC should preserve their governance meaning.

---

## 2. Series A State Machine
## Urban Ride-Hailing (`Cbase ∪ Chigh`)

Series A is the high-risk use case.  
Its lifecycle is gate-heavy and incident-sensitive.

### 2.1 State Diagram

```text
draft -> gated -> active -> trigger_event -> suspended -> reviewed -> reactivated
                                                \-> terminated
```

### 2.2 State Descriptions

- `draft`  
  The use case is defined, but not yet approved for deployment.

- `gated`  
  Series A has entered the deployment gate or reactivation gate.  
  No live operation is permitted until gate conditions are satisfied.

- `active`  
  Vehicles or services are operating within the approved operational design domain.

- `trigger_event`  
  A safety-critical, compliance-critical, or audit-relevant event has been detected.

- `suspended`  
  The affected deployment, vehicle, subsystem, or service has been paused.

- `reviewed`  
  Human oversight, incident review, and any required evidence preservation have occurred.

- `reactivated`  
  Authorized personnel have cleared the suspended deployment to resume operation.

- `terminated`  
  The deployment or service is withdrawn or ended.

### 2.3 Representative Transition Rules

| From | To | Trigger | Required Control |
|---|---|---|---|
| `draft` | `gated` | deployment request | deployment gate initiated |
| `gated` | `active` | deployment gate approved | formal approval record |
| `active` | `trigger_event` | collision, near miss, ODD deviation, regulator request | trigger detector |
| `trigger_event` | `suspended` | trigger confirmed | incident response orchestrator |
| `suspended` | `reviewed` | review completed | evidence bundle + human review |
| `reviewed` | `reactivated` | clearance granted | reactivation gate |
| `reviewed` | `terminated` | no safe resumption approved | termination decision |

### 2.4 Governance Meaning

The Series A state machine demonstrates that high-risk use is not governed only at the moment of deployment.  
It is governed continuously through trigger-response-evidence cycles, reviewability, and reactivation controls.

---

## 3. Series B State Machine
## Executive Fleet Leasing (`Cbase ∪ Ctransparency`)

Series B is the limited-risk use case.  
Its lifecycle is lighter than Series A but remains sensitive to operational overreliance and risk-tier drift.

### 3.1 State Diagram

```text
draft -> approved -> active -> dependence_alert -> review
                                 |                 |
                                 |                 -> remain_B
                                 |                 -> narrowed
                                 \-> reclassification_trigger -> transferred
```

### 3.2 State Descriptions

- `draft`  
  The use case is proposed but not yet approved.

- `approved`  
  The use case has been approved as a limited-risk deployment.

- `active`  
  The system is in use for scheduling, routing, dispatch support, or related functions.

- `dependence_alert`  
  The system has become materially influential in workflow operation, such that human users may be relying too heavily on AI-assisted outputs.

- `review`  
  Responsible personnel are reviewing the extent of operational dependence, documentation adequacy, and need for narrowing or reclassification.

- `remain_B`  
  The system remains in the limited-risk category, possibly with added supervision or documentation.

- `narrowed`  
  The system remains in Series B, but its scope or dependence level is reduced.

- `reclassification_trigger`  
  The system appears to be drifting toward a higher-risk function or governance burden.

- `transferred`  
  The use case is moved into a different governance structure, potentially Series A or another approved series.

### 3.3 Representative Transition Rules

| From | To | Trigger | Required Control |
|---|---|---|---|
| `draft` | `approved` | approval completed | documented boundary and personnel |
| `approved` | `active` | go-live | baseline logging + user notice |
| `active` | `dependence_alert` | overreliance threshold reached | workflow dependence monitor |
| `dependence_alert` | `review` | alert confirmed | documentation and management review |
| `review` | `remain_B` | limited-risk status retained | review memo |
| `review` | `narrowed` | scope reduced | operational narrowing decision |
| `active` | `reclassification_trigger` | higher-impact use or external effect detected | tier review |
| `reclassification_trigger` | `transferred` | reassignment approved | reclassification record |

### 3.4 Governance Meaning

The Series B state machine shows that limited-risk use is governed less through conformity-style gates and more through transparency, documentation, review, and escalation when drift occurs.

---

## 4. Series C State Machine
## Predictive Maintenance (`Cbase only`)

Series C is the minimal-risk use case.  
Its lifecycle is the lightest, but still structured to prevent silent migration into higher-risk use.

### 4.1 State Diagram

```text
draft -> approved -> active -> material_change_review -> remain_C
                                              \
                                               -> tier_review -> transferred
```

### 4.2 State Descriptions

- `draft`  
  The use case is proposed in internal predictive maintenance or comparable internal analytics.

- `approved`  
  The use case has been approved as minimal-risk.

- `active`  
  The system is operating within the approved internal predictive maintenance boundary.

- `material_change_review`  
  A significant change to the system, provider, model, data source, or use context is under review.

- `remain_C`  
  The change is accepted without reclassification; the use case remains minimal-risk.

- `tier_review`  
  The change or proposed use indicates a possible migration beyond minimal-risk.

- `transferred`  
  The use case is reassigned to another governance structure or series.

### 4.3 Representative Transition Rules

| From | To | Trigger | Required Control |
|---|---|---|---|
| `draft` | `approved` | minimal-risk approval completed | baseline designation |
| `approved` | `active` | internal deployment begins | baseline logs enabled |
| `active` | `material_change_review` | model/provider/data/workflow change | change control review |
| `material_change_review` | `remain_C` | minimal-risk classification retained | change approval record |
| `material_change_review` | `tier_review` | possible customer-facing or higher-risk drift | tier review service |
| `tier_review` | `transferred` | reassignment approved | reclassification decision |

### 4.4 Governance Meaning

The Series C state machine demonstrates that even minimal-risk use should not be ungoverned.  
It remains bounded by baseline controls and subject to escalation when proposed use exceeds its approved risk tier.

---

## 5. Cross-Series State Logic

The PoC should also support cross-series governance logic.

### 5.1 Cross-Series Transition Principles

- Series A should not downgrade to a lower-risk state without formal review and approval.
- Series B may remain in place, narrow, or transfer to a higher-risk structure depending on review.
- Series C may remain minimal-risk or transfer upward when proposed use exceeds internal-only or minimal-risk conditions.

### 5.2 Cross-Series Transfer Model

```text
Series C -> Series B -> Series A
```

A transfer should occur only when:

(a) the Company determines that the use case has materially changed in scope, risk, dependence, or external effect; and  
(b) the destination series has the appropriate governance layer for continued operation.

### 5.3 No Reverse Migration by Implication

No series should be treated as downgraded merely because its current deployment appears stable or because a narrower use is temporarily observed.  
Reverse migration should require explicit governance action.

---

## 6. Event-to-State Mapping

The following governance events should typically result in state transitions.

| Event | Typical State Effect |
|---|---|
| `DEPLOYMENT_REQUESTED` | `draft -> gated` or `draft -> approved` |
| `MATERIAL_CHANGE_SUBMITTED` | `active -> material_change_review` |
| `INCIDENT_REPORTED` | `active -> trigger_event` or `active -> review` |
| `OVERRIDE_EXECUTED` | `active -> narrowed` or `active -> suspended` |
| `RECLASSIFICATION_TRIGGERED` | `active -> tier_review` or `active -> transferred` |
| `AUDIT_EXPORT_REQUESTED` | no state change necessarily required, but may accompany `review` |

---

## 7. PoC Implementation Notes

To operationalize these state machines, the implementation should preserve:

- a current state value for each series deployment
- authorized transitions only
- actor identity for state-changing actions
- timestamped transition logs
- linkage between transition events and evidence

Recommended implementation pattern:

```text
state_machine/
  series_a_machine.py
  series_b_machine.py
  series_c_machine.py
  transition_rules.py
  transition_log.py
```

Each machine should expose functions such as:

- `request_deployment()`
- `submit_material_change()`
- `report_incident()`
- `execute_override()`
- `start_reclassification_review()`
- `terminate_use_case()`

---

## 8. Interpretation

These state machines are intended to make the rider architecture operationally legible.  
They show that each series is not merely a formal legal bucket, but a governed lifecycle with explicit entry conditions, escalation paths, review states, and exit rules.

In this formulation:

- Series A is gate-heavy and incident-reactive
- Series B is documentation- and drift-sensitive
- Series C is baseline-governed but transition-aware

The state-machine model therefore complements the rider texts and the clause-to-control matrix by expressing the legal architecture as a sequence of governed operational states.
