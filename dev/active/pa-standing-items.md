# PA Standing Items Tracker

**Purpose**: Track PA-domain items that are pending PM input, blocked on external action, or queued for PA execution but not yet started. Persistent surface so items don't get lost to transcript / PM memory / PA context window.

**Origin**: Created 2026-05-27 at duty cycle v0.6.2 adoption Day 0 per CIO's suggested-path step 2 (reuse existing or create). PA hadn't previously maintained a standing-items tracker; created new at adoption.

**Duty Cycle role (v0.6 design ratified)**: This file IS the canonical **Task List** (Doc 2 of the three per-agent duty-cycle docs). Per the formalizing-not-proliferating principle, no parallel "task list" doc is created. Tasks added during Mail Loop step 4 land here. Task Loop reads from here. PM-injected tasks (the load-bearing (0, 1) decision-table row) also land here.

**Update cadence**: append-only ledger with status updates in-place. PA updates at session-start (review carryforward) and after each substantive session (capture new items + close completed ones). Distinct from `exec-open-items-tracker.md` (exec-owned, project-wide) — this is PA-owned, methodology-and-product-management scope.

⚠️ **PRUNED 2026-08-11 (fire 15:49 PT)** — this file had accreted ~11 weeks of items from the 2026-05-27 v0.6.2 adoption through 2026-08-01 with almost none retired on schedule (the "Resolved — preserved for one cycle then removed" rule hadn't fired since adoption). The May/June items below were checked against current state rather than assumed dead — three (marked ✅ below) had a real, checkable resolution; the rest had gone quiet with no corroborating activity across ~2 months and are pruned as abandoned/superseded, not confirmed-closed. **`pa-carry-forward.md`'s "PM Attention" section is the live surface** — it's rewritten every substantive fire and is what Exec's cohort-attention rollup reads. This file is the slower-moving Task List underneath it; if it goes quiet again, that's the tell to prune again.

---

## How to Read This

| Status | Meaning |
|---|---|
| **Pending PM** | Awaiting PM decision, concurrence, or approval |
| **Pending external** | Awaiting other-role action (CIO, Lead Dev, Docs, etc.) |
| **PA-queued** | Bandwidth-gated PA work; ready to execute when scheduled |
| **Watch** | Standing observation surface; trigger-bound |
| **Active** | Currently in flight |
| **Resolved** | Closed; preserved for one cycle then removed |

---

## Long-horizon topics (address over time)

_Strategic threads PM flagged to revisit — not operational/owed items; no near-term action._

_(T1 promoted to Active 2026-08-31 — see below. Nothing else currently sits in this section.)_

## Active Standing Items

### Active

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Architecture/BYOC — live thread with PM** | 2026-07-26, converged with the BYOC strategic conversation 2026-08-18 | **Current state lives in `pa-carry-forward.md` PM Attention section, not here** — it's rewritten every substantive fire. The 08-10 architecture-diagram connector-overlap question and 08-18's BYOC conversation are the same underlying topic; carry-forward tracks both together now. This row exists only so the Task List doesn't look empty on the thread that's actually the most active one PA owns; don't duplicate the detail in both places. |
| T1 | ✅ **Cross-Piper synthesis — DELIVERED to PM 2026-09-03** | Noted 2026-06-07, triggered 2026-08-31, delivered 2026-09-03 | PM's 08-31 ask (compare PA and Piper Open as the bar Piper Morgan needs to clear) answered with a compressed rollup memo (`mailboxes/pa/sent/deliver-pa-to-pm-t1-piper-alpha-piper-open-comparison-2026-09-03.md`), pointing to the full working draft (`dev/active/t1-cross-piper-comparison-2026-08-31.md`) for detail. Six convergent lessons, one PA-specific divergence (multi-agent state coordination), and PM's own trust-model answer all covered. Explicitly labeled DRAFT v0 in the delivery — good enough to act on, not exhaustively audited. **Correction, same day**: don't auto-close this on silence — no PM reply yet is not the same as PM confirming no more depth is wanted (never read signal from a non-reply). Leave as Delivered until PM actually responds or enough time passes that it's fair to treat as settled, not on a fixed next-fire timer. |

### Pending external action

_(none as of this update — see Resolved below)_

### PA-queued

_(none as of this prune)_

### Watch

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Cross-pollination signal** — Klatch (paused), Atlas, Globe sibling projects | Pre-migration carry | Per `[[project_sibling_projects]]` memory. Surfaces if any sibling-project signal reactivates. Same underlying thread as T1 above; kept in both sections because one is "revisit over time" and this is "watch for a trigger" — merge if they ever diverge in practice. |

### Resolved (preserved for one cycle)

| # | Item | Resolved | Notes |
|---|---|---|---|
| R5 | **ALPHA_FEATURE_GUIDE refresh — PA's part done** | 2026-08-13 | Docs confirmed: correction folded (all tags now cite `origin/main`), all 7 code-level findings incorporated, PA's "Email or User ID" nuance kept, the #4 dispatch-layer grep Docs ran independently confirmed PA's standup-only read. PM picked up the 4-item live click-through directly. Nothing further for PA — Docs folds PM's results and ships. Full trail: this session's 08-13 log, three sent memos in `mailboxes/pa/sent/`. |

---

## Pruned 2026-08-11 — disposition of everything removed

**Confirmed resolved, with evidence:**
- **check-branch.sh Model-A mailbox blocker** (filed 05-28, "awaiting Lead Dev fix-choice") — resolved, but not by either option this item proposed. #1259 (2026-06-19) retired the main-worktree-bridge approach entirely in favor of push-to-ref (`mail-send.sh`, `commit-tree` — never trips `check-branch.sh` because it isn't `git commit`). The hook itself was separately found to have an invalid matcher (dead on every host/account, root-caused by HOST 2026-07-25) — also moot now that mail doesn't route through it.
- **Cron-shape experiment (PA lane)** — the Day-7 recommendation (windowed `42 6,9,12,15,18,21 * * *`, dropping the two overnight no-op fires) is exactly the cron PA runs today. Recommendation adopted; nothing left to watch.
- **Roadmap v17 §M5/BYOC review** — delivered 5/31, already marked resolved in two places in the prior version of this file. Duplicate bookkeeping, not a live item.
- **HOST Agent-360 v0.3 response**, **#358 ADR-058 scope**, **Year-anniversary MVP-date update** — each already marked DONE/executed in the prior version; had sat past their "one cycle" retention since May/June.

**No corroborating evidence found; pruned as abandoned, not confirmed-closed** (if any of these turn out to still matter, they'll resurface from a fresher source — PM, a mailbox thread, or a GitHub issue — rather than from this stale row):
- Skunkworks writeup PM signoff + fan-out, and the dependent thin-full-stack-PoC proposal + sub-pass 4.b dispatch (filed 05-21/05-27) — three months quiet, no fan-out ever landed, no reference in any carry-forward since.
- Outcomes smoke test scope (filed 05-27, gated on a CIO synthesis that would have landed ~05-31) — gate window closed 10 weeks ago with no follow-up.
- Discovered-work tiered "buried" bar concur, MEM-975 Week-2 slot, memory pin draft on discovered-work discipline (all filed 05-27) — the memory pin was never created (checked the live memory index directly — no `feedback_discovered_work*` entry exists); MEM-975's Week 2 window (~06-01) is long past.
- Discovered-work weekly sweep cadence (last ran 06-12, "Next: Fri 6/19") — never continued past that one entry.
- methodology-34 refresh review, PDR-005 line-376 MCPB stale ref, §M5 PoC line-128 sharpen, Attention Dashboard v0.2 co-shape — all filed early-to-mid June against a PDR-005/v18 process that PDR-006's 2026-07-31 ratification has since moved past.
- Duty-cycle-on-Model-A emeritus handoff (filed 05-31) — the migration it describes completed long ago; Model A is now the documented default on Amber (CLAUDE.md, 2026-07-25).
