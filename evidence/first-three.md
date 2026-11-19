# Compare the first three labs

These observations came from separate Codex sessions in new folders.

## Skill description and instructions

We asked Codex [the same kit question](../prompts/product.md) in two
fresh sessions. With the broad description, Codex opened
`triage-order/SKILL.md` and asked for the order number. With the narrower
description, it read the product guide and said the kits include
assembly instructions. It did not open the order skill in that run.
For the [double-charge ticket](../prompts/order.md), Codex opened the
skill and checked order 1042 in all three versions. The first reply was
addressed to the customer. The final instructions produced a Billing
note with four headings: Customer question, Order facts, Team, and
Next action.

Give your agent the [five recorded runs](skill-selection.jsonl) and the
two descriptions. Ask why the kit question matched the first description,
which instruction made the agent ask for an order number, and where it
found the answer after the edit. Then ask which instruction gave the
Billing note its four headings.

## Reuse the lookup

For the [same order ticket](../prompts/order.md), Codex wrote and ran
Python in the terminal to find order 1042. After the change, it ran
`python3 scripts/lookup_order.py 1042`. Both found 2500 cents captured and
2500 cents pending.

Ask what the agent had to write in the first run and why it could run
the supplied file in the second. Reusing the same script gives the same
result for the same input and data. It saves the tokens a model would
spend writing a new helper for each order.

The agent reported 1239 output tokens in the first run and 380 in the
second. The two sessions also had different input and cache usage.

## Move the save instruction into a rule

Codex saved the [already-written note](../prompts/save.md) next to the
example in `support/`.
After adding `AGENTS.md` and removing the save instruction from the skill,
Codex saved the same note under `drafts/`. The contents matched. In the
second Reflection, it pointed to the rule in `AGENTS.md` and explained
that it could save a finished note without opening the triage skill.

Ask your agent which rules it loaded at the start of each session.
Have it point to the project file and explain why the two saves went
to different folders.
