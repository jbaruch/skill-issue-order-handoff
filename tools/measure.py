#!/usr/bin/env python3
"""Record Codex routing or a Clef run followed by Codex for unclear tickets."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parent.parent
LABELS = "billing for charges or refunds, shipping for delivery, unclear otherwise"
FALLBACK = "Use the paired recordings in evidence/README.md for Reflection."


def codex(prompt):
    started = perf_counter()
    command = ["codex", "exec", "--ignore-user-config", "--ephemeral", "--json",
               "--sandbox", "read-only", "-"]
    result = subprocess.run(command, input=prompt, text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise RuntimeError("Codex did not finish. Run codex login status and check your quota.")
    events = [json.loads(line) for line in result.stdout.splitlines()]
    messages = [row["item"]["text"] for row in events if row["type"] == "item.completed"
                and row["item"]["type"] == "agent_message"]
    usage = next((row.get("usage") for row in reversed(events) if row["type"] == "turn.completed"), None)
    return {
        "source": "codex", "elapsed_ms": round(1000 * (perf_counter() - started)),
        "usage": usage, "text": messages[-1] if messages else "",
    }


def clef(ticket, script):
    result = subprocess.run([sys.executable, str(script), "--live", ticket],
                            text=True, capture_output=True, timeout=25)
    if result.stdout:
        return json.loads(result.stdout)
    raise RuntimeError("Clef did not produce a log. Check that the script is available.")


def run(row, mode, script):
    ticket = row["text"]
    if mode == "reasoning":
        call = codex(f"Classify this synthetic Brickbox ticket. Use {LABELS}. "
                     "Put the label alone on the first line. If unclear, put one short "
                     f"clarifying question on the next line. Do not use tools.\n\n{ticket}")
        text = call["text"].splitlines()
        return {"case": row["id"], "ticket": ticket, "route": text[0].strip().lower() if text else None,
                "question": text[1] if len(text) > 1 else None, "calls": [call]}
    call = clef(ticket, script)
    if call["source"] != "clef":
        return {"case": row["id"], "ticket": ticket, "status": "unavailable", "calls": [call]}
    calls = [call]
    question = None
    if call["label"] == "unclear":
        clarification = codex("A decision model returned unclear. Ask one short question that "
                              f"would help route the ticket. Do not use tools.\n\n{ticket}")
        calls.append(clarification)
        question = clarification["text"]
    return {"case": row["id"], "ticket": ticket, "route": call["label"],
            "question": question, "calls": calls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("reasoning", "clef"))
    parser.add_argument("--script", type=Path, default=ROOT / "skills/triage-order/scripts/route.py")
    args = parser.parse_args()
    if args.mode == "clef" and not all(
        os.environ.get(name) for name in ("CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN")
    ):
        parser.exit(1, f"Set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN. {FALLBACK}\n")
    rows = json.loads((ROOT / "fixtures/routes.json").read_text())
    for row in rows:
        try:
            recorded = run(row, args.mode, args.script)
        except (OSError, subprocess.TimeoutExpired, RuntimeError, ValueError) as exc:
            parser.exit(1, f"Could not record {row['id']} ({type(exc).__name__}). "
                        f"{FALLBACK}\n")
        print(json.dumps(recorded), flush=True)
        if recorded.get("status") == "unavailable":
            error = recorded["calls"][0]["error"]
            parser.exit(1, f"{error}. {FALLBACK}\n")


if __name__ == "__main__":
    main()
