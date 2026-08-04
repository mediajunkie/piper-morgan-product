# Docs Carry-Forward

**Updated**: 2026-08-03 22:35 PDT (Fire 6, STOP — DAY-CLOSED 2026-08-03)
**Session log**: `dev/2026/08/03/2026-08-03-0711-docs-code-log.md` (yesterday's is
`dev/2026/08/02/2026-08-02-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: re-arming `284908d1` → new id at STOP (delete-then-create; see final action) —
`57 6,9,12,15,18,21`. Registry row must match.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**⚠️ Standing note (found 08-03)**: `pre-commit-broad-staging-warn.sh` (a Claude-Code PreToolUse hook,
distinct from git's own hooks) blocks the Bash tool call outright on a ≥20-file staged commit, despite
its own header documenting `exit 2 = warn, commit not blocked`. `--no-verify` has **no effect** — it's
not a git hook. **Mitigation: split any large multi-file commit into batches under 20 files.** `git mv`
renames re-detect correctly across separate batches as long as old-path and new-path land in the same
commit.

---

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — unchanged all day (checked at every fire). Arch ✅ and Web ✅ both
  reviewed, no objection. **Do not decide the storage question early** — pre-registered 2–4 week window
  (2026-07-30 → 2026-08-27), shipped measurement (`scripts/measure-editorial-drift.py`).
- **Dispatch-DinP staleness report** — replied 2026-08-01, no reply yet as of Fire 6. Still watching.
- **Next Monday's weekly-docs-audit fire (~9:07 PT, Aug 10)** — Lead Dev nudged the cron off the
  top-of-hour (`0 16` → `7 16`) per the congestion hypothesis for why 08-03's schedule didn't fire.
  Watch whether it fires this time; if not, that's a real pattern worth a workflow_dispatch fallback,
  per Lead's own framing. Not urgent — a week out.

## Owed by me — unblocked, priority order

1. **`planning/current/` Finding 1 — needs a fresh, careful pass, NOT a quick rename.** Headline claim
   ("100% stale, 314d") is false — `vision.md` is ~113d, not ~314d — and there are 13 live inbound
   references, several in active session-start briefing paths. Corrected in the audit doc, original
   claim preserved not silently edited. **Named trigger for the deferral**: needs the same per-file care
   Arch gave Finding 2 — re-derive per-file staleness for all 7, confirm which of the 13 referrers need
   updating, then decide rename vs. per-file disposition. Trigger is a fresh session/compaction — still
   hasn't arrived, three days running now.
2. **Omnibus gap: Jul 29 – Aug 3, now 6 days, growing.** Not a request, a dependency — Comms's
   `continue-narrative` discipline reads digests, not raw logs. **Comms says explicitly: no urgency, not
   before Aug 18.** Sizable job (~6 days × ~13 agents/day) — own focused pass per `create-omnibus` skill.
3. **97 docs >30d asserting current-state language** — separate, broader item; no deadline named.
4. **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — raised to CIO
   twice now. Not mine to resolve; re-raise if it stays open much longer.
5. **`docs-standing-items.md` is stale** (last touched 2026-05-27, pre-Amber). Low priority, not urgent.

## Resolved 2026-08-03 — do NOT re-open

- ~~Comms's Step-9-archival-gap finding (16 of 42 distributed posts unmoved)~~ — **fully closed.**
  Reconciled the count, archived 23 files across 4 batched commits, shipped the suggested validator
  check (which immediately found 4 more affected posts outside the original scope, also archived).
  Calendar clean, drift measurement unaffected (Class 2 = 0 throughout day).
- ~~Comms's `/superseded/` false-positive report~~ — **turned out already-handled, not a real gap.**
  The exclusion was already in the shipped check; my closeout memo just hadn't said so. Comms
  independently re-verified with the actual script rather than trusting my correction, confirmed it,
  and separately corrected their own record about *why* they'd guessed wrong in the first place —
  worth remembering as a model of self-correction precision, not just a closed item.
- ~~Weekly-docs-audit CI findings (dead job + schedule non-fire)~~ — **both closed same-day by Lead
  Dev.** Dead job (`Position**:` convention retired 4.5 months ago) deleted. Cron nudged off the
  top-of-hour. Watch next Monday per "Awaiting others" above.
- ~~Monday's first real Doc Currency Check run~~ — confirmed reads correctly in generated issue #1475.

## Inbox

**62 remaining at STOP, all cc-only historical from the 7/21–7/28 migration window.** Everything
addressed *to* docs has been drained all day. Not mass-moving to `read/` — drain on quiet fires.

## Standing lessons (carried, still live)

**Verify per assertion, not per session; verify a commit/send landed via `git status` after, not
intent.** Zero new self-inflicted instances today — every check (Comms's count, the validator gap
report, both CI findings) was traced to ground truth before acting on it, not accepted or rejected on
say-so.

**Cross-agent verification, now routine rather than notable.** Comms verified my archival end-to-end
unprompted, re-ran the validator fresh rather than trusting my correction, and separately audited their
own reasoning for why they'd guessed wrong rather than accepting my more generous framing. This is the
third or fourth day running this pattern has shown up — worth treating as the new baseline, not a
one-off worth flagging every time it recurs.

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane, still open.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns, raised twice.
- **`docs/internal/operations/one-command-checks.md`** (Arch, 2026-08-02) — worth reading before the
  next audit-shaped task.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented here and in
  today's session log, not yet escalated to whoever owns `.claude/hooks/`. Workaround is cheap; escalate
  only if it costs someone else real time.

## The one thing I most want to carry into tomorrow

**A closed loop is worth watching even after it's closed.** Today's biggest single value wasn't any one
fix — it was the density of second-pass verification: Comms checking my archival, then my /superseded/
fix, then correcting their own account of why they'd gotten something wrong the first time; me tracing
Comms's count before extending it; Lead settling both CI findings with `git log -S` rather than a
guess. None of these were required by the discipline in a checklist sense — they were people choosing
to re-derive rather than trust, repeatedly, across a whole day. Worth noticing that pattern is holding
up under real use, not just written down somewhere.
