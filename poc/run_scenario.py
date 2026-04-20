from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict


# Make the repository root importable when running:
#   python poc/run_scenario.py ...
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from poc.series_a.deployment_gatekeeper import (  # noqa: E402
    DeploymentGatekeeper,
    DeploymentGatekeeperConfig,
)
from poc.series_b.workflow_dependence_monitor import (  # noqa: E402
    WorkflowDependenceMonitor,
    WorkflowDependenceMonitorConfig,
)
from poc.series_c.promotion_blocker import (  # noqa: E402
    PromotionBlocker,
    PromotionBlockerConfig,
)


class ScenarioRunnerError(Exception):
    """Raised when a scenario cannot be executed."""


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ScenarioRunnerError(f"Scenario file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_summary(output_path: Path, summary: Dict[str, Any]) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    return output_path


def run_series_a_deployment_gate(payload: Dict[str, Any]) -> Dict[str, Any]:
    gatekeeper = DeploymentGatekeeper(
        DeploymentGatekeeperConfig(
            registry_dir=REPO_ROOT / "poc" / "shared" / "series_registry",
            output_dir=REPO_ROOT / "poc" / "series_a" / "gates",
            events_base_dir=REPO_ROOT / "poc" / "shared",
            event_schema_path=REPO_ROOT / "poc" / "shared" / "events" / "event.schema.json",
        )
    )
    record = gatekeeper.evaluate_gate(**payload)
    record_path = gatekeeper.write_gate_record(record)
    return {
        "scenario_type": "series_a_deployment_gate",
        "status": record["status"],
        "record_path": str(record_path),
        "failures": record["failures"],
        "record": record,
    }


def run_series_b_workflow_dependence(payload: Dict[str, Any]) -> Dict[str, Any]:
    monitor = WorkflowDependenceMonitor(
        WorkflowDependenceMonitorConfig(
            output_dir=REPO_ROOT / "poc" / "series_b" / "dependence",
            events_base_dir=REPO_ROOT / "poc" / "shared",
            event_schema_path=REPO_ROOT / "poc" / "shared" / "events" / "event.schema.json",
        )
    )
    record = monitor.evaluate(**payload)
    record_path = monitor.write_record(record)
    return {
        "scenario_type": "series_b_workflow_dependence",
        "status": record["status"],
        "triggered": record["triggered"],
        "record_path": str(record_path),
        "record": record,
    }


def run_series_c_promotion_attempt(payload: Dict[str, Any]) -> Dict[str, Any]:
    blocker = PromotionBlocker(
        PromotionBlockerConfig(
            registry_dir=REPO_ROOT / "poc" / "shared" / "series_registry",
            output_dir=REPO_ROOT / "poc" / "series_c" / "promotion_blocks",
            tier_review_output_dir=REPO_ROOT / "poc" / "shared" / "tier_review" / "reviews",
            events_base_dir=REPO_ROOT / "poc" / "shared",
            event_schema_path=REPO_ROOT / "poc" / "shared" / "events" / "event.schema.json",
        )
    )
    record = blocker.evaluate_promotion_attempt(**payload)
    record_path = blocker.write_block_record(record)
    return {
        "scenario_type": "series_c_promotion_attempt",
        "status": record["status"],
        "blocked": record["blocked"],
        "record_path": str(record_path),
        "recommended_tier": record["tier_review"]["recommended_tier"],
        "record": record,
    }


def run_scenario_file(scenario_path: Path) -> Dict[str, Any]:
    scenario = load_json(scenario_path)

    scenario_id = scenario.get("scenario_id", scenario_path.stem)
    scenario_type = scenario.get("scenario_type")
    payload = scenario.get("payload", {})

    if not scenario_type:
        raise ScenarioRunnerError("Scenario missing required field: scenario_type")

    if scenario_type == "series_a_deployment_gate":
        result = run_series_a_deployment_gate(payload)
    elif scenario_type == "series_b_workflow_dependence":
        result = run_series_b_workflow_dependence(payload)
    elif scenario_type == "series_c_promotion_attempt":
        result = run_series_c_promotion_attempt(payload)
    else:
        raise ScenarioRunnerError(f"Unsupported scenario_type: {scenario_type}")

    return {
        "scenario_id": scenario_id,
        "scenario_type": scenario_type,
        "description": scenario.get("description", ""),
        "result": result,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a PoC governance scenario.")
    parser.add_argument(
        "scenario",
        type=str,
        help="Path to scenario JSON file, e.g. poc/scenarios/series_a_deployment_request.json",
    )
    parser.add_argument(
        "--write-summary",
        action="store_true",
        help="Write a summary JSON under poc/scenarios/results/",
    )
    args = parser.parse_args()

    scenario_path = Path(args.scenario).resolve()
    output = run_scenario_file(scenario_path)

    print(json.dumps(output, ensure_ascii=False, indent=2))

    if args.write_summary:
        results_dir = REPO_ROOT / "poc" / "scenarios" / "results"
        summary_path = results_dir / f'{output["scenario_id"]}_result.json'
        write_summary(summary_path, output)
        print(f"\nWrote summary to {summary_path}")


if __name__ == "__main__":
    main()
