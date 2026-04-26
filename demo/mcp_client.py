from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class MCPClient:
    def __init__(self) -> None:
        server_path = Path(__file__).with_name("mcp_server.py")
        self._request_id = 0
        self._process = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

    def __enter__(self) -> "MCPClient":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def close(self) -> None:
        if self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()

    def _send(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if self._process.stdin is None or self._process.stdout is None:
            raise RuntimeError("MCP server pipes are not available.")

        self._request_id += 1
        payload = {"id": self._request_id, "method": method, "params": params or {}}
        self._process.stdin.write(json.dumps(payload) + "\n")
        self._process.stdin.flush()

        line = self._process.stdout.readline()
        if not line:
            stderr = self._process.stderr.read() if self._process.stderr else ""
            raise RuntimeError(f"MCP server stopped unexpectedly. {stderr}")

        response = json.loads(line)
        if response.get("error"):
            raise RuntimeError(response["error"])
        return response["result"]

    def list_tools(self) -> list[dict[str, Any]]:
        return self._send("tools/list")["tools"]

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._send("tools/call", {"name": name, "arguments": arguments or {}})