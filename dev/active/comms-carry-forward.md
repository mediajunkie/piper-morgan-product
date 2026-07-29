# Comms carry-forward — 2026-07-29, WORK fire (12:20 PT)

**Host**: Amber.local · **Model A**, stable worktree `~/Development/piper-morgan-worktrees/comms`, branch `claude/comms-cycle`
**Cron**: `17634487` · `12 6,9,12,15,18,21 * * *` (armed 09:58; registry row un-parked)
**Session log**: `dev/2026/07/29/2026-07-29-0948-comms-code-log.md`
**Predecessor**: `dev/2026/07/29/2026-07-29-0642-comms-code-log.md` (Desktop / Model B, `DAY-CLOSED` ✓ — closed early to unblock this migration)

---

## Current state

- **Migration COMPLETE.** Comms is up on Amber, cycling, registry row cleared. Environment verified rather than assumed (0 behind origin, git identity clean, memory pool 168 files, toolchain present).
- **Weekly Ship #053 "The Invariant Held" — reviewed and fixed** (`132c680c4`). **Two questions are back with PM and are the only thing between this and Docs**:
  1. `pubDate` reads **Thu 2026-07-30**, but Ships #046–#052 all published Wednesday and PM called this "today's" Ship (Wed 07-29). One word either way — not changed unilaterally, because it is a publication date.
  2. **"Driver runs clean"** in Product & experience is unglossed and has no referent in any of the six workstream memos or the summary report. Did not invent a gloss.
- **Genuinely open, awaiting PM's steer**: Beats 21-23 (Write-Path Chase Aug 11, Alpha Launches Aug 13, Architect's Own Trap Aug 18) — drafted, fact-checked, footer-chained. Needs PM's voice-pass + art.
- **Genuinely open, awaiting PM's answer**: the watchdog-wording question on "What the Running System Found" (published — non-blocking).
- **Standing structural gap**: the building-narrative queue **runs dry after Aug 18**. The one item with a real date on it.
- **BYOC marketplace narrative**: ~6 weeks stale, PM-gated. Re-checked live 07-29, still no direction memo.

## Findings filed this session (not yet acted on by their owners)

- **To CIO** (`83d82817a`): `amber-onboarding-delta-2026-07-29.md` §1 asks migrating roles to re-run the **command-shape** hook probe, which CLAUDE.md's `RESOLVED 2026-07-26` block lists under *"do not re-run these."* The doc predates the resolution by three days. Ordinary drift, CIO's to correct — but three more roles read that doc on day one.
- **Cron is session-only and auto-expires after 7 days.** Every registry row cleared this week (arch's, mine) asserts a liveness that decays silently around **Aug 5** unless something re-arms. Raised to CIO; not mine to fix.
- **`check-acronyms.py` false positive**: flags "the chief architect role (Arch)" as a ROLE-GLOSS problem, but that is the house style PM **ratified Jul 28**. Will fire on every future draft until the script's glossary absorbs it. Low priority, unfiled.
- **Dangling `draftPath` is chronic, not a one-off**: #052's `draftPath` also points at a file absent from `drafts/`. Worth a sweep at some point; not urgent.

## Environment facts established on Amber (so nobody re-derives them)

- Filesystem is **case-INSENSITIVE**, same as Desktop — the `draftPath` silent-divergence hazard transfers unchanged.
- Cron is the ordinary `CronList`/`CronDelete`/`CronCreate` surface, not `mcp__scheduled-tasks`.
- `mail-send.sh` push-to-ref **works** from an Amber worktree, first attempt, no retry. The two-call inbox-side-deletion gap is **still untested** — no send has exercised it yet.
- **Hook probe, corrected order (B-first, empty index printed and verified before each cell)**: **Probe B compound → BYPASSED. Probe A standalone → BLOCKED, naming `check-branch.sh`.** Exactly what the index-state model predicts. So the hook is alive but **does not cover the shape used in ordinary work** — assume `git add … && git commit …` on `mailboxes/` paths is ungated here, and stage-then-commit-bare when a commit must be gated. `mail-send.sh` is structurally safe regardless (`commit-tree`, never `git commit`).

## State flags

- Session: active, mid-day. Inbox **empty** (MANIFEST only). Mail loop drained.
- Queue at this fire: **(0 unblocked, 3 PM-gated)** — Ship #053's two questions, the Beats 21-23 voice-pass, the watchdog wording. Nothing unblocked is being held.
- Next scheduled fire 15:12; last fire of the day 21:12 → STOP.
