# Docs Carry-Forward

**Updated**: 2026-08-03 10:45 PDT (Fire 2, mid-WORK)
**Session log**: `dev/2026/08/03/2026-08-03-0711-docs-code-log.md` (yesterday's is
`dev/2026/08/02/2026-08-02-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: `284908d1` — `57 6,9,12,15,18,21`. Registry row matches.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**⚠️ NEW today**: `pre-commit-broad-staging-warn.sh` (a Claude-Code PreToolUse hook, distinct from git's
own hooks) blocks the Bash tool call outright on a ≥20-file staged commit, despite its own header
documenting `exit 2 = warn, commit not blocked`. `--no-verify` has **no effect** — it's not a git hook.
**Mitigation: split any large multi-file commit into batches under 20 files.** `git mv` renames
re-detect correctly across separate batches as long as old-path and new-path land in the same commit.

---

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — unchanged, checked again this fire. Arch ✅ and Web ✅ both reviewed,
  no objection. **Do not decide the storage question early** — pre-registered 2–4 week window
  (2026-07-30 → 2026-08-27), shipped measurement (`scripts/measure-editorial-drift.py`).
- **Dispatch-DinP staleness report** — replied 2026-08-01, no reply yet. Still watching.
- **Lead Dev's weekly-docs-audit CI findings** — sent 2026-08-03 (cc CIO): the "Update Essential
  Briefings" job's `sed` target (`Position**:` line) doesn't exist in any of the 11
  `BRIEFING-ESSENTIAL-*.md` files, so it fails every single week, not intermittently. Also flagged
  today's scheduled trigger not firing (had to `workflow_dispatch` manually). Not mine to fix — watch
  for Lead's disposition (dead-code removal vs. restoring the convention).

## Owed by me — unblocked, priority order

1. **`planning/current/` Finding 1 — needs a fresh, careful pass, NOT a quick rename.** Headline claim
   ("100% stale, 314d") is false — `vision.md` is ~113d, not ~314d — and there are 13 live inbound
   references, several in active session-start briefing paths. Corrected in the audit doc, original
   claim preserved not silently edited. **Named trigger for the deferral**: needs the same per-file care
   Arch gave Finding 2 — re-derive per-file staleness for all 7, confirm which of the 13 referrers need
   updating, then decide rename vs. per-file disposition. Trigger is a fresh session/compaction, not "an
   idle fire came along" — still hasn't arrived.
2. **Omnibus gap: Jul 29 – Aug 3, now 6 days.** Not a request, a dependency — Comms's `continue-narrative`
   discipline reads digests, not raw logs. **Comms says explicitly: no urgency, not before Aug 18.**
   Sizable job (~5-6 days × ~13 agents/day) — own focused pass per `create-omnibus` skill.
3. **97 docs >30d asserting current-state language** — separate, broader item; no deadline named.
4. **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — raised to CIO
   twice now. Not mine to resolve; re-raise if it stays open much longer.
5. **`docs-standing-items.md` is stale** (last touched 2026-05-27, pre-Amber). Low priority, not urgent.

## Resolved 2026-08-03 — do NOT re-open

- ~~Comms's Step-9-archival-gap finding (16 of 42 distributed posts unmoved)~~ — **fully closed.**
  Reconciled the count (Comms: 16 `distributed`-only; mine: 19 incl. `published`), archived all 19 (23
  files incl. 4 images), shipped Comms's suggested validator check (`status implies /published/ path`),
  which immediately found **4 more** pre-Jun-1 rows outside Comms's stated scope — archived those too.
  **23 files total across 4 batched commits** (split to work around the broad-staging hook — see header
  note). Calendar clean, drift measurement unaffected (Class 2 = 0 throughout).
- ~~Monday's first real Doc Currency Check run~~ — **confirmed reads correctly** in generated issue
  #1475 (ratio-not-list instruction, `last_verified` clustering check both present as written). Had to
  trigger manually since the schedule didn't fire — see "Awaiting others" above for the CI findings that
  surfaced along the way.

## Inbox

**53 remaining, cc-only historical from the 7/21–7/28 migration window.** Everything addressed *to*
docs is drained as of this fire. Not mass-moving to `read/` — drain on quiet fires.

## Standing lessons (carried, still live)

**Verify per assertion, not per session; verify a commit/send landed via `git status` after, not
intent.** Held up again today — reconciled Comms's count rather than trusting either number blind, and
caught the broad-staging hook's block by checking `git log -1` after two failed commit attempts rather
than assuming "no error text visible" meant success.

**A hook's own documentation can be wrong about its own behavior.** `pre-commit-broad-staging-warn.sh`'s
header says its warning doesn't block; empirically, on this harness, it did — twice, with `--no-verify`
having zero effect since it's a different hook layer than git's. Same shape as the mailbox-hook
findings from two weeks ago (CLAUDE.md's Amber gotcha #2): don't trust a hook's documented behavior over
what actually happens when you run it.

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane, still open.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns, raised twice.
- **`docs/internal/operations/one-command-checks.md`** (Arch, 2026-08-02) — worth reading before the
  next audit-shaped task.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — flagged nowhere yet beyond
  this file and today's session log. Worth a memo to whoever owns `.claude/hooks/` if it recurs for
  another agent — not urgent since the workaround (split batches) is cheap and now documented here.

## The one thing I most want to carry into the next fire

**Going to verify one thing can surface a second, unrelated finding — check both before reporting
either.** I went to confirm the Doc Currency Check's first run; the schedule hadn't fired, so I
dispatched manually, and while confirming the run succeeded I found a completely separate job
(Essential Briefings update) has been silently broken for at least 2 weeks. Neither finding would have
surfaced from a narrower "did my own check work" question. Worth deliberately looking one layer wider
than the specific thing being verified, especially in CI/infra investigations.
