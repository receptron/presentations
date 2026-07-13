# E1 multi-trial results: three independent trials (2026-07-13)

Per review (round 5): the full 24-prompt corpus was re-run twice more with
independent agents under the identical harness (same guidance docs, same
production validator, same session model), giving **three independent trials
per prompt** (trial 1 = `pilot/` + `full/`; trials 2–3 = `trial2/`, `trial3/`).
Decoding parameters are the harness defaults and not user-settable; repeated
independent trials are therefore the variance measurement, as the review
preferred over parameter pinning.

## Headline: zero variance across trials

| Trial | Authored | First-attempt valid | Declines (correct) | Failure |
|---|---|---|---|---|
| 1 | 23 | 22 (95.7%) | 1 (p22) | p20 — `file` in `table.of` |
| 2 | 23 | 22 (95.7%) | 1 (p22) | p20 — same invariant |
| 3 | 23 | 22 (95.7%) | 1 (p22) | p20 — same invariant |

- **Aggregate: 66/69 authored schemas first-attempt valid (95.7%); per-trial
  variance: 0.**
- **Per-prompt success is bimodal, not noisy: 23 of 24 prompts succeeded 3/3;
  p20 failed 3/3 — on the same path (`fields.receipts.of.*.type`) each time.**
  The failure is a deterministic property of the prompt–schema-language pair
  (receipts-as-attachments inside a row table hits the sub-schema type
  restriction), not sampling luck.
- **Retry convergence: 3/3 p20 failures repaired in one attempt** when given
  the validator's path-precise error (trial-1 repair previously recorded;
  trials 2–3 repaired under the same protocol and re-validated).

## Behavioral consistency on the adversarial prompts

- p22 ("write me a poem"): declined in 3/3 trials.
- p19 ("organize my life"): authored a valid generic organizer in 3/3 trials
  rather than asking a clarifying question — the semantic-judgment miss is
  *systematic*, not occasional, which strengthens the §6.1 disclosure (and
  points at prompt-guidance, not sampling, as the fix).
- p21 (contradictory "kanban by date"): resolved *differently but validly*
  across trials — day-of-week enum board (trial 1) vs. mood-score enum board +
  calendar view (trial 3). Design diversity under constraint, with validity
  invariant.

## Notes

- All 69 authored schemas and both decline notes are committed under
  `runs/{pilot,full,trial2,trial3}/`.
- One trial-2 launch (p01) hit a transient infrastructure error and was
  relaunched; the retried run is an independent sample like any other.
- These trials measure schema-authoring reliability (E1). The E2 task columns
  remain single-trial, disclosed as such in §6.4.
