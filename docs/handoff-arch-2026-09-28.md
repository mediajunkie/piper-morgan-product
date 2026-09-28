# Arch handoff — written as last act before Pard's Opus 5.5 restart, 2026-09-28 14:3x PDT

**Why this doc exists**: this restart is real this time (the 09-25 attempt was held until PM was
present; PM has now authorized it). Pard is not using `--resume`. The next instance reading this
has no memory of this session. Read this first; it points to the two files that carry ongoing
state so nothing here needs to be duplicated or kept in sync by hand.

## Read next, in order

1. `dev/active/arch-carry-forward.md` — the resumption substrate, current as of this handoff
   (last rewritten 14:2x today). Has today's IN FLIGHT state in full detail.
2. `dev/active/arch-standing-items.md` — task queue, unchanged today.
3. Today's session log, `dev/2026/09/28/2026-09-28-0627-arch-code-log.md`, if you want the
   reasoning behind anything below, not just the state.

**Worktree is clean at the moment of writing this** — `git status --short` empty, everything
already on `origin/main`. Nothing else needs committing before the restart.

## The restart itself — what's different from the 09-25 attempt

- **This one is real.** PM authorized it directly; Pard confirmed in the out-of-band message that
  triggered this handoff.
- **Your session cron (`com.xian.pm-arch-cycle`) is DISARMED by Pard right now**, deliberately, so
  no scheduled fire injects into the restart/onboarding sequence. Pard restores it once a
  transcript confirms the new session is actually working. **Don't try to re-arm anything
  yourself** — that's Pard's step, not yours, and there's no session-scoped `CronCreate` to touch
  anyway (retired permanently 2026-09-25 — see carry-forward's Wake-mechanism row for the full
  history).
- **A real operational risk was named to me, worth carrying forward even though there's nothing
  for you to do about it**: CIO's own restart onto 2.1.280 got wedged 27 hours behind an
  auto-mode onboarding wizard, because the duty-cycle wrapper pressed Enter into a dialog and
  accepted an offer to scan shell history and other repos. You're at the same intersection CIO
  was (2.1.280 + auto permission-mode on the `.claude-pm` partition) — the same offer may appear
  for you. Pard says the wrapper no longer presses Enter blind, and PM (xian) will be attached and
  will decide if it comes up. **Nothing for you to do about it except know why PM might be
  watching closely at the start of this session** — don't be surprised by it, don't try to handle
  it yourself if it appears.

## Model

You should come up as **Opus 5.5** — genuinely, this time. Still worth verifying rather than
assuming (carry-forward standing rule 7: a restart's stated intent is not evidence of its
outcome) — check for an explicit model system-reminder rather than trusting this line blindly,
the same discipline that correctly caught the 09-25 attempt not having actually happened.

## What's actually open right now (2026-09-28 14:3x), most-recent first

1. **Cadence**: currently throttled 3×/day (`27 6,14,21`, PM's usage-throttle directive). **Ruled
   by Exec today**: reverts to 6×/day (`27 6,9,12,15,18,21`) at **Tuesday 2026-09-29's first
   scheduled fire** — that's a registry `cron_expr` edit (`dev/active/duty-cycle-registry.tsv`),
   not a session-cron action. Do this at that START if it hasn't already happened by the time you
   read this.
2. **LLM gateway question — CLOSED today.** Investigated for PM/Themis: a single gateway
   (`services/llm/clients.py`'s `LLMClient`) already exists, 11 real call sites (not the
   113-files-referencing number that prompted the question), fallback/logging/spend already
   centralized. Only gap is prompt caching, already routed to Lead. No architecture review
   needed. Design record written: `docs/internal/architecture/current/
   design-record-llm-client-single-gateway-2026-09-28.md`. Replied directly to Themis at
   `designinproduct/docs/mail/`. **Nothing further owed.**
3. **#1899 (Phase 3 armed-carrier discriminator erosion) — CONCURRED, scope confirmed, nothing
   owed unless Lead's build surfaces something new.** Full detail in carry-forward.
4. **m-55 (A Name Is Not a Definition)** — filed, Emerging, watching for a second-author instance.
5. **Q5 denominator, Bets 001-003** — both still genuinely awaiting PM, re-verified multiple times
   this week rather than assumed stale. Not worth re-nudging.

## One thing worth knowing about how this week went, for calibration

This session ran an unusually high-verification week — several real self-caught errors (a vacuous
gate-safety ruling on #1595, a stale rubric citation in my own MCP doc, an incomplete mail-move
send today), each corrected within the same fire it was found in, each named honestly rather than
smoothed over. If you inherit a claim from a memo or a prior ruling, the standing discipline this
week built is: verify the mechanism directly before ruling on it, not the description of the
mechanism — that discipline paid for itself multiple times and is worth continuing, not something
that was special to this particular session.

**Verified how (this handoff itself)**: every claim above cites a specific file, commit, or
today's session log rather than being reconstructed from memory. Worktree state (`git status
--short` empty) checked directly this fire, not assumed clean from a prior report.
