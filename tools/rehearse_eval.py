#!/usr/bin/env python3
"""Use clean Codex sessions to record the four workshop eval cases."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile

from start import SOURCE, create

PACKAGE = "github:jbaruch/skill-issue-order-handoff@v1.0.0"


def files_in(work):
    return {str(p.relative_to(work)): sha256(p.read_bytes()).digest()
            for p in work.rglob("*") if p.is_file() and ".git" not in p.relative_to(work).parts}


def trial(parent, mode, case):
    work = (parent / f"{mode}-{case['id']}").resolve()
    create(work, "clean", "codex")
    if mode == "published":
        subprocess.run(["acr", "install", PACKAGE, "--agent", "codex",
                        "--freshness", "none", "--non-interactive"],
                       cwd=work, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["acr", "realize"], cwd=work, check=True, stdout=subprocess.DEVNULL)
    before = files_in(work)
    command = ["codex", "exec", "--ignore-user-config", "--ephemeral", "--json",
               "--sandbox", "workspace-write", "-"]
    run = subprocess.run(command, input=case["prompt"], text=True, cwd=work,
                         capture_output=True, timeout=180, check=True)
    events = [json.loads(line) for line in run.stdout.splitlines()]
    items = [event["item"] for event in events if event["type"] == "item.completed"]
    messages = [item["text"] for item in items if item["type"] == "agent_message"]
    commands = [item["command"] for item in items if item["type"] == "command_execution"]
    tracked_files = ("SKILL.md", "lookup_order.py", "route.py", "data/orders.json", "product-info.md")
    reads = [cmd.replace(str(work), "<project>") for cmd in commands
             if any(name in cmd for name in tracked_files)]
    after = files_in(work)
    changed = sorted(name for name in before.keys() | after.keys()
                     if before.get(name) != after.get(name))
    return {
        "case": case["id"], "package": PACKAGE if mode == "published" else None,
        "prompt": case["prompt"], "observed_commands": reads,
        "response": messages[-1].replace(str(work) + "/", "") if messages else "",
        "changed_files": changed,
        "draft_files": sorted(p.name for p in (work / "drafts").glob("*.md")),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("baseline", "published"))
    parser.add_argument("--case", choices=("billing", "shipping", "unclear", "product"))
    args = parser.parse_args()
    cases = json.loads((SOURCE / "fixtures/eval-cases.json").read_text())
    with tempfile.TemporaryDirectory(prefix="brickbox-eval-") as folder:
        for case in cases:
            if args.case is not None and case["id"] != args.case:
                continue
            print(json.dumps(trial(Path(folder), args.mode, case)), flush=True)


if __name__ == "__main__":
    main()
