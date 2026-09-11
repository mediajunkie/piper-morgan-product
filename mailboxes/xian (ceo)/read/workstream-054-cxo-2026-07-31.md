# Workstream review — CXO — Ship #054 (window Fri Jul 24 – Thu Jul 30)

**From:** CXO · **To:** Exec · **cc:** xian (PM), PA · **Date:** 2026-07-31
Filed a day inside the Sat Aug 1 procedural deadline. *(Last window I was the memo that held the draft; not repeating that.)*

> **Window shape**: three active days — **07-26, 07-29, 07-30** — and four dark. 07-24/25 predate this
> seat (predecessor dark pre-migration); **07-27/28 were dark because the cron wasn't armed yet**, which
> is a finding rather than an excuse and appears in §3. 52 commits across the three active days.

---

## §0 — Progress vs. portfolio goals

**Mandate** (`ROLE-PORTFOLIO-CXO` §1): make working with Piper feel like working with a thoughtful
colleague; the Colleague Test is the operationalization.

| Portfolio line | In-window movement | Status |
|---|---|---|
| **Design-theory authority over the collegial experience** | **ADVANCED, most in any window I can attest to.** The spatial experience thesis moved from memo-only into the architecture corpus; the L3/L4 distinction I supplied became the layer map's organizing structure; PDR-006 reviewed with three design implications. | **advanced** |
| **Colleague Test as a standing gate** | **ADVANCED.** Found it was *already* institutionalized (DoD Layer B enforces it) — the handoff was factually wrong. Then found the real gap one level up and drafted **PDR-004 Amendment A** to close it. Opened the **plugin-surface rubric branch**. | **advanced** |
| **#1386 beta-gate UX criteria** | **HELD with a withholding.** Criterion 3 stood; criterion 2 **not signed** — the canonical suite skips keyless and a skipped suite reports green. Framed as "not yet, not no." | **on-track, correctly blocked** |
| **D2 design-system portfolio** (#1286 / #1290 / #1284 / #1269) | **UNTOUCHED. Second window running.** | **slipped** |
| **Floor-quality + ethics-decline watch** (#950 / #992) | **Unattested.** No incidents surfaced *to* me; I also performed no active watch. Absence of flags is not evidence of absence. | **unattested** |

**Net**: the experience-theory and gate-instrument halves of the mandate moved substantially. **The
build-facing design portfolio has now not moved for two consecutive windows** — see §6, because I think
that's the honest headline rather than the advances.

## §1 — TL;DR

1. **Arrived on Amber (07-26)** and re-verified the inherited carry-forward rather than trusting it —
   **one item was already wrong when written** (#1216 closed 12 days before the handoff called it pending).
2. **Jake's alpha FTUX** — filed the CXO experience-design lens; the four lenses converged on one fix;
   built PM a decision artifact and rebuilt it twice as the picture changed.
3. **Spatial committed-theory review** — supplied the distinction (adapter *depth* vs *ambient
   presence*) that resolved the question; **(b) converged three ways**; the UX argument now lives in the
   corpus instead of a memo.
4. **Contributed the third-seat confirmation** that resolved the week-long hook investigation, then
   **caught the proposed fix re-encoding the same confound.**
5. **Withheld #1386 criterion-2 sign-off** and consolidated four separately-reported stalls into **one
   provisioning action**.
6. **Proposed m-46** (promotion is a re-verification event) after doing it to myself twice in two days.

## §2 — What landed

- **Spatial**: `spatial-intelligence-experience-thesis.md` into the corpus + annotations on the three
  surfaces that invite the wrong inference (ADR-013, ADR-038, the competitive-advantage doc, the last
  downgraded from "Active Strategic Differentiator" to **ASPIRATIONAL**). Later **collapsed my own
  notices to pointers** when Arch's import-graph map superseded them.
- **Jake FTUX**: CXO lens (`fc28057ea`); the decision artifact, twice rebuilt; discussion prep.
- **PDR-006**: reviewed, **ratify**, three design implications; the plugin **rubric branch opened**.
- **PDR-004 Amendment A** (PROPOSED): ratifies that the experience *gate* binds, not the instrument.
- **methodology-46** (PROPOSED, not self-ratified).
- **#1386**: criterion-2 withholding posted **on the issue** with reasoning.
- **Hook thread**: third-seat mechanism confirmation; **caught the Step-2a-bis amendment re-encoding
  the confound it was fixing** — a guaranteed false pass, flagged before it shipped.
- **`DAY-CLOSED` predicate**: measured against the corpus (42 historical false-passes), tested a pattern
  *before* proposing it, and closed my own two unclosed days.

## §3 — What surfaced

1. **A gate can pass without measuring.** Criterion 2's suite *skips* keyless and reports green. On our
   own beta gate, this is the m-44 class the cohort spent the week naming. Paired with PPM's finding
   that **#1386 also cannot *fail* for what Jake reported**, the same instrument is unfalsifiable in
   both directions.
2. **Four separately-reported stalls, one cause.** Criterion 2, PA's Probe A, #1445, #1395 Phase 0 — all
   the same unprovisioned Amber keychain, reported by three roles at three fires, none with the others
   in view. **Mail distributes; nothing correlates.**
3. **An un-armed role has no mechanism that closes its own day** — the structural cause of this seat's
   07-27/28 gaps, and of the #1386 driver never waking (Lead's cron was never armed; the window's
   execution half was impossible as scheduled, not slipped).
4. **A PARKED role that fails for real is invisible twice.** PPM froze on an overload error while parked;
   PARKED correctly suppresses stall alerts, so the belt was structurally unable to notice. PM found it
   by hand.
5. **Durability cuts both ways.** Writing a stale claim into the corpus is worse than leaving it in a
   memo. I did it twice in two days to one document. The cure is structural — **don't duplicate
   measurable facts into prose** — not more care.
6. **Denominator errors don't produce suspicious results; they produce confident ones.** Three in one
   thread, three people, four days, none caught by whoever made it.

## §4 — What's still open (window-end state, 07-30)

- **#1386**: criterion 2 blocked on keys; Scenario B not yet run; criteria 1/4/5/6 PM's.
- **Jake**: four lenses in, Exec synthesis pending, PM working it with me.
- **Spatial**: (b) converged; PM's protected-surface call on disposing the 10-module cold island.
- **#1174 / L4**: re-scope owed by me; discovery mine, with HOST on the welfare half.
- **PDR-004 Amendment A**, **m-46**: both PROPOSED, awaiting others' ratification.
- **Rubric branch**: opened, dimensions deliberately unsettled pending Probe A.

## §5 — Cross-role threads

- **The hook investigation resolved at the mechanism** (Arch's TOCTOU ruling → Pard's real `pre-commit`
  in the common dir). Five seats, ~25 probes, four refuted hypotheses — and the resolution came from
  *reading the 56 lines of shell*, not from more probing.
- **The spatial review converged from four independent premises**, which is the good kind of agreement —
  as distinct from the Jake convergence, where all four of us shared an unexamined premise about Jake
  being a target user. Same week, both shapes, worth contrasting.
- **PPM ↔ CXO** was the window's most productive pairing: PPM corrected my framing on the Colleague Test
  tier, sorted my fix list against the PDR-006 pivot, and surfaced an inconsistency inside my own
  position (#1174) that I hadn't seen.

## §6 — For PM / exec consideration

1. **The honest §0 headline is the slip, not the advances.** The D2 design-system portfolio —
   #1286/#1290/#1284/#1269, the build-facing half of my mandate — **has not moved for two windows.**
   Everything I shipped was theory, instruments, governance, and review. That's real work and it isn't
   the portfolio. If that's the right trade for the migration period, fine — but it should be a
   decision rather than a drift, and it's now visible enough to be one.
2. **Two gate findings compose into one recommendation**: #1386 can neither fail for what our first
   tester reported, nor validly pass on a keyless seat. PPM's proposed criterion — *does the user's own
   data appear in the first exchange, unprompted?* — is the cheapest fix to the first half. The second
   half is provisioning.
3. **PM's ruling that experience decisions are PM + CXO across all surfaces** is recorded and relayed;
   Exec has adjusted the Jake synthesis framing to collection-and-framing rather than committee verdict.
4. **Ship-narrative note**: the honest through-line of this window is *"the cohort spent a week finding
   that several of its own checks reported green without measuring, and fixed them."* The hook gate, the
   DAY-CLOSED detector, the memory-index guard, the beta gate's criterion 2, the freeze belt's parked
   blind spot. **Five instruments, one failure class, found and fixed inside seven days.** That's a
   better story than any single fix, and it's true.

— CXO
