#!/usr/bin/env python3
"""Make a new folder for one Brickbox exercise."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

SOURCE = Path(__file__).resolve().parent.parent
NATIVE = {
    "codex": (".agents/skills", "AGENTS.md", ".codex/config.toml"),
    "claude-code": (".claude/skills", "CLAUDE.md", ".mcp.json"),
    "cursor": (".cursor/skills", ".cursor/rules/order-notes.mdc", ".cursor/mcp.json"),
}
STAGES = {
    "1-before", "1-description", "1-solved", "2-before", "2-solved",
    "3-before", "3-solved", "4-before", "4-solved", "5-before", "5-solved",
    "6-before", "6-solved", "clean",
}
PREAMBLE = """# Prepare an order handoff

Process steps in order. Do not skip ahead.

"""
MANUAL = """## Step 1 — Find the order

Write `scratch_lookup.py` in this project from the recipe below. Run it
and leave the file so the attendee can read it. Read `data/orders.json`, find the given order number, and print
the currency, shipping status, total completed payments in cents, and total
pending holds in cents. The payment status `captured` means completed.
Proceed immediately to Step 2.

"""
FIXED = """## Step 1 — Find the order

Run `python3 scripts/lookup_order.py ORDER_NUMBER` from the project folder
with the number from the ticket. Proceed immediately to Step 2.

"""
SAVE = """Save order notes in `drafts/` when the attendee requests a file.
List completed payments and pending holds separately.
"""
NOTE = """## Step 2 — Write the handoff

Use the headings **Customer question**, **Order facts**, **Team**, and
**Next action**. Use the order facts you found. Send a payment question to
Billing and an arrival question to Shipping. Ask one question when the
team is unclear. Finish here.
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_skill(work, skill_dir, stage):
    if stage == "1-before":
        description = (
            "Handle Brickbox customer support requests about orders and kit contents, "
            "including whether kits come with assembly instructions. "
            "An order number is required for every request covered by this skill."
        )
    else:
        description = "Prepare a support handoff from an incoming Brickbox order ticket."
    if stage.startswith("1-"):
        body = """## Step 1 — Find the order number

This process requires an order number for every request it handles,
including questions about kits. If the customer did not give one, reply
"I need your order number to help." End your turn there. Do not look up
product facts or answer the customer's question until they provide it.

## Step 2 — Write the note

Look up that order in `data/orders.json` and write a short note in chat.
Finish here.
"""
    elif stage == "2-before":
        body = MANUAL + NOTE + SAVE
    else:
        body = FIXED + NOTE + (SAVE if stage != "3-solved" else "")
    write(work / skill_dir / "triage-order/SKILL.md",
          f"---\nname: triage-order\ndescription: {description}\n---\n\n{PREAMBLE}{body}")


def setup_save_tool(work, agent, config):
    server = {"command": "python3", "args": ["tools/save_server.py"]}
    if agent == "codex":
        content = '[mcp_servers.brickbox]\ncommand = "python3"\nargs = ["tools/save_server.py"]\n\n[mcp_servers.brickbox.tools.save_handoff]\napproval_mode = "approve"\n'
    else:
        content = json.dumps({"mcpServers": {"brickbox": server}}, indent=2) + "\n"
    write(work / config, content)
    (work / "tools").mkdir(exist_ok=True)
    shutil.copy2(SOURCE / "tools/save_server.py", work / "tools/save_server.py")


def install_hook(work, agent):
    package = work / "local-hook"
    package.mkdir(exist_ok=True)
    hook = package / "protect_draft_location.py"
    if not hook.exists():
        shutil.copy2(SOURCE / "hooks/protect_draft_location.py", hook)
    write(package / "agent-plugin.yaml", """schemaVersion: 1
name: brickbox/local-hook
version: 1.0.0
description: Save location check for the workshop.
source:
  repository: https://github.com/brickbox/local-hook
artifacts:
  hooks:
    - id: protect-draft-location
      event: pre-tool-use
      path: protect_draft_location.py
""")
    subprocess.run(["acr", "install", "./local-hook", "--agent", agent,
                    "--freshness", "none", "--non-interactive"], cwd=work, check=True)
    subprocess.run(["acr", "realize"], cwd=work, check=True)


def create(work, stage, agent):
    work.mkdir(parents=True, exist_ok=False)
    subprocess.run(["git", "init", "-q"], cwd=work, check=True)
    readme = "# Brickbox\n\nBrickbox sells toy-brick kits.\n"
    if stage.startswith("1-"):
        readme += "\n[Product guide](data/product-info.md)\n"
    write(work / "README.md", readme)
    (work / "data").mkdir()
    shutil.copy2(SOURCE / "fixtures/orders.json", work / "data/orders.json")
    shutil.copy2(SOURCE / "fixtures/product-info.md", work / "data/product-info.md")
    skill_dir, rule_host, config = NATIVE[agent]
    if stage[0] in "123":
        write_skill(work, skill_dir, stage)
    if stage in {"2-solved", "3-before", "3-solved"}:
        path = work / "scripts"
        path.mkdir()
        shutil.copy2(SOURCE / "skills/triage-order/scripts/lookup_order.py", path)
    if stage in {"3-before", "3-solved"}:
        write(work / "support/order-1058-shipping.md", """Order 1058 · Shipping

The shipping label was created. Check tracking before giving an arrival date.
""")
    if stage == "3-solved":
        rule = (SOURCE / "rules/order-notes.md").read_text()
        if agent == "cursor":
            rule = "---\nalwaysApply: true\n---\n\n" + rule
        write(work / rule_host, rule)
    if stage in {"4-before", "4-solved", "clean"}:
        setup_save_tool(work, agent, config)
    if stage == "4-before":
        write(work / "local-hook/protect_draft_location.py", """#!/usr/bin/env python3
import json
import sys

event = json.load(sys.stdin)
# Add the decision here. Exit 2 to deny a save.
raise SystemExit(0)
""")
    if stage == "4-solved":
        install_hook(work, agent)
    if stage in {"5-before", "5-solved"}:
        local_scripts = work / "scripts"
        local_scripts.mkdir()
        shutil.copy2(SOURCE / "skills/triage-order/scripts/lookup_order.py", local_scripts)
        route = (SOURCE / "skills/triage-order/scripts/route.py").read_text()
        if stage == "5-before":
            start = route.index("LABELS = {")
            end = route.index("\nURL =", start)
            route = route[:start] + 'LABELS = {"unclear": "Add the Billing and Shipping definitions here."}' + route[end:]
        write(local_scripts / "route.py", route)
    if stage in {"6-before", "6-solved"}:
        for entry in ("skills", "rules", "hooks"):
            shutil.copytree(SOURCE / entry, work / "package" / entry,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copy2(SOURCE / "LICENSE", work / "package/LICENSE")
        manifest = (SOURCE / "agent-plugin.yaml").read_text()
        if stage == "6-before":
            manifest = manifest.split("artifacts:")[0] + "artifacts: {}\n"
        write(work / "package/agent-plugin.yaml", manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=sorted(STAGES | {"enable-hook"}))
    parser.add_argument("--agent", choices=NATIVE, default="codex")
    parser.add_argument("--at", type=Path)
    args = parser.parse_args()
    work = (args.at or SOURCE / ".workshop" / args.stage).resolve()
    try:
        if args.stage == "enable-hook":
            if args.at is None or not (work / "local-hook").is_dir():
                parser.error("Use --at with the 4-before folder you already made.")
            install_hook(work, args.agent)
        else:
            create(work, args.stage, args.agent)
    except FileExistsError:
        parser.exit(1, f"{work} already exists. Reuse it or choose a new folder with --at.\n")
    print(work)


if __name__ == "__main__":
    main()
