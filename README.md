# ICAIL2026-Governance-by-Design

Companion repository for the ICAIL 2026 paper on governance-by-design for AI compliance.

This repository develops a modular governance architecture for AI deployment using legal-organizational design.  
Its central claim is that selected AI governance duties can be expressed not only as technical controls, but also as operating-agreement clauses, governance events, evidence objects, and deployment-specific intervention rules.

The repository currently contains three connected layers:

1. **Legal design artifacts** for the ICAIL 2026 paper  
2. **Modular clause architecture** for risk-tiered governance  
3. **Computational PoC modules** for executable governance-by-design  

---

## 1. Repository Scope

This repository is a **research companion artifact**, not production software and not legal advice.

It is intended to support:

- the paper’s legal and institutional design claims;
- rider-style governance drafting for deployment-specific AI systems;
- a modular clause architecture based on `Cbase`, `Chigh`, and `Ctransparency`;
- a minimal computational PoC showing how governance clauses can be represented as events, state transitions, and evidence-producing controls.

---

## 2. How to Read This Repository

This repository currently contains **two partially overlapping stories**:

### A. Paper-facing legal and governance artifacts
These materials correspond directly to the ICAIL 2026 paper and its legal design argument.

Use these if you want to understand:

- the legal architecture;
- the rider structure;
- the clause-set model;
- the three-series case structure used in the paper.

### B. PoC-facing implementation artifacts
These materials translate the legal architecture into a computational proof-of-concept.

Use these if you want to understand:

- governance events;
- evidence objects;
- state machines;
- runtime modules;
- scenario replay.

### Recommended reading paths

#### If you are reading the paper
Start here:

1. **Legal Drafts for ICAIL 2026**
2. **Clause Architecture**
3. **Series Structure Overview**
4. **Modular PoC documentation**

#### If you are inspecting the PoC
Start here:

1. **PoC Implementation Layout**
2. **State Machines**
3. **Governance Events**
4. **Evidence Model**
5. **Scenario replay files**
6. **Runtime modules**

---

## 3. Legal Design Artifacts

This repository explores how Delaware Series LLC structures can serve as purpose-bound governance units for AI deployment.  
Rather than treating AI ethics as a question of explainability alone, it emphasizes human authority, controlled deployment, reviewability, and retained organizational responsibility.

### 3.1 Series-Specific Riders Used in the ICAIL 2026 Case Structure

- [Series A High-Risk AI Alignment Rider](docs/series_a-urban-ride-hailing-high-risk-rider.md)  
  A Delaware Series LLC rider for Level-4 autonomous urban ride-hailing, implementing high-risk controls through oversight gates, audit readiness, and trigger-action-evidence clauses.

- [Series B Limited-Risk AI Transparency Rider](docs/series_b-executive-fleet-leasing-limited-risk-rider.md)  
  A Delaware Series LLC rider for AI-assisted executive fleet scheduling and routing, combining baseline governance with transparency, user notice, and documentation duties.

- [Series C Minimal-Risk AI Baseline Governance Rider](docs/series_c-predictive-maintenance-minimal-risk-rider.md)  
  A Delaware Series LLC rider for internal predictive maintenance models, preserving baseline logging, change control, and accountability with minimal governance overhead.

### 3.2 Series Structure Overview

| Series | Use Case | Risk Tier | Operating Agreement Formula | Core Rider Logic |
|---|---|---|---|---|
| **Series A** | Urban Ride-Hailing | **High-Risk** | `OAride = Cbase ∪ Chigh` | Oversight gates, trigger-action-evidence clauses, audit readiness, evidence preservation, suspension/reactivation controls |
| **Series B** | Executive Fleet Leasing | **Limited-Risk** | `OAfleet = Cbase ∪ Ctransparency` | Baseline governance plus user notice, documentation, transparency, and reclassification safeguards |
| **Series C** | Predictive Maintenance | **Minimal-Risk** | `OAmaint = Cbase only` | Baseline logging, change control, incident escalation, and accountability with minimal overhead |

---

## 4. Modular Clause Architecture

This repository models AI governance in Series LLC form through a modular clause architecture.

- `Cbase` = baseline governance clauses applicable across all AI-related series
- `Chigh` = supplemental clauses for high-risk AI use cases
- `Ctransparency` = supplemental clauses for limited-risk AI use cases

Accordingly:

- `OAride = Cbase ∪ Chigh`
- `OAfleet = Cbase ∪ Ctransparency`
- `OAmaint = Cbase only`

### 4.1 Refactored Legal Drafts by Clause Set

- [Common Cbase AI Governance Rider](docs/common-cbase-ai-governance-rider.md)  
  A baseline Delaware Series LLC governance rider providing common clauses for purpose limitation, human responsibility, change control, baseline logging, and incident escalation across AI-related series.

- [Series A Chigh Add-On](docs/series_a-urban-ride-hailing-chigh-add-on.md)  
  A high-risk add-on for Level-4 autonomous urban ride-hailing, implementing oversight gates, trigger-action-evidence duties, audit readiness, and reactivation controls.

- [Series B Ctransparency Add-On](docs/series_b-executive-fleet-leasing-ctransparency-add-on.md)  
  A limited-risk add-on for AI-assisted executive fleet scheduling and routing, adding user notice, internal documentation, transparency, and reclassification safeguards.

- [Series C Cbase Designation Notice](docs/series_c-predictive-maintenance-cbase-designation.md)  
  A minimal-risk designation notice for internal predictive maintenance, applying Cbase only with no additional high-risk or transparency supplements.

### 4.2 Clause-Set Overview

| Series | Use Case | Risk Tier | Formula | Clause Set |
|---|---|---|---|---|
| **Series A** | Urban Ride-Hailing | **High-Risk** | `OAride = Cbase ∪ Chigh` | Baseline governance plus oversight gates, trigger-action-evidence obligations, audit readiness, and reactivation controls |
| **Series B** | Executive Fleet Leasing | **Limited-Risk** | `OAfleet = Cbase ∪ Ctransparency` | Baseline governance plus user notice, documentation, transparency, and reclassification safeguards |
| **Series C** | Predictive Maintenance | **Minimal-Risk** | `OAmaint = Cbase only` | Baseline governance only, with minimal overhead and preserved logging/accountability expectations |

---

## 5. Additional Legal Drafts

These drafts are broader or alternative rider formulations developed alongside the ICAIL materials.

- [Series A High-Risk AI Alignment Rider](docs/series_a-high-risk-ai-alignment-rider.md)  
  A Delaware Series LLC operating agreement rider for a high-risk AI use case, establishing purpose-binding, human oversight, deployment gates, override and shutdown authority, incident escalation, and organizational accountability.

- [Series B Standard-Risk AI Governance Rider](docs/series_b-standard-risk-ai-governance-rider.md)  
  A Delaware Series LLC rider for standard-risk AI use cases, emphasizing purpose limitation, human supervision, change control, reclassification triggers, and containment of drift into high-risk deployment.

- [Series C Experimental AI Sandbox Rider](docs/series_c-experimental-ai-sandbox-rider.md)  
  A Delaware Series LLC rider for experimental and sandbox AI use cases, emphasizing purpose limitation, sandbox isolation, human supervision, transition review, and prevention of premature production deployment.

- [Delaware High-Risk Alignment Rider Draft](docs/delaware-high-risk-ai-alighment-rider.md)  
  A series-level addendum to a Delaware LLC operating agreement for trace governance, evidentiary preservation, purpose-binding, human oversight, and accountability in AI-assisted and agentic operations.

These drafts are useful for broader governance design discussions, but the **primary ICAIL 2026 story** is the three-series structure in Sections 3 and 4 above.

---

## 6. Legacy Trace-Based PoC

This repository also contains an earlier trace-based PoC companion artifact for the ICAIL 2026 paper:

**Governance-by-Design for AI Compliance: Compiling EU AI Act Duties into Computable Operating-Agreement Clauses**

This older PoC demonstrates how regulatory duties can be represented as computable governance clauses with trigger-action-evidence (TAE) semantics.

### 6.1 Legacy PoC Components

- `clauses/`  
  Machine-readable clause templates corresponding to rider logic.

- `traces/`  
  Synthetic execution traces illustrating governance events and evidence production.

- `schema/`  
  Evidence-store schemas for audit-relevant artifacts.

- `checker/`  
  Minimal validation scripts for checking TAE satisfaction over traces.

- `examples/`  
  Example outputs and sample files.

### 6.2 Legacy Example Scenarios

#### Mobility incident
`traces/mobility_incident_trace.json`

A critical safety incident in a high-risk autonomous mobility deployment, including incident generation, stop order, attempted override, remedy tracking, corrective action, and reporting artifacts.

#### Normal compliant deployment
`traces/normal_operation_trace.json`

A routine high-risk deployment in which required gates, verification records, logging artifacts, and audit records are present.

#### Reasoning trace scenario
`traces/reasoning_trace_example.json`

A safety-critical LLM-agent workflow in which a reasoning trace is preserved, gated by human approval, and later reconstructed for audit or dispute review.

#### Series-specific trace set
- `traces/series_a_incident_trace.json`
- `traces/series_b_transparency_trace.json`
- `traces/series_c_internal_monitoring_trace.json`

These traces correspond to the series-specific rider templates.

### 6.3 Legacy PoC Coverage

The legacy Python checker does not implement the EU AI Act as statutory text.  
Rather, it implements the paper’s clause-level operationalization of selected duties, especially:

- human oversight;
- logging and record-keeping;
- risk management and gatekeeping;
- monitoring, corrective action, and reporting workflows.

### 6.4 Running the Legacy PoC

```bash
python checker/trace_checker.py traces/mobility_incident_trace.json
python checker/trace_checker.py traces/normal_operation_trace.json
python checker/reasoning_trace_checker.py traces/reasoning_trace_example.json
python checker/series_rider_checker.py traces/series_a_incident_trace.json
python checker/series_rider_checker.py traces/series_b_transparency_trace.json
python checker/series_rider_checker.py traces/series_c_internal_monitoring_trace.json
```

---

## 7. Modular PoC (Current Refactoring Direction)

The repository is also evolving toward a more modular PoC architecture that separates:

- governance semantics;
- runtime services;
- events;
- evidence;
- state transitions;
- scenario replay.

### 7.1 PoC Documentation

- [PoC Implementation Layout](docs/poc-implementation-layout.md)  
  Outlines a modular proof-of-concept implementation for the rider architecture, mapping `Cbase`, `Chigh`, and `Ctransparency` to shared services, series-specific overlays, and replayable governance scenarios.

- [State Machines](docs/state-machines.md)  
  Describes the operational lifecycle of Series A, B, and C as governed state machines, including deployment, incident, review, suspension, reclassification, and transfer states.

- [Evidence Model](docs/evidence-model.md)  
  Defines the evidence objects, storage layers, integrity controls, and export profiles that support the modular rider architecture across Series A, B, and C.

- [Governance Events](docs/governance-events.md)  
  Defines the shared event taxonomy, lifecycle, and series-specific event profiles that drive the executable governance layer across Series A, B, and C.

- [Clause-to-Control Matrix](docs/clause-to-control-matrix.md)  
  Maps the modular rider architecture (`Cbase`, `Chigh`, and `Ctransparency`) to an executable PoC governance layer, including controls, events, evidence objects, and state transitions for Series A, B, and C.

### 7.2 Current PoC Modules

#### Shared layer
- [Shared policy and schema files](poc/shared/)  
  Shared governance policy, event schema, evidence schemas, and tier policy logic.

- [Change-control modules](poc/shared/change_control/)  
  Event storage, material change request handling, and approval workflow modules.

- [Incident and override modules](poc/shared/)  
  Incident severity classification, incident management, and human override modules.

#### Series-specific layer
- [Series A runtime modules](poc/series_a/)
- [Series B runtime modules](poc/series_b/)
- [Series C runtime modules](poc/series_c/)

These contain initial implementation modules for:

- Series A deployment gating;
- Series B workflow-dependence monitoring;
- Series C promotion blocking.

#### Scenario replay
- [Series A deployment gate](poc/scenarios/series_a_deployment_request.json)
- [Series B dependence drift](poc/scenarios/series_b_routing_dependence_drift.json)
- [Series C promotion attempt](poc/scenarios/series_c_customer_facing_promotion_attempt.json)
- [Scenario runner](poc/run_scenario.py)

### 7.3 Running the Modular PoC

```bash
python poc/run_scenario.py poc/scenarios/series_a_deployment_request.json --write-summary
python poc/run_scenario.py poc/scenarios/series_b_routing_dependence_drift.json --write-summary
python poc/run_scenario.py poc/scenarios/series_c_customer_facing_promotion_attempt.json --write-summary
```

### 7.4 Minimal Tooling

- [Makefile](Makefile)
- [justfile](justfile)
- [requirements.txt](requirements.txt)

Example usage:

```bash
make install
make init-dirs
make scenarios
make summary
```

or:

```bash
just install
just init-dirs
just scenarios
just summary
```

---

## 8. Current Refactoring Status

The repository currently contains both:

1. a **legacy trace-based PoC**, and  
2. a **new modular runtime-oriented PoC**.

This is intentional during the transition period.

### Current design direction

The modular PoC is moving toward clearer separation between:

- **legal/governance semantics**
- **application services**
- **storage/infrastructure**
- **input data**
- **runtime outputs**

The likely future architecture is:

- `docs/` for paper-facing documentation
- `data/` for registry/scenario inputs
- `src/` for implementation code
- `runtime/` for generated outputs

For now, the repository keeps these materials together because the legal design and the computational PoC still evolve in close relation to one another.

---

## 9. Rider Construction Method

The rider templates in this repository follow a two-layer construction method for operationalizing selected EU AI Act duties into computable governance clauses.

### 9.1 Fundamental (common) layer

This layer contains **fundamental governance clauses** that apply across all series, regardless of risk tier. These clauses establish the baseline organizational infrastructure required for computable governance, including:

- maintenance of an evidence store;
- baseline governance-event logging;
- audit access and retrieval duties;
- override logging and traceability of governance interventions.

Conceptually, this corresponds to the shared governance substrate:

`Cbase`

### 9.2 Risk-based (series-specific) layer

This layer contains **risk-based rider modules** added according to the regulatory and operational profile of a given series.

This yields three series-specific patterns:

- **Series A / Chigh**: emergency stop, strict evidence verification, tamper-evident logging, deployment gates, corrective action, and reporting;
- **Series B / Ctransparency**: transparency notice, approval logging, escalation, and periodic governance review;
- **Series C / Cbase only**: lightweight internal logging, update traceability, anomaly review, and maintenance-action accountability.

### 9.3 Construction principle

**Series-specific Rider = Fundamental Governance Layer + Risk-Based Layer**

or, in the paper’s notation:

**OA_i = C_base ∪ C_tier ∪ C_context**

where:

- `C_base` provides the shared governance substrate;
- `C_tier` adds risk-tier-specific governance intensity;
- `C_context` captures deployment-specific constraints where necessary.

---

## 10. Suggested Use of This Repository

### If your focus is legal design
Read:

- Section 3
- Section 4
- Section 9

### If your focus is the original paper companion PoC
Read:

- Section 6

### If your focus is the current modular implementation direction
Read:

- Section 7
- Section 8

---

## 11. Scope and Limitations

This repository is a research artifact intended to support reproducibility of the paper’s formal model, rider template, and case-study workflow.

It is:

- not production software;
- not legal advice;
- not a complete compliance system;
- not a full implementation of the EU AI Act.

Rather, it is an institutional-design and governance-by-design research artifact.

---

## 12. Relation to the Paper

This repository corresponds to the paper’s:

- modular clause architecture;
- rider templates;
- trigger-action-evidence semantics;
- three-series case structure;
- computational companion discussion.

---

## 13. Citation

If you use or discuss this repository, please cite the ICAIL 2026 paper.

Hiroshi G. Okuno and Mayumi J. Okuno,
*Governance-by-Design for AI Compliance: Compiling EU AI Act Duties into Computable Operating-Agreement Clauses*,
*Proceedings of the 21st International Conference on Artificial Intelligence and Law (ICAIL '26)*, 
JUne 8-12, 2026, Singapore.

---

## 14. Authors

- Hiroshi G. Okuno
- Mayumi J. Okuno

---

## 15. Last Updated

Last updated: 2026-04-23 18:31 JST

