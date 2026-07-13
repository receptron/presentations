# E1 full-corpus results (2026-07-13)

24 prompts (corpus.json), each authored by an independent agent given the production
authoring guide and type contract, validated with the production validator
(`CollectionSchemaZ` + `acceptParsedSchema` from `@mulmoclaude/core`). Pilot batch
(6) in `../pilot/`, remainder (18) here.

## Headline numbers

| Metric | Result |
|---|---|
| Prompts | 24 (EN 16 / JA 8; 4 adversarial) |
| Appropriate declines (out-of-scope p22 "write a poem") | 1 — declined, correctly |
| Schemas authored | 23 |
| **First-attempt valid (Zod + gates)** | **22/23 (95.7%)** |
| Valid after 1 feedback retry | 23/23 (100%) |
| JSON parse errors | 0 |

## The single failure — and its repair

p20 (adversarial-overspecified home inventory, 14 requested fields): placed a `file`
field inside a `table.of` sub-schema; the validator's narrower sub-field type set
forbids it (`fields.receipts.of.receipt.type: invalid option`). Given the validator's
issue verbatim (as `manageCollection` would return it), the repair agent converged in
one attempt: receipt rows keep the table shape, storing workspace-relative paths as
strings. This exercised the exact loop the architecture claims: obscure cross-field
invariant → hard rejection with a path-precise error → model self-repair → valid.

## Semantic fidelity on the hard features (coded by inspection)

- **p08 medications**: `spawn {unit: day, interval: 30}` on completion + trigger with
  lead days — the requested "refill done → next one 30 days later" exactly.
- **p10 invoices**: `ref` field `clientId -> clients` (cross-collection relation) +
  due-date trigger for the overdue reminder.
- **p12 chores**: the advanced *field-driven* spawn variant —
  `spawn.fromField: frequency` with a `map` of weekly/monthly to recurrence units;
  the schema language's most obscure feature, used correctly and unprompted.
- **p18 oseibo (ja)**: `ref` `recipient -> contacts` against the pre-existing
  collection, as requested.
- **p20 home inventory**: warranty expiration as `triggerField` with
  `triggerLeadDays: 30`, paired with a completion enum so the bell can clear.
- **p19 (vague "organize my life")**: authored a generic `life-organizer` rather
  than asking a clarifying question — valid, but arguably the wrong move for a real
  assistant; scored as a semantic-judgment miss even though the schema validates.
  (The production system's conversational loop would allow asking; the harness's
  one-shot format biases toward authoring. Disclose.)

## Caveats for the paper writeup

- Authoring agents ran in a test harness (session model + the same guidance docs the
  production system provides), not inside the full MulmoClaude runtime. Same
  validator, same docs, different agent shell — disclose in §6.
- Semantic fidelity above is author-coded on the complex subset; the paper's E1
  should code all 23 against a pre-registered feature checklist, ideally with a
  second coder.
- One retry was needed in 24 prompts; retry-convergence statistics need a larger n
  to be meaningful. The interesting result is qualitative: the error → repair loop
  worked exactly as designed on a genuinely obscure invariant.
