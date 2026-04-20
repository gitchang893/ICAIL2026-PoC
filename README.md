# ICAIL2026-Governance-by-Design
Companion repository for the ICAIL 2026 paper on Governance-by-Design

# I. Legal Drafts

This repository explores how Delaware Series LLC structures can serve as purpose-bound governance units for high-risk AI use cases.  
Rather than treating AI ethics as a question of explainability alone, it emphasizes human authority, controlled deployment, reviewability, and retained organizational responsibility.  
It contains draft legal riders, governance frameworks, and related research materials.

## Legal Drafts for ICAIL-2026 paper

- [Series A High-Risk AI Alignment Rider](docs/series_a-urban-ride-hailing-high-risk-rider.md)  
  A Delaware Series LLC rider for Level-4 autonomous urban ride-hailing, implementing high-risk controls through oversight gates, audit readiness, and trigger-action-evidence clauses.

- [Series B Limited-Risk AI Transparency Rider](docs/series_b-executive-fleet-leasing-limited-risk-rider.md)  
  A Delaware Series LLC rider for AI-assisted executive fleet scheduling and routing, combining baseline governance with transparency, user notice, and documentation duties.

- [Series C Minimal-Risk AI Baseline Governance Rider](docs/series_c-predictive-maintenance-minimal-risk-rider.md)  
  A Delaware Series LLC rider for internal predictive maintenance models, preserving baseline logging, change control, and accountability with minimal governance overhead.

## Series Structure Overview

| Series | Use Case | Risk Tier | Operating Agreement Formula | Core Rider Logic |
|---|---|---|---|---|
| **Series A** | Urban Ride-Hailing | **High-Risk** | `OAride = Cbase ∪ Chigh` | Oversight gates, trigger-action-evidence clauses, audit readiness, evidence preservation, suspension/reactivation controls |
| **Series B** | Executive Fleet Leasing | **Limited-Risk** | `OAfleet = Cbase ∪ Ctransparency` | Baseline governance plus user notice, documentation, transparency, and reclassification safeguards |
| **Series C** | Predictive Maintenance | **Minimal-Risk** | `OAmaint = Cbase only` | Baseline logging, change control, incident escalation, and accountability with minimal overhead |

## Clause Architecture

This repository models AI governance in Series LLC form through a modular clause architecture.  
`Cbase` denotes baseline governance clauses applicable across all AI-related series, while additional clause sets are layered according to risk tier: `Chigh` for high-risk use cases and `Ctransparency` for limited-risk use cases.  
Accordingly, the operating agreement formulas are expressed as `OAride = Cbase ∪ Chigh`, `OAfleet = Cbase ∪ Ctransparency`, and `OAmaint = Cbase only`.

## Re-Factoring Legal Drafts for ICAIL-2026 Paper by the Modular Clause Architecture

- [Common Cbase AI Governance Rider](docs/common-cbase-ai-governance-rider.md)  
  A baseline Delaware Series LLC governance rider providing common clauses for purpose limitation, human responsibility, change control, baseline logging, and incident escalation across AI-related series.

- [Series A Chigh Add-On](docs/series_a-urban-ride-hailing-chigh-add-on.md)  
  A high-risk add-on for Level-4 autonomous urban ride-hailing, implementing oversight gates, trigger-action-evidence duties, audit readiness, and reactivation controls.

- [Series B Ctransparency Add-On](docs/series_b-executive-fleet-leasing-ctransparency-add-on.md)  
  A limited-risk add-on for AI-assisted executive fleet scheduling and routing, adding user notice, internal documentation, transparency, and reclassification safeguards.

- [Series C Cbase Designation Notice](docs/series_c-predictive-maintenance-cbase-designation.md)  
  A minimal-risk designation notice for internal predictive maintenance, applying Cbase only with no additional high-risk or transparency supplements.

## Series Structure Overview

| Series | Use Case | Risk Tier | Formula | Clause Set |
|---|---|---|---|---|
| **Series A** | Urban Ride-Hailing | **High-Risk** | `OAride = Cbase ∪ Chigh` | Baseline governance plus oversight gates, trigger-action-evidence obligations, audit readiness, and reactivation controls |
| **Series B** | Executive Fleet Leasing | **Limited-Risk** | `OAfleet = Cbase ∪ Ctransparency` | Baseline governance plus user notice, documentation, transparency, and reclassification safeguards |
| **Series C** | Predictive Maintenance | **Minimal-Risk** | `OAmaint = Cbase only` | Baseline governance only, with minimal overhead and preserved logging/accountability expectations |

## Additional Legal Drafts

- [Series 1 High-Risk AI Alignment Rider](docs/series_a-high-risk-ai-alignment-rider.md)  
  A Delaware Series LLC operating agreement rider for a high-risk AI use case, establishing purpose-binding, human oversight, deployment gates, override and shutdown authority, incident escalation, and organizational accountability.

- [Series 2 Standard-Risk AI Governance Rider](docs/series_b-standard-risk-ai-governance-rider.md)  
  A Delaware Series LLC rider for standard-risk AI use cases, emphasizing purpose limitation, human supervision, change control, reclassification triggers, and containment of drift into high-risk deployment.

- [Series 3 Experimental AI Sandbox Rider](docs/series_c-experimental-ai-sandbox-rider.md)  
  A Delaware Series LLC rider for experimental and sandbox AI use cases, emphasizing purpose limitation, sandbox isolation, human supervision, transition review, and prevention of premature production deployment.

- [Delaware High-Risk Alignment Rider Draft](docs/delaware-high-risk-ai-alighment-rider.md)  
  Series-level addendum to a Delaware LLC operating agreement for trace governance,
  evidentiary preservation, purpose-binding, human oversight, and accountability in
  AI-assisted and agentic operations.

## Series Structure Overview

| Series | Rider | Primary Use Case | Core Governance Function | Escalation Path |
|---|---|---|---|---|
| **Series 1** | [Series A High-Risk AI Alignment Rider](docs/series_a-high-risk-ai-alignment-rider.md) | High-risk AI use cases with potentially material effects on rights, obligations, compliance, safety, or other substantial interests | Purpose-binding, human oversight, deployment gates, override and shutdown authority, incident escalation, and retained organizational responsibility | Independent review, heightened controls, suspension, shutdown, or reassignment |
| **Series 2** | [Series B Standard-Risk AI Governance Rider](docs/series_b-standard-risk-ai-governance-rider.md) | Standard-risk AI use cases such as drafting, summarization, workflow support, and internal operational assistance | Purpose limitation, human supervision, change control, reclassification triggers, and containment of drift into high-risk deployment | Reclassification to heightened governance or transfer to another series |
| **Series 3** | [Series C Experimental AI Sandbox Rider](docs/series_c-experimental-ai-sandbox-rider.md) | Experimental, research, testing, red-teaming, benchmarking, prototype, and sandbox use cases | Sandbox isolation, controlled testing, limited data and tool access, transition review, and prevention of premature production deployment | Transition to Series 2 or Series 1, narrowing, or termination of the experiment |


# II. Governance-by-Design PoC

This repository provides a minimal proof-of-concept (PoC) companion artifact for the ICAIL 2026 paper:

**Governance-by-Design for AI Compliance: Compiling EU AI Act Duties into Computable Operating-Agreement Clauses**

## Overview

The repository illustrates how regulatory duties can be represented as computable governance clauses with trigger-action-evidence (TAE) semantics. It is intended as a reproducibility companion for the paper's formal model, rider template, and case-study trace.

## Contents

- `clauses/`  
  Machine-readable clause templates corresponding to the High-Risk Alignment Rider.

- `traces/`  
  Synthetic execution traces used to illustrate governance events and evidence production.

- `schema/`  
  Evidence-store schema for audit-relevant artifacts.

- `checker/`  
  Minimal validation scripts for checking trigger-action-evidence satisfaction over traces.

- `examples/`  
  Example outputs and sample files.


## Example scenarios

This repository includes two synthetic execution traces.

### 1. Critical safety incident (`traces/mobility_incident_trace.json`)

Series A (`S_ride`) represents a high-risk urban autonomous-mobility deployment. During operation, a collision occurs, generating an `IncidentRecord` from vehicle sensors and logs. The record is then committed in tamper-evident form, producing an `IntegrityProof`. After reviewing the evidence, the Alignment Officer issues a `STOP` order, causing the system to transition into the `STOPPED` state and halting inference/API serving. If a manager attempts to bypass the stop order, the attempt is recorded through `AttemptedOverride` and `RemedyRecord`. The workflow concludes with a corrective action plan (`CAP`) and, where required, an external reporting packet, with `ProofOfSubmission` preserved in the evidence store.

This scenario illustrates the paper’s central claim that regulatory duties can be operationalized as **trigger-action-evidence (TAE)** controls: the incident is the trigger, the emergency stop is the action, and the resulting records (such as `StopOrderRecord` and `ProofOfSubmission`) constitute the evidence. In this way, governance simultaneously constrains authority and produces audit-relevant records during operation.

### 2. Normal compliant deployment (`traces/normal_operation_trace.json`)

This trace represents a normal high-risk deployment in which the required conformity outputs, verification records, logging artifacts, and scheduled audit records are all present. Because the relevant governance gates are satisfied, deployment proceeds without emergency intervention. The scenario shows how the same framework supports routine compliant operation, not only exceptional incident handling.

## Additional reasoning-trace scenario (`traces/reasoning_trace_example.jso`)

The reasoning-trace PoC models a safety-critical LLM-agent decision workflow. An agent is asked to produce a recommendation or decision in a high-impact setting. Before the decision is executed, the system generates a structured `ReasoningTraceRecord`, attaches an `IntegrityProof`, and stores both as tamper-evident evidence artifacts. Because the output is classified as high-risk or safety-critical, execution is gated until a designated human reviewer records an `ApprovalRecord`. At a later stage, an audit or dispute request triggers generation of a `ReconstructionPacket`, linking the reasoning trace, the approval record, and the final decision outcome.

This scenario illustrates how AI reasoning can be preserved not merely as transient model output, but as a verifiable governance record. In that sense, the PoC shows how reasoning traces can function as evidentiary artifacts that connect technical decision processes to organizational accountability, auditability, and review.

## Series-specific example scenarios

This repository also includes three synthetic execution traces corresponding to the Series-specific rider templates.

### 1. Series A: High-risk autonomous mobility (`traces/series_a_incident_trace.json`)

This scenario models a serious incident in a high-risk urban autonomous-mobility deployment. A collision is detected, an incident record is generated, and the event is preserved through tamper-evident logging. A designated verifier records a verification artifact, after which the Alignment Officer issues an emergency stop. The workflow concludes with corrective-action and reporting steps, preserving both a corrective action plan (`CAP`) and proof of submission (`ProofOfSubmission`).

This trace illustrates the strongest governance mode in the repository: emergency intervention, strict logging, evidence verification, and post-incident remediation for a high-risk series.

### 2. Series B: Transparency and controlled deployment (`traces/series_b_transparency_trace.json`)

This scenario models a controlled deployment in a fleet-scheduling and routing context. A deployment request is submitted, a transparency notice is issued to the relevant client or user-facing interface, and the resulting approval is recorded. Later, a scheduled governance review is completed and logged.

This trace illustrates a medium-intensity governance pattern centered on transparency, approval logging, and periodic review rather than emergency shutdown or full incident escalation.

### 3. Series C: Internal monitoring workflow (`traces/series_c_internal_monitoring_trace.json`)

This scenario models an internal predictive-maintenance workflow. An internal alert is generated by the maintenance model, a model update is recorded, the anomaly is reviewed by the engineering team, and the resulting maintenance action is linked back to the prediction and review record.

This trace illustrates a lightweight governance mode focused on internal logging, model-update traceability, anomaly review, and maintenance-action accountability.

## EU AI Act coverage

The current Python checker does not directly implement the EU AI Act as statutory text. Rather, it implements the paper’s clause-level operationalization of selected EU AI Act duties, as summarized in **Table 1** and instantiated in **Appendix A** (High-Risk Alignment Rider).

In particular, the current PoC covers:

- **Art. 14 (Human oversight)** through emergency stop and override-related clauses (`2.1`, `2.2`);
- **Arts. 12, 18–19 (Logging, record-keeping, and retention)** through tamper-evident logging, retention, and verification-record clauses (`3.1`–`3.3`);
- **Arts. 9, 15, 17, 43 (Risk management / conformity and change-control gates)** through pre-deployment and reassessment clauses (`4.1`, `4.2`);
- **Arts. 9–10, 72–73 (Monitoring, corrective action, and incident/reporting workflows)** through maintenance-trigger and corrective-action/reporting clauses (`5.1`–`5.3`).

The checker therefore validates whether the expected evidence artifacts for these trigger-action-evidence (TAE) clauses are present in the supplied synthetic traces. It is a research PoC and does not attempt full legal compliance determination under the EU AI Act.

## Repository components

### Core Governance-by-Design PoC

- `clauses/high_risk_alignment_rider.yaml`  
  A machine-readable clause template corresponding to the High-Risk Alignment Rider in Appendix A.

- `traces/mobility_incident_trace.json`  
  A synthetic execution trace for the critical safety-incident scenario in the autonomous-mobility case study.

- `traces/normal_operation_trace.json`  
  A synthetic execution trace for a normal compliant high-risk deployment without emergency escalation.

- `checker/trace_checker.py`  
  A minimal checker for trigger-action-evidence (TAE) clause satisfaction over the supplied synthetic traces.

- `schema/evidence_store_schema.json`  
  A minimal schema for audit-relevant evidence artifacts stored in the evidence store.

- `examples/expected_output.txt`  
  An example output file illustrating the expected checker result.

### Additional reasoning-trace PoC

- `clauses/reasoning_trace_clauses.yaml`  
  Machine-readable governance clauses for reasoning-trace preservation.

- `traces/reasoning_trace_example.json`  
  A synthetic trace showing trace generation, integrity preservation, human approval, and reconstruction.

- `checker/reasoning_trace_checker.py`  
  A minimal checker for clause satisfaction over the reasoning-trace example.

- `schema/reasoning_trace_schema.json`  
  A minimal schema for reasoning-trace evidence artifacts.

## Modular Implementation for PoC Implementation

- [PoC Implementation Layout](docs/poc-implementation-layout.md)  
  Outlines a modular proof-of-concept implementation for the rider architecture, mapping `Cbase`, `Chigh`, and `Ctransparency` to shared services, series-specific overlays, and replayable governance scenarios.

- [State Machines](docs/state-machines.md)  
  Describes the operational lifecycle of Series A, B, and C as governed state machines, including deployment, incident, review, suspension, reclassification, and transfer states.

- [Evidence Model](docs/evidence-model.md)  
  Defines the evidence objects, storage layers, integrity controls, and export profiles that support the modular rider architecture across Series A, B, and C.

- [Governance Events](docs/governance-events.md)  
  Defines the shared event taxonomy, lifecycle, and series-specific event profiles that drive the executable governance layer across Series A, B, and C.

- [PoC Policy and Schemas](poc/shared/)  
  Includes the shared governance policy, event schema, evidence schemas, and initial tier policy logic for the executable PoC governance layer.

- [PoC Change Control Scaffolds](poc/shared/change_control/)  
  Includes initial Python scaffolds for event storage, material change request handling, and approval workflow management in the executable governance layer.

- [PoC Incident and Override Scaffolds](poc/shared/)  
  Includes initial Python scaffolds for incident severity classification, incident management, and human override recording in the executable governance layer.

- [Series A Runtime Scaffolds](poc/series_a/), [Series B Runtime Scaffolds](poc/series_b/), [Series C Runtime Scaffolds](poc/series_c/)  
  Includes initial series-specific Python scaffolds for Series A deployment gates, Series B workflow-dependence monitoring, and Series C promotion blocking.

- Scenario replay: [Series A deployment gate](poc/scenarios/series_a_deployment_request.json), [Series B dependence drift](poc/scenarios/series_b_routing_dependence_drift.json), [Series C promotion attempt](poc/scenarios/series_c_customer_facing_promotion_attempt.json), and [runner](poc/run_scenario.py)

## How to Run

```bash
python poc/run_scenario.py poc/scenarios/series_a_deployment_request.json --write-summary
python poc/run_scenario.py poc/scenarios/series_b_routing_dependence_drift.json --write-summary
python poc/run_scenario.py poc/scenarios/series_c_customer_facing_promotion_attempt.json --write-summary
```

## Rider construction method for EU AI Act-oriented governance

The rider templates in this repository follow a two-layer construction method for operationalizing selected EU AI Act duties into computable governance clauses.

### 1. Fundamental (common) layer

The first layer contains **fundamental governance clauses** that apply across all series, regardless of risk tier. These clauses establish the baseline organizational infrastructure required for computable governance, including:

- maintenance of an evidence store;
- baseline governance-event logging;
- audit access and retrieval duties;
- override logging and traceability of governance interventions.

In the repository, this common layer is represented by:

- `clauses/base_governance_rider.yaml`

Conceptually, this corresponds to the paper’s idea of a shared governance substrate (`C_base`) that provides the minimal authority, logging, and audit framework for all deployments.

### 2. Risk-based (series-specific) layer

The second layer contains **risk-based rider modules** that are added on top of the common layer according to the regulatory and operational profile of a given series. These modules implement different governance intensities for different deployment contexts.

In the repository, this produces three series-specific riders:

- `clauses/series_a_high_risk_rider.yaml`  
  A **high-risk rider** for Series A, adding emergency stop authority, strict evidence verification, tamper-evident logging, pre-deployment gates, and corrective-action/reporting workflows.

- `clauses/series_b_transparency_rider.yaml`  
  A **limited-risk / transparency-oriented rider** for Series B, adding transparency notice, deployment approval logging, escalation, and periodic governance review.

- `clauses/series_c_internal_monitoring_rider.yaml`  
  A **minimal-risk / internal monitoring rider** for Series C, adding lightweight internal logging, update traceability, anomaly review, and maintenance-action accountability.

### Construction principle

The overall construction principle is therefore:

**Series-specific Rider = Fundamental Governance Layer + Risk-Based Layer**

or, in the terminology of the paper:

**OA_i = C_base ∪ C_tier ∪ C_context**

where:

- `C_base` provides the common governance substrate;
- `C_tier` adds the risk-tier-specific governance intensity;
- `C_context` captures deployment-specific constraints where needed.

Under this method, the three series riders are not independent ad hoc documents. Rather, they are structured instantiations of the same modular governance design, with different risk-based supplements layered onto a shared fundamental governance core.

### Relation to the paper

This construction method mirrors the paper’s modular governance architecture. Series A corresponds most closely to the paper’s worked high-risk case study, while Series B and Series C provide PoC elaborations of the paper’s limited-risk and minimal-risk tiers. Together, they show how the same governance-by-design method can generate different operating-agreement riders for heterogeneous AI deployments.

 ### Series-specific rider templates

 In addition to the compact High-Risk Alignment Rider discussed in the paper, this repository provides a more explicit set of series-specific rider templates corresponding to the three-series architecture used in the case-study discussion. These rider templates should be understood as PoC instantiations that further elaborate the paper’s modular governance design.

- `clauses/base_governance_rider.yaml`  
  Common governance clauses applicable across all series.

- `clauses/series_a_high_risk_rider.yaml`  
  High-risk rider for Series A (urban autonomous mobility), corresponding to the paper’s emergency-stop, logging, verification, and reporting logic.

- `clauses/series_b_transparency_rider.yaml`  
  Governance rider for Series B (fleet scheduling/routing), emphasizing transparency, approval logging, escalation, and periodic review.

- `clauses/series_c_internal_monitoring_rider.yaml`  
  Lightweight governance rider for Series C (predictive maintenance), focusing on internal logging, update traceability, anomaly review, and maintenance action records.

### Series-specific synthetic traces

- `traces/series_a_incident_trace.json`  
  A high-risk incident scenario for Series A, covering emergency stop, tamper-evident logging, verification, and corrective-action/reporting steps.

- `traces/series_b_transparency_trace.json`  
  A controlled-deployment scenario for Series B, covering transparency notice, approval logging, and periodic governance review.

- `traces/series_c_internal_monitoring_trace.json`  
  An internal monitoring workflow for Series C, covering alert logging, model update traceability, anomaly review, and maintenance action linkage.  

## How to run

Run the checker from the repository root:

```bash
python checker/trace_checker.py traces/mobility_incident_trace.json
python checker/trace_checker.py traces/normal_operation_trace.json

```

```bash
python checker/reasoning_trace_checker.py traces/reasoning_trace_example.json

```

The script reads a synthetic trace, collects the evidence artifacts recorded in the trace, and checks whether the expected trigger-action-evidence (TAE) clauses are satisfied.

### Series-specific rider traces

```bash
python checker/series_rider_checker.py traces/series_a_incident_trace.json
python checker/series_rider_checker.py traces/series_b_transparency_trace.json
python checker/series_rider_checker.py traces/series_c_internal_monitoring_trace.json

```

```md
These commands validate the synthetic traces associated with the Series A, Series B, and Series C rider templates.
```

## Example output

### 1. Example output for the mobility incident trace:

```text
Trace ID: mobility_incident_001
Scenario: AutoFleet Series A critical safety event
Collected artifacts: ['AttemptedOverride', 'CAP', 'IncidentRecord', 'IntegrityProof', 'MaintenanceRecord', 'ProofOfSubmission', 'RemedyRecord', 'StopOrderRecord', 'VerificationRecord']

[PASS] Clause 2.1
[PASS] Clause 2.2
[PASS] Clause 3.1
[PASS] Clause 3.3
[PASS] Clause 5.2

Overall result: PASS
```
The same output is also provided in `examples/expected_output.txt`.

### 2. Example output for the normal compliant deployment:

```text
Trace ID: normal_operation_001
Scenario: AutoFleet Series A normal compliant deployment
Collected artifacts: ['AuditReport', 'DeployApprovalRecord', 'IntegrityProof', 'RetentionRecord', 'UpdateAssessment', 'VerificationRecord']

[PASS] Clause 3.1
[PASS] Clause 3.2
[PASS] Clause 3.3
[PASS] Clause 4.1
  Note: Either denial or approval evidence satisfies the gate outcome.
[PASS] Clause 4.2
  Note: Either reassessment or audit output is accepted.

Overall result: PASS
```
The same output is also provided in `examples/expected_output2.txt`.

### 3. Example output for reasoning trace:

```text
Trace ID: reasoning_trace_001
Scenario: LLM agent safety-critical recommendation with approval gate
Collected artifacts: ['ApprovalRecord', 'DecisionRecord', 'IntegrityProof', 'ReasoningTraceRecord', 'ReconstructionPacket']

[PASS] Clause RT-1
[PASS] Clause RT-2
[PASS] Clause RT-3
[PASS] Clause RT-5

Overall result: PASS
```

### 4. Example output for Series A

```text
Trace ID: series_a_incident_001
Scenario: Series A high-risk autonomous mobility incident
Series: Series A
Collected artifacts: ['CAP', 'IncidentRecord', 'IntegrityProof', 'ProofOfSubmission', 'StopOrderRecord', 'VerificationRecord']

[PASS] Clause A-1
[PASS] Clause A-2
[PASS] Clause A-3
[PASS] Clause A-5

Overall result: PASS
```
### 5. Example output for Series B

```text
Trace ID: series_b_transparency_001
Scenario: Series B controlled deployment with transparency and review
Series: Series B
Collected artifacts: ['DeployApprovalRecord', 'GovernanceReviewRecord', 'TransparencyNoticeRecord']

[PASS] Clause B-1
[PASS] Clause B-2
[PASS] Clause B-4

Overall result: PASS
```

### 6. Example output for Series C

```text
Trace ID: series_c_monitoring_001
Scenario: Series C predictive maintenance internal monitoring workflow
Series: Series C
Collected artifacts: ['AnomalyReviewRecord', 'InternalLogRecord', 'MaintenanceActionRecord', 'ModelUpdateRecord']

[PASS] Clause C-1
[PASS] Clause C-2
[PASS] Clause C-3
[PASS] Clause C-4

Overall result: PASS
```


## Scope

This repository is a research artifact intended to support reproducibility of the paper's formal model, rider template, and case-study workflow. It is not production software, not legal advice, and not a complete compliance system.

## Relation to the paper

The repository corresponds to the paper's:
- formal trigger-action-evidence semantics,
- High-Risk Alignment Rider template,
- autonomous mobility case study,
- reproducibility discussion.

## Citation

If you use or discuss this repository, please cite the ICAIL 2026 paper.

## Authors

- Hiroshi G. Okuno
- Mayumi J. Okuno

## Last Edit
Last updated: 2026-04-20 13:29 JST

