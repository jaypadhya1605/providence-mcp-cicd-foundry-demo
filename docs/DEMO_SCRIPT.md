# Demo Script

## Opening

"Providence asked us to combine MCP and CI/CD into one operating model: developers start in a Foundry project, use GitHub for change control, and every change is evaluated before it moves from dev to test and then to production."

## Demo Steps

1. Open [Demo-mapping.md](../Demo-mapping.md) and point to the ask-to-artifact table.
2. Open [docs/AZURE_RESOURCES.md](AZURE_RESOURCES.md) and show the existing Foundry/APIM/App Insights resources.
3. Open [spec-kit/feature-spec.md](../spec-kit/feature-spec.md) and explain that Spec Kit captures the what and why before coding.
4. Open [skills/providence-mcp-cicd-demo/SKILL.md](../skills/providence-mcp-cicd-demo/SKILL.md) and explain that skills package repeatable agent workflows.
5. Run:

   ```powershell
   python demo/run_demo.py
   ```

6. Open `eval-outputs/github-actions-summary.md` and show the evaluation table.
7. Open `eval-outputs/promotion-decision.json` and show dev/test/prod status.
8. Run:

   ```powershell
   python demo/run_demo.py --simulate-failure --ci --fail-on-gate
   ```

9. Explain that GitHub Actions would block the PR when the custom evaluator gate fails.

## Closing

"The important pattern is not this particular sample prompt. The pattern is that MCP provides controlled project context, GitHub captures change, evaluators provide evidence, and CI/CD promotes only when the evidence passes."