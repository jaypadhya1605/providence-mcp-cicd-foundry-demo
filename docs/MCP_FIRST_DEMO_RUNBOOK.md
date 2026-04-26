# MCP-First Demo Runbook

Use this flow when the audience needs to understand the Azure AI Foundry MCP connection before seeing the code and CI/CD gate.

## Storyline

Start in Azure AI Foundry because that is the product experience Providence needs to understand first. The repo is the implementation view of the same pattern: how an agent calls MCP tools, how those tool results shape the response, and how GitHub Actions promotes or blocks the change.

## Step 1 - Show MCP Tools In Azure AI Foundry

1. Open Azure AI Foundry.
2. Open the Providence demo project.
3. Open the agent you created for the demo.
4. Go to the agent tools area.
5. Show that the agent can be connected to MCP servers.
6. Show the GitHub MCP connection.
7. Show the Microsoft Learn MCP connection.

For Microsoft Learn MCP, use:

```text
https://learn.microsoft.com/api/mcp
```

Expected Microsoft Learn tools:

- `microsoft_docs_search`
- `microsoft_code_sample_search`
- `microsoft_docs_fetch`

Suggested Foundry agent prompt for Microsoft Learn MCP:

```text
Use Microsoft Learn MCP to find current guidance for Azure AI Foundry agents and MCP tools. Summarize the key setup steps for a developer.
```

Suggested Foundry agent prompt for GitHub MCP:

```text
Use GitHub MCP to inspect the repository jaypadhya1605/providence-mcp-cicd-foundry-demo. Explain what the GitHub Actions workflow does and how it gates promotion from dev to test to prod.
```

Talk track:

```text
This is the first important idea: MCP is how the agent reaches governed external context and actions. In Foundry, the agent can use MCP tools such as GitHub and Microsoft Learn. The agent is no longer limited to static prompt text; it can call tools, inspect trusted sources, and reason over the results.
```

## Step 2 - Show The Same Pattern In Code

Open the repo in VS Code after the Foundry UI portion. Use this exact order.

### 2.1 MCP Server Definition

Open `demo/mcp_server.py`.

Show these sections:

- `PATIENT_CONTEXTS` - synthetic Providence-like context.
- `_tool_definitions()` - the MCP tool catalog.
- `_call_tool()` - the implementation behind each tool.
- `handle_message()` - JSON-RPC style message handling for initialize, tools/list, and tools/call.

Talk track:

```text
This local MCP server is our demo-safe version of the external tool layer. In the Foundry UI we connected the agent to real remote MCP servers like GitHub and Microsoft Learn. In code, we define a local MCP-compatible server so the same idea is repeatable, deterministic, and safe for a live audience.
```

Key tools to point out:

- `get_foundry_project_context` - project and environment context.
- `get_promotion_policy` - dev/test/prod gate rules.
- `get_patient_context` - synthetic scenario context.
- `get_github_cicd_context` - GitHub workflow context.

### 2.2 MCP Client Definition

Open `demo/mcp_client.py`.

Show these sections:

- `MCPClient.__enter__()` - starts the local MCP server process.
- `_send()` - sends JSON-RPC messages to the server.
- `list_tools()` - discovers available tools.
- `call_tool()` - invokes a specific MCP tool.

Talk track:

```text
The client is the bridge between the agent workflow and the MCP server. The server defines what tools exist. The client discovers those tools and calls them. This is the same mental model as Foundry calling GitHub MCP or Microsoft Learn MCP, just shown locally so we can inspect every moving part.
```

### 2.3 Agent Connection

Open `demo/run_demo.py`.

Show the `run()` function.

Point out this flow:

1. Start `MCPClient()`.
2. Call `list_tools()`.
3. Call `get_foundry_project_context`.
4. Call `get_promotion_policy`.
5. Call `get_github_cicd_context`.
6. For each scenario, call `get_patient_context`.
7. Pass all MCP context into the agent response builder.
8. Run custom evaluators on the response.

Then open `demo/agent.py`.

Show `build_agent_response()` and the `mcp_tools_used` field.

Talk track:

```text
This is where the MCP connection becomes visible inside the agent behavior. The agent response is not just a prompt completion. It is grounded in tool-provided context: patient scenario, Foundry project, promotion policy, and GitHub workflow information. The `mcp_tools_used` field is intentionally included so the evaluation artifact can prove which tools contributed to the answer.
```

### 2.4 Why Define Local Server And Client

Use this explanation:

```text
We define a local MCP server and client for three reasons. First, it lets us teach the protocol without relying on tenant auth or network latency. Second, it gives developers a controlled dev loop before connecting to live Foundry tools. Third, it makes the CI/CD gate deterministic, so a failed evaluator means behavior changed, not that a remote service was temporarily unavailable.
```

## Step 3 - Run The Local MCP Demo

Run:

```powershell
python demo/run_demo.py
```

Open:

```text
eval-outputs/demo-run.json
```

Show:

- `mcp_tools`
- `foundry_context`
- `github_context`
- each response's `mcp_tools_used`
- each response's `evaluation`

Talk track:

```text
This output is the proof trail. The agent used MCP tools, generated a response, and the custom evaluator scored the response. That gives us evidence we can attach to CI/CD.
```

## Step 4 - Show GitHub Actions As The Promotion Gate

Open `.github/workflows/providence-mcp-cicd-evaluation.yml`.

Show:

- `dev-evaluation-gate`
- `Run unit tests`
- `Run custom evaluator gate`
- artifact upload
- `promote-to-test`
- `prod-handoff`

Run the workflow manually in GitHub Actions:

```text
use_case = success
```

Then run:

```text
use_case = failure
```

Talk track:

```text
Now the same local MCP and evaluator loop becomes a release gate. Success moves from dev to test and records a production handoff. Failure blocks in dev, but still uploads artifacts so the developer knows exactly what failed.
```

## Step 5 - Map Back To Providence's Ask

Close with this mapping:

| Providence ask | What they saw |
|---|---|
| MCP tools in Foundry | Agent connected to GitHub MCP and Microsoft Learn MCP in Azure AI Foundry UI |
| Developer implementation | Local MCP server and client in `demo/mcp_server.py` and `demo/mcp_client.py` |
| Agent connected to MCP | `demo/run_demo.py` passes MCP tool output into `demo/agent.py` |
| GitHub CI/CD | GitHub Actions workflow runs evaluator gate |
| Dev to test to prod | Passing run promotes to test and records prod handoff |
| Failure path | Bad AI output is blocked in dev |
| Evaluation evidence | `eval-outputs/` artifacts and job summary |

## Best Closing Line

```text
The important pattern is that Providence can start from a Foundry agent connected to MCP tools, then carry the same tool-grounded behavior into developer code, custom evaluation, and GitHub CI/CD promotion gates.
```