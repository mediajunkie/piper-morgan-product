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
| 2 | **T-axis probe execution — PM ruled "spend the tokens," CXO owns the axis, PA runs it** | 2026-09-20 | PM ruled (relayed by Exec) to spend tokens on the T-axis probe now. CXO (axis owner, no harness on their own seat) handed execution to PA directly: *"PA — I'm not handing you a deadline (there isn't one — the framed urgency was CXO's own now-retracted error) and I'm not specifying your round design."* **Blocked on CXO sending pre-registered scoring properties "this cycle"** — do not design or run a round before that lands (CXO's own prediction record on this instrument is 0-for-3, and pre-registration is the stated mitigation). Separately: CXO is proposing to PM/PPM a split of the T axis into T-own-surface (measurable now, tokens can close it) vs. T-MCP-surface (blocked on increment-1 infra, stays honestly unmeasured) — not PA's call, just context for why "spend now" doesn't necessarily mean the axis fully closes. Full memo: `mailboxes/pa/inbox/response-cxo-to-exec-pa-cc-pm-t-axis-spending-the-tokens-what-it-can-and-cannot-buy-2026-09-20.md`. |
| 3 | **Usage-correlation model — PM tasking, no deadline, question sent, awaiting PM** | 2026-09-20 | PM (via Exec): *"rather than handwaving... build a richer model. Also, research what's out there."* Same method as T1. **Prior-art pass complete** (`dev/active/usage-correlation-model-prior-art-2026-09-20.md`): four converging fields all say a proxy-only model with zero ground-truth readings is uncalibrated and potentially biased, not just weaker. **Load-bearing finding**: Lead's `usage-per-account-capture-2026-09-19.md` (PM-reaffirmed 09-15) already proposes the exact calibration mechanism needed and has **zero rows captured, unimplemented**. **Calibration-shape question sent 19:21 fire** — `mailboxes/pa/sent/question-pa-to-exec-cc-pm-calibration-shape-for-usage-model-and-leads-unimplemented-proposal-2026-09-20.md`: does Lead's proposal (or something like it) get implemented, since without it no model here can ever be calibrated. **Pending PM's answer** — do not guess a calibration shape and build on it. **Not blocked in full**: the dispatch-tier dimension doesn't need PM's dashboard and can proceed independently — not yet started, next unblocked unit of work on this item. |

### Pending external action

_(none as of this update — see Resolved below)_

### PA-queued

_(none as of this prune)_

### Watch

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Cross-pollination signal** — Klatch (paused), Atlas, Globe sibling projects | Pre-migration carry | Per `[[project_sibling_projects]]` memory. Surfaces if any sibling-project signal reactivates. Same underlying thread as T1 (now resolved, see below); kept as "watch for a trigger" since PM's DinP/Themis discussion (see T1's resolution note) may reactivate cross-pollination specifically. |

### Resolved (preserved for one cycle)

| # | Item | Resolved | Notes |
|---|---|---|---|
| T1 | ✅ **Cross-Piper synthesis — PM RESPONDED 2026-09-19, endorsed** | Delivered 2026-09-03, PM responded 2026-09-19 (16 days) | PM read it, verbatim: *"I read PA's analysis and it's excellent as usual... I support the observations and recommendations,"* with an unprompted apology for the delay (relayed by Exec, `mailboxes/pa/sent/deliver-pa-to-pm-t1-piper-alpha-piper-open-comparison-2026-09-03.md` was the delivery). The one outstanding question (draft-then-review vs. review-then-draft) was already answered by PM 09-02 and recorded in the doc's own divergence section — nothing re-litigated. **Now in wider circulation**: Exec asked CIO/PPM/CXO to read it against their own current thinking (not as an FYI), and shared it with Themis at Design in Product per PM's explicit request, for both DinP OS and the Pimento skunkworks. Nothing further owed by PA on this thread — the "convergent lessons" finding is doing real work elsewhere now. Full loop: `dev/active/t1-cross-piper-comparison-2026-08-31.md` (the document), `mailboxes/pa/inbox/relay-exec-to-pa-cc-pm-xian-read-t1-supports-it-and-apologises-for-the-delay-2026-09-19.md` (PM's response, relayed). |
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
