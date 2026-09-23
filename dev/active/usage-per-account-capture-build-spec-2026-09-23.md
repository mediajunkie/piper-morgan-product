# Usage-per-account capture — build spec (outcome-oriented)

**Author**: PA. **Filed**: 2026-09-23. **Status**: SPEC — for a `prog` subagent to build against.
PM ruled 09-22 (re-confirmed 09-23): build Lead's proposal via PA-written spec + subagent, not
diverting Lead. Implements `dev/active/usage-per-account-capture-2026-09-19.md` (Lead's proposal)
now that its two named unknowns are closed by Pard (mediajunkie, 09-23 — memo in
`mailboxes/pa/read/answer-pard-to-pa-...-2026-09-23.md`).

## Outcome (what "done" means, in one sentence)

A repo-tracked TSV that, for each of the two Anthropic accounts this cohort draws on, carries one
honest row per reading of the account's actual usage percentage — written by a mechanism outside
the seats it measures, and readable by anyone triaging a silent role ("was the account at the
ceiling when this seat went quiet?").

## The two facts this build rests on (verified by Pard, not assumed)

1. **Where the number lives**: `GET https://api.anthropic.com/api/oauth/usage`, the same
   unpublished endpoint the CLI's `/usage` screen calls, bearer-authed with the account's OAuth
   token from the login keychain. Pard's reader already does this:
   `~/Development/mediajunkie/scripts/usage-read.sh [config-dir]` → one TSV line
   `config_dir ⇥ 5h% ⇥ 5h_reset ⇥ 7d% ⇥ 7d_reset`, or `UNREADABLE` (no credential) /
   `UNMEASURABLE` (endpoint shape changed). **Reuse it. Do not re-implement the endpoint call.**
2. **Seat→account mapping is a function of `CLAUDE_CONFIG_DIR`, not seat name**:
   `~/.claude-pm` → pipermorgan.ai account (**all 11 PM seats**, week resets Thu 22:00 PT);
   `~/.claude` → designinproduct.com account (Pard, Janus, and the small projects, week resets
   Wed 21:00 PT). So there are exactly **two rows per reading**, not one per seat.

## Deliverables

### D1 — the surface: `dev/heartbeats/usage-per-account.tsv`

Append-only, tab-separated, header row first. Columns (Lead's shape, extended with the two
windows the endpoint actually exposes — capture what is read, don't derive):

```
ts_local	account	config_dir	five_hour_pct	five_hour_reset	seven_day_pct	seven_day_reset	source	note
2026-09-23 11:1x PDT	pipermorgan.ai	~/.claude-pm	5	2026-09-23T22:20	100	2026-09-25T05:00	usage-read.sh	
2026-09-23 11:1x PDT	designinproduct.com	~/.claude	14	2026-09-23T21:00	88	2026-09-24T04:00	usage-read.sh	
```

- `account` is the human label (the two above, fixed); `config_dir` is the machine key.
- A failed read still writes a row: `five_hour_pct`=`UNREADABLE` or `UNMEASURABLE` verbatim from
  the reader, remaining numeric columns empty, `note` carries the reader's reason text. **Silence
  must be diagnostic** — an absent row and a failed read must not look the same (same G6
  principle as `duty-cycle-heartbeat.sh`).
- `source` is `usage-read.sh` for automated rows, `xian-manual` for hand-pasted ones (Lead's
  fallback, kept — the endpoint is unpublished and may change shape).
- **Size**: 2 rows/reading × ~1–4 readings/day ≈ <3k rows/year. A single file is fine; note the
  reason in the file's header comment so the next reader doesn't "fix" it into per-day rotation
  without cause. If cadence ever exceeds hourly, rotate then — not now.
- **A one-time `account ⇥ seats` companion block** at the bottom of the same file (Lead's ask),
  as a `#`-prefixed comment block: `pipermorgan.ai: arch cio comms cxo docs exec host lead pa
  ppm web (all via CLAUDE_CONFIG_DIR=~/.claude-pm)` / `designinproduct.com: pard janus + small
  projects (~/.claude)`. Readers of the TSV must skip `#` lines.

### D2 — the writer: `scripts/usage-capture.sh`

```
scripts/usage-capture.sh [--reader PATH] [--dry-run]
```

- For each of the two `(account, config_dir)` pairs, call the reader (default
  `~/Development/mediajunkie/scripts/usage-read.sh`, overridable for tests), parse its one line,
  append one row to D1. Read at call time, never cache the token (it rotates); never print it.
- Exit non-zero if the reader is missing entirely (that's a setup fault, distinct from a read
  fault — say which). A read fault (`UNREADABLE`/`UNMEASURABLE`) is **recorded, not fatal** —
  exit 0 after writing the failure row, so a cron driver doesn't treat it as a crash.
- Commit + push the appended row(s) to `origin/main` from whatever checkout it runs in, staging
  **only** that one path (explicit-path discipline; never `git add -A`). Mirror how
  `duty-cycle-heartbeat.sh` handles its own commit — read that script first and follow its
  pattern rather than inventing one.
- `--dry-run` prints the rows it would append and touches nothing.

### D3 — who runs it, and from where (the structural constraint — do not skip this)

Lead's proposal is explicit and correct: **a seat refused at the ceiling can't write anything,
so the writer must sit outside the refused set.** That rules out driving this from any PM seat's
`CronCreate` (session-scoped, dies with the session, and the session is exactly what the ceiling
kills). The driver is a **real system crontab entry on Amber** (or Pard's equivalent), same
posture as the cohort-freeze watchdog's "watcher outside the frozen set."

The subagent **does not install the crontab entry** — that's a host-level change and is
Pard's/PM's to make. The subagent delivers: the script, a tested invocation, and a
ready-to-paste crontab line in the script's header comment (suggested cadence: every 3 hours,
off-minute — e.g. `23 */3 * * *` — matching "daily, more often near a ceiling" from Lead's
proposal without polling). PA hands the line to Pard by mail after the build lands.

### D4 — the reader-side lookup (small, and the reason the surface exists)

`scripts/usage-lookup.sh <YYYY-MM-DD HH:MM> [account]` — prints the most recent row at or
before the given timestamp for the account (default: pipermorgan.ai). This is the one-line answer
to "was the account near ceiling when seat X went quiet?" that the 09-14 incident took a forensic
reconstruction to get. Keep it to that; do **not** wire it into `duty-cycle-freeze-check.sh` in
this build — that integration is a separate, CIO/HOST-owned decision about the watchdog's
output, and this spec's job is to make it a one-line change for them, not to make it.

### D5 — tests: `scripts/test-usage-capture.sh`

Mirror `scripts/test-duty-cycle-freeze-check.sh`'s style. Use `--reader` to point at a stub
that emits (a) a good line for each account, (b) `UNREADABLE`, (c) `UNMEASURABLE`, (d) garbage.
Assert: correct rows appended for (a); failure rows with reason text for (b)/(c); non-zero exit
and no row for a missing reader; (d) lands as `UNMEASURABLE`, never as a plausible number.
`--dry-run` appends nothing. `usage-lookup.sh` returns the right row for a timestamp between two
readings and says `NO-ROW` (not empty output) before the first.

## Acceptance criteria

- [ ] D1 exists with header, comment block, and at least one real row per account captured by
      running D2 live once from the subagent's own shell (this is the "Verified how" line).
- [ ] D2 handles all four reader outcomes as specified; token never appears in any output or
      the git history (grep the diff before committing).
- [ ] D3 crontab line is in the script header and is **not** installed.
- [ ] D4 works on the live file; `NO-ROW` case tested.
- [ ] D5 passes, output pasted into the closure evidence.
- [ ] No changes outside `scripts/usage-capture.sh`, `scripts/usage-lookup.sh`,
      `scripts/test-usage-capture.sh`, `dev/heartbeats/usage-per-account.tsv`, and the
      subagent's own session log. Anything else discovered → file an issue, don't fix in-band.

## Explicitly not in scope (Lead's list, unchanged)

Automated enforcement, per-request metering inside Piper, any change to model-pinning policy,
installing the crontab, and integrating the lookup into the watchdog's output.

**Verified how (for this spec)**: Lead's proposal and Pard's answer both read in full this fire;
the reader's source (`usage-read.sh`, 2026-09-23 11:10) read directly, including its keychain
service derivation and its two failure modes; `dev/heartbeats/` layout and
`duty-cycle-heartbeat.sh`'s size-discipline rationale (lines 35–39) read to decide the
single-file-vs-rotation question rather than guess it. `dev/heartbeats/usage-per-account.tsv`
confirmed absent before writing this (`ls`, exit 1) — nothing pre-existing to complete.
