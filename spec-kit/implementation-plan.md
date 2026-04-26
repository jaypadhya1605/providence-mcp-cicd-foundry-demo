# Implementation Plan - Providence MCP + CI/CD Foundry Demo

## Architecture

```text
Developer change
  -> GitHub pull request
  -> GitHub Actions
  -> local MCP context server
  -> Providence assistant response
  -> custom evaluator gate
  -> promotion decision: dev passed, test ready, prod requires approval
```

## Components

| Component | Purpose |
|---|---|
| `demo/mcp_server.py` | Exposes Foundry, promotion-policy, GitHub, and patient-scenario context as MCP-compatible stdio tools |
| `demo/mcp_client.py` | Calls the local MCP server over JSON lines |
| `demo/agent.py` | Creates deterministic Providence assistant responses using MCP context |
| `demo/evaluators.py` | Scores required fields, PHI leakage, groundedness, and MCP context usage |
| `demo/run_demo.py` | Orchestrates the full run and writes CI/CD outputs |
| `.github/workflows/providence-mcp-cicd-evaluation.yml` | Runs the same gate in GitHub Actions |
| `skills/` | Reusable playbooks an AI assistant could load for this demo |
| `spec-kit/` | Specs, plan, tasks, and learning docs |

## Azure Strategy

The demo reuses existing resources from `azure-resources.docx`. No Azure resources are created in this review pass because live calls currently fail on tenant mismatch.

Once the Azure context is fixed, the live path is:

1. List deployments in the target Foundry account.
2. Fill `FOUNDRY_MODEL_DEPLOYMENT_NAME` in `.env`.
3. Enable `LIVE_FOUNDRY_ENABLED=true`.
4. Replace deterministic response generation with a live Foundry model or agent response.
5. Keep the evaluator gate and GitHub workflow unchanged.

## GitHub Actions Gate

The workflow runs:

```powershell
python demo/run_demo.py --ci --fail-on-gate
```

If any evaluator fails, the command exits non-zero. This is the PR gate.

## Evaluation Strategy

The first-review evaluator stack is deterministic so the demo is stable:

- Required fields: verifies the response contains operational fields Providence reviewers expect.
- PHI leak scan: catches synthetic SSN/MRN/email/phone patterns.
- Groundedness: verifies the response cites MCP source context and includes required keywords.
- MCP usage: verifies the response records tool usage.

The live Foundry version can add LLM-judge evaluators later, but deterministic checks should stay because they are auditable and cheap.