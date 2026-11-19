# Recorded workshop runs

Open the relevant run in your agent and use the same Reflection questions
as the live exercise.

## Skills, scripts and rules

[The first three labs](first-three.md) document the files the agent read
or wrote and the result. Treat skill selection as unknown if a run
shows only the list of available skills.

## Hooks

[The three saves](hooks.md) show the root write before the hook, the
denial after the hook, and the successful write under `drafts/`.

## Clef

Compare [the reasoning run](clef-reasoning.jsonl) with [the Clef run](clef.jsonl).
Both chose Billing, Shipping, and Unclear for the same tickets. The
reasoning-only calls took 9.09 seconds. Clef took 5.58 seconds including
the Codex follow-up for the unclear ticket. Use the per-call usage to
compare tokens. A dollar comparison needs separate billing or pricing data.

## Jev

This comparison comes from the earlier version of Lab 5.

Compare [the reasoning run](reasoning.jsonl) with [the Jev run](jev.jsonl).
The recorded pair uses the same three tickets. The Jev log includes the
follow-up call for the unclear ticket.

Both chose Billing, Shipping, and Unclear in that order. The three
reasoning-only calls took 12.89 seconds in total. The Jev run took 3.97
seconds including the reasoning follow-up. These are elapsed times from
one run of the lab on the presenter's machine. The two paths recorded
54,536 and 19,268 input tokens, respectively. Use the per-model
counts and cached tokens in the logs when discussing cost. A dollar
comparison also needs model prices or billing records.

## Local package

In a clean Codex practice folder, `acr validate`, `acr install`,
`acr realize`, and `acr check` all passed for the local working copy.
Compare the [package manifest](../agent-plugin.yaml) with the files
ACR put in the project.

| Package source | Location in the Codex project |
| --- | --- |
| `skills/triage-order/SKILL.md` | `.codex/skills/acr__jbaruch__skill-issue-order-handoff__triage-order/SKILL.md` |
| `skills/triage-order/scripts/` | `scripts/` next to the installed `SKILL.md` |
| `rules/order-notes.md` | `AGENTS.md` |
| `hooks/protect_draft_location.py` | `.codex/hooks/acr__jbaruch__skill-issue-order-handoff__protect-draft-location/protect_draft_location.py` |

Ask your agent which entry in the manifest put each file there and how
Codex discovers it.

## Copilot

The [first review](https://github.com/jbaruch/skill-issue-order-handoff/pull/1#pullrequestreview-5979482565)
flagged the incorrect amount paid. The [review after setup](https://github.com/jbaruch/skill-issue-order-handoff/pull/1#pullrequestreview-5979515807)
found the same problem and named our Captured Only rule. Both reviewed
the same change to the payment calculation.

The [review job](https://github.com/jbaruch/skill-issue-order-handoff/actions/runs/44587758808)
installed and checked v1.0.0. The setup printed the rule from `AGENTS.md`.
Here is the [setup file](../.github/workflows/copilot-code-review.yml).
GitHub's built-in reviewer did the review.

## Eval

Compare the [clean run](eval-baseline.jsonl) and the
[run with v1.0.0](eval-published.jsonl). Each request ran in its own
clean Codex session. Use the [scorecard](../answers/scorecard.md).
The recorded packaged runs used the skill's reasoning fallback when
the TypeSafe key was unavailable in the agent's shell. The published
v1.0.0 package used for those evals includes the earlier Jev router.

[One scoring pass](eval-scores.md)
