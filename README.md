# icail2026-governance-by-design
Companion repository for the ICAIL 2026 paper on Governance-by-Design

# Governance-by-Design PoC

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

## EU AI Act coverage

The current Python checker does not directly implement the EU AI Act as statutory text. Rather, it implements the paper’s clause-level operationalization of selected EU AI Act duties, as summarized in **Table 1** and instantiated in **Appendix A** (High-Risk Alignment Rider).

In particular, the current PoC covers:

- **Art. 14 (Human oversight)** through emergency stop and override-related clauses (`2.1`, `2.2`);
- **Arts. 12, 18–19 (Logging, record-keeping, and retention)** through tamper-evident logging, retention, and verification-record clauses (`3.1`–`3.3`);
- **Arts. 9, 15, 17, 43 (Risk management / conformity and change-control gates)** through pre-deployment and reassessment clauses (`4.1`, `4.2`);
- **Arts. 9–10, 72–73 (Monitoring, corrective action, and incident/reporting workflows)** through maintenance-trigger and corrective-action/reporting clauses (`5.1`–`5.3`).

The checker therefore validates whether the expected evidence artifacts for these trigger-action-evidence (TAE) clauses are present in the supplied synthetic traces. It is a research PoC and does not attempt full legal compliance determination under the EU AI Act.

## How to run

Run the checker from the repository root:

```bash
python checker/trace_checker.py traces/mobility_incident_trace.json
python checker/trace_checker.py traces/normal_operation_trace.json

```

The script reads a synthetic trace, collects the evidence artifacts recorded in the trace, and checks whether the expected trigger-action-evidence (TAE) clauses are satisfied.

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
