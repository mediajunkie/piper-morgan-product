# Docs Carry-Forward

**Updated**: 2026-08-05 10:27 PDT (Fire 2, WORK — mid-fire, PM-engaged session)
**Session log**: `dev/2026/08/05/2026-08-05-0727-docs-code-log.md` (yesterday's is
`dev/2026/08/04/2026-08-04-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: `57b0736c`, verified via CronList this fire — `57 6,9,12,15,18,21`. Registry row matches.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).
Split large multi-file commits into batches under 20 files.

## ⚠️ NEW — Friday early-omnibus is now a hard weekly obligation (Exec, 2026-08-05 09:20)

PM's ten-step weekly-reporting cycle is now canonical (`weekly-ship-process-guide.md`
§canonical-cycle, `draft-weekly-ship` v1.10). **Docs owns step 2: the Fri–Thu omnibus logs must be
complete EARLY FRIDAY, every week, unconditionally** — Exec's kickoff memos (step 3) go out the same
morning telling six leads to review them, and step 4 has all six reporting that day. A Friday-morning
gap now blocks the whole downstream chain — no longer best-effort. **First instance: Friday 2026-08-07,
covering Fri Jul 31 – Thu Aug 6.** Add this as a standing Friday trigger below alongside the Monday
ones — this is the second, independently-sourced day-of-week obligation this week, reinforcing that the
generalized mechanism (routed to CIO 08-04) is worth landing rather than accumulating one-off sections.

## ⚠️ Day-of-week duty triggers (added 2026-08-04, PM-directed) — CHECK EVERY START

**Why this section exists**: the Monday 2026-08-03 weekly doc audit (#1475) sat untouched until PM
asked me to check on it Tuesday. Nothing in the duty cycle knew it was Monday. Checking it surfaced a
second, independent finding: the *monthly* housekeeping audit had been silently broken by two real
bugs since the file was written — nobody had been checking whether it fired at all, because nothing
prompted the check. Both now fixed (see Resolved below).

**Read this list at every START, not just Mondays** (a START after a multi-day gap needs to catch up
on any Monday it missed):

- **Every Monday**: Weekly Docs Audit fires via `weekly-docs-audit.yml` (~9am PT). Check
  `gh run list --workflow=weekly-docs-audit.yml --limit 2` fired and succeeded; if not, `gh workflow
  run weekly-docs-audit.yml` and work the checklist issue yourself. Don't assume it ran — verify.
- **First Monday of each month**: Monthly Housekeeping Audit fires via
  `monthly-housekeeping-audit.yml` (fixed 08-04, cron was correct-looking but wrong per POSIX
  day-of-month/day-of-week OR semantics — see Resolved). Same check.
- **Every Friday, EARLY**: omnibus logs for Fri–Thu complete and ready before Exec's kickoff memos go
  out same morning (new 2026-08-05, see box above). First instance Aug 7, covering Jul 31–Aug 6. This
  is now load-bearing for the whole weekly-reporting chain, not best-effort.
- **Not mine, but worth knowing exists**: Skill-Candidates Review (1st Tuesday, PM+Exec owned) and
  Role Health Check (4-weekly, HOST owned) — see `docs/internal/operations/
  staggered-audit-calendar-2026.md` for the full cadence table if a date ever looks Docs-adjacent.

**Proposed but not yet shipped**: a generic "Day-of-Week Duty Check" step in the shared
`duty-cycle-tick` skill (Step 3, right after reading carry-forward) — routed to CIO 2026-08-04, cc PM.
No reply yet; this section is the interim fix for Docs specifically until/unless that lands.

---

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — unchanged, checked again this fire. Arch ✅ and Web ✅ both reviewed,
  no objection. **Do not decide the storage question early** — pre-registered 2–4 week window
  (2026-07-30 → 2026-08-27), shipped measurement (`scripts/measure-editorial-drift.py`).
- **Dispatch-DinP staleness report** — replied 2026-08-01, no reply yet. Still watching.
- **CIO's response on the day-of-week duty-check proposal** — sent 2026-08-04, no reply yet. Not
  urgent; my own interim fix (the section above) works standalone regardless of CIO's disposition.
- **Next Monday's weekly-docs-audit fire (~9:07 PT, Aug 10)** — Lead nudged the cron off the
  top-of-hour after 08-03's schedule didn't fire. Watch whether it fires this time.
- **#1475 (weekly doc audit) and #1486 (monthly housekeeping audit)** — both still OPEN, both have
  substantive evidence posted, neither claimed complete. Not mine to close solo — #1475 covered maybe
  half the checklist; #1486 was just created today (the actual overdue August run, a few days late)
  and hasn't been worked at all yet, only verified to now fire and render correctly.

## Awaiting PM specifically — two decisions on the converter bug (website#31)

Filed 2026-08-05 after PM asked why the Ship #054 "Metrics" line rendered boldface-degraded-to-italic.
Root cause found and fixed-in-proposal (regex in `publish-post.js`), NOT applied yet — two things need
PM's call, not mine to assume:
1. Fix going forward only, or also regenerate `blog-content.json` for the ~15-post Ship back-catalog
   (visibly changes "Thanks,"/"Week of..." from familiar italic to bold on every past Ship)?
2. Should `**Metrics (date):**` become a real `###` header in the Ship template, independent of the
   bug fix? Related: `blog-post-template.md`'s "Metrics tables" section still prescribes real markdown
   tables; practice has used bold-label + bullet-list since at least #050 and nobody updated either
   side to match the other.

## Owed by me — unblocked, priority order

1. **`planning/current/` Finding 1 — needs a fresh, careful pass, NOT a quick rename.** Headline claim
   ("100% stale, 314d") is false — `vision.md` is ~113d, not ~314d — and there are 13 live inbound
   references, several in active session-start briefing paths. **Named trigger for the deferral**: a
   fresh session/compaction — still hasn't arrived, six days running now.
2. **97 docs >30d asserting current-state language** — separate, broader item; no deadline named.
3. **#1486's actual checklist** — the monthly housekeeping audit issue now exists and fires correctly,
   but nobody has worked the checklist itself yet (agent infra, pattern/ADR counts, dev/active cleanup,
   metrics snapshot). Not urgent — first genuinely-correct run, no backlog of misses to catch up on.
4. **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — CIO owns.
5. **`docs-standing-items.md` is stale** (last touched 2026-05-27, pre-Amber). Low priority, not urgent.
6. **Friday early-omnibus (Aug 7)** — new hard deadline, see box above. Not urgent yet (2 days out) but
   the highest-priority item once Thursday closes.

## Resolved 2026-08-05 — do NOT re-open

- ~~Weekly Ship #054 ("Clear Is Not a Measurement")~~ — **fully closed.** Template audit clean (10
  applicable PASS, 4 Ship-calibrated N/A by convention), published via `publish-post.js`, live
  content-check confirmed (distinctive phrase, not status code), calendar updated + draft archived.
  LinkedIn syndication (Dispatch-DinP) applied same fire: status→distributed, linkedinURL, liPubDate.
- ~~Converter double-`<em>` bug~~ — **found, root-caused, filed** (website#31). NOT fixed — two scope
  decisions handed to PM, see box above. Do not apply the regex fix or regenerate back-catalog without
  PM's answer.

## Resolved 2026-08-04 — do NOT re-open

- ~~Today's blog post ("The List That Lies")~~ — **fully closed.** Proofread (14-check template audit
  clean, one word-count flag not a block), published, archived, calendar updated, drift clean.
- ~~Comms's soft-404 finding (`publish-to-blog` verification gap)~~ — **fully closed.** Fixed v0.22
  (`e71abedfc`) — content-check method, not status code, in both Step 9's gate and the Quality
  Checklist.
- ~~Omnibus gap, Jul 29 – Aug 3 (6 days, ~70 logs)~~ — **fully closed.** All 6 written to
  `docs/omnibus-logs/` via 6 parallel extraction agents + synthesis. Landed shorter than the
  HIGH-COMPLEXITY target line budget (155–194 vs. 450–600) — flagged honestly to Comms and in the
  commit rather than claimed as full compliance. Comms notified directly since the gap was blocking
  their narrative-front work. Step 10.5 (activity-log CSV reconciliation) explicitly deferred, not
  silently skipped.
- ~~Monday's weekly doc audit (#1475) — verified NOT done, partially closed~~ — real evidence posted
  (Doc Currency ratio, GitHub issues sync, link integrity, one false alarm caught before reporting, one
  flagged-not-confirmed `pmorgan.tech` staleness concern). Issue left open — too much of the checklist
  genuinely uncovered to claim done.
- ~~Monthly housekeeping audit — found broken, two bugs fixed and behaviorally verified~~ — cron fired
  every day 1–7 regardless of weekday (POSIX day-of-month/day-of-week OR semantics), fixed to
  weekly-Monday + runtime day<=7 guard. Unescaped backticks in the JS template literal caused a syntax
  error on every run since the file was authored — likely never once succeeded. Both fixed; verified
  via `node --check` on all 3 script blocks AND a real `workflow_dispatch` run that created issue
  #1486 with correctly-rendered markdown.

## Inbox

**~104 remaining, cc-only**, as of this fire. Both memos directly addressed to docs this fire (Dispatch
syndication ask, Exec's Friday-obligation memo) drained and replied/actioned. Everything else cc-only —
dense multi-agent threads (heartbeat mechanism, alt-text/404 fixes, drift-check work), nothing owed. Not
mass-moving to `read/` — drain on quiet fires.

## Standing lessons (carried, still live)

**Don't wave off a rendering quirk as "pre-existing, not my problem" just because it matches prior
output.** I initially treated the `<em><em>` doubling as an established (if ugly) pattern because it
matched #053 exactly — correct as a publish-blocker judgment (matching prior practice), wrong as a final
verdict. PM asked one direct question ("shouldn't a header be a real header?") and reading the actual
converter code instead of re-asserting the pattern-match found a real bug live on 15+ consecutive
posts. Matching precedent is right for *should this block today's publish* — it is not the same
question as *is this actually correct*, and conflating them would have left a real bug uninvestigated
indefinitely.

**A user's stated assumption ("I believe X has always been true") is itself worth checking, not just
accepting as context.** PM said "the footers have always been italicized, I believe" — checking that
against the raw markdown source (not the rendered output) found the *belief* was based on 15+ Ships of
buggy rendering, not actual authored intent. Gently correcting a stated assumption, backed by evidence,
was the right move — not deferring to it because it came from PM.

**Checking your own new discipline immediately can surface a second, unrelated finding.** Implementing
the Monday-trigger check for the weekly audit led directly to checking the monthly one too (same
remit, same table) — which turned out to be the more consequential find, a workflow that had likely
never worked at all. The lesson from two days ago ("going to verify one thing can surface a second")
held again, in a different shape.

**Verify a fix behaviorally, not just statically, before calling it done.** `node --check` confirmed
syntax; it did not confirm the fix actually worked end-to-end. Running the real workflow and reading
the actual rendered issue body is what closed the loop — a static pass alone would have been the same
shape as this week's other "clear is not a measurement" findings.

**A finding that arrives as "check if this affects you too" is worth checking properly, not pattern-
matching.** Held again today with Comms's soft-404 finding — reading the actual skill text found the
exact gap in two places a guess could have missed or over-applied.

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane, still open.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns, raised twice.
- **`docs/internal/operations/one-command-checks.md`** (Arch, 2026-08-02) — worth reading before the
  next audit-shaped task.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
- **Blog index is client-rendered, returns a shell** — Comms's finding, not urgent, not mine unless it
  becomes one.
- **Skill-Candidates Review (1st Tuesday) is today** — PM+Exec owned, not mine to act on, but worth
  knowing it's the same week as the monthly housekeeping audit per the staggered calendar's own noted
  "wrinkle" (two Monday-anchored-adjacent audits landing close together).

## The one thing I most want to carry into the next fire

**A design question PM asks in passing can be the fastest route to a real, previously-undiscovered
defect.** PM's ask wasn't "check if the monthly audit is broken" — it was "help me build a mechanism so
audits don't get missed." Building the mechanism for my own lane required actually checking whether the
thing I was building a trigger for had ever worked, and it hadn't. The design question and the
verification question turned out to be the same question, one layer down.
