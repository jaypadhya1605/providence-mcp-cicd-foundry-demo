# Demo Mapping - Providence MCP + CI/CD Session

## Executive Story

Providence asked for one combined session, not two disconnected demos: MCP context setup, GitHub integration with an Azure AI Foundry project, CI/CD progression from dev to test to production, and evaluations embedded into that delivery lifecycle.

## Ask To Demo Coverage

| Meeting ask | What this repo shows | Files to open or run |
|---|---|---|
| Combine MCP + CI/CD into one session | A single CLI demo where MCP context tools feed the assistant, then evaluators generate a CI/CD promotion decision. | [demo/run_demo.py](demo/run_demo.py), generated `eval-outputs/github-actions-summary.md` |
| Show GitHub integrated with a Foundry project | Workflow uses Foundry project variables and GitHub Actions gate output. | [.github/workflows/providence-mcp-cicd-evaluation.yml](.github/workflows/providence-mcp-cicd-evaluation.yml), [.env.template](.env.template) |
| Show dev -> test -> prod progression | Promotion decision explicitly separates dev pass, test readiness, and prod team handoff. | [demo/run_demo.py](demo/run_demo.py), generated `eval-outputs/promotion-decision.json` |
| Show developer workflow in dev | Default `DEMO_ENVIRONMENT=dev`; local MCP server and deterministic assistant let developers iterate safely. | [README.md](README.md), [demo/mcp_server.py](demo/mcp_server.py) |
| Show prod team takeover downstream | Prod is not auto-promoted; it requires approval after the test gate. | [spec-kit/constitution.md](spec-kit/constitution.md), generated `promotion-decision.json` |
| Include custom evaluator using CI/CD | Deterministic custom evaluators run as the PR gate. | [demo/evaluators.py](demo/evaluators.py), [.github/workflows/providence-mcp-cicd-evaluation.yml](.github/workflows/providence-mcp-cicd-evaluation.yml) |
| Evaluator can be used on a model or agent | Local assistant simulates the agent under test; the same evaluator contract can score live Foundry responses. | [docs/LIVE_FOUNDRY_PATH.md](docs/LIVE_FOUNDRY_PATH.md), [demo/evaluators.py](demo/evaluators.py) |
| Changes reflected through GitHub Actions | `--simulate-failure` creates a failing gate that GitHub Actions would block. | `python demo/run_demo.py --simulate-failure --ci --fail-on-gate` |
| Evaluations integrated into GitHub | Workflow uploads eval artifacts and writes a PR-summary markdown table. | [.github/workflows/providence-mcp-cicd-evaluation.yml](.github/workflows/providence-mcp-cicd-evaluation.yml) |

## GitHub Actions Use Cases

| Use case | How to run | Expected outcome |
|---|---|---|
| Success path | Manual workflow dispatch with `use_case = success` | Dev evaluator gate passes, test promotion job runs, prod handoff checkpoint runs |
| Failure path | Manual workflow dispatch with `use_case = failure` | Dev evaluator gate fails with `BLOCK_IN_DEV`, artifacts upload, test/prod jobs do not run |

## Recommended Demo Run-Of-Show

1. Start with the sentence from the meeting notes: Providence wants a practical pattern for developers working in Foundry with GitHub, then promoting through CI/CD with evaluation evidence.
2. Show [docs/AZURE_RESOURCES.md](docs/AZURE_RESOURCES.md) so the audience sees this is anchored to their existing resources.
3. Show [spec-kit/feature-spec.md](spec-kit/feature-spec.md) and [spec-kit/implementation-plan.md](spec-kit/implementation-plan.md) to explain spec-driven development.
4. Show [skills/providence-mcp-cicd-demo/SKILL.md](skills/providence-mcp-cicd-demo/SKILL.md) to explain reusable skills.
5. Run `python demo/run_demo.py`.
6. Open the generated GitHub summary and promotion decision.
7. Run the failing simulation to show how a PR gate blocks unsafe change.
8. Close on the handoff: dev can iterate, test gets measurable evidence, prod gets a controlled approval point.