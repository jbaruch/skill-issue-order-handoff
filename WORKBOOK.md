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
2. Keep that terminal open in the repository for steps marked **Terminal**.
3. Open the exact folder the setup command prints in your agent. Start a
   fresh session there.

Use the **Reflection** prompts to ask your agent what it did and why.
Ask in the session where it did the work. Have it show the instruction,
command, or result behind its answer. If it can only infer a cause, ask
it to say so.

## 1. Frontmatter matters

**Start here.** Open the `1-before` folder you made during setup. The
order skill's description says it covers both orders and kit contents.
Your agent uses that description to decide when to open the skill.

**Before.** In a fresh session, paste the [kit question](prompts/product.md)
by itself. In the
[recorded run](evidence/first-three.md#frontmatter-matters),
Codex opened the order skill and asked for an order number.

**Reflection.** In that session, ask what the agent opened and why. If
it opened the order skill, ask which words in the description matched
the question and why it asked for an order number.

Start another fresh session in the same folder. Paste the
[double-charge ticket](prompts/order.md) by itself. Ask which skill the
agent opened, if any, and why. Record both replies and what the agent
actually opened. A session that has already read the skill can reuse
its instructions, so use a fresh session for each request.

**What you build.** In `triage-order/SKILL.md`, replace just the
`description` line at the top:

```yaml
description: Prepare a support handoff from an incoming Brickbox order ticket.
```

**After.** Run both requests again in fresh sessions. Compare what the
agent opened and what it said. The kit question should lead to the
product guide. The double-charge ticket still belongs with the order skill.

**Reflection.** In each session, ask why the agent took that path and
what it read. Why did the kit question go to a different source? What
in the new description still matched the double-charge ticket?

**Working copy.** Use `1-solved` for the skill with the narrower
description. If either run takes a different path, ask why, compare with
the [recorded runs](evidence/first-three.md#frontmatter-matters),
and move on.

## 2. Look up an order

**Terminal**

```sh
python3 tools/start.py 2-before --agent "$agent"
```

**Before.** In that folder, give your agent the [same order ticket](prompts/order.md).
The skill gives it a recipe for writing a helper. Open
`scratch_lookup.py` if it created the file. If the agent ran Python
directly in the terminal, ask it to show you that code. If it skipped
writing code, use the [recorded lookup](evidence/first-three.md#reuse-the-lookup)
for the before run and go straight to the working copy for the after run.

**Reflection.** In the same session, ask how the agent looked up the
order. Have it show the code it wrote and the command it ran.

**What you build.** Ask the same agent to keep the helper for future tickets.

> Let's reuse the lookup you just wrote. Save a copy as
> `scripts/lookup_order.py` that takes an order number. Update the lookup
> step in the triage-order skill to run that script on future tickets.
> Show me what changed and how you checked it.

If Codex asks to edit `SKILL.md`, review the proposed lookup change and
choose **Yes, proceed**. Check the updated skill and script before
opening the next session.

**After.** In a fresh session paste the same lookup request. Both runs
should find 2500 cents captured and 2500 cents pending. If the agent
writes another helper, ask which instruction led it to do that, then
use `2-solved` for the second run.

**Reflection.** Ask in the new session. "What command did you run?
Did you have to write lookup code this time? What do we gain by using
the same script on future tickets?" The same script gives the same
answer for the same input and data. The agent saves the tokens it
would spend writing a new helper.

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

**Before.** Open the printed folder in a fresh agent session and paste
the [save request](prompts/save.md) as the first message. Check where the
note landed and keep that session available for Reflection. In the
recorded run, the agent saved the note next to the example in `support/`.

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

**After.** Start a fresh session in the same folder and paste the same
save request first. Compare both file paths and check that the text
matches. The second note should be in `drafts/`. If the agent saves it
elsewhere, compare with the [recorded saves](evidence/first-three.md#move-the-save-instruction-into-a-rule).

**Reflection.** After both saves, ask each session about the save it
already made. "Which project rules were loaded at startup? Which skill
did you open for the save, if any? What made you choose that folder?
Show me the evidence from that run."

Then ask the second session "If a skill suggested a different folder,
what would you follow and why?" Have it explain what the practice
folder's rule required. Some of the other rules may come from your
own setup.

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

**Before.** Open the printed folder in your agent. It has the local
Brickbox save tool and uses the project from before we added the rule.
In Codex, trust the practice project if prompted. The `/mcp` command
lists the connected programs. Check that Brickbox appears, then paste
the [root save request](prompts/root-write.md). Approve the tool call if
asked. Look for `1042.md` in the practice folder and check the save result.
If Brickbox is missing from the tool list, go straight to the
[recorded calls](evidence/README.md#hooks) and do the Reflection.

**What you build.** Open `local-hook/protect_draft_location.py`. The
first line tells ACR to run the hook with Python. Keep it when you edit.
The event includes `tool_name` and `tool_input.path`. For the Brickbox save
tool, allow a Markdown file directly under `drafts/`. Return exit
status 2 with a short message for other destinations. Return 0 for an
allowed save or a different tool. The [finished hook](hooks/protect_draft_location.py)
shows the input fields and the two tool names. Install your hook from
the workshop repo:

```sh
python3 tools/start.py enable-hook --agent "$agent" --at .workshop/4-before
```

**After.** Open a new agent session in the same practice folder. If
Codex shows **Hooks need review**, choose **Review hooks**. You can also
enter `/hooks`. Open **PreToolUse**, select the new hook from the practice
folder, and press `t` to trust it.

If the first run saved a file, rename it from the workshop repo so you
can tell whether the second run created a file:

```sh
mv .workshop/4-before/1042.md .workshop/4-before/first-run.saved
```

If the first run left no file, use the first row of the recorded calls
for the before result and continue.

Repeat the root save request. Read the tool result and check whether
`1042.md` appeared again. Finally paste the
[allowed save request](prompts/draft-write.md) and open `drafts/1042.md`.
The root save should report your block message. If it reports a hook
error, check the first line and try the working copy once. If the
client still can't run it, use the recorded calls for Reflection.

**Reflection.** Ask "Which calls reached the save tool? Why did the
hook stop the root save? Show me the hook message and the file you
saved under `drafts/`." The hook can stop the call before the save
tool runs.

**Working copy.** `4-solved` includes the hook. It uses the same two
prompts. If your client doesn't show the local tool or the hook result,
open [the recorded calls](evidence/README.md#hooks) in your agent and ask
the same questions.

## 5. Route a ticket with Jev

When you write a workflow, choose how each step runs. Code looks up the
order from an exact number. A decision model picks a team from a fixed
list. A reasoning model works out what to ask when the ticket is unclear.
[The rule for choosing a mechanism](https://github.com/jbaruch/coding-policy/blob/main/skills/coding-contracts/references/script-delegation.md)

**Start here.** Use the three messages in [the routing cases](fixtures/routes.json).
The task is to choose Billing, Shipping, or Unclear. If the message is
unclear, the next step is one question for the customer.

**Before.** Let the reasoning model choose. The recorder below uses
Codex for the reasoning run and for Jev's follow-up on the unclear
ticket. If you use a different agent, ask it to classify the three
messages and use the recorded pair for the time and token comparison.

**Terminal · from the folder you cloned**

```sh
python3 tools/measure.py reasoning > reasoning.jsonl
```

**What you build.** Make `5-before` with `python3 tools/start.py 5-before --agent "$agent"`.
In that folder, fill in the three choices in `scripts/route.py`. The finished code is in `5-solved`
under `scripts/route.py`. Expand the option descriptions so the model
can tell a charge question from a delivery question. Route Unclear to
your reasoning model, which asks one question.

**After.** Run the same tickets with Jev and compare the two logs. For
the live run, load your TypeSafe key in the terminal that runs the recorder.
If either run is unavailable, use both [saved logs](evidence/README.md#jev)
for Reflection so the tickets and calls are comparable.

**Terminal · from the folder you cloned**

```sh
python3 tools/measure.py jev --script .workshop/5-before/scripts/route.py > jev.jsonl
```

**Reflection.** Give your agent the two logs. Ask "Why did one case go
straight to Billing and another need a follow-up? Which calls explain
the difference in time and tokens? What can we tell about cost from
these logs?" Count any reasoning call made after Jev. Use the same
tickets in both runs. Check the cost field before making a dollar claim.

**Working copy.** `5-solved` has the completed Jev script. To use it, create that
folder with `tools/start.py` and use its script path in the last command. Open the
[recorded logs](evidence/README.md#jev) if you skip either live run.

## 6. Build and install the package

**Terminal**

```sh
python3 tools/start.py 6-before --agent "$agent"
python3 tools/start.py clean --agent "$agent" --at .workshop/package-consumer
```

**Before.** Open a fresh agent session in `package-consumer` and give
it the [same order ticket](prompts/order.md). After it replies, ask
which files it used and whether it had a lookup script.

**What you build.** Open `.workshop/6-before/package/agent-plugin.yaml`.
The manifest is the package's list of files. Declare the triage skill,
the rule, and the hook. The lookup and Jev scripts live inside the skill
folder and travel with it. Use the [working manifest](agent-plugin.yaml)
if you need an example.

**Terminal · from the workshop repo**

```sh
(
  cd .workshop/package-consumer &&
  acr validate ../6-before/package &&
  acr install ../6-before/package --agent "$agent" --freshness none --non-interactive &&
  acr realize &&
  acr check
)
```

**After.** Open a fresh agent session in that same copy. Give it the order ticket
again and have it show where it found the lookup script.
If the agent reports that live routing is unavailable, check the local lookup
and payment facts. The live Jev call runs in your terminal in Lab 5.

**Reflection.** Ask "How are the artifacts organized in the package?
Where did the rule, skill, scripts, and hook land here? Why did each go
there? Show me a file in both places and the part of the manifest that
describes it."

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
package. After the demo, give your agent the
[review](evidence/README.md#copilot) and the
[rule](rules/order-notes.md). Ask which finding applies the rule about
pending holds and how the code change would affect a support note.

## 7. Evals are tests for context artifacts

An eval checks what the agent does with the instructions and tools you
give it. Write down what should happen before you run the cases. Keep
the requests and the checks so you can rerun them when the package changes.

In Lab 1, the agent could open the right skill and find the right payment
facts while writing straight to the customer. Here, we also check whether
the reply gives Billing a handoff it can act on.

**Start here.** Use [fresh requests](fixtures/eval-cases.json) and the
[scorecard](answers/scorecard.md). For a billing request, check the
payment facts and the team named in the reply or draft. For a product
question, check the answer and whether the agent left the files alone.

**Terminal**

```sh
python3 tools/start.py clean --agent "$agent" --at .workshop/eval-before
python3 tools/start.py clean --agent "$agent" --at .workshop/eval-after
```

**Before.** Copy the `prompt` text from one case at a time into a fresh
agent session in `eval-before`. Paste each request by itself. Save the
replies and any drafts outside the practice folder for scoring.

**What you build.** Install Baruch's published release in `eval-after`,
starting with the command below.

**Terminal · from the workshop repo**

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

**After.** Run the same cases in the installed copy. Give the two
runs and your scorecard to your agent. Ask it to show where each
point came from.

**Reflection.** Ask "Why did one run score higher? Show me the note,
choice, or edit that earned the point. What would you change and rerun?"
If scores tie, ask which claims about improvement the results support.

**Working copy.** The [saved runs](evidence/README.md#eval) and scorecard
let you compare the same requests if you skip either run.

## Use this in your own work

Pick one task you run often. Save an example of the current result.
Make one change, repeat the task, and ask the agent why it acted
differently. Keep the evidence that helped you decide whether to keep
the change.
