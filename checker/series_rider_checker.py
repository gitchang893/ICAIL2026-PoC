import json
import sys
from pathlib import Path

CLAUSE_REQUIREMENTS = {
    # Series A
    "A-1": ["StopOrderRecord"],
    "A-2": ["IntegrityProof"],
    "A-3": ["VerificationRecord"],
    "A-4": ["DeployDeniedLog"],
    "A-5": ["CAP", "ProofOfSubmission"],

    # Series B
    "B-1": ["TransparencyNoticeRecord"],
    "B-2": ["DeployApprovalRecord"],
    "B-3": ["IncidentEscalationRecord"],
    "B-4": ["GovernanceReviewRecord"],

    # Series C
    "C-1": ["InternalLogRecord"],
    "C-2": ["ModelUpdateRecord"],
    "C-3": ["AnomalyReviewRecord"],
    "C-4": ["MaintenanceActionRecord"],
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
    missing = [a for a in required if a not in artifacts]
    return {
        "clause": clause_id,
        "status": "PASS" if not missing else "FAIL",
        "missing": missing
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python checker/series_rider_checker.py <trace.json>")
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
    print(f"Series: {trace.get('series', 'unknown')}")
    print(f"Collected artifacts: {sorted(artifacts)}")
    print()

    overall_pass = True
    for clause_id in expected:
        result = check_clause(clause_id, artifacts)
        print(f"[{result['status']}] Clause {result['clause']}")
        if result["missing"]:
            print(f"  Missing: {', '.join(result['missing'])}")
            overall_pass = False

    print()
    print("Overall result:", "PASS" if overall_pass else "FAIL")


if __name__ == "__main__":
    main()
