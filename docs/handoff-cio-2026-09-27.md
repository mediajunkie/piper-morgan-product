# CIO Handoff — 2026-09-27

Written as my **last act before a model restart** (Sonnet 5 → `claude-opus-5-5`), triggered by
Pard out-of-band, PM-authorized, first `.claude-pm` seat to go through this specific restart
mechanism. Unlike `docs/handoff-cio-2026-09-18.md` (a PM-directed standdown, wait-to-be-woken),
**this is not a standdown** — the LaunchAgent wake mechanism (`com.xian.pm-cio-cycle`,
`7 10,16,22 * * *`) keeps its schedule; Pard is disarming it only for the duration of onboarding
and restoring it once a transcript confirms the new session is working. Next fire is 16:07 today
regardless of how long onboarding takes. Sourced from `origin/main` at commit `ded374e66d`, not
from chat history — treat this as the bridge, not a summary of a transcript you can still see.

## Who you are and what you own

You are **CIO (Chief Innovation Officer)** for the Piper Morgan agent cohort. Worktree
`~/Development/piper-morgan-worktrees/cio` (Model A, stable, reused every session — see CLAUDE.md
§"Worktree model"), branch `claude/cio-cycle`, upstream `origin/main`. Role briefing:
`docs/briefing/BRIEFING-ESSENTIAL-CIO.md`. Session-log slug: `cio-code`.

You own: the **methodology corpus** (`docs/internal/development/methodology-core/`, currently
through **m-55**, index at that directory's `INDEX.md`), the **duty-cycle continuity
infrastructure** (`.claude/skills/duty-cycle-tick/SKILL.md`, currently v1.41, plus
`scripts/duty-cycle-freeze-check.sh`, `scripts/duty-cycle-heartbeat.sh`,
`dev/active/duty-cycle-registry.tsv`), and the CIO-domain standing-items tracker
(`dev/active/cio-standing-items.md`) and carry-forward (`dev/active/cio-carry-forward.md`) — read
both before doing anything else. The carry-forward's own `currency_claim` frontmatter says it's
current within 1 day; check that claim rather than trust it blind
(`python3 scripts/check-refresh-promises.py --state-files cio`).

## What actually changed today, in order

1. **Migrated off session-scoped `CronCreate` onto Pard's boot-persistent LaunchAgent** (this was
   2026-09-25, not today, but it's the reason today's restart has no cron-management ritual at
   all — see the "⚠️ Cron mechanism gate" at the top of the `duty-cycle-tick` skill, which tells a
   LaunchAgent seat to skip every `CronList`/`CronCreate`/`CronDelete` step in the procedure). You
   are the **first (and, as of this writing, still the only) Piper Morgan seat on this
   mechanism** — 10 of 11 roles still depend on the session-cron prose the gate is additive to,
   so don't delete it if you ever touch that skill; the real removal trigger is full-cohort
   migration or a PM/Pard ruling, not "it's moot for me now."
2. **Just committed 7 weeks of previously-untracked probe data**
   (`dev/active/probe-userpromptsubmit-cio.log`, commit `91de32a7a6`), triggered by Pard's
   restart-readiness check flagging it as a live instrument log held by nothing but the
   filesystem. It was never actually gitignored — `git check-ignore` returns no match — despite my
   own 2026-08-05 and 2026-08-11 session logs both describing it as "gitignored scratch." That
   description was wrong from the start; nobody had reason to check it until a restart made the
   untracked state actually dangerous. **Two follow-ups I deliberately did NOT resolve today**,
   named rather than silently dropped: (a) whether the file's permanent home should move out of
   `dev/active/` (sprint-cleaned territory) to somewhere durable by convention, not just by
   accident of never having been swept yet; (b) whether the probe itself (`.claude/hooks/
   PROBE-userpromptsubmit.sh`, wired via the untracked, seat-local `.claude/settings.local.json`)
   should keep running — its own pre-registered research question (does `UserPromptSubmit` fire,
   does a seat-local hook load without restart) was answered same-day on 2026-08-05, and everything
   since has been unplanned bonus data, not active research.
3. **This handoff.**

## What's genuinely in flight

- **Usage throttle, in effect through Monday** (PM, relayed by Exec, 2026-09-26 ~05:4x): cut
  idle/baseline fire frequency ~40-50%, hold non-essential subagent dispatches/audits/big synthesis
  passes, consolidate broadcasts into fewer denser sends. My own cadence (3x/day) already
  complied without change. **Check whether this has lifted** before resuming any non-essential
  work pattern — it was still in force as of this morning's 10:07 fire (re-verified against
  `docs/internal/architecture/decisions/decisions.log`, nothing suggesting an early lift).
- **Standing item 8c** (`dev/active/cio-standing-items.md`) — a real design ruling on the
  freeze-watchdog's liveness signal (keep heartbeat/last-invoked as the sole required gate; add a
  corroborating check that names a stale-reading-with-recent-real-commits as a likely
  marker-mechanism failure, not a flat "assume stopped"). Ruled 2026-09-26, **implementation
  deliberately deferred to Monday**, named explicitly per the throttle. Not started. This is the
  first thing to pick up once the throttle lifts or Monday arrives.
- **Standing item 8b** (Agent 360 v0.5, HOST's cohort-wide survey) — window ~2 weeks, targets
  ~2026-10-09, not urgent.
- **The Opus 5.5 trial sequencing itself is a live discrepancy worth knowing about, not resolving
  for you**: my own carry-forward (written this morning, before this restart) said "arch first,
  then cio" and cited Arch's 06:27 today-log as evidence Arch's own restart hadn't happened yet.
  Pard's restart message to me, later the same morning, says I'm "next in the PM batch" without
  confirming Arch went first. I did not re-verify Arch's status before writing this doc — if you
  want to know whether Arch is also on `claude-opus-5-5` yet, check Arch's own today-log directly
  rather than assume either framing.
- **Fleet-wide git-attribution incident** (Pard's shared-`user.name`-config bug, 2026-09-25/26,
  231 misattributed commits across the cohort, reverted, history not rewritten) — closed on my
  side, zero dependency found in any script I own. No follow-up needed.
- No standing item is sitting unblocked-and-un-actioned — every active row in
  `cio-standing-items.md` carries a named blocker or an explicit named-trigger deferral as of
  yesterday's fire, re-verified this morning. Read that file's "Genuinely still open" table
  directly rather than re-derive it here.

## Cohort facts easy to get wrong from a cold read

- **`mailboxes/pard/` is gravestoned — `mail-send.sh` hard-refuses writing there.** Pard's real
  inbox is `~/Development/mediajunkie/docs/mail/`, outside this repo. To reach Pard, address `to:
  pard` in the memo header and deliver to `mailboxes/exec/inbox/` — Exec relays externally. I
  mistakenly wrote directly to the gravestoned path twice in the weeks before this doc (caught and
  deleted both times before it reached `mail-send.sh`); the mistake is easy to make because the
  path *looks* like every other role's mailbox.
- **Cc discipline**: PM is cc'd only when a memo (a) contains a decision only PM can make, (b)
  relays a ruling of PM's, or (c) contains something PM would want to contradict — not by default
  "to be safe." Everything else reaches PM through the attention rollup.
- **Bearer credentials (invite codes, API keys, tokens) never appear in full anywhere in this
  repo** — it's public. Masked form only (`ZVHW…8B35`). `scripts/mailbox_bearer_lint.py` gates on
  this now; don't rely on remembering the rule, the gate will catch it, but don't test it either.
- **`gh run list`/`gh project item-list` can return a transiently-stale result without erroring**
  — sanity-check the returned timestamp, don't trust a non-erroring call as current data by
  default. Observed and re-tested multiple times in September; reads as GitHub-side read-path lag,
  not a flag-specific bug.
- **The two-consecutive-empty-rounds rule for exiting a duty-cycle fire to idle** is PM's own
  16-state-table formalization (2026-09-22) — one clean pass through mail+tasks+criteria-line is
  NOT enough; you need the round you just finished AND the round before it both empty. This is in
  `duty-cycle-tick`'s Step 3 point 5 if you need the exact table.

## How this seat specifically gets things wrong — read this twice

These are my own repeat errors, named so a successor (or a restarted me) recognizes the shape
before repeating it:

- **I described a file as "gitignored scratch" in a session log without ever running
  `git check-ignore` on it, and the claim silently propagated across two more session logs and
  seven weeks before anyone checked it.** This is exactly what today's probe-log decision caught.
  The generalizable lesson: a claim about a file's git status is checkable in one command — run
  it, don't reuse your own prior prose as if re-stating it were the same as re-verifying it. This
  is CLAUDE.md's "never guess at facts you can look up" rule, but the specific trap is trusting
  *yourself* from weeks ago rather than an external source — self-citation reads as more reliable
  than it is.
- **I've twice written directly to `mailboxes/pard/inbox/`** despite having built the hard-refuse
  guard myself the day before the first mistake. Both times caught before the write reached
  `mail-send.sh`. The pattern: muscle memory for "write to mailboxes/{role}/inbox/" is stronger
  than remembering a specific path is special-cased, even right after building the special case.
  If you're about to write to any role's mailbox, glance at the path once more before the write,
  not just once when you decided who to address.
- **I once began executing a destructive plan (deleting the cron-management prose from a
  cohort-shared skill) that I had explicitly promised Pard/Exec/PM in mail, before catching
  mid-edit that 10 of 11 seats still depended on the content I was about to delete.** Course-
  corrected to an additive gate instead, and rewrote the pending reply to describe what I actually
  did rather than send the already-drafted inaccurate version. The lesson: a promise made in mail
  is not a reason to skip re-verifying the promise's premise at execution time, especially when
  the premise ("my seat's situation generalizes to the whole cohort") is the exact kind of claim
  that ages fastest.

## Verified how

Every claim above about today's changes is sourced from this session's own actions on
`origin/main` — commit `91de32a7a6` (probe log), the `duty-cycle-tick` skill's own "Cron mechanism
gate" section (re-read in full this session after a compaction), and
`dev/active/cio-carry-forward.md` / `dev/active/cio-standing-items.md` as they stood as of this
morning's 10:07 fire, re-verified against `decisions.log` and Arch's own today-log rather than
trusted as-written. The Opus-5.5-sequencing discrepancy is stated as a discrepancy, not resolved,
because I did not re-check Arch's status after receiving Pard's message — an honest gap, not an
oversight glossed over. I have not independently verified Pard's restart-mechanism claims about
other `.claude-pm` seats (Janus, Themis, Coral) — those are Pard's own report, quoted, not
reproduced.

— CIO, 2026-09-27
