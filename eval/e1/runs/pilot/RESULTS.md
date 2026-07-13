# E1 pilot results (2026-07-13)

Six prompts spanning the difficulty range, each authored by an independent agent
given the production authoring guide (`collection-skills.md`) and type contract,
then validated with the production validator (`CollectionSchemaZ` +
`acceptParsedSchema` from `@mulmoclaude/core` dist).

## First-attempt validity: 6/6

| id | difficulty | slug chosen | JSON | Zod | gates |
|---|---|---|---|---|---|
| p01-books | simple | books | ok | pass | pass |
| p04-jobs | moderate (kanban) | job-applications | ok | pass | pass |
| p07-subscriptions | complex (recurring) | subscriptions | ok | pass | pass |
| p09-wine | complex (conditional) | wine-cellar | ok | pass | pass |
| p15-hoken | complex (ja, recurring) | insurance | ok | pass | pass |
| p21-conflict | adversarial (contradictory) | daily-mood | ok | pass | pass |

## Semantic fidelity (hard features)

- **p07**: `triggerField: renewsOn`, `triggerLeadDays: 3`, `spawn` on `status ∈ {paid}`
  advancing monthly with `carry` of stable fields, `completionDoneValues: [paid, canceled]` —
  all four requested behaviors declared correctly.
- **p15**: `triggerLeadDays: 14`, yearly `spawn` on `支払済み`, Japanese labels — correct.
- **p09**: `rating` field with `when: {field: opened, in: [true]}` — the requested
  ask-only-after-opened behavior, expressed exactly as the production restaurants schema does.
- **p21 (contradictory: "kanban organized by date")**: resolved rather than failed —
  authored a required day-of-week enum as `kanbanField` (Mon–Sun board) plus
  `calendarField: date` for a true date view, and explained the reasoning. Graceful
  degradation of an unsatisfiable request into a valid, defensible design.

## Notes for the full run

- Validity alone is a weak signal at this success rate; the full run should also
  code semantic fidelity per prompt (planned features present/absent/wrong).
- Adversarial prompts (p19 vague, p22 out-of-scope) need a decline path: agents may
  write `DECLINED.md` instead of forcing a schema.
- Pilot agents were run with the session model via the Agent tool, not the full
  MulmoClaude runtime; the full E1 writeup must disclose this harness difference
  (same guidance docs, same validator, different agent shell).
