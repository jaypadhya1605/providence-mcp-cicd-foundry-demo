# Providence Session 5 - MCP + CI/CD Foundry Demo

This repo is the review-ready build for the Monday Providence demo. The story is one connected flow:

1. Developers work against an Azure AI Foundry project in dev.
2. A local MCP-compatible context layer exposes Foundry, policy, patient-scenario, and GitHub CI/CD context as tools.
3. A Providence assistant uses that context to answer care-management scenarios.
4. Custom evaluators score every response.
5. GitHub Actions treats the evaluation result as the promotion gate from dev to test, with prod handoff documented.

The default demo is deterministic and local, so it can run in front of an audience without relying on network latency or tenant auth. Private Azure inventory, presenter notes, and learning materials are intentionally kept out of the public repo.

## Quick Start

```powershell
# Optional, but recommended in OneDrive workspaces
mkvenv
.\.venv\Scripts\Activate.ps1

python demo/run_demo.py
```

Generated outputs land in `eval-outputs/`:

- `demo-run.json` - scenario responses, MCP tools used, evaluator details
- `promotion-decision.json` - dev/test/prod gate decision
- `github-actions-summary.md` - PR-comment style summary for GitHub Actions

To simulate a failing PR gate:

```powershell
python demo/run_demo.py --simulate-failure --ci --fail-on-gate
```

## GitHub Actions CI/CD Demo

The workflow in [.github/workflows/providence-mcp-cicd-evaluation.yml](.github/workflows/providence-mcp-cicd-evaluation.yml) supports two manual demo paths:

- `use_case = success` runs the normal evaluator gate and promotes the release candidate from dev to test.
- `use_case = failure` injects a bad response, blocks in dev, uploads the failed evaluation artifacts, and prevents test/prod handoff jobs from running.

For the hosted MCP path, run the workflow manually with `run_hosted_mcp_smoke = true` and either set repository variable `MCP_HTTP_ENDPOINT` or provide `hosted_mcp_endpoint`. This adds a live pre-check that calls the Azure-hosted MCP server before the local evaluator gate runs.

For a code-side presenter runbook, use [code-demo.md](code-demo.md).

## GitHub Push

This project is ready to publish as a public GitHub repo after confirming no private resource inventory files are staged. The local `.gitignore` excludes `.env`, virtual environments, generated evaluator output, keys/certs, Word documents, PowerPoint decks, and local-only learning folders.