# E2 harness verification (2026-07-13)

Host-level verification that the ablation infrastructure behaves as designed,
run against the MulmoClaude `eval-ablation-mode` branch (commit `837c2965`,
PR receptron/mulmoclaude#2082 — run from the branch; not merged to main by
design). Three servers, three scratch workspaces, identical synthetic seed
(`seed-workspace.sh`: a collection with completion bell, 3-day trigger lead,
and monthly spawn).

| Boot configuration | Spawn successor | Due-record bell | Far-future record |
|---|---|---|---|
| Normal (`PORT=3101`) | ✅ `m-done-20260801` created at boot reconcile (correct +1 month civil advance) | ✅ bell for "Replace filter" (due within lead) | ✅ silent |
| Ablated (`MULMOCLAUDE_ABLATION=validation,reconciler`) | ✅ none (file set unchanged) | ✅ none (no notifier state at all) | ✅ silent |
| Fake clock (`MULMOCLAUDE_FAKE_NOW=2026-12-24`, normal mode) | — | — | ✅ bell for "Service boiler" (trigger 2026-12-25) fired **in July** under the injected December clock |

The ablated boot logs `ABLATION ACTIVE: reconciler disabled — no watchers,
bells, or spawn recurrence (evaluation only)`, so an accidentally-ablated
server is unmissable. The `validation` half of the switch is covered by unit
tests in the MulmoClaude PR (ablated `putItems` writes an out-of-enum row
verbatim; `getItems` stays silent).

## Operational notes for the task runs

- **Always set `DISABLE_MACOS_REMINDER_NOTIFICATIONS=1`.** The normal-mode
  boot attempted to mirror the synthetic bell into macOS Reminders (blocked
  only by missing osascript authorization). Without this flag, synthetic
  evaluation reminders could sync to the author's real iPhone.
- Server: `PORT=<p> MULMOCLAUDE_WORKSPACE_PATH=<scratch> MULMOCLAUDE_AUTH_TOKEN=<t>
  npx tsx server/index.ts` from the branch checkout. Boot reconcile runs
  within seconds; no client build needed for host-level checks.
- Ports 3101–3103 used; the author's production instance on 3001 is never
  touched, and no eval server logs into the relay.

## Status

Infrastructure verified. Next: agent-in-the-loop task runs (T1–T10 per
`../task-suite.md`) for S and B1 via the chat surface, B3 via codegen
sessions; B2 pending the human-operator decision.
