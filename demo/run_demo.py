from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .agent import build_agent_response
    from .config import ROOT, load_config
    from .evaluators import evaluate_case
    from .mcp_client import MCPClient
except ImportError:
    from agent import build_agent_response
    from config import ROOT, load_config
    from evaluators import evaluate_case
    from mcp_client import MCPClient


DATASET = ROOT / "datasets" / "care_scenarios.jsonl"
OUTPUT_DIR = ROOT / "eval-outputs"


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _promotion_decision(results: list[dict[str, Any]], config_environment: str) -> dict[str, Any]:
    passed = all(result["evaluation"]["gate_passed"] for result in results)
    return {
        "decision": "PROMOTE_TO_TEST" if passed else "BLOCK_IN_DEV",
        "current_environment": config_environment,
        "dev": "passed" if passed else "failed",
        "test": "ready_for_release_candidate_eval" if passed else "not_ready",
        "prod": "requires_prod_team_approval_after_test_evidence" if passed else "not_eligible",
        "case_count": len(results),
        "failed_cases": [result["case_id"] for result in results if not result["evaluation"]["gate_passed"]],
    }


def _write_summary(path: Path, run_payload: dict[str, Any], decision: dict[str, Any]) -> None:
    lines = [
        "# Providence MCP + CI/CD Evaluation Summary",
        "",
        f"Decision: **{decision['decision']}**",
        "",
        "| Case | Gate | Required fields | PHI leak | Groundedness | MCP usage |",
        "|---|---|---:|---:|---:|---:|",
    ]

    for result in run_payload["results"]:
        metrics = result["evaluation"]["metrics"]
        lines.append(
            "| {case} | {gate} | {required:.2f} | {phi:.2f} | {grounded:.2f} | {mcp:.2f} |".format(
                case=result["case_id"],
                gate="pass" if result["evaluation"]["gate_passed"] else "fail",
                required=metrics["required_fields"]["score"],
                phi=metrics["phi_leak"]["score"],
                grounded=metrics["groundedness"]["score"],
                mcp=metrics["mcp_usage"]["score"],
            )
        )

    lines.extend(
        [
            "",
            "## Promotion Status",
            "",
            f"- Dev: `{decision['dev']}`",
            f"- Test: `{decision['test']}`",
            f"- Prod: `{decision['prod']}`",
            "",
            "This is the markdown artifact a GitHub Action can attach to a pull request.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(simulate_failure: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    config = load_config()
    cases = _load_jsonl(DATASET)

    with MCPClient() as mcp:
        tools = mcp.list_tools()
        foundry_context = mcp.call_tool("get_foundry_project_context")
        promotion_policy = mcp.call_tool("get_promotion_policy")
        github_context = mcp.call_tool("get_github_cicd_context")

        results: list[dict[str, Any]] = []
        for case in cases:
            patient_context = mcp.call_tool("get_patient_context", {"scenario_id": case["id"]})
            response = build_agent_response(
                case=case,
                patient_context=patient_context,
                promotion_policy=promotion_policy,
                foundry_context=foundry_context,
                github_context=github_context,
                simulate_failure=simulate_failure,
            )
            evaluation = evaluate_case(case, response, patient_context)
            results.append(
                {
                    "case_id": case["id"],
                    "query": case["query"],
                    "patient_context": patient_context,
                    "response": response,
                    "evaluation": evaluation,
                }
            )

    run_payload = {
        "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "demo": "Providence MCP + CI/CD Foundry demo",
        "mode": "failure-simulation" if simulate_failure else "normal",
        "mcp_tools": tools,
        "foundry_context": foundry_context,
        "github_context": github_context,
        "promotion_policy": promotion_policy,
        "results": results,
    }
    decision = _promotion_decision(results, config.demo_environment)
    return run_payload, decision


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Providence MCP + CI/CD evaluation demo.")
    parser.add_argument("--simulate-failure", action="store_true", help="Inject a bad change so the CI gate fails.")
    parser.add_argument("--ci", action="store_true", help="Print CI-friendly output.")
    parser.add_argument("--fail-on-gate", action="store_true", help="Return non-zero when the evaluation gate fails.")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)
    run_payload, decision = run(simulate_failure=args.simulate_failure)

    _write_json(OUTPUT_DIR / "demo-run.json", run_payload)
    _write_json(OUTPUT_DIR / "promotion-decision.json", decision)
    _write_summary(OUTPUT_DIR / "github-actions-summary.md", run_payload, decision)

    print("Providence MCP + CI/CD demo complete")
    print(f"Decision: {decision['decision']}")
    print(f"Wrote: {OUTPUT_DIR / 'demo-run.json'}")
    print(f"Wrote: {OUTPUT_DIR / 'promotion-decision.json'}")
    print(f"Wrote: {OUTPUT_DIR / 'github-actions-summary.md'}")

    if args.fail_on_gate and decision["decision"] != "PROMOTE_TO_TEST":
        if args.ci:
            print("CI gate failed because one or more evaluators failed.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())