# Recorded workshop runs

Open the relevant run in your agent and use the same Reflection questions
as the live exercise.

## Skills, scripts and rules

[What we observed in the first three labs](first-three.md) links the
request, the files read or written, and the result. Treat skill selection
as unknown if a run shows only the list of available skills.

## Hooks

[The three saves](hooks.md) show the root write before the hook, the
denial after the hook, and the successful write under `drafts/`.

## Jev

Compare [the reasoning run](reasoning.jsonl) with [the Jev run](jev.jsonl).
The recorded pair uses the same three tickets. The Jev log includes the follow-up call
for the unclear ticket.

Both chose Billing, Shipping, and Unclear in that order. The three
reasoning-only calls took 12.89 seconds in total. The Jev run took 3.97
seconds including the reasoning follow-up. These are elapsed times from
one run of the lab on the presenter's machine. The logs give token usage
and include no dollar charges.

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
the TypeSafe key was unavailable in the agent's shell. For live Jev
results, use the separate lab 5 logs above.

[One scoring pass](eval-scores.md)
