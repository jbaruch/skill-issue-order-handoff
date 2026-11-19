# Compare the first three labs

These observations came from separate Codex sessions in new folders.

## Skill description and instructions

With the broad description, Codex opened `triage-order/SKILL.md` before
replying to the kit question. The skill required an order number, so
Codex asked for one. With the narrower description, it read
`data/product-info.md` and said the kit includes assembly instructions.
For the double-charge ticket, it opened the skill and checked order 1042
in both runs. The final instructions gave the Billing note four headings:
Customer question, Order facts, Team, and Next action.

Give your agent the [five recorded runs](skill-selection.jsonl) and the
two descriptions. Ask why the kit question matched the first description,
which instruction made the agent ask for an order number, and where it
found the answer after the edit. Then ask which instruction gave the
Billing note its four headings.

## Reuse the lookup

Before the change, Codex created `scratch_lookup.py` and ran
`python3 scratch_lookup.py 1042`. After the change, it ran
`python3 scripts/lookup_order.py 1042`. Both found 2500 cents captured
and 2500 cents pending.

Ask what the agent had to write in the first run and why it could run
the supplied file in the second. Reusing the same script gives the same
result for the same input and data. It saves the tokens a model would
spend writing a new helper for each order.

The agent reported 932 output tokens in the first run and 474 in the
second. The two sessions also had different input and cache usage.

## Move the save instruction into a rule

Codex saved the already-written note next to the example in `support/`.
After adding `AGENTS.md` and removing the save instruction from the skill,
Codex saved the same note under `drafts/`. The contents matched. In the
second Reflection, it pointed to the rule in `AGENTS.md` and explained
that it could save a finished note without opening the triage skill.

Ask your agent which rules it loaded at the start of each session.
Have it point to the project file and explain why the two saves went
to different folders.
