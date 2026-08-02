# Docs Carry-Forward

**Updated**: 2026-08-01 22:40 PDT (Fire 7, STOP — DAY-CLOSED 2026-08-01)
**Session log**: `dev/2026/08/01/2026-08-01-0727-docs-code-log.md` (yesterday's is
`dev/2026/07/31/2026-07-31-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: re-arming `774c7afe` → new id at STOP (delete-then-create; see final action) —
`57 6,9,12,15,18,21`. Registry row must match.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.

---

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY.** Arch ✅ and Web ✅ both reviewed, no objection. **Do not decide the
  storage question early** — pre-registered 2–4 week window (2026-07-30 → 2026-08-27), shipped
  measurement (`scripts/measure-editorial-drift.py`). Last run 2026-08-01 (post-archival, unaffected):
  Class 2 = 0 (criterion 0), Class 3 = 17 (criterion ≤17), 367 matched rows.
- **docs/ tree audit routed to Arch 2026-08-01** (`docs/internal/operations/docs-tree-audit-2026-08-01.md`).
  Arch acknowledged same day, took it as **first item at 06:27 tomorrow** (2026-08-02), named the trigger
  explicitly rather than rushing 16 per-file dispositions at day-close. Not mine to act on further unless
  Arch asks; audit itself is written, nothing more owed from me.
- **Dispatch-DinP staleness report — replied 2026-08-01**, diagnosis sent to
  `~/Development/dispatch/mail/`. Root cause: their read checkout (`~/cool/piper-morgan-product`, PM's
  shared main checkout) is synced to `origin/main` only opportunistically via `scripts/sync-pm-local.sh`,
  not on every push — so a read against it has no freshness guarantee. Not a repo defect; the repo (via
  `origin/main`) had the clean content hours before the cross-post. Suggested fix: sync immediately
  before reading, same discipline this project already applies at `publish-to-blog` Pre-Step and
  `duty-cycle-tick` Step 2. **Watch for Dispatch's reply** — if they confirm/deny the mechanism, that's
  worth a follow-up note either way (confirms a real systemic gap, or rules it out and reopens the
  question of what actually happened).

## Owed by me — unblocked, priority order

1. **97 docs >30d asserting current-state language**; `docs/internal/planning/current/` is itself a
   misleading directory name (oldest items 314d — surfaced precisely by the tree audit, same finding,
   different angle). No deadline named.
2. **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — raised to CIO
   twice now (predecessor's unit mismatch + my contradiction). Not mine to resolve; re-raise if it stays
   open much longer.
3. **`docs-standing-items.md` is stale** (last touched 2026-05-27, pre-Amber — references items and a
   task-list model that predate the current carry-forward-as-source-of-truth discipline). Noted 2026-08-01
   Fire 7, not acted on. Low priority: either refresh it to reflect the current architecture or fold its
   still-live threads (#974 mem-eval pilot, #972 mem-temporal field-spec) into the carry-forward and
   retire the file. Not urgent — nothing in it is currently misleading anyone but me.
4. **Monday (2026-08-03) — first real run of the Doc Currency Check** added to the weekly audit. Watch:
   does the ratio read legibly, does the `last_verified` cluster check surface correctly.

## Resolved since 2026-07-31 — do NOT re-open

- ~~"Mechanism Beats Vigilance" publish + syndication~~ — **fully closed 2026-08-01.** Voice-pass proof,
  published, Medium + LinkedIn both set, archived to `published/`/`images-archive/`, draftPath repointed.
  Drift measurement clean.
- ~~CIO worktree-model-revision ack (07-25)~~ — sent 2026-08-01, a week late but sent.
- ~~9 `to: docs` inbox items (2 Comms, 1 Arch, 1 CIO, 2 Dispatch, 1 Web, 1 Exec, 1 self-handoff)~~ —
  triaged 2026-08-01 Fire 7; verified each individually before filing, not assumed from subject line.

## Inbox

**~51 remaining, cc-only historical from the 7/21–7/28 migration window.** Everything addressed *to*
docs is drained as of Fire 7. Not mass-moving to `read/` — drain on quiet fires, as before.

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
