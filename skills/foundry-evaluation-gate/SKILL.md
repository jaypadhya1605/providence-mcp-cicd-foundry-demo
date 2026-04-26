---
name: foundry-evaluation-gate
description: "Use when building or reviewing Providence custom evaluator gates for Foundry model or agent changes in GitHub Actions CI/CD."
---

# Foundry Evaluation Gate

## When To Use

Use this skill when the discussion is about custom evaluators, GitHub Actions quality gates, model or agent changes, or blocking a PR based on evaluation evidence.

## Procedure

1. Inspect [../../demo/evaluators.py](../../demo/evaluators.py).
2. Confirm each evaluator has a clear pass threshold.
3. Run the normal evaluation gate:

   ```powershell
   python demo/run_demo.py --ci --fail-on-gate
   ```

4. Run the failure simulation:

   ```powershell
   python demo/run_demo.py --simulate-failure --ci --fail-on-gate
   ```

5. Explain which evaluator failed and why.
6. Show the generated `github-actions-summary.md` as the PR comment artifact.

## Gate Rules In This Demo

- Required fields must all be present.
- PHI leak scan must find zero matches.
- Groundedness score must be at least `0.75`.
- MCP usage must be present in the response.

## Best Practice

Keep deterministic gates for hard controls like PHI patterns. Add LLM-judge evaluators later for semantic quality, but do not replace deterministic safety checks with judge prompts.