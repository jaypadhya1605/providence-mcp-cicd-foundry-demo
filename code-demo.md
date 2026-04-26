
Open these files in this order:

2. [demo/mcp_server.py](demo/mcp_server.py)
3. [demo/mcp_http_server.py](demo/mcp_http_server.py)
4. [demo/agent.py](demo/agent.py)
5. [demo/evaluators.py](demo/evaluators.py)
6. [demo/run_demo.py](demo/run_demo.py)
7. [.github/workflows/providence-mcp-cicd-evaluation.yml](.github/workflows/providence-mcp-cicd-evaluation.yml)

### Say

"There are three layers in this repo. First, the MCP layer defines tools and exposes them to Foundry. Second, the agent and evaluator layer turns MCP context into a response and scores it. Third, the GitHub Actions layer turns those scores into a release decision."

### Explain The files to run in the demo
```text
demo/mcp_server.py                 = local MCP tools
demo/mcp_http_server.py            = hosted HTTP bridge for Foundry
demo/agent.py                      = deterministic demo agent response
demo/evaluators.py                 = custom evaluator gate
demo/run_demo.py                   = local orchestration
demo/smoke_mcp_http.py             = hosted MCP smoke test
.github/workflows/...yml           = CI/CD promotion workflow
```


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 2. Explain The MCP Server

Open [demo/mcp_server.py](demo/mcp_server.py).

Find:

```python
_tool_definitions()
```
Then find:

```python
_call_tool()
```

### Say
"This file is the MCP tool server. It defines what tools the agent can call. In this demo, the tools return Foundry project context, promotion policy, synthetic patient scenario context, and GitHub CI/CD context."
"The `_tool_definitions` function is the catalog. It tells MCP clients what tools exist and what inputs each tool accepts."
"The `_call_tool` function is where a tool call becomes a result. When the agent asks for the promotion policy, this code returns the dev, test, and prod gate rules."



```text
mcp_server.py defines what the AI can do.
```
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 3. Explain The HTTP Bridge

Open [demo/mcp_http_server.py](demo/mcp_http_server.py).


### Say

"The MCP server is useful locally, but Foundry needs a reachable HTTPS endpoint. This file turns the same MCP tool behavior into an HTTP-compatible MCP endpoint."
"That is why we hosted it on Azure Container Apps. Foundry can call the hosted `/mcp` endpoint, discover the tool catalog, and invoke the same tools that we can test locally."


```text
mcp_server.py defines tools. mcp_http_server.py exposes those tools to Foundry.
```
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 4. Explain The Agent Response

Open [demo/agent.py](demo/agent.py).

```python
build_agent_response(...)
```

Then find the intentional failure block:

```python
if simulate_failure and scenario_id == "chest_pain_triage":
```

### Say
"This file simulates the agent response for the CI/CD. The important part is that the response is built from MCP context, not from an uncontrolled free-form answer."
"The `build_agent_response` function builds the response that our evaluators will inspect."
"This failure block is intentional. It removes a required escalation field and injects an MRN-like marker. That gives us a reliable way to prove the CI/CD gate can block a bad agent change."

### Keep It Simple

```text
agent.py creates the response. The failure flag creates a bad response on purpose.
```
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 5. Explain The Evaluators


Open [demo/evaluators.py](demo/evaluators.py).

Find these functions:

```python
required_fields_score()
phi_leak_score()
groundedness_score()
mcp_usage_score()
evaluate_case()
```

### Say

"This is the governance layer. These evaluators decide whether the agent response is acceptable for promotion."
"The required-fields makes sure operational fields are present. The PHI check looks for PHI-like patterns. The groundedness check makes sure the response is connected to the expected context. The MCP usage check confirms that tool usage was recorded." "The gate only passes when every required metric passes. That is what makes this useful in CI/CD."

### Keep It Simple

```text
evaluators.py decides whether the response is safe enough to promote.
```
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 6. Explain The Demo Orchestrator

Open [demo/run_demo.py](demo/run_demo.py).

Find:

```python
_promotion_decision()
```

Then find the CLI flags:

```python
--simulate-failure
--ci
--fail-on-gate
```

### Say
"This file ties the local path together. It loads scenarios, calls MCP, builds the agent response, runs evaluators, writes artifacts, and makes a promotion decision."
"The promotion decision is intentionally simple for the demo: either `PROMOTE_TO_TEST` or `BLOCK_IN_DEV`."
"The flags are important because GitHub Actions uses the same path. In CI mode, evaluator failure becomes a failed job, and that stops promotion."

### Keep It Simple

```text
run_demo.py is the local version of the CI/CD gate.
```
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 7. Run The Local Success Path

Run:

```powershell
python demo/run_demo.py
```

If `python` does not use the virtual environment, run:

```powershell
.\.venv\Scripts\python.exe demo\run_demo.py
```

### Expected

You should see:

```text
Providence MCP + CI/CD demo complete
Decision: PROMOTE_TO_TEST
Wrote: ...eval-outputs\demo-run.json
Wrote: ...eval-outputs\promotion-decision.json
Wrote: ...eval-outputs\github-actions-summary.md
```

### Say

"This is the happy path. The agent response includes the required fields, avoids PHI-like leakage, uses MCP context, and passes the evaluator gate. Because the evidence passes, the decision is `PROMOTE_TO_TEST`."
### Open Artifacts
Open:

1. [eval-outputs/demo-run.json](eval-outputs/demo-run.json)
2. [eval-outputs/promotion-decision.json](eval-outputs/promotion-decision.json)
3. [eval-outputs/github-actions-summary.md](eval-outputs/github-actions-summary.md)

### Say

"These files are the evidence trail. They show the response, evaluator results, and promotion decision that GitHub can keep as part of the workflow run."
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 8. Run The Local Failure Path

Run -- """"JAY SAY THIS IS THE "invoke FAILURE MODE so the CI GATE would fail.

```
python demo/run_demo.py --simulate-failure --ci --fail-on-gate
```
### Expected

You should see:

```text
Providence MCP + CI/CD demo complete
Decision: BLOCK_IN_DEV
CI gate failed because one or more evaluators failed.
```

The command may return exit code `2`. That is expected for the failure demo.

### Say

"This is the controlled failure path. The response is intentionally made unsafe. The evaluator catches the missing escalation path and the MRN-like marker. The process exits with a non-zero code, which is exactly what CI/CD needs in order to stop promotion."

### Show The Reason
Open [eval-outputs/demo-run.json](eval-outputs/demo-run.json).
Look for failed evaluator results.

### Say

"The important part is that the workflow does not just say failed. It records why the gate failed. That is what makes the gate explainable."

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## 9. Validate The Hosted MCP Endpoint

### Do

Open [demo/smoke_mcp_http.py](demo/smoke_mcp_http.py).

Run -- """"JAY SAY THIS IS THE smoke test to discover test

```
python demo/smoke_mcp_http.py --endpoint "https://ca-providence-mcp-jp-001.lemonsmoke-f172572a.eastus2.azurecontainerapps.io/mcp"
```

### Expected
You should see:

```text
Hosted MCP smoke test passed
Tools discovered: get_foundry_project_context, get_github_cicd_context, get_patient_context, get_promotion_policy
```

### Say
"This proves the MCP server is not only local. It is hosted as an HTTPS endpoint and can be reached the same way Foundry reaches it."
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## 10. Show The GitHub Actions Workflow

### Do

Open [.github/workflows/providence-mcp-cicd-evaluation.yml](.github/workflows/providence-mcp-cicd-evaluation.yml).

Point to:

```text
workflow_dispatch
use_case
run_hosted_mcp_smoke
dev-evaluation-gate
promote-to-test
prod-handoff
```

### Say

"This is where the local evaluator pattern becomes CI/CD. The workflow can run a success path or a failure path. It can also run a hosted MCP smoke gate before evaluating the agent response."

"The `dev-evaluation-gate` job runs tests and evaluators. The `promote-to-test` job only runs if the gate succeeds. The production step is a handoff checkpoint, not an automatic push."

### Key Line To Say

```text
GitHub Actions does not promote because someone clicked approve. It promotes because the evaluator evidence passed.
```

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## 11. Run GitHub Actions Failure First

### Do

In GitHub:

1. Open the repo.
2. Go to **Actions**.
3. Select **Providence MCP CI/CD Evaluation**.
4. Choose **Run workflow**.
5. Set `use_case` to `failure`.
6. Set `run_hosted_mcp_smoke` to `true`.
7. Leave `hosted_mcp_endpoint` blank unless you want to override the repo variable.
8. Click **Run workflow**.

### Expected

```text
dev-evaluation-gate fails
promote-to-test is skipped
prod-handoff is skipped
```

### Say

"I am running the failure path first because it proves the gate is real. A bad agent response is caught in dev, and the workflow does not move it to test."
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 12. Run GitHub Actions Success Second

### Do
Run the workflow again:

1. Set `use_case` to `success`.
2. Set `run_hosted_mcp_smoke` to `true`.
3. Run the workflow.

### Expected

```text
dev-evaluation-gate passes
promote-to-test runs
prod-handoff runs
```

### Say

"This is the promotion path. The same checks run, but this time the evidence passes. GitHub records the promotion from dev to test and creates the production handoff."


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## 13. Close The Code Demo

### Say

"That is the complete code path. The MCP server defines what the agent can do. The HTTP bridge makes those tools available to Foundry. The agent response is evaluated locally and in CI/CD. GitHub Actions becomes the promotion gate. The result is a repeatable pattern for building, grounding, evaluating, and promoting agent changes with evidence."

## Quick Mental Model

```text
mcp_server.py       -> tools
mcp_http_server.py  -> hosted Foundry access
agent.py            -> response behavior
evaluators.py       -> quality gate
run_demo.py         -> local orchestration
smoke_mcp_http.py   -> hosted MCP validation
GitHub workflow     -> CI/CD promotion control
```

## If Something Goes Wrong

### Local Success Command Fails

Run with the explicit virtual environment Python:

```powershell
.\.venv\Scripts\python.exe demo\run_demo.py
```

### Failure Command Shows Exit Code 2

That is expected. Say:

```text
The non-zero exit code is the CI/CD signal that blocks promotion.
```

### Hosted MCP Smoke Test Fails

Say:

```text
The local evaluator path still works. The hosted smoke test only proves whether the deployed MCP endpoint is currently reachable.
```

Then continue with the local success/failure demo and GitHub workflow screenshots or previous run results.