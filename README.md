# Build a Brickbox support skill

QCon San Francisco · How To Write Skills That Actually Work

Build a skill that turns a customer's order question into a note for
the next support teammate. Open the [workbook](WORKBOOK.md) to start.

## Before the workshop

- Git and Python 3.11 or later. On Windows, use WSL for the terminal tools.
- A working session in Codex, Claude Code, or Cursor. Baruch will use Codex.
- [ACR 0.6.0](https://github.com/jbaruch/agentic-context-registry/releases/tag/v0.6.0)
  for the hook and package labs.
- A [TypeSafe API key](https://console.typesafe.ai/keys) for the live Jev lab.
  Load it as `TYPESAFE_API_KEY` in your terminal. If you're using the
  prepared recordings, open [the two logs](evidence/README.md#jev) in your agent.

**Terminal**

```sh
git clone https://github.com/jbaruch/skill-issue-order-handoff.git
cd skill-issue-order-handoff
python3 --version
acr version
```

Keep this terminal at the top of the folder you cloned. Choose your agent
once and use the same value when you open later exercises.

```sh
agent=codex                 # or claude-code or cursor
python3 tools/start.py 1-before --agent "$agent"
```

Open the printed folder in a new agent session. The helper makes a new
project with sample orders and keeps your previous work. Each exercise
has a working copy you can open if you skip an edit or need to catch up.
[Working copies](answers/README.md)

Lab 1 puts the skill in `.agents/skills` for Codex, `.claude/skills`
for Claude Code, or `.cursor/skills` for Cursor. Open
`triage-order/SKILL.md` in that folder to edit it.

The order data is made up. All support notes and drafts stay in the lab
folder. The Copilot review is a presenter demo.

## Install the published package

From a clean project folder containing the sample order data:

```sh
acr install github:jbaruch/skill-issue-order-handoff@v1.0.0 --agent "$agent" --freshness none --non-interactive
acr realize
acr check
```

`acr realize` puts the files where your selected agent looks for them.
`acr check` confirms the files match the version you installed.
