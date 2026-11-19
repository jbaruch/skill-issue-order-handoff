# Build a Brickbox support skill

QCon San Francisco · How To Write Skills That Actually Work

Brickbox, a fictional online store, wants to automate common support
questions. You'll build a skill that helps an agent look up a customer's
order and explain whether they were charged twice. Open the
[workbook](WORKBOOK.md) to start.

## Before the workshop

- Git and Python 3.11 or later. On Windows, use WSL for the terminal tools.
- A working session in Codex, Claude Code, or Cursor. Baruch will use Codex.
- [ACR 0.6.0](https://github.com/jbaruch/agentic-context-registry/releases/tag/v0.6.0)
  for the hook and package labs.
- A Cloudflare account ID and [Workers AI API token](https://developers.cloudflare.com/workers-ai/get-started/rest-api/)
  for the live Clef lab. [Lab 5](WORKBOOK.md#5-route-a-ticket-with-clef)
  shows how to load them in the workshop terminal. You can also use
  [the two recorded logs](evidence/README.md#clef).

**Terminal**

```sh
git clone https://github.com/jbaruch/skill-issue-order-handoff.git
cd skill-issue-order-handoff
python3 --version
acr version
```

Keep one terminal at the top of the folder you cloned. Use it for
workshop commands. Choose your agent once in that terminal:

```sh
agent=codex                 # or claude-code or cursor
python3 tools/start.py 1-before --agent "$agent"
```

The helper prints the practice folder it created. Open your agent in
that exact folder. For Codex, from a second terminal at the workshop
repo, run `codex -C .workshop/1-before`. In an editor, open the printed
folder and start a new session there.

Each practice folder holds a copy of the sample data and files for that
exercise. Pulling updates into the workshop repo leaves existing
practice copies as they were. To start over, make a fresh one with
`--at .workshop/1-fresh` and open the new path. Each exercise also has
a working copy you can open if you skip an edit or need to catch up.
[Working copies](answers/README.md)

Lab 1 puts the skill in `.agents/skills` for Codex, `.claude/skills`
for Claude Code, or `.cursor/skills` for Cursor. Open
`triage-order/SKILL.md` in that folder to edit its description.

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
