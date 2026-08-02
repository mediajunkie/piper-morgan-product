# Docs Carry-Forward

**Updated**: 2026-08-02 07:50 PDT (Fire 1, mid-WORK)
**Session log**: `dev/2026/08/02/2026-08-02-0727-docs-code-log.md` (yesterday's is
`dev/2026/08/01/2026-08-01-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: `efd5b41e` — `57 6,9,12,15,18,21`. Registry row matches (updated Fire 1).
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**⚠️ main is busy today** — 2 of 4 pushes this fire were rejected non-fast-forward and needed
`git fetch + git rebase origin/main` before re-push. Expect this; don't skip the post-push verify.

---

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — unchanged, checked this fire. Arch ✅ and Web ✅ both reviewed, no
  objection. **Do not decide the storage question early** — pre-registered 2–4 week window
  (2026-07-30 → 2026-08-27), shipped measurement (`scripts/measure-editorial-drift.py`).
- **Arch's ADR-070 supersession note** — I gave the go-ahead 2026-08-02 (Fire 1). Holding the 4
  PM-033/034-era files (`pm-033a-mcp-consumer-architecture`, `pm034-deployment-guide`,
  `mcp-integration-points`, `mcp-integration-mapping`) until Arch's note lands, per Arch's own gate.
  **Watch for it** — once it's in, archive those 4 the same way as the other 8 (banner + move to
  `docs/internal/architecture/archive/`, verify zero-inbound first).
- **Dispatch-DinP staleness report** — replied 2026-08-01, no reply yet as of this fire. Still watching.

## Owed by me — unblocked, priority order

1. **`planning/current/` Finding 1 — needs a fresh, careful pass, NOT a quick rename.** Re-derived
   staleness 2026-08-02 before acting (per the audit's own "re-run before acting" rule) and found the
   headline claim ("100% stale, 314d") is false: `vision.md` was touched 2026-04-11, ~113d not ~314d.
   Also found **13 live inbound references**, several in active session-start briefing paths
   (`BRIEFING-CURRENT-STATE.md`, `BRIEFING-piper-alpha.md`, `BRIEFING-ESSENTIAL-CHIEF-STAFF.md`,
   `BRIEFING-ESSENTIAL-PPM.md`, `ppm-code-startup.md`) — more than the audit's proposal assumed a rename
   would touch. Corrected in the audit doc (`90f80c6ec`→rebased), original claim preserved not silently
   edited. **Named trigger for the deferral**: this needs the same per-file care Arch gave Finding 2, not
   end-of-fire mechanical work — re-derive per-file staleness for all 7, confirm which of the 13
   referrers actually need updating, then decide rename vs. per-file disposition.
2. **97 docs >30d asserting current-state language** — separate, broader item; no deadline named.
3. **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — raised to CIO
   twice now. Not mine to resolve; re-raise if it stays open much longer.
4. **`docs-standing-items.md` is stale** (last touched 2026-05-27, pre-Amber). Low priority, not urgent.
5. **Monday (2026-08-03) — first real run of the Doc Currency Check** added to the weekly audit. Watch:
   does the ratio read legibly, does the `last_verified` cluster check surface correctly.

## Resolved since 2026-08-01 STOP — do NOT re-open

- ~~8 of 16 tree-audit Finding-2 files archived~~ — done 2026-08-02 (`markdown-formatting-analysis`,
  `file-scoring-algorithm`, `inchworm-execution-plan`, `github-issue-sequence-diagram`,
  `entity-relationship-diagram`, `spacing-system`, `python-environment-specifications`,
  `current-state-documentation`), each with a context banner, `docs/internal/architecture/archive/`.
  4 consciousness docs linked in `NAVIGATION.md` (Arch-ruled KEEP, live subsystem). `scripts/
  setup_mcp_dev.sh`'s 3 broken doc pointers fixed. A real `.gitignore` landmine caught and fixed in the
  same pass — `archive/` bare pattern would have silently swallowed any NEW file dropped in the new
  architecture-archive destination; scoped negation added. 4 remaining MCP-cluster files gated on Arch's
  ADR-070 note (go-ahead given, watching for it).
- ~~CIO worktree-model-revision ack (07-25)~~ — sent 2026-08-01.
- ~~13 `to: docs` inbox items (2026-08-01 + 2026-08-02 combined)~~ — all triaged, verified individually.

## Inbox

**~50 remaining, cc-only historical from the 7/21–7/28 migration window.** Everything addressed *to*
docs is drained as of this fire. Not mass-moving to `read/` — drain on quiet fires, as before.

## Standing lessons (carried, still live)

**Verify per assertion, not per session.** Two more instances 2026-08-01, both self-inflicted process
slips rather than factual errors, both caught the same way — reading `git status` after acting rather
than trusting a command matched intent: (1) a bad pathspec silently aborted a `git add`, landing a commit
with 0 real diff while the message claimed the calendar update; (2) a `mail-send.sh` call included the
new (moved-to) paths for 9 triaged memos but not the old (moved-from) inbox paths, leaving them showing
as uncommitted after a "successful" send. **The fix in both cases was the same habit**: don't read a
commit or send as done until `git status --short` confirms it.

**Cross-agent staleness diagnosis discipline (new, 2026-08-01)**: when another agent reports "the repo is
stale," don't take the framing at face value — walk the actual commit history against the timeline they
describe before agreeing there's a repo-side defect. This time the repo was fine; the read path wasn't.
Worth remembering the inverse is just as possible — a future report like this could be a genuine repo
defect, and the discipline is "check," not "assume it's always the reader's checkout."

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane, still open. Three hypotheses dead.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns, raised twice.
- **`sync-pm-local.sh`'s opportunistic cadence** — surfaced today as the likely root cause of Dispatch's
  staleness report. Not proposing a change to it (its deliberate design tradeoff is documented and
  sound for PM's own workflow) — flagging only that any other consumer reading that same checkout
  inherits the same freshness gap, and won't know it unless told, as Dispatch now has been.

## The one thing I most want to carry into tomorrow

**A correct diagnosis beats a fast apology.** Dispatch's report could have been answered with "sorry,
we'll fix the sync" — instead, five minutes of `git log` on the actual file turned a vague "something's
stale somewhere" into an exact commit, an exact timestamp, and a specific likely mechanism. That's the
same discipline as "open the authoritative surface" one layer up: don't just open my own authoritative
surface, open the one the *claim* is about before agreeing with it.
