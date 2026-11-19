#!/usr/bin/env python3
"""Keep writes from the workshop save tool inside drafts/."""
import json
from pathlib import PurePosixPath
import sys


def main():
    event = json.load(sys.stdin)
    if event.get("tool_name") not in {
        "mcp__brickbox__save_handoff", "mcp__brickbox_save_handoff",
    }:
        return 0
    path = PurePosixPath(event.get("tool_input", {}).get("path", ""))
    if len(path.parts) != 2 or path.parts[0] != "drafts" or path.suffix != ".md":
        print("Draft save blocked. Use drafts/<order-number>.md.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
