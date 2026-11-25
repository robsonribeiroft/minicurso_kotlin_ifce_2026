"""Cliente MCP mínimo (JSON-RPC 2.0 sobre stdio) para o servidor `deckcraft-cli mcp`.

Uso como biblioteca:
    with DeckcraftMCP(cli_path, read_roots=[...], write_roots=[...]) as mcp:
        mcp.call("batch", {"commands": [...]})
"""
from __future__ import annotations

import json
import subprocess
import sys
from typing import Any


class MCPError(RuntimeError):
    pass


class DeckcraftMCP:
    def __init__(self, cli: str, read_roots: list[str] | None = None,
                 write_roots: list[str] | None = None, connect: int | None = None):
        args = [cli, "mcp"]
        if connect is not None:
            args += ["--connect", str(connect)]
        for r in read_roots or []:
            args += ["--automation-read-root", r]
        for w in write_roots or []:
            args += ["--automation-write-root", w]
        self.args = args
        self._id = 0
        self.proc: subprocess.Popen | None = None

    # -- ciclo de vida -------------------------------------------------
    def __enter__(self) -> "DeckcraftMCP":
        self.proc = subprocess.Popen(
            self.args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=sys.stderr, text=True, encoding="utf-8", bufsize=1)
        self._request("initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "minicurso-kotlin-builder", "version": "1.0"},
        })
        self._notify("notifications/initialized")
        return self

    def __exit__(self, *exc) -> None:
        if self.proc:
            self.proc.stdin.close()
            self.proc.wait(timeout=30)

    # -- JSON-RPC -------------------------------------------------------
    def _send(self, msg: dict) -> None:
        self.proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def _notify(self, method: str, params: dict | None = None) -> None:
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self._send(msg)

    def _request(self, method: str, params: dict | None = None) -> Any:
        self._id += 1
        rid = self._id
        msg = {"jsonrpc": "2.0", "id": rid, "method": method}
        if params is not None:
            msg["params"] = params
        self._send(msg)
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise MCPError("servidor MCP encerrou a conexão")
            resp = json.loads(line)
            if resp.get("id") != rid:
                continue  # notificações / logs
            if "error" in resp:
                raise MCPError(json.dumps(resp["error"], ensure_ascii=False))
            return resp["result"]

    # -- API de alto nível ---------------------------------------------
    def tools(self) -> list[dict]:
        return self._request("tools/list")["tools"]

    def call(self, tool: str, arguments: dict | None = None) -> str:
        res = self._request("tools/call", {"name": tool, "arguments": arguments or {}})
        text = "\n".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        if res.get("isError"):
            raise MCPError(f"{tool}: {text}")
        return text


if __name__ == "__main__":
    cli = sys.argv[1]
    with DeckcraftMCP(cli) as mcp:
        for t in mcp.tools():
            print(f"### {t['name']}: {t.get('description','')}")
            print(json.dumps(t.get("inputSchema", {}), ensure_ascii=False))
