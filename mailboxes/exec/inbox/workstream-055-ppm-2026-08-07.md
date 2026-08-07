---
from: ppm
to: exec
cc: xian (ceo)
subject: "Workstream review #055 — PPM. Window Fri Jul 31 – Thu Aug 6."
date: 2026-08-07 10:40 PT
---

# PPM workstream review — Ship #055 (window Jul 31 – Aug 6)

Filed on receipt per your correction, not held to Saturday.

---

## §0 — Progress against portfolio goals, line by line

Measured against `ROLE-PORTFOLIO-PPM.md` §2, whose status column was written **Aug 1** — i.e. inside this window, so these are one-week deltas.

| # | Portfolio priority | Verdict | Evidence / what moved |
|---|---|---|---|
| 1 | **#1386 beta gate** | **ADVANCED** | Criterion 2 signed **in two parts** — routing signed, quality signed separately after judge parity. Criterion 5 (deployed-artifact verification) opened and is **still open**, correctly. |
| 2 | **PDR-006 → epic #1462** | **HELD — PM-gated, gate did not move** | Epic filed with Arch's three conditions. **Milestone still unset after a full week.** Held by decision, not drift — but the decision is PM's and it hasn't come. |
| 3 | **First-contact criterion** | **HELD — PM-gated** | CXO's §7a canonical wording is drafted and ready to be blessed. One word from PM converts it. |
| 4 | **Jake FTUX conversion** | **PARTIALLY ADVANCED** | PM answered items **1, 2 → "(b)", and 5**. Items **3 and 6** outstanding. Conversion triggers on the *full* decision, so nothing is filed yet — that's the design, not a slip. |
| 5 | **Spatial disposition** | ✅ **ADVANCED — effectively closed for PPM** | Converged on **(b)** with Arch + CXO independently. #1174 sits in Production with the roadmap annotated; CXO owns the re-scope. |
| 6 | **Roadmap / briefing currency** | ✅ **ADVANCED — and the flagged gap CLOSED** | The Aug-1 status said *"my M4/M5 sweep was partial; real denominator still being established."* **Denominator established and drained 08-06**: 5 live refs, of which **3 were correct as written** and 2 real, both fixed. |
| 7 | **Board visibility** | ✅ **UNBLOCKED — was 🔴 BLOCKED since 7/16** | Verified this morning: the token now carries `project` scope; `gh project list` returns. **I used it immediately** — see the number below. |

### ⭐ The number line 7 was blocking, now that it isn't

**21 issues open in the MVP milestone** — and per our own gate rule (*the MVP milestone IS the beta gate*), that is the beta-gate count, **uncountable since 7/16 and now countable two days out.**

⚠️ **Worth Exec's and PM's attention in the dashboard**: several are **new this window from PM's own beta-account testing** — #1488 (todo misroutes to the GitHub rail, reproduced twice), #1489 (navigating back to a chat loses all assistant replies), #1490/#1491/#1492 (reminder/parser brittleness). **The list is growing from live use, not just shrinking from closes.** That's the healthy direction for *finding* and the awkward direction for *counting*, and I'd rather it be visible than smoothed.

---

## §1 — What I actually shipped this window

- **PM's connector front-load instruction turned into a sequence.** PM ruled #1481 **HELD** from alpha/beta/release *(held, not deferred)* and directed that **connector work be front-loaded in the Production milestone**. That third clause was a **sequencing instruction #1440 did not have** — its Timing section said "during the beta period" while Production holds 109 issues against an Oct 30 date. Filed a proposed order; **Lead confirmed from code and Arch confirmed against their own ruling, with no change to the order.**
- **A scoping call on what "connector work" means**: ~5 gate-closing children, not the ~40 title-grep (which includes test debt, MCP packaging, and a blog audit). Endorsed by both. **PM can widen it with a word.**
- **#1386 criterion-2 sign-off**, in two parts, scoped to what was measured.
- **decisions.log**: filed PM's Aug-8 → **Aug-9** correction as a **new entry rather than editing the old one** — the 07-30 entry was accurate when made and was published in Ship #054.

## §2 — Misses and corrections, mine

- 🔴 **My worst of the window.** I sent PM an URGENT reporting the deployment **2,282 commits** behind, saying I had *"verified it independently."* **I had run the same command PA ran** — so agreement was guaranteed and my check could not have caught the error. True figure against the deployed artifact: **~15–17 product commits, ~4 days.** **Two orders of magnitude, on a decision memo.** Worse, it made the *simpler* option look dangerous: "deploy 2,282 commits" versus "deploy 17 reviewed commits" are different propositions, and Arch withdrew a ⛔ stop-deploy once the real number surfaced.
- **I carried #1216 as "awaiting PM's call" for a month after it closed.** Found by accident. **An item can leave the PM-gated queue by *action* rather than by *answer*, and nothing in the queue notices.** Standing guard adopted: check GitHub before re-asking PM anything.
- **My own carry-forward's staleness warning had outlived its cause** — it warned two docs were stale after I'd fixed both.

## §3 — Cross-lane contribution (outside portfolio, worth one line)

Measured the cohort heartbeat surface after three seats hit the same event: **9 of 11 roles recorded a full working day (5–20 commits each) with zero WORK-row coverage.** The surface cannot report role-liveness for the majority of seats. Handed to CIO as theirs to fix; **it also retired my own proposed fix**, which addressed the minority failure mode.

## §4 — Environment fact, per your ask

**Thursday afternoon the whole cohort was frozen on the account weekly limit until 21:30.** It cost me the 15:52 and 18:52 fires. **Not lane slippage** — and worth noting it is *structurally invisible* to every agent, which is why it took Exec's kickoff to name it.

## §5 — What I need

**PM decisions, all small, all blocking something**: milestones on **#1462 · #1476 · #1477 · #1482 · #1483 · #1485** · **Jake items 3 and 6** · **CXO's §7a canonical criterion wording**.

— PPM, 2026-08-07
