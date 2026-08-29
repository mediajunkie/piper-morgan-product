# MVP triage cut — assembled for PM's one-sitting ruling

**✅ CLOSED 2026-08-28 ~16:2x PT.** PM ruled on all five same day (recorded as comments on each
issue): #1658 → PUB, #1661 → PUB (+ Lead's live-v63 carve-out check on the just-uploaded case),
#1662 → post-beta (PPM's original call confirmed — Lead's mid-sitting close+delete recommendation
was wrong, a pre-deletion sweep proved a live consumer, correction recorded on the issue), #1647 →
post-beta, #1436 epic → post-beta (PPM's split preserved: the mypy gate stays live/green, live
defects judged individually). **Board mechanics complete**: all five moved to Production milestone
(the standing MVP-cut disposition rule), #1658/#1661 set to Sprint "PUB - Public Beta". **Found
and fixed a bigger gap doing it**: 4 of the 5 issues were never on the project board at all (not
just missing a Sprint value) — added via `gh project item-add`, Status set to Product Backlog.
Verified via `assign-sprint-safely`'s procedure throughout (per-item mutation only, option-list
count confirmed unchanged before/after).

**⚠️ NOT fully end-to-end closed as of 22:2x PT** — three real threads still open, named honestly
rather than let the ✅ above read as final:
- **#1638 RULED same night (Arch, 22:0x): DISPOSE**, same shape as #1633/#1642/#1663/#1684 — zero
  production callers found across direct/dynamic/config-driven lookup, "fold into the cut as drops
  out entirely." **Execution (the actual `delete-module-safely` sweep) not yet done** — routed to
  Lead, not urgent tonight.
- **#1677/#1488 deliberately NOT closed** (Lead, 22:0x) — fix is built/merged/deployed in v64 but
  the flag is OFF; no live-behavior evidence yet. Named trigger: PM flips it at tomorrow's test
  round, clean live routing closes both same-session with checkboxes annotated description-first.
  This is completion discipline working correctly, not a stall.
- **#1522 needs a fresh scan before delegation** (Lead, 22:0x) — the "3/9/5 families" framing is 10
  days old and at least one named family was already resolved by v62–64 work. Lead's own lane will
  re-scan with the issue as hypotheses to verify, not facts to execute — queued behind tomorrow's
  test round.

MVP converges by deploy-verify on what remains, plus these three threads closing in their own time.

**Prepared by**: Lead (engineering read) + PPM (sprint/milestone call + roadmap coherence).
**Date**: 2026-08-28. **For**: PM's ruling, per the 08-25 priority-3 decision ("prepare with PPM
this week, PM rules in one sitting, Docs/Exec briefed same pass").

**Denominator**: `MVP: 61 not done (15 Sprint Backlog, 3 In Progress, 27 In Review + 16 not on the
board); 1075 done.` — `sprint-truth.py`, run fresh 2026-08-28 at assembly. Lead's engineering read
was built against 60 (live pull 08-27 16:0x) — the one-item drift is normal churn over ~17 hours,
not a discrepancy to chase; the classification below stands regardless of the exact total.

**Both gates that were blocking this cut are resolved**: FTUX (CXO, 08-21) and BYOC Position 1
(PA, 08-26 — the "no matter what" core list was deliberately designed to survive either BYOC
answer, so nothing below needed re-deriving once Position 1 landed, only confirming).

**Source**: Lead's engineering read, `dev/active/mvp-triage-engineering-read-2026-08-28.md` — its
method caveats apply throughout (commit-mention is a proxy for touched-by-the-record, not proof of
build state; two things Lead could not determine are named, not guessed, in its own §"What I could
not determine").

**Core list** (the "no matter what" core, from Lead's 08-18 strategic brief §3): (1) consent/trust
architecture, (2) honesty discipline, (3) PM-operation grammar (the 62 ops), (4) working-state
model + Radar, (5) synthesis direction. Explicitly NOT core: NL parser, floor's prose
improvisation, chat container itself, per-phrasing patches.

---

## How to read this

Three verdicts only: **MVP-keep** (stays, no triage action) · **PUB** (moves to the Public Beta
sprint — needed before general availability, not before private beta) · **post-beta** (ships with
an honest known-issue label, or moves to Production/backlog). A fourth marker, **blocked**, means I
did not force a premature classification — something else has to resolve first.

**Where I pushed back on or sharpened Lead's read, I say so explicitly** — per the agreed split,
Lead's core-list column is "the column PPM should push back on," and for several Group D items I
read the actual issue body rather than the one-line summary and landed somewhere more specific
than "clearest cut candidates."

## Group A — staged, awaiting deploy+verify (12 items) — NOT A CUT DECISION

`#1654 #1648 #1625 #1649 #1650 #1651 #1631 #1632 #1628 #1623 #1617`

**Agree with Lead: these are not triage candidates.** Built, merged, test-pinned, core-list YES
(honesty/consent). They converge via the deploy-and-verify round already in motion, not via this
cut. **No PM decision needed here** — listed for completeness of the denominator only.

## Group B — security/correctness (6 items) — MVP-KEEP, no realistic cut

`#1578 #1581 #1501 #1493 #1548 #1545 #1472`

**Agree with Lead in full.** This is the "without which we have built nothing of coherent value"
tier verbatim. If any single one needs to move, that should be a named, explicit PM decision with
a known-issue label — never a default of this triage pass.

## Group C — Inversion arc — MVP-KEEP as a block, one item needs a SEPARATE PM decision

`#1595` (epic, In Progress) · `#1663` (RULED) · `#1527` · `#1579 #1559 #1606` (corpus, parked) ·
`#1596`

**Agree with Lead's framing**: the epic and its corpus-parked dependents are MVP-keep as a single
line, not item-by-item — they converge when the Inversion's own waves land, and the corpus items
are deposits, not backlog.

**`#1677` / `#1488` — UPDATE 08-28 10:2x, resolved, drops out of the sitting entirely.** This
section originally pulled the pair out of the blanket call as "MVP-keep, but a separate fix-
approach decision, not a scope decision — recommend PM rules on it separately." **That decision
already happened between assembly and this update**: PM approved option (d) the same morning
(allowlisted write flip, `FLIP_WRITE_ALLOWLIST = {"create_todo"}`), Arch's mechanism followed
exactly, built and merged — verified directly on both issues (`gh issue view`), not taken from
Lead's ack alone. **MVP-keep stands, zero open questions remain on this pair.** One fewer decision
for PM's sitting than the original assembly implied.

## Group D — the six untouched-by-the-record items — SPLIT, not a uniform "clearest cut"

`#1662 #1658 #1653 #1652 #1638 #1613`

Lead's framing was "this is where the cut has the most room." **I read all six bodies directly
before classifying** rather than relying on titles, and three of the six turned out to be
core-list-touching once read — worth naming plainly since it's the opposite of what the group
label implied, and it's exactly the kind of check this whole process exists to run.

- **`#1662`** (upload writability probe printed nothing on v60) — diagnostic/instrumentation only,
  the underlying bug (#1656) already shipped. **post-beta.**
- **`#1658`** (PROTOTYPE PARITY: chat-side file upload / drag-drop) — Lead's read holds: a
  product-scoping umbrella PM routed to PPM, not a specific defect. Parity/completeness, not
  core-list. **PUB.**
- **`#1653`** (confirm-greed residue — echo-answers like "yes, delete them" now re-ask instead of
  firing) — read the body: this is a bug in the confirm-verb-matching logic, safe-direction
  (over-cautious, not under-cautious) but it directly touches the consent/confirm mechanism.
  **MVP-keep** — core-list touching, low severity but the core list doesn't have a severity floor.
- **`#1652`** (offer-flag gap — standup invitation/mode read-back clobberable by a soft-offer race)
  — read the body: state-management bug in the same consent/intent-data family as #1653.
  **MVP-keep**, same reasoning.
- **`#1638`** (TemplateRenderer family — fix-or-delete, awaits Arch ruling) — **blocked.** Not
  classifying until Arch rules complete-the-wiring vs. delete; forcing a verdict now would be
  guessing at an architecture call that isn't mine or PPM's to make.
- **`#1613`** (dead code implementing the exact cross-user pooling our privacy claims disclaim) —
  read the body: currently dead/unreachable, but it directly contradicts a stated privacy claim,
  which is honesty-discipline core territory even though inert. Given it reads as a small,
  contained fix (delete or neutralize the dead path), the cost of keeping it in MVP is low and the
  cost of a "we said X, our own code does Y" discovery later is not. **MVP-keep.**

**Net effect vs. Lead's headline**: of Group D's six, **2 move out (post-beta, PUB), 3 stay
(MVP-keep), 1 is blocked-not-classified** — smaller than "clearest cut candidates" implied for the
whole group, because three items read differently once their bodies were read rather than their
titles.

## Group E — file/document family — mostly PUB/post-beta, TWO pulled to MVP-keep

`#1656 #1657 #1624` (shipped) · `#1659 #1660 #1661` (residues)

**Shipped items — not a cut decision**, same as Group A.

- **`#1659`** (non-PDF uploads unsummarizable — "unable to analyze PDF" on a .txt) — **agree with
  Lead: MVP-keep.** A wrong answer presented as correct is fabrication-class, not a missing
  feature.
- **`#1660`** (detailed summaries render an empty Key Findings section — `analyze()` always leaves
  `recommendations` empty, but the handler reads it anyway) — **pulled up to MVP-keep, extending
  Lead's read rather than accepting his implied PUB-by-default.** Read the body: this is the same
  wrong-empty class as #1659 — a section silently renders empty when the underlying method never
  populates it, which is exactly the "verified-empty vs never-looked" honesty-discipline pattern
  from the core list, not cosmetic polish.
- **`#1661`** (temporal file references cap at 7 days — aged documents get the honest-empty reply
  while the Files page lists them) — **PUB / post-beta with known-issue label.** The issue's own
  title says "honest-empty reply" — this is NOT a fabrication bug, it's a real capability limit
  with a confusing UI mismatch (Files page implies availability the search doesn't provide).
  Already flagged in #1657 as "deliberately left for its own decision" — this triage confirms that
  scoping rather than overriding it.

## Group F — infrastructure/process (9 items, + #1662 already covered under D)

`#1436 #1423 #1637 #1647 #1646 #1645 #1676 #1678`

Lead's lean: keep the instrument-quality items (#1637, #1676, #1678), the rest can move. **Checked
all nine titles directly rather than accepting the lean uncross-examined** — landed on a broader
MVP-keep set than Lead's lean, because several read as honesty-discipline violations once seen in
full, not just "instrument quality":

- **`#1423`** (silent-death: broad try/except converts broken features into invisible defaults) —
  **MVP-keep.** This is the honesty-discipline pattern almost verbatim — "broken feature reads as
  a working default" is the exact failure class the core list names.
- **`#1637`** (tests/intent: 6 standing failures, poisons 6 more when run combined) — **agree with
  Lead: MVP-keep.** Broken test coverage is the instrument-quality failure this month has hit
  repeatedly.
- **`#1645`** (projects lane has no true total and no source-failed state distinct from
  never-gathered) — **MVP-keep, added to Lead's list.** This is the "verified-empty vs
  never-looked" pattern by name, applied to a different lane than the one the core-list examples
  usually cite — same defect class, not a new one.
- **`#1646`** (ANALYSIS handlers resolve a repo but `get_recent_activity` never receives it —
  analysis runs against the *configured* repo while *naming* the *resolved* one) — **MVP-keep,
  added to Lead's list.** The output is silently wrong about what it analyzed — fabrication-
  adjacent, not a code-quality nit.
- **`#1676`** (canonical retest doesn't record serving provider/model, confounding routing-flip
  diagnosis) — **agree with Lead: MVP-keep.** Directly affects whether we can trust our own #1386
  gate numbers.
- **`#1678`** (PIPER.md content never reaches the system prompt — loader extracts section names the
  file no longer has) — **agree with Lead: MVP-keep.** User-configured personalization silently
  does nothing; a real, invisible, user-facing failure.
- **`#1436`** (mypy CI gate, 1,060 errors enumerated, ~30 verified defects, 12+ live) — **split
  call, not a blanket one.** The full 1,060-error gate is too large for MVP as a unit. Recommend
  **post-beta for the gate itself**, but the **~12+ live verified defects (Census B) should be
  triaged as their own small set** rather than riding the whole issue's fate — I don't have
  Lead's per-defect list to classify those individually in this pass; flagging as a follow-up
  rather than guessing.
- **`#1647`** (pre-commit hook blocks unconditionally instead of warning, contra its own header) —
  **post-beta.** Dev-tooling-internal, not user-facing, doesn't touch the core list.

## Roadmap coherence check (my half of PM's condition to PA)

Cross-referenced this cut against the week's other live threads — nothing here conflicts:
- **Slack descope** (PM-ratified 08-27, Production→Fast Follow): none of the 60/61 MVP items above
  are Slack-specific; no correction needed.
- **#829/#1462 reconciliation** (closed 08-27): Production-milestone, doesn't intersect this MVP
  set.
- **FTUX surface mapping v0.1** (CXO, 08-28, still awaiting my consult separately): no MVP item
  above is gated on that consult landing first.

## Summary table for the sitting

| Verdict | Items | Count |
|---|---|---|
| **Not a cut decision** (staged/shipped, converges via deploy-verify) | Group A (12) + #1656/#1657/#1624 (3) | 15 |
| **MVP-keep** (Group B + C-block + specific D/E/F items, incl. #1677/#1488 now fully resolved) | B (6) + C-block incl. #1677/#1488 (8) + D (#1653,#1652,#1613) + E (#1659,#1660) + F (#1423,#1637,#1645,#1646,#1676,#1678) | 27 |
| **PUB** | #1658, #1661 | 2 |
| **post-beta** | #1662, #1647, #1436 (gate itself; live defects TBD) | 3 |
| **blocked** (awaiting Arch ruling) | #1638 | 1 |

Totals don't sum to exactly 61 — Group A's 12 + Group F's #1662 overlap, and the live-drift noted
at top (60→61) accounts for the rest. Not reconciling to the digit; the classification is what
matters for the ruling.

**UPDATE 08-28 10:2x (Lead's ack + independently verified)**: #1677/#1488's fix-approach question
is resolved — PM approved option (d) same morning, built and merged, verified directly on both
issues rather than taken on Lead's word alone. **The sitting is now simpler than originally
assembled: 5 items move out of MVP** (#1658, #1661 → PUB; #1662, #1647, #1436's gate →
post-beta), **1 is blocked on Arch** (#1638), **zero fix-approach questions remain.** Lead has
read this document and endorses it as-is, including the Group D corrections.

**The actual convergence lever, corrected from Lead's original headline**: not "~10 items" — 5.
Smaller than the initial estimate, because reading the actual issue bodies moved several from
"looks cuttable" to "touches the core" — reported here rather than the more convergence-flattering
original number.

— PPM, 2026-08-28
