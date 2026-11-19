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

Pause for **Reflection** before and after each change. Ask your agent what
it did and why. In the same session, have it show the instruction, command,
or result behind its answer. If it can only infer a cause, ask it to say so.

## 1. Write the support skill

**Start here.** Open the `1-before` folder you made during setup.
Its triage skill says it handles both order questions and questions
about what comes in a kit.

**Before.** Ask your agent the [kit question](prompts/product.md). If it
opens the order skill and still answers the kit question, ask which
instructions it followed or skipped and why, then use the
[recorded reply](evidence/first-three.md#skill-description-and-instructions)
for the comparison and move on.

Open a fresh session in the same practice folder. Paste the full
[double-charge ticket prompt](prompts/order.md) about order 1042. For
both requests, record the agent's reply and the files it opened.

**What you build.** Change only the skill description to say it prepares
a handoff from an incoming Brickbox order ticket.

**After.** Run both requests again in fresh sessions. Compare what the
agent opened and what it said before and after you changed the
description. Then keep the description and give the
handoff four headings in the instructions: customer question, order facts,
team, and next action. Repeat the order request and read both notes.
Check that the finished note gives Billing these facts and the next step.

> **Order 1042 · Billing**
>
> The customer thinks they paid twice. The order shows one completed $25
> payment and one pending $25 hold. Ask if the second entry appears as
> completed on their bank statement.

**Reflection.** Ask your agent what it opened for each question and why.
If it opened the order skill for the kit question, ask which words in
the description made the skill look relevant and which instructions it
followed. After the change, ask where it found the kit facts and why it
used that source.
For the double-charge ticket, ask which instruction gave the Billing
note its four headings.

**Working copy.** Use `1-description` to see the description edit on its
own, or `1-solved` for the complete skill. Compare the
[recorded runs](evidence/first-three.md#skill-description-and-instructions)
if you skip a run or get a different result.

## 2. Look up an order

**Terminal**

```sh
python3 tools/start.py 2-before --agent "$agent"
```

**Before.** In that folder, give your agent the [lookup request](prompts/lookup.md).
The skill tells it to write a small helper from a recipe. Open
`scratch_lookup.py`, the file it wrote to read the order data. If the
file is missing, ask the agent how it found the order, then use the
[recorded lookup](evidence/first-three.md#reuse-the-lookup) for the
comparison and start from `2-solved`.

**What you build.** Save a reusable lookup in `scripts/lookup_order.py`.
It takes an order number, reads `data/orders.json`, and prints the
shipping status and payment totals. You can start with the helper you
just reviewed. Change the skill to call that file rather than giving the
agent the recipe.

**After.** In a fresh session paste the same lookup request. Both runs
should find 2500 cents captured and 2500 cents pending. If the agent
writes another helper, ask which instruction led it to do that, then
use `2-solved` for the second run.

**Reflection.** Ask "How did you find the order each time? Show me the
helper you wrote in the first run and the script you called in the
second. Why reuse that script next time?" Listen for two benefits.
The same script gives the same answer for the same input and data.
The agent also saves the tokens it would spend writing a new helper.

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

**Before.** Open the printed folder in a fresh agent session. It has an
example note in `support/`. Start by asking the agent:

> Use only files inside this practice folder. Which rules came from this
> folder when the session started? Point to the rule file for each one.
> How do those rules differ from skills?

Check any paths your agent names. Rules it reports may come from its
personal setup. You'll add this practice folder's rule in the next step.

Then paste the [save request](prompts/save.md) in the same session.
The note is already written. Check where the agent saved it. In the
recorded run it saved the note in `support/`.

**What you build.** Open `triage-order/SKILL.md` in this practice folder.
In Codex, look under `.agents/skills/`. In Claude Code, use
`.claude/skills/`, and in Cursor, use `.cursor/skills/`. Move the
instruction to save under `drafts/` into a project rule. In the same rule, write
"Captured Only. Count completed payments as paid and list pending
holds separately." At the top of the practice folder, use `AGENTS.md`
for Codex or `CLAUDE.md` for Claude Code. In Cursor, use
`.cursor/rules/order-notes.mdc` and set `alwaysApply: true` in its
header. Remove the save instruction from the skill.

**After.** Start a fresh session in the same folder. Ask the same
opening questions, then paste the same save request. The new note
should be in `drafts/`. If the agent saves it elsewhere, ask which
instruction it followed and compare with the [recorded saves](evidence/first-three.md#move-the-save-instruction-into-a-rule).

**Reflection.** Ask before and after the change. "Which rules are loaded
when this session starts? What's the difference between an always-on
rule and a skill in this project? Which skill did you open for the save
request, if any? Why did you choose that folder? Show me the instruction."
A save-only request gives the project rule a job even if the agent
never opens the triage skill.

**Working copy.** Run `python3 tools/start.py 3-solved --agent "$agent"`
from the workshop repository. Open the printed folder in a fresh
session and paste the same save request.

## 4. Block a write

**Terminal**

```sh
python3 tools/start.py 4-before --agent "$agent"
```

**Before.** Open the printed folder in your agent. It has the local
Brickbox save tool and uses the project from before we added the rule.
In Codex, trust this workshop project and check that `/mcp` lists Brickbox.
If prompted in another client, approve the local Brickbox tool. Paste
the [root save request](prompts/root-write.md). The agent calls the tool.
Look for `1042.md` in the project folder.

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

From the workshop repo, rename the file from the first run so you can
tell whether the second run created a file:

```sh
mv .workshop/4-before/1042.md .workshop/4-before/first-run.saved
```

Repeat the root save request. Read the tool result and check whether
`1042.md` appeared again. Finally paste the
[allowed save request](prompts/draft-write.md) and open `drafts/1042.md`.
The root save should report your block message. If it reports a hook
error, check the Python line, reinstall the hook, and rerun both saves.

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
python3 tools/measure.py reasoning > reasoning.jsonl
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

**Before.** In `package-consumer`, give your agent the same order
ticket. Use the full prompt, including its instruction to work inside
that folder. Ask which files it used and whether it had a lookup script.

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
install path above to `../6-solved/package`. This is a local install.

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

**Start here.** Use [fresh requests](fixtures/eval-cases.json) and the
[scorecard](answers/scorecard.md). For a billing request, check the
payment facts and the team named in the note. For a product question,
check that the agent answers from the kit information and leaves the
project files alone.

**Terminal**

```sh
python3 tools/start.py clean --agent "$agent" --at .workshop/eval-before
python3 tools/start.py clean --agent "$agent" --at .workshop/eval-after
```

**Before.** Give one request at a time to the agent in `eval-before`.
Use a fresh session for each. Keep the responses in a scratch note
outside the practice folder and record any edits made by the agent.

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
