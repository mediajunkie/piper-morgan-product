# CIO Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the duty-cycle-tick skill. Holds the genuinely transient "where am I right now" state. Durable owed/queued items live in `cio-standing-items.md` (the Task List); PM-attention items live in `duty-cycle-escalations-cio.md`.

**Last updated**: 2026-06-12 ~18:10 PT — **migration FULLY complete** (cio-cycle RETIRED; doc-staleness refreshed; PA phase-2 reply sent; recurring-audit triage — #974 closed). Cron `d982e3d0`. HOST pair drafted (PM executes this eve/tomorrow). Prior: ~17:40 bootstrap, ~17:20 handoff.

---

## ⚠️ REGISTER NOTE (m-41 — read first)

Per the carry-forward register-separation cure (m-41, Proven 6/12): this document separates **durable role context** (carry forward as-is) from **operating-model variant** (do NOT copy; adopt current canonical). The variant block is explicitly labeled at the bottom. Everything else is durable.

---

## 🔥 TOP CONTEXT — Token efficiency is PM ULTRA-HIGH priority (6/11)

Do not let this thread drop. Surface actively in PM statuses. Live levers: windowed-cron (ratified + distributed), session-log-primary per-lane (pending PM), Routines watchdog (pending PM funding), cohort token tracking (`metrics/cohort-fire-log.tsv` — append a row per substantive fire; you're dogfooding for the cohort).

## MIGRATION STATE (you are part of this)

- **CIO migration COMPLETE (6/12 ~17:40)**: new-CIO bootstrapped on DinP / Opus 4.8 / **ephemeral worktree** (Option B — NOT cio-cycle; bootstrap §5 was stale, plan-of-record + carry-forward won the fork). Cron `d982e3d0` (windowed `7 3,10,13,16,19,22`). **Supervision underway**: HOST pair DRAFTED (`dev/active/host-migration-handoff-2026-06-12.md` + `host-bootstrap-brief-2026-06-12.md`), surfaced to PM for review — encodes the **plan-of-record-wins** conflict rule + ephemeral correction (so HOST doesn't hit CIO's §5 trap). **Next in queue** (one at a time, gently, PM executes): Comms, CXO, PPM, Arch, Docs.
- **Lead Dev migration is IN PROGRESS in parallel** (PM kicked it off 6/12 ~17:05). LD's prompts are ready: `dev/active/lead-migration-handoff-completion-2026-06-12.md` + `dev/active/lead-bootstrap-brief-2026-06-12.md`. LD self-authored an exceptional handoff (`dev/active/lead-dev-handoff-2026-06-12.md` — §6 tacit-knowledge section is the wave's model artifact).
- **LD worktree-exception question is DELEGATED TO LD** (PM 6/12 eve): LD determines empirically whether the dev-server+WIP shape needs a Model-A named-worktree exception; LD's evidence sets the cohort precedent. Watch for LD's determination at their bootstrap report-back.
- **The plan of record**: `dev/active/cohort-plan-of-record-2026-06-12.html` — PM-reviewed page covering operating pattern (Option B ephemeral canonical; Model A deprecated + exception rubric), cron rules, logging rules, migration runbook + status, open decisions, deprecations. This is the reference for all supervision work.
- **Exec is settled** — ephemeral worktree, NO do-over (old-CIO briefly recommended one in error; corrected same-day). Exec's diagnostic memo (`mailboxes/cio/read/memo-exec-to-cio-cc-pa-migration-bootstrap-instruction-gaps-2026-06-12.md`) is the founding artifact for the wave's fixes.
- **cio-cycle RETIRED 6/12** (PM-authorized): worktree removed + branch deleted (fully merged, nothing stranded). CIO is ephemeral-only; migration fully complete. **Doc-staleness DONE 6/12** (`e1a2f2e72`): CLAUDE.md (worktree-default ¶ + Rule 1) + BRIEFING-CURRENT-STATE.md line 26 refreshed Model A → Option-B-canonical + migration status; plan-of-record named as source of truth. Still queued (low-pri): reconcile `cohort-agent-status.md` (drift 6/6); a fuller CLAUDE.md §"Git Worktrees" reconciliation (left Model-A setup intact for the PM-approved exception case).
- **RESOLVED 6/12 — PA skunkworks BYOC phase-2 ratification reply SENT** (`2c111e45f`, to PA cc PM; original→read R100). CIO verdict: ratify direction; **gate cross-user synthesis on write-governance + consent** (ties to #972 MEM-TEMPORAL + HOST trust boundaries); add a runtime-portability lens to skill design; firewall from M3/M5 roadmap. **Watch-not-mint**: server-owned-config + main-anchored-continuity = 2 instances of "runtime-agnostic state placement" (3rd → candidate Emerging pattern).

## PM-PENDING DECISIONS (on `duty-cycle-escalations-cio.md`; don't block other work — Rule 2)

1. **Session-log-primary per-lane cohort take** — synthesis READY (Docs: omnibus-safe-or-better; HOST: register-separation, per-lane by fire-density). If PM ratifies: 3-piece comm = per-lane surface-mode registry + Docs methodology touch-up (cycle-log optional in create-omnibus/cleanup-dev-active) + m-31 amendment (CIO authors the register-separation layer).
2. **Routines watchdog** (~$70/mo) — funding-trigger criterion MET per 6/11 empirical Gap-C investigation (dormancy is the dominant halt mechanism; 6 of 9 roles needed PM intervention 6/11 morning). The structural cure for session-dormancy cron death.
3. **Thin-prompt cohort-rollout broadcast** — proposal complete since 6/7 + windowed-cron folded in by HOST; largely superseded-in-practice by the migration wave itself (each bootstrap brief carries the patterns); HOST to reconcile. Low urgency.

## METHODOLOGY CATALOG — current state + WATCH items

- **m-41 (Mechanism Displaces Unreferenced Discipline) — PROVEN 6/12** (PM ratified + Arch concurred 3/3). 2nd instance = Exec's variant-preservation trap. Cure-class refined by Arch: "no-path-of-least-resistance-bypasses." Cure instantiations: skill v1.5 dual-surface; carry-forward register-separation (this doc's REGISTER NOTE); MANIFEST `<!-- curated -->` marker (#1106).
- **m-42 (Reflexive Verification — Self-Exempt Under Pressure) — Emerging, filed 6/11** on Arch's 5-instance/2-role recognition. Instance #6 (CIO mail-discipline slip, 6/11), #7 (CIO bootstrap-author caught by variant trap, 6/12), #8 (CIO unconditional `git stash pop` — the exact bolded skill prohibition — popped HOST's stash; recovered clean, 6/12). **Proven gate = naming-reduces-recurrence (self-catch-rate)**; the instance stream is the data. Watch for a structurally different self-exemption (different role or different discipline class).
- **m-40 (layer-then-migrate) — Emerging**; Arch flagged instance #9 (skill-broker, first cross-arc) + #10 candidate (sprint-sequencing contract-vs-build); **cross-author still pending** = the Proven gate. Contingent on BYO convergence/ADR-068 (Arch/M4).
- **m-34 corollary (ship-the-routine-keep-the-loop)** — held as corollary inside m-34's product-layer section (6/10); promotion gate = 2nd "externalize-your-own-moat" instance.
- **m-43 candidate meta-patterns** (2 instances each; watch-not-mint per conservative-bar): (a) Emerging-at-founding/Proven-on-generalization shape (m-30/40/41/42); (b) entry-catches-its-authors-at-authoring-time (m-41, m-42). Either reaching 3 instances → candidate m-43.
- **m-31 amendment owed IF PM ratifies session-log-primary** (the register-separation layer addition — drafted in concept in the 6/11 Fire-8 synthesis memos).

## RECENT SHIPS (context for what's fresh)

- **#1106 CLOSED 6/12** (PM-directed): MANIFEST derive — `regenerate-mailbox-manifests.py` w/ subject→H1→warned-(no subject) precedence + `<!-- curated -->` register preservation; `duty-cycle-tick` v1.7 wires regen into every Mail Loop; Pattern-073 Instance 14 RESOLVED; 10 tests at `tests/unit/test_regenerate_mailbox_manifests.py`.
- **`duty-cycle-tick` v1.7** (current): v1.6 = PM-coined STOP rule ("last scheduled fire of today" — compute next fire; different calendar date → STOP); v1.7 = MANIFEST derive in Mail Loop.
- **Ship #047 CIO workstream review DELIVERED 6/12 AM** (`mailboxes/exec/inbox/workstream-047-cio-2026-06-12.md`); spine nomination: operating-at-scale-reveals-second-order-patterns. Exec synthesizing; publication Wed 6/17.
- **Cron-halt empirical investigation 6/11**: Gap-C dormancy dominant; INCIDENCE rose w/ 6/8 usage-limit + 6/10-12 re-migration restarts; REPL-busy was wrong-direction (memo in cio/sent).

## STANDING PINS WORTH RE-READING (hard-won, recent)

- **Cron-shape change must update the prompt CONSTANTS, not just the live cron** (6/11 Fire 7: Gap-C self-heal re-armed a stale hourly shape from the prompt; fired hourly all morning silently).
- **"Queued" ≠ PM-attention-surface** (PM 6/11): name WHICH list — `cio-standing-items.md` (mine) vs `duty-cycle-escalations-cio.md` (PM's attention). Never ambiguous.
- **Never unconditional `git stash pop`** on shared surfaces — if your `stash push` was a no-op, pop grabs ANOTHER AGENT'S stash (m-42 #8, 6/12).
- **Mail moves: stage BOTH source AND destination** so rename-detection pairs R100 (m-42 #6, 6/11).
- **PM weekday rhythm**: client-primary (OpenLaws ~50%); engaged mornings/evenings; weekends are PRIME TIME not downtime.

## LOW-PRI UNBLOCKED QUEUE (advance at (0,0) per IDLE-means-low-pri)

- Canonical-cron-prompt-template-v0.7.md → windowed default + deprecation banner (Exec Finding 3.1; was held for plan-of-record, which now EXISTS — unblocked).
- procedures→pointers coherence-debt (m-36 Class-1; big-considered — don't rush piecemeal).
- m-40 opportunistic back-refs (not load-bearing).
- `cohort-agent-status.md` reconcile (see MIGRATION STATE cleanup item).

## PARKED / OTHERS' LANES

- #1166 Type-2 dreaming m-27 lens → post-M3 spike (PPM owns PDR-on-convergence).
- BYO-colleague: Exec synthesis with PM (loop-defensibility-gate question = PM's); ADR-068 = Arch/M4.
- derived-INDEX tooling-debt (Lead lane).
- Docs merge-keeper + omnibus continue independently.

---

## ⚠️ OPERATING-MODEL VARIANT (this-session only — do NOT copy; adopt current canonical)

Old-CIO ran: **Model A dedicated worktree** (`claude/cio-cycle` sibling checkout at `../piper-morgan-product-cio-cycle/`) + middle-weight cron prompt + Opus 4.8 then Fable 5 (PM moved model 6/12 16:54 for temp credit balance). **All deprecated/superseded for you**: you run the ephemeral auto-worktree Desktop launched you into (Option B), thin cron prompt, model per PM's launch pick. Canonical cron shape for CIO lane: `7 3,10,13,16,19,22 * * *` (03:07 ultra-thin overnight WATCH carve-out + 22:07 last-fire STOP) — shape is durable, the *mechanics* around it are per the plan-of-record.
