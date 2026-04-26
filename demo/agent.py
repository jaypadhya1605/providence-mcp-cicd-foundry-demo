from __future__ import annotations

from typing import Any


def build_agent_response(
    case: dict[str, Any],
    patient_context: dict[str, Any],
    promotion_policy: dict[str, Any],
    foundry_context: dict[str, Any],
    github_context: dict[str, Any],
    simulate_failure: bool = False,
) -> dict[str, Any]:
    scenario_id = case["id"]
    query = case["query"]
    source_context = patient_context["source_ids"]

    if scenario_id == "chest_pain_triage":
        answer = (
            "This sounds urgent because chest pain with shortness of breath can be an emergency. "
            "Please call 911 or seek emergency care now. I cannot diagnose the cause, but a provider "
            "should evaluate this immediately."
        )
        risk_level = "urgent"
        escalation_path = "Emergency services or nearest emergency department."
        care_guidance = ["Call 911", "Do not drive yourself", "Seek immediate provider evaluation"]
    elif scenario_id == "medication_question":
        answer = (
            "Do not change medication dose without a clinician. Use the Providence care team or pharmacy "
            "workflow to ask a provider to review the medication question."
        )
        risk_level = "needs_clinician_review"
        escalation_path = "Route to licensed clinician or pharmacist review."
        care_guidance = ["Do not change dose", "Contact provider", "Use medication review workflow"]
    else:
        answer = (
            "For billing status, use the patient portal or Providence billing support. This is a billing "
            "question, so I will not provide clinical advice."
        )
        risk_level = "routine"
        escalation_path = "Route to billing support or patient portal."
        care_guidance = ["Check patient portal", "Contact billing support", "No clinical advice needed"]

    response = {
        "answer": answer,
        "risk_level": risk_level,
        "care_guidance": care_guidance,
        "escalation_path": escalation_path,
        "source_context": source_context,
        "foundry_project": foundry_context["foundry_project_name"],
        "github_workflow": github_context["workflow"],
        "promotion_policy": promotion_policy["dev_gate"],
        "mcp_tools_used": [
            "get_foundry_project_context",
            "get_promotion_policy",
            "get_patient_context",
            "get_github_cicd_context",
        ],
        "query": query,
    }

    if simulate_failure and scenario_id == "chest_pain_triage":
        response.pop("escalation_path")
        response["answer"] += " Synthetic failure marker: MRN 123456 should never appear in output."

    return response