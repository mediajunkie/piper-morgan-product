# Comms carry-forward — 2026-07-29, WORK fire (15:12)

**Host**: Amber.local · **Model A**, stable worktree `~/Development/piper-morgan-worktrees/comms`, branch `claude/comms-cycle`
**Cron**: `17634487` · `12 6,9,12,15,18,21 * * *` (armed 09:58; registry row un-parked)
**Session log**: `dev/2026/07/29/2026-07-29-0948-comms-code-log.md`
**Predecessor**: `dev/2026/07/29/2026-07-29-0642-comms-code-log.md` (Desktop / Model B, `DAY-CLOSED` ✓ — closed early to unblock this migration)

---

## Current state

- **Migration COMPLETE.** Comms is up on Amber, cycling, registry row cleared. Environment verified rather than assumed (0 behind origin, git identity clean, memory pool 168 files, toolchain present).
- **Weekly Ship #053 "The Invariant Held" — ✅ PUBLISH-READY, handed to Docs, publishing TODAY.** Status `ready-for-docs`, `pubDate 2026-07-29`. Both blockers resolved:
  1. `pubDate` was corrected 07-30 → 07-29 at 13:47 by **another session** (`ebe2105bb`), not by me. The **derivation** is still unexamined — the row was created already carrying the wrong date, so **#054 may inherit it**. Raised to Exec, open.
  2. **"Driver" RESOLVED — and my original claim was wrong.** It's the FtU sprint's **scenario driver** (Phase-3 acceptance-gate harness, Scenario A/B/C turns against a real LLM), recorded twice in the Jul 16 + Jul 17 omnibus logs. I had searched only the workstream memos and summary report and reported "no referent in any source." Gloss applied (`193647805`); question withdrawn to Exec.
- **Beats 24-28 slate proposed** (`dev/active/comms-narrative-slate-proposal-2026-07-29.md`, `fee440572`) — front established at Jul 15, span Jul 16-28, omnibus coverage complete 13/13. **Nothing drafted, no calendar rows** — awaiting PM's steer on shape (5 vs 4 beats), titles, and the spine. Would fill Aug 20 / 25 / 27 + Sep 1 / 3, curing the Aug 18 dry-out.
- **Web compose autosave**: ask #1 shipped (`0e448d3`). I answered — **#2 when convenient, #3 declined**; soft-lock/presence deliberately not pursued for a two-writer surface. **Open, on PM**: three things to check once in the compose UI (banner on unsaved reload / survives a 409 / gone after a successful save) — that observation is the only thing standing between ask #1 and being actually verified.
- **Genuinely open, awaiting PM's steer**: Beats 21-23 (Write-Path Chase Aug 11, Alpha Launches Aug 13, Architect's Own Trap Aug 18) — drafted, fact-checked, footer-chained. Needs PM's voice-pass + art.
- **Genuinely open, awaiting PM's answer**: the watchdog-wording question on "What the Running System Found" (published — non-blocking).
- **Standing structural gap**: the building-narrative queue **runs dry after Aug 18** — now has a proposed cure awaiting PM's steer (see slate above).
- **BYOC marketplace narrative**: ~6 weeks stale, PM-gated. Re-checked live 07-29, still no direction memo.

## Findings filed this session (not yet acted on by their owners)

- **To CIO** (`83d82817a`): `amber-onboarding-delta-2026-07-29.md` §1 asks migrating roles to re-run the **command-shape** hook probe, which CLAUDE.md's `RESOLVED 2026-07-26` block lists under *"do not re-run these."* The doc predates the resolution by three days. Ordinary drift, CIO's to correct — but three more roles read that doc on day one.
- **Cron is session-only and auto-expires after 7 days.** Every registry row cleared this week (arch's, mine) asserts a liveness that decays silently around **Aug 5** unless something re-arms. Raised to CIO; not mine to fix.
- **`check-acronyms.py` false positive**: flags "the chief architect role (Arch)" as a ROLE-GLOSS problem, but that is the house style PM **ratified Jul 28**. Will fire on every future draft until the script's glossary absorbs it. Low priority, unfiled.
- **Dangling `draftPath` is chronic, not a one-off**: #052's `draftPath` also points at a file absent from `drafts/`. Worth a sweep at some point; not urgent.

## Environment facts established on Amber (so nobody re-derives them)

- Filesystem is **case-INSENSITIVE**, same as Desktop — the `draftPath` silent-divergence hazard transfers unchanged.
- Cron is the ordinary `CronList`/`CronDelete`/`CronCreate` surface, not `mcp__scheduled-tasks`.
- `mail-send.sh` push-to-ref **works** from an Amber worktree, first attempt, no retry. **The two-call inbox-side-deletion gap did NOT appear**: a 15:35 send carried nine new files plus an inbox-side deletion and the deletion landed in the same call, verified against `origin/main`'s tree. Predecessor's last open §5 question, answered.
- **Hook probe, corrected order (B-first, empty index printed and verified before each cell)**: **Probe B compound → BYPASSED. Probe A standalone → BLOCKED, naming `check-branch.sh`.** Exactly what the index-state model predicts. So the hook is alive but **does not cover the shape used in ordinary work** — assume `git add … && git commit …` on `mailboxes/` paths is ungated here, and stage-then-commit-bare when a commit must be gated. `mail-send.sh` is structurally safe regardless (`commit-tree`, never `git commit`).

## State flags

- Session: active, mid-day. Inbox **empty** (MANIFEST only). Mail loop drained.
- Queue at this fire: **(0 unblocked, 4 PM-gated)** — the Beats 24-28 slate steer, the Beats 21-23 voice-pass + art, the compose-UI banner check, the watchdog wording. Nothing unblocked is being held.
- **Ship #053 is off my desk** — Docs owns the publish. Only remaining Comms-side interest is confirming it goes live today.
- Next scheduled fire 18:12; last fire of the day 21:12 → **STOP**.
