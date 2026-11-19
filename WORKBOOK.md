# Brickbox workshop workbook

You're a developer at Brickbox, a fictional online store. The support
team wants to automate common customer questions. Your job is to build
a skill that helps an agent look up an order and explain whether the
customer was charged twice.

The agent will write an internal note that Billing can use to follow up
with the customer about order 1042. You'll begin with a kit question to
see which requests activate the order skill.

## Set up your copy

1. Run the [README setup commands](README.md#before-the-workshop) to clone
   the workshop repository, choose your agent, and create `1-before`.
2. Keep that terminal open in the repository for **Terminal** commands.
3. Open the exact folder the setup command prints in your agent. Start a
   fresh session there.

Paste **Agent** blocks into the session named in that step. Use the
**Reflection** prompts after the run, in the session where the agent
did the work. Ask it to show the instruction, command, or result
behind its answer.

## 1. Frontmatter matters

**Start here.** Open the `1-before` folder you made during setup. The
order skill's description says it covers both orders and kit contents.
Your agent uses that description to decide when to open the skill.

### Before editing the description

**Agent · Kit question.** Paste in a fresh session in `1-before`.

```text
Do Brickbox kits come with assembly instructions?
```

**Agent · Reflection.** Ask in the kit question session.

```text
Which skill did you open, if any? What in its description matched the request? Why did you answer the way you did?
```

**Agent · Double-charge ticket.** Start another fresh session in `1-before`.

```text
I think I was charged twice for order 1042.
```

Ask the same Reflection questions in that session. Record both replies
and the files the agent opened.

**What you build.** In `triage-order/SKILL.md`, replace just the
`description` line at the top:

```yaml
description: Prepare a support handoff from an incoming Brickbox order ticket.
```

### After editing the description

**Agent · Kit question.** Paste in a fresh session in the edited folder.

```text
Do Brickbox kits come with assembly instructions?
```

**Agent · Double-charge ticket.** Start another fresh session in the edited folder.

```text
I think I was charged twice for order 1042.
```

**Agent · Reflection.** Ask in the kit question session.

```text
What did you open to answer the kit question? What led you there?
How did the skill description affect your choice?
```

In the order ticket session, ask which skill it opened and what in
the description still matched the request.

**Working copy.** Use `1-solved` for the skill with the narrower
description. If either run takes a different path, ask why, compare with
the [recorded runs](evidence/first-three.md#frontmatter-matters),
and move on.

## 2. Look up an order

**Terminal**

```sh
python3 tools/start.py 2-before --agent "$agent"
```

**Agent · Before.** Open a fresh session in `2-before` and paste the ticket.

```text
I think I was charged twice for order 1042.
```

The skill gives it a recipe for writing a helper. Open
`scratch_lookup.py` if it created the file. If the agent ran Python
directly in the terminal, ask it to show you that code. If it skipped
writing code, use the [recorded lookup](evidence/first-three.md#reuse-the-lookup)
for the before run and go straight to the working copy for the after run.

**Agent · Reflection.** Ask in the same session.

```text
How did you look up the order? Show me the code you wrote and the command you ran.
```

**Agent · Build.** Give the same agent this follow-up.

```text
Let's reuse the lookup you just wrote. Save a copy as scripts/lookup_order.py that takes an order number. Update the lookup step in the triage-order skill to run that script on future tickets. Show me what changed and how you checked it.
```

If Codex asks to edit `SKILL.md`, review the proposed lookup change and
choose **Yes, proceed**. Check the updated skill and script before
opening the next session.

**Agent · After.** Start a fresh session in the edited folder.

```text
I think I was charged twice for order 1042.
```

Both runs should find 2500 cents captured and 2500 cents pending. If the agent
writes another helper, ask which instruction led it to do that, then
use `2-solved` for the second run.

**Agent · Reflection.** Ask in the new session.

```text
What command did you run? Did you have to write lookup code this time? What do we gain by using the same script on future tickets?
```

The same script gives the same answer for the same input and data. The
agent saves the tokens it would spend writing a new helper.

**Working copy.** To get the reusable script and skill, run
`python3 tools/start.py 2-solved --agent "$agent"` from the workshop
repository. Open the printed folder and use the same lookup request.
To see what the script prints, run `python3 scripts/lookup_order.py 1042`
from that folder.

## 3. Set a project rule

**Terminal**

```sh
python3 tools/start.py 3-before --agent "$agent"
```

**Agent · Before.** In a fresh session in `3-before`, paste this first.

```text
Save this note as a new Markdown file. Preserve the text as supplied.

> Order 1042 · Billing
>
> The customer reports a second charge. The order shows one completed
> payment of $25 and a pending hold of $25. Ask whether the second
> entry appears as completed.
```

Check where the note landed and keep that session available for Reflection.
In the recorded run, it landed next to the example in `support/`.

**What you build.** At the top of the practice folder, create `AGENTS.md`
for Codex or `CLAUDE.md` for Claude Code. In Cursor, create
`.cursor/rules/order-notes.mdc` and add a header with `alwaysApply: true`
between two lines containing `---`. Paste this rule text into the file.

```markdown
# Brickbox order notes

Save support notes under `drafts/` so a teammate can review them before
sending them to a customer.

Captured Only. Count completed payments as paid. Report pending holds separately.
```

Open `triage-order/SKILL.md` in the practice folder. In Codex, look under
`.agents/skills/`. In Claude Code, use `.claude/skills/`, and in Cursor,
use `.cursor/skills/`. Remove any old lines about saving notes under
`drafts/` and listing completed payments separately from holds. The
project rule now covers both.

**Agent · After.** Start a fresh session in the edited folder and paste this first.

```text
Save this note as a new Markdown file. Preserve the text as supplied.

> Order 1042 · Billing
>
> The customer reports a second charge. The order shows one completed
> payment of $25 and a pending hold of $25. Ask whether the second
> entry appears as completed.
```

Compare both file paths and check that the text matches. The second
note should be in `drafts/`. Use the [recorded saves](evidence/first-three.md#move-the-save-instruction-into-a-rule)
if the agent saves it elsewhere.

**Agent · Reflection.** After both saves, ask each session about its own run.

```text
Which project rules were loaded at startup? Which skill did you open for the save, if any? What made you choose that folder? Show me the evidence from that run.
```

Then ask the second session.

```text
If a skill suggested a different folder, what would you follow and why?
```

**Working copy.** Run `python3 tools/start.py 3-solved --agent "$agent"`
from the workshop repository. Open the printed folder in a fresh
session and paste the same save request.

## 4. Block a write

MCP stands for Model Context Protocol. It lets an agent call tools
provided by another program. In this lab, a small local program named
Brickbox provides the `save_handoff` tool. The agent sends a path and
the note text. The tool writes a new Markdown file in the practice
folder and reports where it saved it.

**Terminal**

```sh
python3 tools/start.py 4-before --agent "$agent"
```

**Before · Set up Codex.** Open the printed folder in your agent. It has the local
Brickbox save tool and uses the project from before we added the rule.
In Codex, trust the practice project if prompted. The `/mcp` command
lists the connected programs. Check that Brickbox appears. If it is
missing, go straight to the
[recorded calls](evidence/README.md#hooks) and do the Reflection.

**Agent · Before.** Paste in the session in `4-before`.

```text
Call the Brickbox save_handoff tool once. Use path `1042.md` and text
`Order 1042. Forward to Billing.` Report the result.
```

Approve the tool call if asked. Look for `Called brickbox.save_handoff`
and `Saved 1042.md` in the session, and check that the file exists.

**What you build.** Open `local-hook/protect_draft_location.py`. The
first line tells ACR to run the hook with Python. Keep it when you edit.
The event includes `tool_name` and `tool_input.path`. For the Brickbox save
tool, allow a Markdown file directly under `drafts/`. Return exit
status 2 with a short message for other destinations. Return 0 for an
allowed save or a different tool. The [finished hook](hooks/protect_draft_location.py)
shows the input fields and the two tool names.

**Terminal · Install the hook.** Run from the workshop repo.

```sh
python3 tools/start.py enable-hook --agent "$agent" --at .workshop/4-before
```

**After.** Open a new agent session in the same practice folder. If
Codex shows **Hooks need review**, choose **Review hooks**. You can also
enter `/hooks`. Open **PreToolUse**, select the new hook from the practice
folder, and press `t` to trust it.

**Terminal · Move the first save.** Run from the workshop repo if the
first run created `1042.md`. This lets you check for a new file.

```sh
mv .workshop/4-before/1042.md .workshop/4-before/first-run.saved
```

If the first run left no file, use the first row of the recorded calls
for the before result and continue.

**Agent · After · Attempt the same save.** Paste in the session with the hook trusted.

```text
Call the Brickbox save_handoff tool once. Use path `1042.md` and text
`Order 1042. Forward to Billing.` Report the result.
```

Look for the hook's block message and confirm that `1042.md` is absent.
If the client reports a hook error, try the working copy once or use
the recorded calls.

**Agent · After · Save to the allowed folder.** Paste in the same session.

```text
Call the Brickbox save_handoff tool once. Use path `drafts/1042.md` and
text `Order 1042. Forward to Billing.` Report the result.
```

Open `drafts/1042.md` and check the text.

**Agent · Reflection.** Ask in the session with the hook enabled.

```text
Which calls reached the save tool? Why did the hook stop the first attempt in this session? Show me the hook message and the file you saved.
```

**Working copy.** `4-solved` includes the hook. It uses the same two
prompts. If your client doesn't show the local tool or the hook result,
open [the recorded calls](evidence/README.md#hooks) in your agent and ask
the same questions.

## 5. Route a ticket with Clef

When you write a workflow, choose how each step runs. Code looks up the
order from an exact number. A decision model picks a team from a fixed
list. A reasoning model works out what to ask when the ticket is unclear.
[The rule for choosing a mechanism](https://github.com/jbaruch/coding-policy/blob/main/skills/coding-contracts/references/script-delegation.md)

**Start here.** Each ticket goes to Billing, Shipping, or Unclear. An
unclear ticket needs one question for the customer. The recorder uses
Codex for the before run and for that follow-up after Clef.

**Terminal · Before · Reasoning model.** Run from the workshop repo.

```sh
python3 tools/measure.py reasoning > reasoning.jsonl
```

**Agent · Before · Claude Code or Cursor.** If you're doing the before
run in your agent, paste the block below. Use the saved pair of logs
for the timing and token comparison.

```text
Classify each Brickbox ticket as Billing, Shipping, or Unclear.
For an unclear ticket, ask one question that would help route it.

1. I think I was charged twice for order 1042.
2. When will order 1058 arrive?
3. Something is wrong with order 1061.
```

**Terminal · Build.** Create the practice folder from the workshop repo.

```sh
python3 tools/start.py 5-before --agent "$agent" --at .workshop/5-clef-before
```

In that folder, fill in the three choices in `scripts/route.py`. The finished code is in `5-solved`
under `scripts/route.py`. Expand the option descriptions so the model
can tell a charge question from a delivery question. Route Unclear to
your reasoning model, which asks one question.

**Terminal · Set your Cloudflare credentials.** In the Cloudflare
dashboard, open **Workers AI**, then **Use REST API**. Copy the
account ID and create a Workers AI API token using the template.
Run this block in the Bash or Zsh terminal you'll use for Clef.
Paste each value at its prompt and press Enter. The token is hidden.
[Cloudflare setup](https://developers.cloudflare.com/workers-ai/get-started/rest-api/)

```sh
{
  printf 'Cloudflare account ID. '
  IFS= read -r CLOUDFLARE_ACCOUNT_ID
  printf 'Workers AI token (hidden). '
  IFS= read -rs CLOUDFLARE_API_TOKEN
  printf '\n'
  export CLOUDFLARE_ACCOUNT_ID CLOUDFLARE_API_TOKEN
}
```

**Terminal · After · Clef.** Run from the workshop repo in that same terminal.

```sh
python3 tools/measure.py clef --script .workshop/5-clef-before/scripts/route.py > clef.jsonl
```

If you see a connection error on macOS, try the system certificate file
and run the Clef command again from the same terminal.

```sh
export SSL_CERT_FILE=/etc/ssl/cert.pem
```

**Agent · Reflection.** Give your agent both logs, `reasoning.jsonl` and
`clef.jsonl`. If either run is unavailable, use the two saved logs together.
[Reasoning log](evidence/clef-reasoning.jsonl) · [Clef log](evidence/clef.jsonl)

```text
Compare these two runs on the same tickets. Why did one case go straight
to Billing and another need a follow-up? Which model calls explain the
difference in time and tokens? Include the reasoning call after Clef.
What can these logs tell us about cost?
```

**Terminal · Working copy.** Use this from the workshop repo if you
want the finished Clef script.

```sh
python3 tools/start.py 5-solved --agent "$agent" --at .workshop/5-clef-solved
python3 tools/measure.py clef --script .workshop/5-clef-solved/scripts/route.py > clef.jsonl
```

Use the [recorded logs](evidence/README.md#clef) if you skip either live run.

## 6. Build and install the package

**Terminal**

```sh
python3 tools/start.py 6-before --agent "$agent"
python3 tools/start.py clean --agent "$agent" --at .workshop/package-consumer
```

**Agent · Before.** Open a fresh session in `package-consumer`.

```text
I think I was charged twice for order 1042.
```

**Agent · Before Reflection.** After it replies, ask in the same session.

```text
Which files did you use for the ticket? Did you have a lookup script?
```

**What you build.** Open `.workshop/6-before/package/agent-plugin.yaml`.
The manifest is the package's list of files. Declare the triage skill,
the rule, and the hook. The lookup and Clef scripts live inside the skill
folder and travel with it. The local build is version `1.1.0`. Use the
[working manifest](agent-plugin.yaml) if you need an example.

**Terminal · Validate and install the package.** Run from the workshop repo.

```sh
(
  cd .workshop/package-consumer &&
  acr validate ../6-before/package &&
  acr install ../6-before/package --agent "$agent" --freshness none --non-interactive &&
  acr realize &&
  acr check
)
```

**Agent · After.** Open a fresh session in `package-consumer` after installing.

```text
I think I was charged twice for order 1042.
```

If the agent reports that live routing is unavailable, check the local lookup
and payment facts. The live Clef call runs in your terminal in Lab 5.

**Agent · Reflection.** Ask in the session with the installed package.

```text
Which files did you use for the ticket? How are the rule, skill, scripts,
and hook organized in the package? Where did they land in this project
and why? Show me an example on both sides and the manifest entry for it.
```

**Working copy.** Use `6-solved` for the complete manifest and change the
validate and install paths above to `../6-solved/package`. This is a local
install. If it fails, use the [recorded file locations](evidence/README.md#local-package)
for Reflection.

### Presenter demo · one artifact, shared rules

Your agent uses the installed rules as it works. Codex Auto uses the
agent's context to judge proposed actions. In Baruch's evals, it refused
actions based on the rules in [coding-policy](https://github.com/jbaruch/coding-policy).
In GitHub, the review job installs the Brickbox release so Copilot can
use the project's rules to review a code change.

Baruch will show the built-in GitHub Copilot reviewer using the published
package. After the demo, give your agent the [review](evidence/README.md#copilot)
and the [rule](rules/order-notes.md).

**Agent · Reflection**

```text
Which review finding applies the rule about pending holds? How would
that code change affect a support note?
```

## 7. Evals are tests for context artifacts

An eval checks what the agent does with the instructions and tools you
give it. Write down what should happen before you run the cases. Keep
the requests and the checks so you can rerun them when the package changes.

In Lab 1, the agent could open the right skill and find the right payment
facts while writing straight to the customer. Here, we also check whether
the reply gives Billing a handoff it can act on.

**Start here.** Read the [scorecard](answers/scorecard.md). For a billing request, check the
payment facts and the team named in the reply or draft. For a product
question, check the answer and whether the agent left the files alone.

**Terminal**

```sh
python3 tools/start.py clean --agent "$agent" --at .workshop/eval-before
python3 tools/start.py clean --agent "$agent" --at .workshop/eval-after
```

**Agent · Before.** Paste each of these four blocks by itself. Start a
fresh session in `eval-before` for each one. Keep the replies and any
drafts outside the practice folder for scoring.

```text
I see two $19 entries for order 1061. Did I pay twice?
```

```text
I need to know when the package for order 1058 will show up.
```

```text
I need help with order 1042 but I don’t know which team to ask.
```

```text
Does my Brickbox kit come with a parts list?
```

**Terminal · Install the published package.** Run from the workshop repo.
This uses the earlier `v1.0.0` release for the eval comparison.

```sh
(
  cd .workshop/eval-after &&
  acr install github:jbaruch/skill-issue-order-handoff@v1.0.0 --agent "$agent" --freshness none --non-interactive &&
  acr realize &&
  acr check
)
```

If the release fails to install, use both [saved runs](evidence/README.md#eval)
and go to Reflection.

**Agent · After.** Repeat the four prompts above, one per fresh session
in `eval-after`. Keep the replies and any drafts for scoring.

**Agent · Reflection.** Give the agent both sets of replies and drafts
and the scorecard.

```text
Score both runs using this scorecard. Show which reply, draft, or file
change earned each point. What would you change and rerun?
```

If scores tie, ask which claims about improvement the results support.

**Working copy.** The [saved runs](evidence/README.md#eval) and scorecard
let you compare the same requests if you skip either run.

## Use this in your own work

Pick one task you run often. Save an example of the current result.
Make one change, repeat the task, and ask the agent why it acted
differently. Keep the evidence that helped you decide whether to keep
the change.
