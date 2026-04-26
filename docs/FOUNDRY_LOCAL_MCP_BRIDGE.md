# Foundry Local MCP Bridge

This path lets `myMCP-demo-Agent` call the local demo MCP tools from Azure AI Foundry by exposing the local HTTP MCP adapter through a temporary HTTPS tunnel.

## Important Boundary

Azure AI Foundry cannot call a local stdin/stdout process on your laptop directly. Foundry needs an HTTPS MCP endpoint. In this repo:

- `demo/mcp_server.py` is the MCP tool implementation.
- `demo/mcp_client.py` is the local/CI client for developer tests.
- `demo/mcp_http_server.py` exposes the same server behavior over HTTP so Foundry can reach it through a tunnel.

When `myMCP-demo-Agent` calls the tunnel URL, Foundry is the MCP client. The local `mcp_client.py` remains useful because it shows the same list-tools/call-tools pattern used by the local demo and GitHub Actions.

## Start The Local MCP HTTP Server

Run from the repo root:

```powershell
python demo/mcp_http_server.py --port 8765
```

The endpoint is:

```text
http://127.0.0.1:8765/mcp
```

By default the HTTP bridge redacts Foundry resource identifiers before returning `get_foundry_project_context`. Keep this enabled when using a public tunnel.

## Test Locally

In another terminal:

```powershell
$body = '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
Invoke-WebRequest -Uri "http://127.0.0.1:8765/mcp" -Method Post -Headers @{Accept="application/json, text/event-stream"} -ContentType "application/json" -Body $body | Select-Object -ExpandProperty Content
```

Expected tools:

- `get_foundry_project_context`
- `get_promotion_policy`
- `get_patient_context`
- `get_github_cicd_context`

## Expose Through An HTTPS Tunnel

Use any temporary HTTPS tunnel your tenant allows, such as VS Code port forwarding, Dev Tunnels, or ngrok.

The public URL must forward to:

```text
http://127.0.0.1:8765
```

Then add this MCP URL to `myMCP-demo-Agent` in Azure AI Foundry:

```text
https://<your-tunnel-host>/mcp
```

## Foundry Agent Prompt

Use this prompt after adding the local MCP bridge as a tool:

```text
Use the Providence local MCP tool to get the promotion policy and GitHub CI/CD context. Then explain how a failed custom evaluator blocks promotion from dev to test.
```

Use this prompt for scenario grounding:

```text
Use the Providence local MCP tool to get patient context for scenario_id chest_pain_triage. Answer using only the tool-provided facts and include the source IDs you used.
```

## What To Show In Foundry Traces

After the agent responds, open Traces or Monitor in Foundry and show:

- the user message,
- the agent response,
- the tool invocation against the local MCP bridge,
- latency and status,
- App Insights correlation if enabled for the project.

Talk track:

```text
This proves the Foundry agent can call an MCP server that we own. For the demo we run it locally and expose it through a temporary HTTPS tunnel. In production this same MCP server would be hosted behind a real authenticated endpoint, for example Azure Container Apps or App Service, and observed through Application Insights.
```

## Security Notes

- Keep `MCP_HTTP_PUBLIC_SAFE=true` when tunneling from a laptop.
- Do not expose `.env` values through demo tools.
- Use a short-lived tunnel and close it after the demo.
- For production, host the MCP server in Azure with authentication instead of using a laptop tunnel.