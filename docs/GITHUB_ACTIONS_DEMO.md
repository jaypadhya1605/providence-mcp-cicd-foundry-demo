# GitHub Actions CI/CD Demo

This repo demonstrates a simple AI delivery gate:

1. A developer changes agent, prompt, dataset, skill, or evaluator code in dev.
2. Optional live smoke gate verifies the hosted Providence MCP endpoint is reachable.
3. GitHub Actions runs unit tests and the custom evaluator gate.
4. Passing evaluations promote the release candidate to test.
5. Production remains a handoff checkpoint, not an automatic deployment.

## Public Repo Safety

The committed demo uses synthetic data only. The workflow does not require Azure secrets for the local gate. Live Azure/Foundry deployment can be added later with GitHub OIDC after tenant auth and RBAC are configured.

The Word resource inventory is intentionally ignored because it may contain non-public environment details.

## Hosted MCP Smoke Gate

After the Foundry agent successfully calls the Azure-hosted Providence MCP server, use the same endpoint as an optional GitHub Actions pre-check.

Manual workflow inputs:

```text
run_hosted_mcp_smoke = true
hosted_mcp_endpoint = https://<container-app-fqdn>/mcp
```

You can also set repository variable `MCP_HTTP_ENDPOINT` and leave `hosted_mcp_endpoint` empty.

The hosted smoke gate calls:

- `initialize`
- `tools/list`
- `get_promotion_policy`
- `get_github_cicd_context`

It writes these artifacts:

- `eval-outputs/hosted-mcp-smoke.json`
- `eval-outputs/hosted-mcp-smoke-summary.md`

If this gate fails, the release stays in dev because the live MCP dependency is not healthy enough for the demo path.

## Success Use Case

Run the workflow manually with:

```text
use_case = success
```

Expected result:

- Optional hosted MCP smoke gate passes when enabled.
- `Dev evaluator gate` passes.
- Evaluation artifacts are uploaded.
- The job summary shows `PROMOTE_TO_TEST`.
- `Promote release candidate to test` runs.
- `Production handoff checkpoint` runs and records that prod requires approval.

Equivalent local command:

```powershell
python demo/run_demo.py --ci --fail-on-gate
```

## Failure Use Case

Run the workflow manually with:

```text
use_case = failure
```

Expected result:

- Optional hosted MCP smoke gate passes when enabled.
- `Dev evaluator gate` fails.
- Evaluation artifacts are still uploaded.
- The job summary shows `BLOCK_IN_DEV`.
- The failing case is `chest_pain_triage`.
- Test promotion and prod handoff jobs do not run.

Equivalent local command:

```powershell
python demo/run_demo.py --simulate-failure --ci --fail-on-gate
```

## Talk Track

"GitHub is the change boundary. The evaluator gate converts model or agent behavior into release evidence. If the evidence passes, the change can move from dev to test. If it fails, it stays blocked in dev. Production requires a separate operational handoff."

For the hosted MCP path:

"The Foundry agent proved it can call our MCP server live. GitHub Actions adds a release check on top of that by smoke-testing the same hosted MCP endpoint, then running the deterministic evaluator gate that decides whether the change can move from dev to test."
