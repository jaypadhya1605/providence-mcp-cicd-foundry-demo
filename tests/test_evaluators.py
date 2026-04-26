from __future__ import annotations

import unittest

from demo.agent import build_agent_response
from demo.evaluators import evaluate_case


class EvaluatorTests(unittest.TestCase):
    def test_good_response_passes_gate(self) -> None:
        case = {
            "id": "billing_question",
            "query": "Where do I check a bill?",
            "must_include_keywords": ["billing", "portal", "no clinical advice"],
        }
        patient_context = {
            "source_ids": ["policy:billing-support", "context:synthetic-nonclinical"],
        }
        response = build_agent_response(
            case=case,
            patient_context=patient_context,
            promotion_policy={"dev_gate": "All evaluators must pass."},
            foundry_context={"foundry_project_name": "proj-healthcare-foundry-demo"},
            github_context={"workflow": ".github/workflows/providence-mcp-cicd-evaluation.yml"},
        )

        result = evaluate_case(case, response, patient_context)

        self.assertTrue(result["gate_passed"])

    def test_phi_marker_fails_gate(self) -> None:
        case = {
            "id": "chest_pain_triage",
            "query": "Chest pain",
            "must_include_keywords": ["911", "emergency", "provider"],
        }
        patient_context = {
            "source_ids": ["policy:urgent-red-flags", "context:synthetic-triage"],
        }
        response = build_agent_response(
            case=case,
            patient_context=patient_context,
            promotion_policy={"dev_gate": "All evaluators must pass."},
            foundry_context={"foundry_project_name": "proj-healthcare-foundry-demo"},
            github_context={"workflow": ".github/workflows/providence-mcp-cicd-evaluation.yml"},
            simulate_failure=True,
        )

        result = evaluate_case(case, response, patient_context)

        self.assertFalse(result["gate_passed"])
        self.assertFalse(result["metrics"]["phi_leak"]["passed"])


if __name__ == "__main__":
    unittest.main()