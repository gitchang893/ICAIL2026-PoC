import json
import sys
from pathlib import Path

# Minimal clause-to-required-artifacts mapping
CLAUSE_REQUIREMENTS = {
    "2.1": ["StopOrderRecord"],
    "2.2": ["AttemptedOverride", "RemedyRecord"],
    "3.1": ["IntegrityProof"],
    "3.2": ["RetentionRecord"],
    "3.3": ["VerificationRecord"],
    "4.1": ["DeployDeniedLog", "DeployApprovalRecord"],
    "4.2": ["UpdateAssessment", "AuditReport"],
    "5.1": ["MaintenanceRecord"],
    "5.2": ["CAP", "IncidentRecord", "ProofOfSubmission"],
    "5.3": []
}


def load_trace(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_artifacts(trace: dict) -> set:
    artifacts = set()
    for event in trace.get("events", []):
        for artifact in event.get("artifacts", []):
            artifacts.add(artifact)
    return artifacts


def check_clause(clause_id: str, artifacts: set) -> dict:
    required = CLAUSE_REQUIREMENTS.get(clause_id, [])
    if not required:
        return {
            "clause": clause_id,
            "status": "PASS",
            "missing": [],
            "note": "No artifact requirement defined."
        }

    # Clause 4.1 can be satisfied by either deploy denial or deploy approval evidence
    if clause_id == "4.1":
        ok = ("DeployDeniedLog" in artifacts) or ("DeployApprovalRecord" in artifacts)
        return {
            "clause": clause_id,
            "status": "PASS" if ok else "FAIL",
            "missing": [] if ok else ["DeployDeniedLog or DeployApprovalRecord"],
            "note": "Either denial or approval evidence satisfies the gate outcome."
        }

    # Clause 4.2 can be satisfied by reassessment or scheduled audit evidence
    if clause_id == "4.2":
        ok = ("UpdateAssessment" in artifacts) or ("AuditReport" in artifacts)
        return {
            "clause": clause_id,
            "status": "PASS" if ok else "FAIL",
            "missing": [] if ok else ["UpdateAssessment or AuditReport"],
            "note": "Either reassessment or audit output is accepted."
        }

    missing = [a for a in required if a not in artifacts]
    return {
        "clause": clause_id,
        "status": "PASS" if not missing else "FAIL",
        "missing": missing,
        "note": ""
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python checker/trace_checker.py <trace.json>")
        sys.exit(1)

    trace_path = Path(sys.argv[1])
    if not trace_path.exists():
        print(f"Error: file not found: {trace_path}")
        sys.exit(1)

    trace = load_trace(str(trace_path))
    artifacts = collect_artifacts(trace)
    expected = trace.get("expected_clauses_satisfied", [])

    print(f"Trace ID: {trace.get('trace_id', 'unknown')}")
    print(f"Scenario: {trace.get('scenario', 'unknown')}")
    print(f"Collected artifacts: {sorted(artifacts)}")
    print()

    overall_pass = True
    for clause_id in expected:
        result = check_clause(clause_id, artifacts)
        print(f"[{result['status']}] Clause {result['clause']}")
        if result["missing"]:
            print(f"  Missing: {', '.join(result['missing'])}")
            overall_pass = False
        if result["note"]:
            print(f"  Note: {result['note']}")

    print()
    print("Overall result:", "PASS" if overall_pass else "FAIL")


if __name__ == "__main__":
    main()
