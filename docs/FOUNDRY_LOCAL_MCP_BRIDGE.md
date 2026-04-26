# Foundry Local MCP Bridge

This path lets a Foundry agent call the demo MCP tools from Azure AI Foundry. You can either expose the local HTTP MCP adapter through a temporary HTTPS tunnel for development, or host the same adapter on Azure Container Apps for a stable demo endpoint.

## Important Boundary

Azure AI Foundry cannot call a local stdin/stdout process on your laptop directly. Foundry needs an HTTPS MCP endpoint. In this repo:

- `demo/mcp_server.py` is the MCP tool implementation.
- `demo/mcp_client.py` is the local/CI client for developer tests.
- `demo/mcp_http_server.py` exposes the same server behavior over HTTP so Foundry can reach it through a tunnel.

When the Foundry agent calls the tunnel or hosted URL, Foundry is the MCP client. The local `mcp_client.py` remains useful because it shows the same list-tools/call-tools pattern used by the local demo and GitHub Actions.

## Stable Azure Container Apps Endpoint

For a repeatable demo, host the HTTP bridge in Azure Container Apps and add this MCP URL to the Foundry agent:

```text
https://<container-app-fqdn>/mcp
```

The included `Dockerfile` starts the HTTP bridge on `0.0.0.0` and uses port `8000` by default:

```powershell
az acr build --registry <acr-name> --image providence-mcp-server:demo .

az containerapp create `
  --resource-group <resource-group> `
  --name <container-app-name> `
  --environment <container-app-environment> `
  --image <acr-login-server>/providence-mcp-server:demo `
  --ingress external `
  --target-port 8000 `
  --env-vars MCP_HTTP_PUBLIC_SAFE=true PORT=8000
```

Use this path when Foundry needs a durable HTTPS endpoint and you want traces to show calls to an Azure-hosted MCP server.

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

Then add this MCP URL to the agent in Azure AI Foundry:

```text
https://<your-tunnel-host>/mcp
```

## Foundry Agent Prompt

Use this prompt after adding the local or hosted MCP bridge as a tool:

```text
Use the Providence MCP tool to get the promotion policy and GitHub CI/CD context. Then explain how a failed custom evaluator blocks promotion from dev to test.
```

Use this prompt for scenario grounding:

```text
Use the Providence MCP tool to get patient context for scenario_id chest_pain_triage. Answer using only the tool-provided facts and include the source IDs you used.
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
This proves the Foundry agent can call an MCP server that we own. For local development we can expose it through a temporary HTTPS tunnel. For the stable demo path, the same server runs on Azure Container Apps and can be observed through Foundry traces and Azure monitoring.
```

## Troubleshooting

If Foundry reports this during tool discovery:

```text
Streamable HTTP POST response completed without a reply to request with ID: 1
```

Check that the MCP HTTP bridge supports the Streamable HTTP request shapes Foundry may use during enumeration:

- JSON-RPC batches such as `initialize` plus `tools/list` in one POST.
- Notification-only messages, which should return `202` with no response body.
- JSON responses when the client sends `Accept: application/json, text/event-stream`.
- SSE responses when the client only accepts `text/event-stream`.

## Security Notes

- Keep `MCP_HTTP_PUBLIC_SAFE=true` when tunneling from a laptop.
- Do not expose `.env` values through demo tools.
- Use a short-lived tunnel and close it after the demo.
- For production, host the MCP server in Azure with authentication instead of using a laptop tunnel.