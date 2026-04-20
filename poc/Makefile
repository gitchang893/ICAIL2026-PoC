PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

SCENARIO_DIR := poc/scenarios
RESULT_DIR := poc/scenarios/results

.PHONY: help install init-dirs check \
	scenario-a scenario-b scenario-c scenarios \
	summary clean-results

help:
	@echo "Available targets:"
	@echo "  install        Install minimal Python dependencies"
	@echo "  init-dirs      Create expected PoC directories"
	@echo "  check          Run basic module checks"
	@echo "  scenario-a     Run Series A deployment gate scenario"
	@echo "  scenario-b     Run Series B dependence drift scenario"
	@echo "  scenario-c     Run Series C promotion attempt scenario"
	@echo "  scenarios      Run all scenarios"
	@echo "  summary        List generated scenario result files"
	@echo "  clean-results  Remove generated scenario result files"

install:
	$(PIP) install -r requirements.txt

init-dirs:
	mkdir -p poc/shared/events/indexes
	mkdir -p poc/shared/evidence_model/records
	mkdir -p poc/shared/evidence_model/artifacts
	mkdir -p poc/shared/tier_review/reviews
	mkdir -p poc/shared/change_control/change_requests/indexes
	mkdir -p poc/shared/incidents/cases
	mkdir -p poc/shared/incidents/indexes
	mkdir -p poc/shared/overrides/records
	mkdir -p poc/shared/overrides/indexes
	mkdir -p poc/series_a/gates
	mkdir -p poc/series_b/dependence
	mkdir -p poc/series_c/promotion_blocks
	mkdir -p $(RESULT_DIR)

check:
	$(PYTHON) poc/shared/policy_engine/tier_policy.py
	$(PYTHON) poc/shared/tier_review/tier_review_service.py || true
	$(PYTHON) poc/shared/events/event_writer.py
	$(PYTHON) poc/shared/evidence_model/writers/artifact_linker.py
	$(PYTHON) poc/shared/change_control/change_request.py
	$(PYTHON) poc/shared/change_control/approval_flow.py || true
	$(PYTHON) poc/shared/incidents/severity_rules.py
	$(PYTHON) poc/shared/incidents/incident_service.py
	$(PYTHON) poc/shared/overrides/override_service.py
	$(PYTHON) poc/series_a/deployment_gatekeeper.py
	$(PYTHON) poc/series_b/workflow_dependence_monitor.py
	$(PYTHON) poc/series_c/promotion_blocker.py

scenario-a: init-dirs
	$(PYTHON) poc/run_scenario.py $(SCENARIO_DIR)/series_a_deployment_request.json --write-summary

scenario-b: init-dirs
	$(PYTHON) poc/run_scenario.py $(SCENARIO_DIR)/series_b_routing_dependence_drift.json --write-summary

scenario-c: init-dirs
	$(PYTHON) poc/run_scenario.py $(SCENARIO_DIR)/series_c_customer_facing_promotion_attempt.json --write-summary

scenarios: scenario-a scenario-b scenario-c

summary:
	@echo "Scenario result files:"
	@ls -1 $(RESULT_DIR)/*.json 2>/dev/null || echo "  (none)"

clean-results:
	rm -f $(RESULT_DIR)/*.json
