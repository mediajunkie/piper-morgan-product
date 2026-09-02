# First live flip — the readiness page (Lead, 2026-08-20)

**What this is**: everything needed to decide and execute the first live inversion flip, on one
page, so the decision costs PM a minute rather than an archaeology session. Written at day's end
while the build is fresh; the flip itself happens on PM's word, never automatically.

## Current state — DARK, and dark by construction

`PIPER_INVERSION_LIVE_CATEGORIES` is unset in every environment. Unset = the legacy chain runs,
byte-identical, pinned by test. Nothing about the Inversion touches a live turn today.

## What one flip actually changes

For an in-scope operation only: the constrained routing call chooses the rail key instead of
(pre-classifier → LLM classifier). **The rail, the handlers, and the consent gate are untouched** —
the same handler runs with the same confirmations. Four conditions must ALL hold or the turn
falls to the legacy chain: operation resolves · its group/name/category is flagged · confidence
≥ threshold (default 0.8) · the rail entry declares `EffectClass.READ`. Armed turns (pending
offer, active process, draft in compose) never take the inversion path in this wave.

## The recommended first flip

```
PIPER_INVERSION_LIVE_CATEGORIES=read_status
```
50 keys: listings, status, identity, standup read-out. Chosen because these have zero armed-state
interaction, no referent to resolve, no time expression to parse — the failure mode is "wrong
list shown," never "wrong thing written." **Not** `read_referent` first (referent resolution is
the newer capability) and **not** `QUERY` (the registry category sweeps in four ungrouped
calendar/changes ops — the audit lists them by name).

## What to watch, in order of what would actually hurt

1. **A read answering with the wrong data** — the real risk, and the only one users feel. Watch
   PM's own listing turns (`show my todos`, `what projects do I have?`, `standup`).
2. **Disagreement telemetry** — every live decision logs route/confidence/snapshot presence, and
   flip-1 logs where the legacy pre-classifier would have gone. Sustained disagreement on a
   phrase family is corpus material, not necessarily a bug.
3. **Fall-through rate** — turns landing on legacy despite a live flag (sub-threshold or REFUSED).
   High rate = the grammar is thinner than we think for that class.
4. **Latency** — one constrained call replaces one classifier call; should be a wash. Measure,
   don't assume.

## Revert

`unset PIPER_INVERSION_LIVE_CATEGORIES` (or drop it from the Fly secret/env) and redeploy. No
code change, no migration, no data to unwind — the legacy chain never left. This is why the flag
is env-driven rather than a config file or a database row.

## Honest gaps before flipping (both known, neither blocking a READ flip)

- ~~**#1668**~~ **CLOSED-PENDING-REVIEW 2026-08-21 — the repurpose shipped.** On an
  inversion-routed turn the sampled shadow now computes the LEGACY counterfactual instead of
  re-routing (`shadow_legacy_counterfactual_*` events; legacy-routed turns keep the router
  shadow byte-identically). Cost did not grow: the counterfactual replaces the re-route and
  short-circuits on the deterministic legs, so it spends 0 LLM calls when the pre-classifier or
  multi-intent rules claim and 1 when they don't — never more than the call it replaced. The
  line names which legs ran and which were skipped (m-43); the counterfactual is the unscoped,
  uncached, single-intent legacy route, not the full `classify_multiple`. **This is now watch
  item 2's real instrument**: during a flip, disagreement rows are the corpus artifact.
- **#1670**: the not-live telemetry bucket names predate the flip-group widening, so a rejected
  turn's logged reason can under-describe why. Cosmetic for reading logs, real for corpus
  analysis; a corpus migration.

## What a flip does NOT do

It does not delete the pattern router (that's Phase 3, gated separately), does not change any
write path, does not alter consent behavior, and does not need a code deploy to reverse.
