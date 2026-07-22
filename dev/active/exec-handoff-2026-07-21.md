# Exec (Chief of Staff) — handoff memo, 2026-07-21 21:30 PT

Written per PM/Janus's migration-prep ask (possible session move to Amber/fresh account, not yet scheduled). If a fresh session picks up this role cold, start here, then read `dev/active/exec-carry-forward.md` (rewritten every fire — the living detail) and today's session log (`dev/2026/07/21/2026-07-21-0900-exec-code-log.md`).

## Who I am / what I do

Chief of Staff — cross-workstream synthesis, mailbox triage/relay hub, Weekly Ship drafter (draft → PM fact-check/voice-pass → Comms review → publish; PM gates the Comms handoff, Exec never self-initiates it), duty-cycle fires twice daily (`32 8,20 * * *`), coordination point when PM is away ("coordinate through Exec").

## Active threads right now

1. **Broader cohort silence, flagged to PM this morning (7/21)** — 9 of 10 non-Lead/non-Exec roles were quiet all of 7/20. Sent PM a memo asking for a wider re-prod/wake pass. Awaiting response. *This session's migration-prep note (below) may explain the same underlying cause — Desktop crashes, not a discipline gap.*
2. **This handoff-prep round itself** — I relayed PM/Janus's ask to all 10 other roles tonight (`memo-exec-to-leadership-cc-pm-prepare-handoff-memos-possible-session-migration-2026-07-21.md`, sent to every inbox + PM cc). Not urgent, no firm timeline.
3. **#1386 beta gate** — UNBLOCKED as of 7/20 evening. Lead shipped fixes (now beta v26 per tonight's memo, both Scenario-B candidates live). Scheduling the actual gate run is CXO/PPM/Lead's call now, not exec's. Gate has other unverified criteria (canonical suite, #1278 scope, PM go/no-go) — don't assume close is imminent.
4. **Weekly Ship #052 draft** — drafted 7/19 (`dev/active/weekly-ship-052-draft-2026-07-19.md`, theme "The Mechanism, Not the Memory"), routed to PM, **still awaiting PM's fact-check/voice-pass**. Do not touch the draft file until PM responds.
5. **Worktree-collision defect** — this worktree (`mystifying-lumiere-8bebd3`) has had a directory/branch pairing mismatch since ~7/16 (branch stuck on `claude/infallible-newton-f0ec45` instead of matching the directory). Confirmed real (CIO's fleet audit, a live rebase-conflict sighting). Not dangerous if handled cautiously (explicit-path adds, verify status before every stage, push immediately) — a fresh session in a fresh worktree should sidestep this defect entirely, which may be a side benefit of any migration.
6. **Decisions.log correction filed tonight** — Comms caught a misleading "Routines watchdog funding decision" framing recurring in June logs; PM confirmed it wasn't a real cost tradeoff (existing plan already covers it). Corrective entry appended to `docs/internal/architecture/decisions/decisions.log` (2026-07-21 ~21:10 PT entry) so future retrospectives don't repeat the framing.

## Standing / lower-priority carries

- Lead Dev's #1424/#1427 — still awaiting PM's final calls (since 7/18).
- Stale branches (MUX x3, xpoll-hook) — 7+ days silent despite CXO/CIO active; due a light second touch.
- Account migration to pipermorgan.ai — PM's own call, no deadline.
- Beta Blockers count — last verified count is stale; re-pull from GitHub before citing a number (use the `query-github-board` skill — mandates `totalCount` reconciliation, don't trust a truncated pull).
- A discovered-but-not-acted-on item: `scripts/regenerate-mailbox-manifests.py` legitimately deletes stale `inbox/` duplicates that already have a `read/` twin. Ran it against PM's mailbox 7/21, found 219 such (all old May mail, content safe in `read/`) — declined to commit a 219-file bulk deletion unilaterally. Flagged for Docs/PM discretion, not urgent.

## Mechanics a fresh session needs

- Duty-cycle fires: run the `duty-cycle-tick` skill every time, follow it exactly (cron check → Step 2a pairing check → sync → dispatch by state → mail loop → task loop → session log → commit/push/verify on `origin/main` → carry-forward rewrite → cron management → brief status).
- Mail: `scripts/mail-send.sh` (push-to-ref, explicit paths only) — never raw `git commit` touching `mailboxes/` from a feature branch.
- Never destructive git in PM's *main checkout* specifically (`/Users/xian/Development/piper-morgan/piper-morgan-product/`) — that's PM's live editing workspace, uncommitted changes there are real work.
- Session logs: `dev/2026/MM/DD/{date}-exec-code-log.md`, one per day, wrapped at STOP with the `<!-- DAY-CLOSED: {date} -->` marker.

— Exec, 2026-07-21 21:30 PT
