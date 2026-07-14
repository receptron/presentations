# Nurtured at Home — working notes (not part of the manuscript)

Apparatus moved out of `nurture-paper-text.md` per review (round 4): the
manuscript stays clean; everything an author or artifact reviewer needs to
reproduce or extend the work lives here.

## Citation keys

`[key]` placeholders in the text resolve against the must-cite table in
[nurture-paper-literature-scan.md](nurture-paper-literature-scan.md) for
BibTeX generation at typeset time.

## §2 freshness

Related work was positioned against the literature as scanned and
adversarially verified on 2026-07-13. Several load-bearing sources are recent
preprints in a fast-moving space — run a delta-check against new work
immediately before submission (a check, not a rewrite).

## §5 source references (repo: receptron/mulmoclaude, post-merge main)

- Schema types: `packages/core/src/collection/core/schema.ts`
  (CollectionSchema 436–551, field types 65–96, spawn 157–172, custom views 209–271)
- Zod validator + gates: `packages/core/src/collection/server/discovery.ts`
  (CollectionSchemaZ 535–834, loadOneCollection 882–927)
- Record validation: `server/agent/mcp-tools/manageCollection.ts`
  (putItems, putSchema); `packages/core/src/collection/server/validate.ts`
  (49–117; skip-at-read note 2–7); present-time scan `server/api/routes/plugins.ts`
- Reconciler: `packages/core/src/collection-watchers/watcher.ts` (tick),
  `reconciler.ts` (invariant + reconcile), `collection/server/spawn.ts`
  (create-if-absent, runaway guard)
- View sandbox: collection-plugin `CollectionCustomView.vue`;
  `server/api/auth/viewToken.ts`
- Ablation + clock switches: `server/system/env.ts` (`isAblated`),
  `packages/core/src/collection-watchers/clock.ts` (`evalNow`)
- Workspace counts: author-workspace inventory 2026-07-13
  (`eval/e3/inventory.sh`; aggregate counts only)

## Pre-submission checklist

1. §2 delta-check against literature published after 2026-07-13.
2. Repeated evaluation trials; report variance (E2 single-trial verdicts
   currently disclosed as such). All runs already used the same model
   (Claude Fable 5), so model pinning is done.
3. Formative usability study (removed from the manuscript per review,
   2026-07-13) — run or leave as future work per venue norms.
4. Resolve `[key]` placeholders to BibTeX; typeset figures
   (`docs/figures/`); verify anonymization requirements vs. the
   dogfooded-workspace disclosures.
5. Venue formatting; artifact-evaluation packaging (`eval/` tree +
   MulmoClaude release with ablation switches).

## Camera-ready figure checks (per final review, round 6 — Strong Accept)

- Figure 1: verify the authoring/runtime boundary (the validation-gate line)
  prints thick and unambiguous at final size; bolden the dashed stroke in
  `docs/figures/fig1-architecture.json` if needed and re-render.
- Figure 2: keep the JSON listing within one column/page — elide secondary
  properties with `…` if the venue's format squeezes it; the load-bearing
  elements are `rating`+`when`, `visited`, and the `views` capability set.
