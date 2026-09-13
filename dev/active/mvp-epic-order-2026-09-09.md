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

### 1. CI/infra red (8 items, 4 closed) — cheap, and it's a quiet tax on every epic after it
`#1687` four CI workflows standing red · ~~`#1711`~~ Keychain ACL hang blocks server startup
silently — **CLOSED**. ~~`#1637`~~ 6 standing test failures poisoning 6 — **CLOSED 2026-09-09/10**.
Plus, filed 2026-09-11 from a direct #1687 close-out audit (same author, same denominator problem,
folded in rather than treated as new epics): `#1747` 'Tests' and 'E2E & AAXT' workflows are
STANDING-RED — outside #1687's own four-workflow denominator, so every subsequent "belt fully
green" claim (including this file's own ship-060 citations) silently meant "the five tracked," the
exact m-44 shape #1687 itself documented · ~~`#1748`~~ CI test-isolation defect — tests write fake
provider keys into the shared per-job Postgres via #1382's DB store, conftest later loads one as
real, turning keyless behavior into live 401s that read as product failures — **CLOSED**. ·
~~`#1749`~~ a deterministic-looking search test fails in CI only, passes locally, mechanism
undiagnosed (env-divergence class) — **CLOSED**. Plus, folded 2026-09-12, both found by the #1748
lane: `#1764` (`EncryptedDBCredentialStore` silently collapses `service_name`, dropping the
namespace dimension the OS-keychain contract has — latent today, needs a migration plan if ever
fixed) · `#1765` (2 `test_cross_user_isolation.py` failures reproduce locally on pristine HEAD but
the Tests workflow is green — #1749's env-divergence class, inverted: local-red/CI-green instead of
local-green/CI-red). **Remaining open: `#1687`, `#1747`, `#1764`, `#1765`** — `#1687`'s secret
rotation comment is posted (2026-09-13), awaiting PM's ~3-minute action to actually unblock it.

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

### 3. Acceptance contract (11 items, 8 closed) — freshest pain, design is DONE, unblocks a whole cluster
`#1739` (umbrella, open) · ~~`#1663`~~ · ~~`#1652`~~ · ~~`#1653`~~ · ~~`#1654`~~ · ~~`#1694`~~ ·
~~`#1696`~~ · ~~`#1596`~~ (all six **CLOSED**, per Lead's session log — the epic ran to its floor
Saturday) · ~~`#1752`~~
(found 2026-09-12 during #1654's own adoption — the soft-workflow-offer no-clobber guard doesn't
cover the STATE_QUESTION-survival re-arm path, a silent-drop shape adjacent to #1652's arm half;
**turned out to be an accidental duplicate of the already-fixed #1753 — closed, net zero change
here**) · `#1771` (found 2026-09-12 during #1769's adoption, the sixth contract adoption — the
shared decline vocabulary folds "maybe later"-class deferrals into DECLINE, which is harmless at
most seams but abandons the resumable flow at the resume-offer seam) · `#1695` (moved here from
Singletons 2026-09-12 — compose-framed draft can arm a subject still carrying the bare repo phrase
because the collaborate-gate ARM path doesn't resolve it, only the execute/file path does; same
arm/consume-rail family as the rest of this epic). **Remaining open: `#1739` (umbrella, closes when
its children do), `#1771`, `#1695`** — per Exec's 09-13 accounting, `#1739`'s last real dependency
is PM's own `#1617` standup retest (~90 seconds), which is what actually unblocks this epic's floor.

**Why third**: PM's live round converged three failures onto this one contract today. Both design
passes are already in (Arch's sequencing ruling + CXO's two-axis correction, conceded by Arch) —
Lead builds against a finished spec, not an open question. Closing this epic unblocks the
reminder/standup UX cluster wholesale, per Arch's read.

**Spec address (2026-09-10)**: the user-facing contract consolidated from three separate memos
into one doc — `docs/internal/design/acceptance-contract-user-facing-2026-09-10.md`. Includes
CXO's arm-survival ruling (consent has a freshness property a draft offer doesn't; per-tier
survival policy feeds the DESTRUCTIVE-tier design). Cite that doc going forward, not the mail
thread.

### 4. Corpus/classifier deposits (9 items) — no dependency, pick up opportunistically
`#1505` `#1527` `#1559` `#1579` `#1606` `#1693`. Plus, folded 2026-09-12 (same audit family,
found by agent lanes working these very items): `#1755` (multi-intent path suppresses a genuine
temporal ask when a connect ask rides the same message, found during #1505) · `#1756` (read-lane
pre-classifier patterns claim destructive delete asks, an #1527 sibling) · `#1757` (portfolio
archive/hide/restore patterns carry the same unguarded greedy capture #1527 fixed for delete,
another sibling).

**Why here, not strictly ordered**: Arch's own note — these parallelize freely, cheap,
ratchet-governed gate-side deposits with no dependency on anything else in this list. Placed
fourth as a resting point, but if a fire has spare capacity before epic 3 closes and none of
these touch epic 3's files, pulling one is not a violation of "one epic at a time" — they're
independent by construction. If in doubt, finish the current epic first anyway.

### 5. Honest-empty / GatherOutcome (14 items, 8 closed) — lands after the acceptance-contract idiom proves out
~~`#1717`~~ (the audit's own meta-evidence for this cousin — **CLOSED**, scored 4/4 by CXO 09-12)
· ~~`#1730`~~ · ~~`#1736`~~ · ~~`#1738`~~ (shared with Deliverable below — all three **CLOSED**).
Plus, folded 2026-09-12: ~~`#1754`~~ (ConversationHandler clarify/chitchat lane unreachable,
independent same-day finding overlapping `#1759` — see that item's note — **CLOSED**, per Arch's
GO) · ~~`#1759`~~ (dead clarify-carrier machinery, found during #1730's own diagnosis — disposed
per Lead's #1730 Gap-2 proposal + Arch's same-day concurrence — **CLOSED/DELETED**) · `#1760`
(test-theatre mock mismatch, found via #1736) · `#1761` (consumer_core.py fabricates "No
description available," self-identified honest-empty candidate) · `#1763` (get_project_status
rider-failure evidence, tied to #1738) · ~~`#1767`~~ (dead file-disambiguation state on
`ConversationSession`, found during the #1759 deletion sweep, zero live referents — **CLOSED**,
per Arch's GO) · ~~`#1768`~~ (`classify_conscious` zero-caller dead code, residual from #1759's own
deletion — **CLOSED**, per Arch's GO-conditional). Plus, moved
here from Singletons 2026-09-12: `#1697` (files.html renders blank "Uploaded by:" because the live
API response has no `owner_id` field — a rendering-a-missing-field defect, same family as #1736/
#1761's fabricated-absence class, inverted: blank instead of a fabricated placeholder) · `#1718`
(BYOC key validation discards the failure reason, showing flat "invalid" for both auth errors and
quota/billing errors — already framed in this file as the audit's error-surfacing cousin #3,
alongside Fast Follow's `#1108`) · `#1772` (N=1 degrade reply named three unarmed sources, found
during #1717's own scoring — a scope-directive leak at the delivered layer). **Remaining open:
`#1760`, `#1761`, `#1763`, `#1697`, `#1718`, `#1772`** (6 of 14) — this epic is currently the one
Lead is actively working, per their own log (opened right after epic 3 hit its floor Saturday).

**#1717 status (2026-09-12)**: code-done and live on v86 — awaits one harness re-run + CXO's voice
read against the contract's §6 acceptance test (item 1, the composition case). CXO's call, not
PPM's; noting here for tracking only.

**#1730 status (2026-09-12)**: Gap 1 evidence-complete. Gap 2's structural ruling landed same-day —
Lead proposed "ask-only-when-armed as an invariant" (option 3), Arch concurred with one condition
(the enforcement table's site census must be mechanical, not hand-maintained). #1759 (above) is
disposed as part of this ruling. Tracked here; the actual ruling and enforcement-table work is
Lead/Arch's.

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

### 6. Rendered deliverable (3 items + 2 shared with GatherOutcome/Security) — same reasoning as 5
`#1729` · shares `#1732` (security, **CLOSED**) and `#1738` (GatherOutcome). Plus, folded
2026-09-12: `#1762` (render-truncation sweep, ~18 more "...and N more" sites, self-identified as
#1738's class / epic-6 threading).

**Why here**: same "prove the idiom first" logic as epic 5; MCP-path-first per the ratified scope
ruling, per Arch. **Same CXO flag applies** — name the copy-owner before scoping the fix.

**Joint invariant with epic 5, confirmed by Arch (2026-09-10)**: §5b's rule (provenance must
survive rendering unchanged; a render cap may shorten what the user sees, never what the system
believes it has) applies here too — the direction (not yet the build) is that the renderer
consumes the structured GatherOutcome and never becomes the model's own evidence about the world.
Fix design waits for this epic's turn; nothing jumps the queue.

### 7. False-trails / claimed-not-wired (4 items) — pre-existing epic, no stated urgency
`#1522` (the epic itself, PM-directed) · `#1735` · `#1678` · `#1708` (moved here from Singletons
2026-09-12 — `ALPHA_QUICKSTART.md`, the tester-facing onboarding doc, tells testers to clone a
branch 7,614 commits stale and describes the live hosted app as a future plan; a claimed-state vs.
actual-state mismatch on a first-contact surface, the exact false-trails shape).

### 8. Spatial-disposal (2 items) — pre-existing epic, no stated urgency
`#1698` (the epic itself, PM-ruled 08-15/16) · `#1700`.

### 9. Silent-death inventory (3 items, 2 closed) — genuinely its own epic, not a forced grouping
`#1423` (the inventory-and-un-swallow task, open) — broad try/except on core paths converts broken
features into invisible defaults. ~~`#1420`~~/~~`#1422`~~ (the two confirmed instances #1423 names,
both already fixed and closed — neither was ever surfaced to a user because the pattern's whole
effect is that they can't). **Item count corrected 2026-09-13** — Exec's own epic-accounting read
(`dev/active/epic-accounting-2026-09-13.html`) counted all three where this file had only listed
`#1423`; the fuller count is right, since #1420/#1422 are the concrete instances the inventory
exists to cover, not incidental mentions. **Why its own epic**: this shares no real membership with
any epic
above — it's an inventory-and-un-swallow task at the exception-handling layer, not a rendering,
security, or contract-adoption concern. Arch's original framing ("genuinely its own epic-of-one")
was correct when written; PM's 2026-09-12 ruling (relayed via Janus — every MVP item needs an epic
home, singleton or not) makes it official rather than parking it in an unordered pile.

### 10. Composer UX polish (1 item) — genuinely its own epic, PM's own live feedback
`#1737` — the web chat composer ticker-tapes horizontally instead of growing vertically as PM
types a longer message, so only the tail of what was typed stays visible. **Why its own epic**:
pure frontend UX, no shared surface with anything else in this file. Kept in MVP rather than moved
out — PM reported it live as direct usability friction on the primary chat surface, which reads as
gating rather than deferrable polish; if that reading is wrong, this is the file's cheapest possible
correction (move one item's milestone).

---

**Retired 2026-09-12**: the old "Singletons" section (`#1423`/`#1695`/`#1697`/`#1708`/`#1718`/
`#1737`) is gone. Per PM's ruling (relayed via Janus, 2026-09-12 evening): discovered work is fine,
but every MVP item needs an epic home — a singleton pile outside the epic-relative view was
invisible to the instrument PM actually reads. Four of six had genuine homes in existing epics
(`#1695`→3, `#1697`/`#1718`→5, `#1708`→7); two (`#1423`, `#1737`) genuinely share no membership with
anything else and got their own epics (9, 10) rather than a forced fit. The cross-milestone note
on `#1718`/`#1108` carries forward into epic 5's entry above.

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
- 2026-09-12 13:09 WORK (PPM): 10 unmilestoned issues triaged, all folded into already-open epics
  (none reopened): `#1755`/`#1756`/`#1757` → epic 4 (now 9 items, classifier-audit siblings of
  #1505/#1527); `#1754`/`#1759`/`#1760`/`#1761`/`#1763` → epic 5 (now 9 items — #1754/#1759 are
  independent same-day findings of the same ConversationHandler dead-code shape, #1759's
  disposition already ruled DELETE per Lead/Arch's same-day #1730 Gap-2 concurrence); `#1762` →
  epic 6 (now 3+2 shared items). Also closed `#1166` (Type-2 Dreaming three-way convergence,
  CXO/PPM/Arch, done since 2026-06-08) — corrected the stale `roadmap.md` Dreams row in the same
  pass (had read "spec-read pending" for three months after convergence landed). Recorded #1717
  and #1730's same-day status for tracking (both are CXO's and Lead/Arch's calls respectively,
  not PPM's — noted here only so the file stays accurate).
- 2026-09-12 16:09 WORK (PPM): 5 more unmilestoned issues triaged (0→5 in one fire, all filed
  today from Lead's lanes) — `#1764`/`#1765` → epic 1 (both #1748-lane findings, #1765 is #1749's
  env-divergence class inverted); `#1767`/`#1768` → epic 5 (dead-code siblings of #1759, same
  deletion sweep); `#1771` → epic 3 (found during #1769's own adoption — #1769 itself was already
  closed+milestoned by Lead before this fire, net epic-3 change is +1 not +2). Verified against
  #1748 as a known-good control — no collateral damage. **Ratified Exec's filing-convention
  extension** (flagged same-day): new issues get Product Backlog status AND a milestone at filing
  time, not just Status — "unset" should not be a reachable state for either field. Lead will fold
  this into lane briefs the same day. This is the third time this week unmilestoned drift has hit
  double digits across a few fires; the ratification is meant to close the gap at the source
  rather than keep relying on per-fire triage to catch it.
- 2026-09-12 19:09 WORK (PPM): PM ruling relayed via Janus — discovered-work triage into epics is
  "clear and welcome," but every MVP item needs an epic home, no exceptions. Retired the
  Singletons section: `#1695`→epic 3, `#1697`/`#1718`→epic 5, `#1708`→epic 7 (real membership
  fits, found on full reads rather than the original title-only classification). `#1423`/`#1737`
  got their own new epics (9, 10) since neither shares real membership with anything — same
  standard the file has used all along (an honest epic-of-one beats a forced fit), just now
  applied to the last two holdouts instead of parking them unordered. Also fixed `#1772` (had MVP
  milestone but was missing from the project board entirely — filing with `--milestone` doesn't
  board-add, a new drift shape sprint-truth.py's "not on the board" check just caught for the
  first time) and folded it into epic 5. Noted Lead's three Rule-0 delete proposals (`#1754`/
  `#1767`/`#1768`) and Arch's GO/GO/GO-conditional rulings for tracking — Lead/Arch's call, not
  PPM's, no epic-order change needed since deletion doesn't move milestone membership.
- 2026-09-13 09:58 START (PPM): Exec published an epic-accounting doc for PM
  (`dev/active/epic-accounting-2026-09-13.html`), computed live from the GitHub API. Caught and
  corrected one real gap in it (missing epic 10 entirely — flagged to Exec/PM) and adopted one
  real improvement to this file (epic 9's item count was undercounting its own two named
  instances, `#1420`/`#1422` — now 3 items, matching Exec's fuller read). While cross-checking,
  refreshed live-closure state across epics 1, 3, and 5 (many items closed since last night:
  epic 1 now 4 closed of 8, epic 3 ran to its floor — 8 of 11 closed, only the umbrella + 2 stay
  open — epic 5 is 8 of 14 closed and is the epic Lead is now actively working). Also confirmed
  Lead posted the #1687 secret-rotation comment PM was waiting on — the WATCH FOR line in
  tonight's cron prompt can drop once PM actually does the ~3-minute rotation.
