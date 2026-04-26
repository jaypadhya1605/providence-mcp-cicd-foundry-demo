# Feature Spec - Providence MCP + CI/CD Foundry Demo

## User Story

As a Providence platform or AI engineering team member, I want to see how GitHub, Azure AI Foundry, MCP context, and custom evaluations fit into one delivery workflow so that teams can safely move AI changes from dev to test to production with measurable evidence.

## Requirements

1. The demo must combine MCP and CI/CD into one story.
2. The demo must visibly use the documented Azure AI Foundry project context.
3. The demo must show GitHub as the change-control and CI/CD surface.
4. The demo must model dev -> test -> prod progression.
5. The demo must include custom evaluator logic.
6. The demo must show how evaluator results can block or allow promotion.
7. The demo must be runnable locally before live Azure auth is fixed.
8. The demo must avoid real PHI and avoid committing secrets.
9. The demo must include learning docs for spec-kit and skills.

## Acceptance Criteria

| Criteria | Evidence |
|---|---|
| Local end-to-end demo runs | `python demo/run_demo.py` completes with exit code 0 |
| MCP-style context is used | Generated `demo-run.json` lists tool calls per scenario |
| Custom evaluators run | Generated `demo-run.json` contains evaluator metrics |
| CI/CD gate can pass | `promotion-decision.json` has decision `PROMOTE_TO_TEST` |
| CI/CD gate can fail | `python demo/run_demo.py --simulate-failure --ci --fail-on-gate` exits non-zero |
| GitHub workflow exists | `.github/workflows/providence-mcp-cicd-evaluation.yml` |
| Ask-to-demo mapping exists | `Demo-mapping.md` |
| Jay learning docs exist | `spec-kit/JAY_LEARNING.md` and `skills/JAY_LEARNING.md` |

## Out Of Scope For First Review

- Pushing to GitHub.
- Creating or deleting Azure resources.
- Running live Foundry model calls before the tenant mismatch is fixed.
- Storing Application Insights instrumentation keys or credentials in repo files.