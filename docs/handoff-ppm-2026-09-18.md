# Handoff — PPM (Principal Product Manager), 2026-09-18

**Written for the Amber restart.** Assume you are a fresh or freshly-compacted PPM session with no
memory of the last month. This file plus `dev/active/ppm-carry-forward.md` is what you have.
Everything here is verifiable from `origin/main`; nothing depends on chat history.

## Who you are and what you own

Principal Product Manager. Owns the MVP epic-order file (what Lead works next, one epic at a time),
board hygiene (milestone/status correctness, board-add gaps), mailbox triage, and issue triage
against precedent. Tier-1 leadership. Worktree `~/Development/piper-morgan-worktrees/ppm`, branch
`claude/ppm-cycle`, Model A. Briefing: `docs/briefing/BRIEFING-ESSENTIAL-PPM.md`.

## Cron

`52 6,9,12,15,18,21 * * *` — six fires/day, 06:00–22:00, last fire (21:52) is STOP. Job `4bcf1e1b`
armed 2026-09-18 11:5x on PM's direct ask to resume after the 09-16→09-18 cohort-wide standdown.
**`CronList` at every fire; it dies silently on session exit and at 7 days.** If zero jobs, re-arm
immediately and note it in the fire entry.

## The single most important thing in flight

**`dev/active/mvp-epic-order-2026-09-09.md`** is the ordered-epics source of truth PM asked for —
one epic at a time, fully closed, before the next. 11 epics as of last touch (2026-09-15 evening).
Epic 2 (Security/tenancy) was closed 2026-09-12, found incomplete two days later, and **reopened**
rather than given a successor epic — PM's direct ruling, see "how this seat gets things wrong" below.

⚠️ **PM has an outstanding, unanswered choice, offered 2026-09-14 evening, still open as of this
write**: epics 9 (Silent-death inventory) and 10 (Composer UX polish) are thin (1-3 items each) —
keep them as epics, or revert to a named short list under a stricter "epic = multi-item track"
definition. **Checked exhaustively before writing this line** (grepped every mailbox, `decisions.log`,
GitHub) — no reply has landed anywhere. Don't chase it; check again before assuming either way.

## State of the milestone

`python3 scripts/sprint-truth.py` is the only legitimate denominator — **run it fresh, never quote
this line as current**. At time of writing: `MVP: 56 not done (33 Sprint Backlog, 3 In Progress,
6 In Review, 14 Product Backlog); 1176 done. PLUS 0 unmilestoned. 33 NOT STARTED.` Identical to the
line Exec's 09-18 closeout memo quoted — nothing moved on the board during the standdown, which
checks out (the whole cohort was dark).

**Watch its "NOT ON THE BOARD" line every fire.** `gh issue create --milestone` does NOT board-add —
hit repeatedly this month (`#1772`, `#1785`, `#1807`, `#1818`), on both open and closed issues. Fix
each time is `gh project item-add`, never a convention change.

## Open items PM is parked on

- **The epics-9/10 choice** (above) — the only live PM-gated item specific to this seat.
- **Scope-guard `#1744`** — both halves built and dispatch-tested; stays open until PM decides
  branch-protection bypass vs. a scoped PAT for the bot's delivery path. Not a PPM call.
- **`#1386`'s beta-gate criteria** — criterion 6 fires at MVP close (`due_on` 2026-10-30, not yet
  due); criteria 2/4/5 all re-run fresh at MVP close (artifact-execution results); only criterion 1
  stands unqualified. Not actionable before MVP close — don't misreport the shape as "one left."
- **`#1818`** (filed 2026-09-15) — a genuine, deliberately-unrushed design question: should a
  zero-cost deterministic greeting pass the `#1807` keyless gate? Needs CXO/Arch to rule, not PPM.

## How this seat gets things wrong — read this part twice

These are mine, earned, and each cost real rework:

- **A month-long mailbox triage bug, repeated after being fixed once.** Triaged mail landed at
  `mailboxes/ppm/inbox/read/` instead of `mailboxes/ppm/read/` — first found and fixed 2026-08-10
  (21 files), and the exact habit resumed the very next day, growing to 188 files by 2026-09-10
  (`#1743`). The lesson: cleaning up an instance is not the same as fixing the cause. The actual
  fix was a CI-enforced nesting-invariant lint (`scripts/mailbox_filename_lint.py`), not a fourth
  manual sweep. **If you catch yourself doing a cleanup for the second time, stop and ask whether
  the fix belongs in a check instead of in your own discipline.**
- **Proposing a new epic instead of reopening a closed one that wasn't actually done.** Created
  "epic 12" (Tenancy hardening) 2026-09-14 to house findings against an already-closed epic 2,
  reasoning it "kept epic 2's closure true for what it contained." PM overruled hours later: *"if
  we discover more work on an epic than we realized and we closed it before discovering that work,
  then yes we need to reopen the epic... the truth is more important than the feeling of progress."*
  **When a closed epic's own scope turns out incomplete, reopen it — a successor epic is a way of
  not saying the first one was wrong.**
- **A wrong close-reason on a real closure** (`#1166`, `not_planned` when the work was actually
  `completed`) — caught and fixed same-fire, but only because I happened to reread my own action
  before moving on. Double-check close-reason against what actually happened, not habit.
- **A `mail-send.sh` cc-without-delivery-path miss** — cc'd roles in a memo's header without also
  passing their actual delivery paths to the send call. The tool warns correctly when this happens;
  the fix is to read the warning and send the missing paths immediately, not to assume the header
  alone delivers anything.
- **Trusting a stale carry-forward line as a live claim.** A carry-forward records state at the
  moment it was last touched, not a live fact (Exec's `decisions.log:1831` finding, 2026-09-06,
  generalizes past their own seat). Before citing anything from `ppm-carry-forward.md` as current,
  check whether the underlying GitHub/board state has actually been re-verified since.

## Cohort facts that are easy to get wrong

- **Leadership is 7** (exec, arch, cxo, ppm, cio, host, comms). **Staff is 4** (lead, pa, docs,
  web). `docs/briefing/ROSTER.md` is the authority.
- **Model allocation, PM 2026-09-18: Fable reserved for Lead Developer; everyone else Opus or
  Sonnet.** Sub-agent dispatches inherit the dispatcher's model unless set explicitly — that
  inheritance exhausted the Fable tier on 09-13 and refused two roles' fires. Choose deliberately.
- **The usage ceiling dropped ~17% on 2026-09-13** when a summer promotion ended — the same
  workload now reads meaningfully higher against the limit with nothing about cohort behavior
  having changed. If reconstructing "what changed" from a cold read, use that denominator or the
  conclusion will wrongly blame a person or a habit.
- **Registry authority: anyone may PARK any row; only the owning session may UN-PARK its own.**
  The failure modes are not symmetric — an un-parked dark role generates alerts nobody can act on.
  Un-park order matters: re-arm cron, `CronList`-verify exactly one job, **then** overwrite the row.
- Mail goes via `scripts/mail-send.sh` (push-to-ref straight to `main`). Pass **every** changed path
  in ONE call — a split multi-call move/rename risks a stranded-path warning or a silent no-op on
  the second half (#1731/#1746, related but distinct mechanisms, still not fully disambiguated).
- **`sprint-truth.py` GraphQL calls can hit a shared cohort-wide burst throttle** ("API rate limit
  exceeded" while `gh api rate_limit` shows full quota) — not your own quota. Retry after a pause,
  or verify a single item via a small direct GraphQL query instead of blocking on the full pull.

## Verified how

`CronList` → one job `4bcf1e1b` (not a config read, an actual tool call this session). Registry
row → `diff` against the pre-edit file confirmed only the `ppm` line changed. Sync → `git fetch` +
`git rev-list --left-right --count origin/main...HEAD` read `138\t0` before the fast-forward, `0\t0`
after. Milestone state → `python3 scripts/sprint-truth.py`, fresh run this session, not a quoted
line. Epics-9/10 reply search → `grep -rli` across every mailbox's inbox/read/sent plus
`decisions.log`, zero hits. Denominator: this file covers PPM's own seat only, not the other four
roles PM parked alongside it (cio, lead, cxo, pa) — their handoffs are theirs to write when they wake.
