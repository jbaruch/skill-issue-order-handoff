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

The agent reported 556 output tokens in the first run and 264 in the
second. The two sessions also had different input and cache usage.

## Move the save instruction into a rule

The save-only request supplied the complete note. In the first run,
Codex wrote `support/order-1042-billing.md` without opening the triage
skill. After the change, it wrote `drafts/order-1042-billing.md`.
It looked at the skill in the second run. The save instruction had
already moved out of that file and into `AGENTS.md`.

Ask the agent which instruction tells it where to save the note.
Compare the two files that could have contained the instruction.
