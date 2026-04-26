---
name: providence-mcp-cicd-demo
description: "Use when rehearsing or explaining the Providence MCP plus CI/CD Foundry demo, including GitHub Actions, evaluator gates, and dev/test/prod promotion."
---

# Providence MCP + CI/CD Demo

## When To Use

Use this skill when preparing or running the Monday Providence demo that combines MCP context, Azure AI Foundry, GitHub, CI/CD, and custom evaluations.

## Procedure

1. Read [../../Demo-mapping.md](../../Demo-mapping.md) to anchor the demo in the meeting ask.
2. Read [../../docs/AZURE_RESOURCES.md](../../docs/AZURE_RESOURCES.md) to confirm the resource context and current auth limitation.
3. Run the passing path:

   ```powershell
   python demo/run_demo.py
   ```

4. Open `eval-outputs/github-actions-summary.md` and explain that this is the PR-review summary.
5. Open `eval-outputs/promotion-decision.json` and explain dev -> test -> prod.
6. Run the failing path:

   ```powershell
   python demo/run_demo.py --simulate-failure --ci --fail-on-gate
   ```

7. Open [.github/workflows/providence-mcp-cicd-evaluation.yml](../../.github/workflows/providence-mcp-cicd-evaluation.yml) and show how GitHub Actions enforces the same gate.

## Talk Track

"The MCP layer supplies controlled context. The assistant uses that context. The evaluator gate checks behavior. GitHub Actions decides whether the change can move forward. Production remains a separate handoff."