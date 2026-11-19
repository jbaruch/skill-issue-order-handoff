# Brickbox workshop workbook

You're a developer at Brickbox, a fictional online store. The support
team wants to automate common customer questions. Your job is to build
a skill that helps an agent look up an order and explain whether the
customer was charged twice.

Here's the first ticket:

> I think I was charged twice for order 1042.

In this workshop, your agent puts its answer in an internal note for
Billing to review. Here's what we want it to write:

> **Order 1042 · Billing**
>
> The customer thinks they paid twice. The order shows one completed $25
> payment and one pending $25 hold. Ask if the second entry appears as
> completed on their bank statement.

That's the handoff. Keep the sample note open. Each exercise changes
how the agent gets part of it right.

Start with the [README setup](README.md#before-the-workshop). Run commands
marked **Terminal** from the folder you cloned unless a step names a
different folder. Open the path each command prints in a fresh agent
session. Pause for **Reflection** after the first run and again after
the change. Ask your agent what it did and why while that session is open.
Have it show the instruction, command, or result behind its answer. If it can only infer a cause, ask it to say so.

## 1. Write the support skill

**Start here.** Open the `1-before` folder you made during setup.
Its triage skill says it handles both order questions and questions
about what comes in a kit.

**Before.** Give the agent the [question about kit contents](prompts/product.md).
In a separate new session from the same folder, give it the
[double-charge ticket](prompts/order.md). Both are support questions.
The first needs the product facts. The second needs the order record.
Paste the whole prompt each time. Both prompts tell your agent to
choose from the skills in this practice project. Record what it says
to the customer and which files it reads for each question.

**What you build.** Change only the skill description to say it prepares
a handoff from an incoming Brickbox order ticket.

**After.** Run both requests again in fresh sessions and ask the agent
what led it to the skill. Compare its replies before and after you
changed the description. Then keep the description and give the
handoff four headings in the instructions: customer question, order facts,
team, and next action. Repeat the order request and read both notes.

**Reflection.** Ask your agent what it opened for each question and why.
If it opened the order skill for the kit question, ask which words in
the description made the skill look relevant and how its instructions
affected the reply. After the change, ask where it found the kit facts.
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
`scratch_lookup.py`, the file it wrote to read the order data.

**What you build.** Save a reusable lookup in `scripts/lookup_order.py`.
It takes an order number, reads `data/orders.json`, and prints the
shipping status and payment totals. You can start with the helper you
just reviewed. Change the skill to call that file rather than giving the
agent the recipe.

**After.** In a fresh session paste the same lookup request. Both runs
should find 2500 cents captured and 2500 cents pending.

**Reflection.** Ask "How did you find the order each time? Show me the
helper you wrote in the first run and the script you called in the
second. Why reuse that script next time?" Listen for two benefits.
The same script gives the same answer for the same input and data.
The agent also saves the tokens it would spend writing a new helper.

**Working copy.** `2-solved` has the reusable script and the skill that
calls it. Run `python3 scripts/lookup_order.py 1042` there.

## 3. Set a project rule

**Terminal**

```sh
python3 tools/start.py 3-before --agent "$agent"
```

**Before.** The instruction to save under `drafts/` lives in the triage
skill. Ask the opening questions below, then paste the
[save request](prompts/save.md). It already contains the whole note.

**What you build.** Move the save instruction into a project rule that
applies across tasks. In the same rule, write "Captured Only. Count completed payments as paid and
list pending holds separately." Use `AGENTS.md` for Codex,
`CLAUDE.md` for Claude Code, or an always-applied rule under
`.cursor/rules/` for Cursor. Remove the save instruction from the skill.

**After.** Start a fresh chat and paste the same save request. Look in
the folder the agent chose.

**Reflection.** Ask before and after the change. "Which rules are loaded
when this session starts? What's the difference between an always-on
rule and a skill in this project? Which skill did you open for the save
request, if any? Why did you choose that folder? Show me the instruction."
A save-only request gives the project rule a job even if the agent
never opens the triage skill.

**Working copy.** `3-solved` has the rule in the right place for your agent.

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

**What you build.** Open `local-hook/protect_draft_location.py`. Check
the save tool's `path` input and return exit status 2 when it names a
location outside `drafts/`. Other tools can continue. To install your
hook, run this in the folder you cloned:

```sh
python3 tools/start.py enable-hook --agent "$agent" --at .workshop/4-before
```

**After.** Open a new agent session. In Codex, review and trust the new
workshop hook under `/hooks`. In the lab terminal rename the first file with
`mv 1042.md first-run.saved`, then repeat the root save request. Open the tool result and check
the folder. Finally paste the [allowed save request](prompts/draft-write.md)
and open `drafts/1042.md`.

**Reflection.** Ask "Did you try to write the file? Why did the first
attempt work and the second stop? What did the hook return?" Ask the
agent to show the file it could save. The rule guided the agent in the
last lab. The hook here can stop a call after the agent chooses to make it.

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
Codex. If you use a different agent, ask it to classify the same three
messages, then open the recorded pair for the comparison.

**What you build.** Make `5-before` with `python3 tools/start.py 5-before --agent "$agent"`.
In that folder, fill in the three choices in `scripts/route.py`. The finished code is in `5-solved`
under `scripts/route.py`. Expand the option descriptions so the model
can tell a charge question from a delivery question. Route Unclear to
your reasoning model, which asks one question.

**After.** Run the same tickets with Jev and compare the two logs.

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
ticket. Ask where it found instructions and helper code.

**What you build.** Open `.workshop/6-before/package/agent-plugin.yaml`.
The manifest is the package's list of files. Declare the triage skill,
the rule, and the hook. The lookup and Jev scripts live inside the skill
folder and travel with it. Use the [working manifest](agent-plugin.yaml)
if you need an example.

**Terminal · in `.workshop/package-consumer`**

```sh
acr validate ../6-before/package
acr install ../6-before/package --agent "$agent" --freshness none --non-interactive
acr realize
acr check
```

**After.** Open a fresh agent session in that same copy. Give it the order ticket
again and have it show where it found the lookup script.

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
Use a fresh session for each. Save the response and check the file edits.

**What you build.** Install Baruch's published release in `eval-after`,
starting with the command below.

**Terminal · in `.workshop/eval-after`**

```sh
acr install github:jbaruch/skill-issue-order-handoff@v1.0.0 --agent "$agent" --freshness none --non-interactive
acr realize
acr check
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
