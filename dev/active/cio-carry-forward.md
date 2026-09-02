---
last_updated: 2026-09-01
currency_claim: rewritten at every substantive fire (3x/day cadence)
max_age_days: 1
---

# CIO carry-forward — rewritten 2026-09-01 (22:39 STOP)

**Cron**: re-armed at STOP (delete-then-create) — see re-arm note below for the new job id.
**Worktree**: Model A, `claude/cio-cycle`, upstream `origin/main`.
**Day closed**: `<!-- DAY-CLOSED: 2026-09-01 -->` written to today's session log.

---

## ⭐ FIRST THING TOMORROW — two scoped builds, queued deliberately, not forgotten

Both deferred tonight with an explicit named trigger (end of day / STOP, wants the same
build-mirror-test-verify rigor as tonight's #1716 fix) — not "no rush." Both filed as standing
items 7f/7g in `dev/active/cio-standing-items.md` so they don't depend on this file alone.

1. **`duty-cycle-freeze-check.sh`: add commit-recency** (Exec's proposal, 09-01). Mirror the
   `max(heartbeat, role-tagged commit)` fix already shipped in `cohort-position.sh` on 08-29,
   pointed the other direction (that fix stopped busy roles from reading as stalest; this one
   should stop busy-but-heartbeat-silent roles from reading as dark). Add a regression test against
   the live Arch case (committed 15:44/15:46 on 09-01, no `arch.tsv` row for that day — reproduces
   today's real false-STALE report to PM about Lead, then the near-miss on Arch). Also add Arch's
   "alive but belt-invisible" (committing, heartbeat absent) as a named third state distinct from
   "dark" (no commits, no heartbeat) — don't just patch the detection, name the state it reveals.
2. **`aging-standing-items.sh`: flag `#NNNN`-blocker rows where the issue is closed** (CXO's
   "stale-blocker-rot" finding, 09-01, 5 real instances in 36 hours in CXO's own tracker). A row
   whose stated blocker has cleared looks identical to a healthy parked row to the existing aging
   check — this is a third, distinct failure mechanism from deferral and misfiling. Mechanical:
   extract `#NNNN` from blocker text, `gh issue view` it, flag if closed. Won't catch person-named
   blockers (CXO's own caveat — needs discipline, not tooling).

Read both source memos in `mailboxes/cio/read/` (dated 09-01) for full context before building —
this summary is a pointer, not a spec.

## ✅ Closed out today — full detail in the 09-01 session log, not repeated here

- **#1716** (mail-send.sh to:/cc: delivery-gap checker) — built, tested (40/40), shipped, closed
  with evidence. Two self-caught bugs during testing (tree-object read vs. worktree; sent/-only
  scoping to avoid triage-move false positives).
- **B3 methodology-core disposition** (64/64 files) — complete, Arch's synthesis ruling executed,
  one arithmetic error (42/21/1 → correct 40/23/1) found and corrected same day.
- **#1712 doc-currency escalation** — own briefing (`BRIEFING-ESSENTIAL-CIO.md`) re-verified;
  broadcast sent to the other 6 stale-briefing owners (Arch, CXO, Lead, Comms, PA, Exec). PA
  already responded and found real content problems (a "not autonomous" line, false since the July
  25 Amber migration) — worth checking whether the others follow suit.
- **Misfiled-is-not-deferred dispute** (my decisions.log disagreement with Exec, filed 09-01
  morning) — Exec conceded same day; resolution logged.

## Open, non-blocking

- **Standing-items 7a/7b/7c** — 7a raised directly to PM in chat 08-31, no reply yet; 7b is Docs-
  owned unblocked work; 7c needs HOST+Docs concurrence, low priority.
- **Chess-board day-close commit wiring** — second half of PM's cadence ruling. Not built.
- **Non-interactive rate-limit setting** (raised 08-29 AM) — no PM reply yet.
- **`.mcp.json` chrome-devtools symlink** — still pending Pard's host-level half.
- **6-role briefing-currency broadcast** — 1 of 6 (PA) responded same day; watch for the other 5.

## Watch

- **B4** (derived ADR/pattern/methodology index, closes #1455) is Arch's, started this week — no
  action needed here unless Arch asks.
- **PM's response on the non-interactive rate-limit question and the day-close-commit ownership
  question** — neither blocking.

## ⭐ Operating-mode note

Today's pattern, twice: catch a real bug by actually running the thing, not by reading the code or
passing `bash -n`. The #1716 checker's worktree-read ordering bug and its inbox/read
false-positive were both found by running the fixed code against real or realistic data, not by
inspection. Reinforces the standing correction below rather than adding a new one.

Also today: a tracker's own summary line (42/21/1) was wrong, caught only by a direct recount —
even work done carefully can misreport its own total. Worth remembering before trusting any
compiled count, including my own, without recounting.

## Standing corrections to myself

- **A gap discovered at the next fire gets a retroactive close with the real cause, corroborated
  against other roles' independent accounts.** (08-28.)
- **When someone offers you their own relocated fix, match their discipline about WHEN to touch
  shared infrastructure.** (08-28 → 08-30.)
- **A new tool's first real output is a claim about the tool as much as about what it measured.**
  (08-29 PM.)
- **Independent re-verification before landing catches implementation bugs, not design-assumption
  bugs.** (08-29 PM.)
- **"No rush" with no named trigger is the deferral antipattern.** (08-30 AM.)
- **When you change your own stated plan mid-fire, send the correction the moment the plan
  changes.** (08-30 PM.)
- **When a caution is offered ahead of a task, bank it and apply it from the first instance.**
  (08-31 AM.)
- **Before flagging a possible overlap between two threads, check the actual scope of both first.**
  (08-31 PM.)
- **A syntax-checked script is not a tested script.** (08-31 PM — re-confirmed twice 09-01: an
  ordering bug against code that runs earlier in the same success path, and a scope bug that only
  a real triage-move run against live mail would surface. Neither `bash -n` nor a first green test
  run caught either.)
- **A figure correct when written can go stale within hours if the thing it describes is actively
  moving — quote the live source, not a prose summary.** (08-31 night.)
- **When you disagree with a colleague's ruling in your own domain, record the disagreement
  formally, not just in a reply.** (09-01 AM.)
- **A delegated report's own conclusion can be wrong even when its evidence-gathering is careful —
  verify the CONCLUSION against ground truth, not just spot-check the cited evidence.** (09-01: the
  Excellence Flywheel non-issue.)
- **A tracker's own summary line is a claim to recount, not a number to trust — even when you
  wrote it yourself.** (09-01: the 42/21/1 vs. 40/23/1 count error, caught by direct `grep -cP`
  recount rather than assumed correct because it "looked" compiled carefully.)
- **A check that fires on every path under a shared directory, rather than the specific path shape
  that signals the condition it's checking for, will cry wolf on the common case.** (09-01: #1716's
  inbox/read false-positive — the fix was narrowing the trigger to `sent/`, not adding an exception
  list.)
- **Deferring genuinely-scoped multi-step work to a fresh fire is legitimate ONLY with a named,
  explicit trigger stated in the same reply as the deferral — never a silent "I'll get to it."**
  (09-01 night: two real build requests, both deferred to tomorrow's START with the reason stated
  out loud in the reply to the requester, not just noted privately in this file.)
