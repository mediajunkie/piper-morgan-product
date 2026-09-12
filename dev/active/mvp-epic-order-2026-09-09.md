# MVP Sprint Backlog — Ordered Epics (source of truth)

**Owner**: PPM. **Status**: live working order — update in place as epics close/reorder, don't
fork a new file per revision. **Purpose**: per PM's 2026-09-09 directive (relayed by Exec), Lead
works ONE epic at a time, fully, before moving to the next. This file is what Lead consults
without needing to ask anyone. Board Status/Sprint fields are the per-issue record; this file is
the *order*, which no GitHub field currently encodes.

**The rule, verbatim from PM's directive**: work the current epic until it's fully closed.
Discovered work goes into (a) the same epic, (b) another epic, or (c) a later milestone — only
work added to the SAME epic delays that epic's closure. Epic-relative progress is legible;
pile-relative progress (the flat "N not done" count) is not.

**Provenance**: cause-factoring by Arch (`factoring-arch-to-ppm...-2026-09-09.md`), 37 Sprint
Backlog items live-pulled 2026-09-09, cross-checked against a fresh pull before ordering (both
agree: 37 items, same membership). Ordering and any reclassification below is PPM's.

---

## Order

### 1. CI/infra red (6 items, 1 closed) — cheap, and it's a quiet tax on every epic after it
`#1687` four CI workflows standing red · `#1711` Keychain ACL hang blocks server startup silently
· ~~`#1637`~~ 6 standing test failures poisoning 6 — **CLOSED 2026-09-09/10**. Plus, filed
2026-09-11 from a direct #1687 close-out audit (same author, same denominator problem, folded in
rather than treated as new epics): `#1747` 'Tests' and 'E2E & AAXT' workflows are STANDING-RED —
outside #1687's own four-workflow denominator, so every subsequent "belt fully green" claim
(including this file's own ship-060 citations) silently meant "the five tracked," the exact m-44
shape #1687 itself documented · `#1748` CI test-isolation defect — tests write fake provider keys
into the shared per-job Postgres via #1382's DB store, conftest later loads one as real, turning
keyless behavior into live 401s that read as product failures · `#1749` a deterministic-looking
search test fails in CI only, passes locally, mechanism undiagnosed (env-divergence class).

**Why first**: every day CI stays red, every other epic's evidence weakens (a green suite means
less when four — now confirmed six — workflows are already known-broken). Cheap relative to its
value. If it turns out not-cheap, the fallback is explicitly accepting these as known-red rather
than let them silently discount every later epic's signal. **#1747 is itself an instance of that
fallback failing quietly** — the denominator drifted from four to six without anyone's "fully
green" claims noticing, which is exactly the m-44 risk this epic exists to retire.

### 2. Security/tenancy (6 items) — **CLOSED IN FULL 2026-09-12** — before beta wave 1, regardless of everything else
~~`#1734`~~ [SECURITY] personality API global-config clobber — **CLOSED**. ~~`#1690`~~ demo plugin
live-mounted by default in every prod deploy — **CLOSED**. ~~`#1732`~~ [SECURITY] chat-render XSS,
no sanitizer — **CLOSED**. ~~`#1733`~~ stale unauthenticated duplicate page — **CLOSED**.
~~`#1741`~~ pattern-suggestions XSS — **CLOSED**. ~~`#1740`~~ twin-file renderer drift —
**CLOSED**. All six live-verified deployed (v74/v76) per Lead's 2026-09-12 memo.

⚠️ **Two epic-2-class findings surfaced by the #1733 close-out sweep, deliberately NOT folded
in**: `#1750` (web/assets/standup.html, the last remaining stale-unauth twin, same class as
#1733) and `#1751` (the CANONICAL /personality-preferences page hardcodes user_id "default" in
its own fetch calls — #1733 had wrongly attributed this only to the deleted twin; real
multi-tenancy bug, adjacent to closed #1419/#1734, blast radius currently limited per the issue's
own read). Folding either into epic 2 would reopen a now-fully-closed epic per PM's rule, and
Lead is already moving on epic 3 — both parked at MVP milestone / Product Backlog status instead,
for a later pass or a small epic-2b if one becomes worth naming. Not urgent by either issue's own
severity read.

**Why here, non-negotiable**: this epic's position doesn't move for scheduling convenience even
half-closed.

**Two more findings folded in (2026-09-10), both surfaced fixing `#1732`, both matched to this
epic rather than filed standalone**: `#1741` [SECURITY] pattern-suggestions UI interpolates
unescaped into innerHTML, outside `#1732`'s chokepoint · `#1740` twin-file renderer drift (a dead
unserved copy of `bot-message-renderer.js` diverged from the live one) — folded here rather than
into false-trails since it's the exact same "fixing X surfaced Y in the same file" shape as
`#1741`, not a separate parallel-system finding.

⚠️ **Caution, not an alarm**: `#1637`/`#1732`/`#1734` closed Sprint Backlog → Done directly,
skipping In Progress (Exec's 09-10 finding — the board's In Progress count is not a reliable
in-flight signal; see the general note below). Reads as PM's verification round closing
already-fixed items, not a violation of one-epic-at-a-time — noting for accuracy, not flagging.

### 3. Acceptance contract (9 items) — freshest pain, design is DONE, unblocks a whole cluster
`#1739` (umbrella) · `#1663` · `#1652` · `#1653` · `#1654` · `#1694` · `#1696` · `#1596` · `#1752`
(found 2026-09-12 during #1654's own adoption — the soft-workflow-offer no-clobber guard doesn't
cover the STATE_QUESTION-survival re-arm path, a silent-drop shape adjacent to #1652's arm half).

**Why third**: PM's live round converged three failures onto this one contract today. Both design
passes are already in (Arch's sequencing ruling + CXO's two-axis correction, conceded by Arch) —
Lead builds against a finished spec, not an open question. Closing this epic unblocks the
reminder/standup UX cluster wholesale, per Arch's read.

**Spec address (2026-09-10)**: the user-facing contract consolidated from three separate memos
into one doc — `docs/internal/design/acceptance-contract-user-facing-2026-09-10.md`. Includes
CXO's arm-survival ruling (consent has a freshness property a draft offer doesn't; per-tier
survival policy feeds the DESTRUCTIVE-tier design). Cite that doc going forward, not the mail
thread.

### 4. Corpus/classifier deposits (6 items) — no dependency, pick up opportunistically
`#1505` `#1527` `#1559` `#1579` `#1606` `#1693`.

**Why here, not strictly ordered**: Arch's own note — these parallelize freely, cheap,
ratchet-governed gate-side deposits with no dependency on anything else in this list. Placed
fourth as a resting point, but if a fire has spare capacity before epic 3 closes and none of
these touch epic 3's files, pulling one is not a violation of "one epic at a time" — they're
independent by construction. If in doubt, finish the current epic first anyway.

### 5. Honest-empty / GatherOutcome (4 items) — lands after the acceptance-contract idiom proves out
`#1717` (the audit's own meta-evidence for this cousin) · `#1730` · `#1736` · `#1738` (shared with
Deliverable below).

**Why after epic 3, not before**: Arch's note — this is design-then-fix, and it benefits from the
acceptance contract proving the single-source-predicate idiom on a live seam first, rather than
inventing a second one in parallel.

✅ **User-facing contract owner named and delivered, ahead of the epic's own position** — CXO,
`docs/internal/design/gather-outcome-user-facing-contract-2026-09-09.md`, written the same day
this order was drafted rather than waiting for epic 5's turn (per Arch: *"cousin 1's aggregation
copy is CXO's user-facing contract, with the #1717 composition case as its acceptance test"* —
goes in the epic's own description verbatim when it's filed).

🔴 **CXO's read also corrects the epic's shape — this is not "add an aggregation rule."**
Aggregation for N-failed-slices already exists in ONE of two failure-reporting paths
(`orchestrator._combine_results`, deterministic string assembly) but not the other (the floor's
five `*_source_failed` directive sites, which the LLM composes freely). **The epic is "one noun,
two mechanisms" — thread `GatherOutcome` through the directive path without leaving the composed
path as a second, differently-honest voice.** CXO's own boundary: this is "two paths located" by
grep, not "two paths confirmed" — re-run the survey when scoping, don't inherit the count. Also:
Exec's live "I wasn't able to check" rider on a *succeeding* turn is a reportability defect
(content that had no business in that answer), not an aggregation defect — fixing aggregation
alone won't touch it; the site is unidentified.

⭐ **CXO's 09-10 framing on `#1738` — argues epics 5 and 6 share a rule, doesn't move either**:
`#1738` isn't a truncation bug, it's a provenance misattribution — the gather was `fresh` and
complete, the *renderer* dropped an item, and the assistant then described its own truncated
render as its evidence ("the list I got back"). Stated as a general rule now in the contract
(§5b, v0.2): a provenance value is a fact about the source and must survive rendering unchanged;
a render cap may shorten what the user sees, never what the system believes it has. Practical
consequence for whoever scopes this: "…and N more" is a claim the assistant must be able to cash —
if it can't name the N, the honest render is "6 archived; here are 5, ask for the rest," not a
silent truncation. CXO explicit: not proposing the fix, not re-ranking the epics.

### 6. Rendered deliverable (2 items + 2 shared with GatherOutcome/Security) — same reasoning as 5
`#1729` · shares `#1732` (security, **CLOSED**) and `#1738` (GatherOutcome).

**Why here**: same "prove the idiom first" logic as epic 5; MCP-path-first per the ratified scope
ruling, per Arch. **Same CXO flag applies** — name the copy-owner before scoping the fix.

**Joint invariant with epic 5, confirmed by Arch (2026-09-10)**: §5b's rule (provenance must
survive rendering unchanged; a render cap may shorten what the user sees, never what the system
believes it has) applies here too — the direction (not yet the build) is that the renderer
consumes the structured GatherOutcome and never becomes the model's own evidence about the world.
Fix design waits for this epic's turn; nothing jumps the queue.

### 7. False-trails / claimed-not-wired (3 items) — pre-existing epic, no stated urgency
`#1522` (the epic itself, PM-directed) · `#1735` · `#1678`.

### 8. Spatial-disposal (2 items) — pre-existing epic, no stated urgency
`#1698` (the epic itself, PM-ruled 08-15/16) · `#1700`.

### Singletons (6 items) — forcing these into groups would be taxonomy theater (Arch's framing)
`#1423` (silent-death pattern — genuinely its own epic-of-one) · `#1695` · `#1697` · `#1708` ·
`#1718` · `#1737`.

**Handling**: no group dependency to respect. Pick up opportunistically between epics, or fold
into whichever numbered epic above touches the same file if one turns out to overlap on
inspection — these were classified from titles, not full reads; PPM's own read of an individual
issue may reclassify it without changing the shape of the other 36.

**Cross-milestone note (2026-09-11)**: `#1718` is the audit's cousin #3 ("an error surfaced to a
user," half-modeled at a broken seam). `#1108` (Fast Follow, out of this file's MVP scope) is a
concrete second instance of the same cousin, per CXO — two OAuth error surfaces, one leaking a raw
slug, one recommending a retry that cannot work. **If `#1718` ever gets promoted from singleton to
a real scoped epic, cite `#1108` alongside it rather than fix either in isolation** — CXO's own
framing, not fixed here since it's a different milestone.

---

## The falsifiability note, carried from Arch's memo (why this ordering is checkable, not asserted)

10 of 37 map directly to the un-modeled-noun audit's cousins; the acceptance-contract control case
arguably makes it 18. The rest group under four pre-existing cause-epics. **If a future factoring
pass finds the singletons refusing to shrink, or an epic's membership turning out wrong on a full
read, that's real information — update this file, don't defend the original grouping.**

## Change log
- 2026-09-09 (PPM): first version, built from Arch's factoring + dependency notes + CXO's
  copy-contract flag. 37 items, 8 epics + 6 singletons.
- 2026-09-09 evening (PPM): epic 5 (GatherOutcome) updated — CXO's copy contract delivered ahead
  of schedule, and CXO's own read corrects the epic's shape from "add an aggregation rule" to
  "unify two existing mechanisms." Scope-guard chokepoint (open question in v1) now has a joint
  CIO+Arch design in progress — GH Action on merge-to-main, PPM named consumer for milestone-
  consistency flags delivered as mail, advisory-first for two weeks before any required check.
- 2026-09-10 (PPM): three items closed (`#1637`, `#1732`, `#1734`) across epics 1 and 2 — marked
  in place rather than removed, so the record shows what closed and when. Folded two new findings
  from fixing `#1732` into epic 2 (`#1740`, `#1741`) rather than filing them as unplaced
  singletons. Added CXO's provenance-vs-rendering framing to epic 5 (argues epics 5/6 share a
  rule; doesn't reorder either). **General note, not epic-specific**: Exec found the board's In
  Progress count is not a reliable in-flight signal — three closures this week went Sprint
  Backlog → Done directly, skipping it. Don't read a flat In Progress count as "nothing is
  moving" when checking this file against live board state. Also added epic 6's §5b pointer per
  Arch's ask, so both cousins carry the joint invariant rather than one.
- 2026-09-10 later (PPM): scope-guard status — both halves shipped
  (`scripts/scope-drift-check.sh`, `.github/workflows/scope-guard.yml`, still dispatch-only, not
  armed). Added a `verdict:` header slot to the memo template per CXO's catch (the promotion
  decision was riding a hand-kept tally, the one bolt-on left in an otherwise chokepoint-shaped
  design) — rate now reads from memo headers via grep, not a habit. Ran two `workflow_dispatch`
  tests (95 and 300 recent commits, both quiet/0-flagged) — verifies the predicate and quiet-run
  path fire correctly; does NOT yet verify the memo-delivery path, which hasn't fired in either
  test. Arms after `#1687` closes per the standing sequencing condition (epic 1, above).
- 2026-09-10 even later (PPM): Arch ran the real synthetic test (`#1744`, fixture issue,
  Blocked). **Predicate proven live** (1/1 flagged correctly). **Delivery half found broken**:
  `GITHUB_TOKEN` can't push to protected main (GH006) — Arch's retry loop had silently swallowed
  the push failure and reported SUCCESS with no memo delivered, a real false-clear. Fixed same-day
  (failed delivery now fails the run loudly). **The remaining decision is PM's**: bot needs either
  a branch-protection bypass grant or a scoped PAT secret — repo-settings change, not ours to make
  unilaterally. `#1744` stays open until the delivery path is actually observed working.
  **CXO also caught a real gap in my own verdict-slot fix**: the grep-count has no denominator, so
  it can't distinguish "zero flags occurred" from "flags occurred and never arrived" — exactly the
  state the bot-can't-push defect put us in. **Fix accepted, sequenced with arming** (a per-run
  ledger, `dev/active/scope-guard-runs.tsv`, one line per run whether quiet or flagging — not
  built yet, since it closes nothing before PM's decision lands anyway). **Not armed. Blocked on
  PM.**
- 2026-09-11 16:11 WORK (PPM): 3 unmilestoned issues triaged — `#1747`/`#1748`/`#1749`, all filed
  same-day from a direct #1687 close-out audit (same author). All stated "Milestone: MVP" in body
  but the field wasn't set; milestone set, added to board, Sprint=Beta Blockers/Status=Sprint
  Backlog matching #1687/#1711 precedent, verified no collateral damage. Folded into epic 1 as a
  continuation rather than new epics — `#1747` is a direct instance of the epic's own risk (the
  belt's tracked-workflow denominator silently drifted from four to six).
- 2026-09-12 10:09 WORK (PPM): epic 2 (Security/tenancy) closed in full — all 6 members done,
  live-verified deployed (Lead, v74/v76). Two epic-2-class follow-on findings (`#1750`, `#1751`)
  from the #1733 close-out sweep deliberately NOT folded in (would reopen a closed epic) — parked
  at MVP/Product Backlog instead. `#1752` (found during #1654's own epic-3 adoption) folded
  directly into epic 3, now 9 items. **Denominator question answered for Lead**: this file's own
  "37 Sprint Backlog items" provenance line (2026-09-09) was a board-Sprint-Backlog snapshot for
  epic-factoring purposes specifically, not a claim about the milestone-wide count — Lead's
  tracker headline should use milestone-wide (matches `sprint-truth.py`'s own convention, which
  this file and PPM's every-fire count both already use). No conflict; just two different
  denominators serving two different purposes, now stated explicitly so it doesn't drift again.
