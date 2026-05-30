# Docs Duty Cycle — Escalations / Attention Doc

**Purpose**: items requiring PM attention per v0.6 Duty Cycle (reframed escalations = attention doc, per Architectural Decision 2).

**Owner**: Documentation Management (Docs)
**Created**: 2026-05-27 12:05 PT at v0.6 cycle adoption

---

## Active escalations (for PM)

- **Docs on-main cron VACATED per ratified "do not register on main" (2026-05-28 ~14:50 PT)** — Following PM's morning ratification (Rule-2→Model-A + Q1 worktree-as-cycle-default) and the cohort convergence (CIO won't re-register, Exec vacated, HOST STOPped, PA never registered), Docs is **not re-registering the on-main cron.** The autonomous loop pauses here by design. **To resume autonomous cycling: relaunch Docs in a `claude/docs-cycle` worktree** once Lead+Arch land the worktree-cycle mechanism (v0.7 item 1, in design) + the overnight never-recreate-gap (item 4, open) resolves — a cron can't self-migrate to a worktree (operator relaunch required). Until then Docs runs **manual-session-open + PM-engaged**. No work is stranded; today's mail is drained and committed (`ee9ddcbeb`).

- **~~#972 MEM-TEMPORAL — 2 design questions~~ RESOLVED 2026-05-30** (PM directives): Q1 = "add a YAML block" (already shipped via May 28 briefing pilot `b40876b87`); Q2 = "drop them— I never asked for that" (memos dropped from scope; spec narrows to standing reference docs only). Spec updated to v0.3. ≥3-examples AC substantially satisfied (17 briefings already carry `valid_from` from the pilot). Remaining: decide session-log-instructions disposition (recommend same as memos by point-in-time logic; flagged in spec), continue YAML-frontmatter upgrade across other standing-doc classes (ADRs/patterns/methodology/serena already queued in standing-items). Closing this attention-doc item; remaining work tracked in standing-items.

## Process observations (for cycle methodology + CIO research)

- **2026-05-27**: Adopting v0.6 cycle as workhorse-tier per PM 8:51 AM PDT directive. Cron offset `:17`. [RESOLVED: launched 12:24 PT job 42a9ed72; cron-id rotated 3x through day to fc464e79.]
- **2026-05-27 Fire 8**: v0.6.3 forward-progress judgment — declined to autonomously edit BRIEFING-CURRENT-STATE (high-blast-radius cohort doc) on a late-evening fire; instead surfaced the #972 clarification blocker above. Holistic-not-tactical: not all "unblocked low-priority work" is appropriate for unsupervised fires — blast-radius is a filter alongside scope.

---

*This file is escalations-as-attention-doc per v0.6 architectural decision 2. Append during cycle fires when items need PM-attention surfacing.*
