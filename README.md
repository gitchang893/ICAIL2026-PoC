# icail2026-governance-by-design
Companion repository for the ICAIL 2026 paper on Governance-by-Design

# Governance-by-Design PoC

This repository provides a minimal proof-of-concept (PoC) companion artifact for the ICAIL 2026 paper:

**Governance-by-Design for AI Compliance: Compiling EU AI Act Duties into Computable Operating-Agreement Clauses**

## Purpose

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

## Scope

This repository is a minimal research artifact. It is not production software, not legal advice, and not a complete compliance system.

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
