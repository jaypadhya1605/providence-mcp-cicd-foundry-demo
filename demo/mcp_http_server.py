from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

try:
    from .mcp_server import handle_message
except ImportError:
    from mcp_server import handle_message


PUBLIC_SAFE_CONTEXT = {
    "subscription_id": "00000000-0000-0000-0000-000000000000",
    "resource_group": "rg-healthcare-foundry-demo",
    "location": "eastus2",
    "foundry_account_name": "ai-healthcare-foundry-demo",
    "foundry_project_name": "proj-healthcare-foundry-demo",
    "foundry_project_endpoint": "https://ai-healthcare-foundry-demo.services.ai.azure.com/api/projects/proj-healthcare-foundry-demo",
    "foundry_account_resource_id": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-healthcare-foundry-demo/providers/Microsoft.CognitiveServices/accounts/ai-healthcare-foundry-demo",
    "apim_service_name": "apim-healthcare-foundry-demo",
    "app_insights_name": "appi-healthcare-foundry-demo",
    "log_analytics_workspace": "law-healthcare-foundry-demo",
    "content_understanding_account_name": "cu-healthcare-foundry-demo",
    "live_foundry_enabled": False,
}


def _public_safe_enabled() -> bool:
    return os.environ.get("MCP_HTTP_PUBLIC_SAFE", "true").lower() != "false"


def _redact_tool_result(request: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    if not _public_safe_enabled():
        return response

    params = request.get("params", {})
    if request.get("method") != "tools/call" or params.get("name") != "get_foundry_project_context":
        return response

    result = response.get("result", {})
    content = result.get("content")
    if isinstance(content, list) and content and isinstance(content[0], dict):
        content[0]["text"] = json.dumps(PUBLIC_SAFE_CONTEXT)
    elif "result" in response:
        response["result"] = PUBLIC_SAFE_CONTEXT
    return response


def _json_bytes(payload: Any) -> bytes:
    return json.dumps(payload).encode("utf-8")


def _sse_bytes(payloads: list[dict[str, Any]]) -> bytes:
    return b"".join(f"event: message\ndata: {json.dumps(payload)}\n\n".encode("utf-8") for payload in payloads)


def _error_response(message: str, request_id: Any = None, code: int = -32000) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _should_reply(request: dict[str, Any]) -> bool:
    return "id" in request and request.get("id") is not None


def _handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    response = _redact_tool_result(request, handle_message(request))
    if not _should_reply(request):
        return None
    return response


def _handle_payload(payload: Any) -> tuple[Any, list[dict[str, Any]]]:
    if isinstance(payload, list):
        responses: list[dict[str, Any]] = []
        for item in payload:
            if not isinstance(item, dict):
                responses.append(_error_response("Invalid JSON-RPC batch item", code=-32600))
                continue
            response = _handle_request(item)
            if response is not None:
                responses.append(response)
        return responses, responses

    if isinstance(payload, dict):
        response = _handle_request(payload)
        if response is None:
            return None, []
        return response, [response]

    response = _error_response("Invalid JSON-RPC payload", code=-32600)
    return response, [response]


def _path_name(path: str) -> str:
    return path.split("?", 1)[0].rstrip("/") or "/"


class MCPHttpHandler(BaseHTTPRequestHandler):
    server_version = "ProvidenceMCPHTTP/0.1"

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._send_common_headers()
        self.end_headers()

    def do_GET(self) -> None:
        path = _path_name(self.path)
        if path in {"/", "/health", "/mcp", "/api/mcp"}:
            self._send_json(200, {"status": "ok", "server": "providence-mcp-cicd-context"})
            return
        self._send_json(404, {"error": "Not found. POST MCP JSON-RPC messages to /mcp."})

    def do_POST(self) -> None:
        path = _path_name(self.path)
        if path not in {"/", "/mcp", "/api/mcp"}:
            self._send_json(404, {"error": "Not found. POST MCP JSON-RPC messages to /mcp."})
            return

        try:
            raw_body = self._read_body()
            payload = json.loads(raw_body)
            json_response, sse_responses = _handle_payload(payload)
        except Exception as exc:
            json_response = _error_response(str(exc))
            sse_responses = [json_response]

        if not sse_responses:
            self._send_empty(202)
            return

        accept = self.headers.get("Accept", "")
        if "application/json" in accept or "text/event-stream" not in accept:
            self._send_json(200, json_response)
        else:
            self._send_sse(200, sse_responses)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")

    def _send_common_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "content-type, accept, mcp-session-id, mcp-protocol-version")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Mcp-Session-Id", "providence-demo-session")
        self.send_header("Mcp-Protocol-Version", "2024-11-05")

    def _read_body(self) -> str:
        if self.headers.get("Transfer-Encoding", "").lower() == "chunked":
            return self._read_chunked_body()

        content_length = int(self.headers.get("Content-Length", "0"))
        return self.rfile.read(content_length).decode("utf-8")

    def _read_chunked_body(self) -> str:
        chunks: list[bytes] = []
        while True:
            size_line = self.rfile.readline().strip()
            if not size_line:
                continue
            chunk_size = int(size_line.split(b";", 1)[0], 16)
            if chunk_size == 0:
                while self.rfile.readline().strip():
                    pass
                break
            chunks.append(self.rfile.read(chunk_size))
            self.rfile.read(2)
        return b"".join(chunks).decode("utf-8")

    def _send_empty(self, status_code: int) -> None:
        self.send_response(status_code)
        self._send_common_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _send_json(self, status_code: int, payload: Any) -> None:
        body = _json_bytes(payload)
        self.send_response(status_code)
        self._send_common_headers()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_sse(self, status_code: int, payloads: list[dict[str, Any]]) -> None:
        body = _sse_bytes(payloads)
        self.send_response(status_code)
        self._send_common_headers()
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the Providence MCP demo over HTTP for Foundry MCP tools.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind.")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT") or os.environ.get("WEBSITES_PORT") or "8765"),
        help="HTTP port. Defaults to PORT/WEBSITES_PORT when hosted.",
    )
    args = parser.parse_args()

    httpd = ThreadingHTTPServer((args.host, args.port), MCPHttpHandler)
    print(f"Providence MCP HTTP server listening on http://{args.host}:{args.port}/mcp")
    print(f"Public-safe redaction: {_public_safe_enabled()}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()