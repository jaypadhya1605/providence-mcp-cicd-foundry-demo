# Demo Mapping - Providence MCP + CI/CD Session

## Executive Story

Providence asked for one combined session, not two disconnected demos: MCP context setup, GitHub integration with an Azure AI Foundry project, CI/CD progression from dev to test to production, and evaluations embedded into that delivery lifecycle.

## Ask To Demo Coverage

| Meeting ask | What this repo shows | Files to open or run |
|---|---|---|
| Combine MCP + CI/CD into one session | Start with Azure AI Foundry MCP tools, then show the local MCP server/client and GitHub Actions evaluator gate. | [docs/MCP_FIRST_DEMO_RUNBOOK.md](docs/MCP_FIRST_DEMO_RUNBOOK.md), [demo/run_demo.py](demo/run_demo.py) |
| Show GitHub integrated with a Foundry project | Workflow uses Foundry project variables and GitHub Actions gate output. | [.github/workflows/providence-mcp-cicd-evaluation.yml](.github/workflows/providence-mcp-cicd-evaluation.yml), [.env.template](.env.template) |
| Show dev -> test -> prod progression | Promotion decision explicitly separates dev pass, test readiness, and prod team handoff. | [demo/run_demo.py](demo/run_demo.py), generated `eval-outputs/promotion-decision.json` |
| Show developer workflow in dev | Default `DEMO_ENVIRONMENT=dev`; local MCP server/client and deterministic assistant let developers iterate safely after seeing the Foundry UI MCP pattern. | [README.md](README.md), [demo/mcp_server.py](demo/mcp_server.py), [demo/mcp_client.py](demo/mcp_client.py) |
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

1. Start in Azure AI Foundry and show the agent connected to GitHub MCP and Microsoft Learn MCP.
2. Ask the Foundry agent to use Microsoft Learn MCP, then ask it to inspect the GitHub repo/workflow through GitHub MCP.
3. Open [docs/MCP_FIRST_DEMO_RUNBOOK.md](docs/MCP_FIRST_DEMO_RUNBOOK.md) and transition from UI to implementation.
4. Show [demo/mcp_server.py](demo/mcp_server.py) and [demo/mcp_client.py](demo/mcp_client.py) to explain the local MCP server/client pattern.
5. Show [demo/run_demo.py](demo/run_demo.py) and [demo/agent.py](demo/agent.py) to explain how MCP context reaches the agent response.
6. Run `python demo/run_demo.py` and open `eval-outputs/demo-run.json`.
7. Open the GitHub Actions workflow and run the success case.
8. Run the failure case to show how a custom evaluator blocks unsafe change in dev.
9. Close on the handoff: MCP grounds the agent, evaluators create evidence, GitHub enforces the dev -> test -> prod boundary.