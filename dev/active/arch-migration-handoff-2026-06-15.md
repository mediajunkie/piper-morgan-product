# Architect Migration Handoff — paste into OLD-account Arch session

**Author**: CIO (supervising the wave) · **Date**: 2026-06-15 · **For**: PM to paste into the old-account Architect session when ready to close it. Same shape as the Docs/PA/HOST/Comms handoffs.

---

Arch — migration handoff. PM is closing this session and opening a fresh Code session on DinP (xian@designinproduct.com), **staying on Opus** (no model change — your tier per the role-model map; this is an **account move ONLY**, which makes yours the lowest-risk migration in the wave). You migrate in the remaining-leads group, after the doers (Lead Dev ✓, PA ✓, Docs ✓, Web). You don't supervise others (CIO does). Clean handoff of your own state:

1. **Update your continuity** so new-Arch resumes cleanly. Unlike Docs, you DO carry dense session-state surfaces — refresh both so nothing is lost across the account switch: `dev/active/arch-carry-forward.md` (rewrite to current — your Fire-N state, current cron, active PM threads, **the 2 open PM calls + any escalation/awareness items**, queued ADR work), `dev/active/arch-standing-items.md` (task queue current). **(The per-role `duty-cycle-escalations-*.md` doc is DEPRECATED as of 2026-06-17 — FOLD ratified by PM; PM-attention items now ride the carry-forward, and the GitHub-verifying cohort rollup + the freeze-registry replaced its other jobs. Don't create/refresh a separate escalations doc.)** Treat the carry-forward as "what I'd tell a same-role colleague covering my desk tomorrow." Specifically capture the **in-flight ADR threads**: MCP connector ADR + topology (owed, #1220, ADR-070 candidate; input doc `docs/internal/architecture/connector-refactor-sprint-scope-2026-06-14.md`); ADR-071 ratification after Lead's #1241 audit; #972 MEM-TEMPORAL schema review (waiting on Docs).

2. **Close your logs (single-surface, skill v1.8)**: write the day-close to your **session log** (the durable record) — day-arc + memory-eval 3-bucket + sign-off checklist + the `<!-- DAY-CLOSED: 2026-06-15 -->` marker. (The cycle log is optional scratch now — no formal close needed. You adopted single-log discipline Fire 37, so this is your settled pattern; just confirm the session log — not the cycle log — carries the day's durable record.)

3. **CronDelete the active duty-cycle cron** (`CronList` to find its id — currently `175b5163`, expression `52 */3 * * *`). The new session arms a fresh CronCreate cron, **windowed** this time (see the bootstrap — your lane moves from the 3hr-interval shape to the cohort-standard windowed schedule; the scheduled-task approach was tried + suspended 6/14).

4. **Commit + push EVERYTHING to `origin/main`** — run + read each:
   ```bash
   git status                    # clean
   git log --oneline @{u}..HEAD  # empty (pushed)
   git log --oneline main..HEAD  # empty — or merge to main now
   ```
   Arch especially: make sure no ADR / pattern-catalog edits (ADR-066 v0.2, the MCP-connector input doc, any in-progress ADR-070/071 drafting) are stranded on a branch.

5. **Report back**: continuity recap (1-line — carry-forward [incl. the PM-attention items] + standing-items refreshed) + the open-threads you're handing off (MCP connector ADR, ADR-071, #972, the 2 PM calls) + crons clear (`CronList`) + the **actual output** of `git log --oneline main..HEAD` (empty is correct). Then stand by for PM to close + reopen.
