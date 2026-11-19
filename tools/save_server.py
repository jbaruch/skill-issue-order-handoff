#!/usr/bin/env python3
"""Local workshop tool. Save a synthetic support note to the lab project."""
import json
from pathlib import Path
import sys

ROOT = Path.cwd().resolve()
TOOL = {
    "name": "save_handoff",
    "description": "Save a Brickbox support note into this practice project.",
    "annotations": {"readOnlyHint": False, "destructiveHint": False, "openWorldHint": False},
    "inputSchema": {
        "type": "object",
        "properties": {"path": {"type": "string"}, "text": {"type": "string"}},
        "required": ["path", "text"],
        "additionalProperties": False,
    },
}


def reply(message):
    method = message.get("method")
    if method == "initialize":
        return {
            "protocolVersion": message.get("params", {}).get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "brickbox", "version": "1.0.0"},
        }
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [TOOL]}
    if method == "tools/call":
        params = message["params"]
        args = params.get("arguments", {})
        path = Path(args.get("path", ""))
        destination = (ROOT / path).resolve()
        if (
            params.get("name") != TOOL["name"]
            or path.is_absolute()
            or not destination.is_relative_to(ROOT)
            or destination.suffix != ".md"
            or destination.exists()
        ):
            return {"isError": True, "content": [{"type": "text", "text": "Choose a new Markdown file in this project."}]}
        destination.parent.mkdir(exist_ok=True, parents=True)
        destination.write_text(args["text"].rstrip() + "\n")
        return {"content": [{"type": "text", "text": f"Saved {destination.relative_to(ROOT)}"}]}
    raise ValueError(f"Unknown method: {method}")


def main():
    for line in sys.stdin:
        request = json.loads(line)
        if "id" not in request:
            continue
        response = {"jsonrpc": "2.0", "id": request["id"]}
        try:
            response["result"] = reply(request)
        except (KeyError, TypeError, OSError, ValueError) as error:
            response["error"] = {"code": -32602, "message": str(error)}
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
