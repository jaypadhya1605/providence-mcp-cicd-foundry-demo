from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from .config import ROOT
except ImportError:
    from config import ROOT


OUTPUT_DIR = ROOT / "eval-outputs"
REQUIRED_TOOLS = {
    "get_foundry_project_context",
    "get_promotion_policy",
    "get_patient_context",
    "get_github_cicd_context",
}


def _normalize_endpoint(endpoint: str) -> str:
    endpoint = endpoint.strip().rstrip("/")
    if not endpoint:
        raise ValueError("MCP endpoint is required. Set MCP_HTTP_ENDPOINT or pass --endpoint.")
    if not endpoint.endswith("/mcp"):
        endpoint = f"{endpoint}/mcp"
    return endpoint


def _parse_sse(text: str) -> Any:
    payloads: list[Any] = []
    for line in text.splitlines():
        if line.startswith("data:"):
            payloads.append(json.loads(line.removeprefix("data:").strip()))
    if not payloads:
        raise ValueError("SSE response did not contain a data payload.")
    return payloads[-1]


def _parse_response(raw_body: bytes, content_type: str) -> Any:
    text = raw_body.decode("utf-8")
    if "text/event-stream" in content_type or text.lstrip().startswith("event:"):
        return _parse_sse(text)
    return json.loads(text)


def _post_json_rpc(endpoint: str, request_id: int, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    body = json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}}).encode("utf-8")
    request = Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        },
    )
    with urlopen(request, timeout=20) as response:
        parsed = _parse_response(response.read(), response.headers.get("Content-Type", ""))

    if isinstance(parsed, list):
        matches = [item for item in parsed if isinstance(item, dict) and item.get("id") == request_id]
        if not matches:
            raise ValueError(f"MCP response did not include a reply for request ID {request_id}.")
        parsed = matches[0]

    if not isinstance(parsed, dict):
        raise ValueError("MCP response was not a JSON object.")
    if "error" in parsed:
        raise ValueError(f"MCP {method} failed: {parsed['error']}")
    return parsed


def _call_tool(endpoint: str, request_id: int, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    response = _post_json_rpc(endpoint, request_id, "tools/call", {"name": name, "arguments": arguments or {}})
    result = response.get("result", {})
    content = result.get("content", [])
    if isinstance(content, list) and content and isinstance(content[0], dict):
        return json.loads(content[0].get("text", "{}"))
    if isinstance(result, dict):
        return result
    raise ValueError(f"Unexpected tool result for {name}.")


def _write_artifacts(payload: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "hosted-mcp-smoke.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Hosted MCP Smoke Test",
        "",
        f"Status: **{payload['status']}**",
        "",
        f"Endpoint: `{payload['endpoint']}`",
        f"Tools discovered: `{len(payload.get('tools', []))}`",
        "",
    ]
    if payload["status"] == "passed":
        lines.extend(
            [
                "Verified hosted MCP calls:",
                "",
                "- `initialize`",
                "- `tools/list`",
                "- `get_promotion_policy`",
                "- `get_github_cicd_context`",
            ]
        )
    else:
        lines.append(f"Error: `{payload.get('error', 'unknown')}`")

    (OUTPUT_DIR / "hosted-mcp-smoke-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(endpoint: str) -> dict[str, Any]:
    normalized_endpoint = _normalize_endpoint(endpoint)
    initialize = _post_json_rpc(normalized_endpoint, 1, "initialize")
    tools_response = _post_json_rpc(normalized_endpoint, 2, "tools/list")
    tools = tools_response.get("result", {}).get("tools", [])
    tool_names = {tool.get("name") for tool in tools if isinstance(tool, dict)}
    missing_tools = sorted(REQUIRED_TOOLS - tool_names)
    if missing_tools:
        raise ValueError(f"Hosted MCP endpoint is missing tools: {', '.join(missing_tools)}")

    promotion_policy = _call_tool(normalized_endpoint, 3, "get_promotion_policy")
    github_context = _call_tool(normalized_endpoint, 4, "get_github_cicd_context")

    return {
        "status": "passed",
        "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "endpoint": normalized_endpoint,
        "server_info": initialize.get("result", {}).get("serverInfo", {}),
        "tools": sorted(tool_names),
        "promotion_policy": promotion_policy,
        "github_context": github_context,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test a hosted MCP HTTP endpoint.")
    parser.add_argument("--endpoint", default=os.environ.get("MCP_HTTP_ENDPOINT", ""), help="Hosted MCP endpoint URL.")
    args = parser.parse_args()

    try:
        payload = run(args.endpoint)
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        payload = {
            "status": "failed",
            "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "endpoint": args.endpoint,
            "error": str(exc),
        }
        _write_artifacts(payload)
        print(f"Hosted MCP smoke test failed: {exc}")
        return 2

    _write_artifacts(payload)
    print("Hosted MCP smoke test passed")
    print(f"Endpoint: {payload['endpoint']}")
    print(f"Tools discovered: {', '.join(payload['tools'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
