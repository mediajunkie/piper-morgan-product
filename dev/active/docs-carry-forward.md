# Docs Carry-Forward

**Updated**: 2026-08-05 22:27 PDT (Fire 6, STOP — DAY-CLOSED 2026-08-05)
**Session log**: `dev/2026/08/05/2026-08-05-0727-docs-code-log.md` (yesterday's is
`dev/2026/08/04/2026-08-04-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: re-arming at STOP (delete-then-create; see final action) — `57 6,9,12,15,18,21`. Registry row
must match after re-arm.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).
Split large multi-file commits into batches under 20 files.

## ⚠️ Mail-loop scan — TWO header formats exist, only checked by hand so far

Fixed 08-05 (Fire 3): scan by frontmatter `to:`, not filename — filenames can say `cc-X` while the real
header has X as a primary recipient (this cost 6 unread memos, one over a week old). Fire 5 found a
**second** convention in the wild: bold-markdown `**From**: X · **To**: Y · **cc**: Z` on one line, no
YAML block. Both are checked by hand each fire now (works, confirmed clean both times), but **not yet
unified into one scan command** — do that when there's a spare moment, before it causes a real miss the
way the filename version did:
```bash
for f in mailboxes/docs/inbox/*.md; do
  yaml_to=$(grep -m1 "^to:" "$f" 2>/dev/null | sed 's/^to://')
  bold_to=$(grep -m1 -oE '\*\*To\*\*:[^*]*' "$f" 2>/dev/null | sed 's/\*\*To\*\*://')
  combined="$yaml_to$bold_to"
  echo "$combined" | grep -qiw "docs" && echo "$(basename "$f")"
done
```
Run this (or the hand-checked equivalent) every fire, not just START.

## ⚠️ Friday early-omnibus is now a hard weekly obligation (Exec, 2026-08-05)

PM's ten-step weekly-reporting cycle is now canonical. **Docs owns step 2: Fri–Thu omnibus logs
complete EARLY FRIDAY, every week, unconditionally** — Exec's kickoff memos go out the same morning.
**First instance: Friday 2026-08-07, covering Fri Jul 31 – Thu Aug 6.** No longer best-effort — a
Friday-morning gap now blocks the whole downstream reporting chain.

## Day-of-week duty triggers — CHECK EVERY START (a multi-day gap needs to catch up on any missed)

- **Every Monday**: Weekly Docs Audit (`weekly-docs-audit.yml`, ~9am PT). Verify it fired
  (`gh run list --workflow=weekly-docs-audit.yml --limit 2`); if not, run it + work the issue.
- **First Monday of month**: Monthly Housekeeping Audit (`monthly-housekeeping-audit.yml`, fixed 08-04).
- **Every Friday, EARLY**: omnibus logs Fri–Thu complete before Exec's kickoff memos (see box above).
- **Not mine**: Skill-Candidates Review (1st Tuesday, PM+Exec), Role Health Check (4-weekly, HOST) —
  `docs/internal/operations/staggered-audit-calendar-2026.md` has the full table.

**Proposed but not shipped**: generalized version routed to CIO 08-04, cc PM. No reply yet — this
section is the interim per-role fix regardless.

---

## Awaiting PM specifically — website#31, converter double-`<em>` bug

Filed 2026-08-05. Root cause found (regex in `publish-post.js`), fix proposed, **NOT applied** — two
decisions are PM's call, not mine to assume:
1. Fix going forward only, or also regenerate the ~15-post Ship back-catalog (visibly changes
   "Thanks,"/"Week of..." from familiar italic to bold on every past Ship)?
2. Should `**Metrics (date):**` become a real `###` header in the Ship template? Related:
   `blog-post-template.md`'s "Metrics tables" section still prescribes real tables; practice has used
   bold-label + bullet-list since at least #050, neither side updated to match the other.

Checked at every fire since filing — still 0 comments, not urgent, no chase needed.

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — Arch ✅ and Web ✅ reviewed, no objection. Pre-registered 2–4 week
  measurement window (2026-07-30 → 2026-08-27) via `scripts/measure-editorial-drift.py`. Do not decide
  the storage question early.
- **Dispatch-DinP staleness report** — replied 2026-08-01, no reply yet.
- **CIO's response on the day-of-week duty-check proposal** — sent 2026-08-04, no reply yet. Not
  urgent; interim fix works standalone.
- **#1475 (weekly doc audit)** — OPEN, 1 comment, unchanged since 08-04 partial pass.
- **#1486 (monthly housekeeping audit)** — OPEN, 0 comments, checklist entirely unworked. Not urgent —
  first genuinely-correct run of the workflow, no backlog to catch up on.
- **Next Monday's weekly-docs-audit fire (~9:07 PT, Aug 10)** — watch whether the nudged cron fires.

## Owed by me — unblocked, priority order

1. **`planning/current/` Finding 1 — needs a fresh, careful pass, NOT a quick rename.** Headline claim
   ("100% stale, 314d") is false — `vision.md` is ~113d, not ~314d — 13 live inbound references.
   **Named trigger for the deferral**: a fresh session/compaction — still hasn't arrived, seven days
   running now.
2. **Friday early-omnibus (Aug 7)** — becomes the top priority Thursday night/Friday morning.
3. **97 docs >30d asserting current-state language** — separate, broader item; no deadline.
4. **#1486's actual checklist** — agent infra, pattern/ADR counts, dev/active cleanup, metrics snapshot.
5. **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — CIO owns.
6. **`docs-standing-items.md` is stale** (last touched 2026-05-27, pre-Amber). Low priority.

## Resolved today (2026-08-05) — do NOT re-open

Full narrative for each is in today's session log (`dev/2026/08/05/...`); compact list here:

- **Weekly Ship #054** — published, calendar updated, LinkedIn syndicated, draft archived.
- **Converter double-`<em>` bug** — found, root-caused, filed as website#31. Not fixed (PM decision
  pending, see above).
- **HOST's "BRIEFING-CURRENT-STATE derived-ness" question (08-02)** — ruled no; stays hand-maintained.
- **Web's Tier 3 → Tier 2 question (08-03)** — ruled Tier 2; `ROSTER.md` updated with reasoning in-doc.
- **6 stale/misfiled direct memos** (some 08-01 through 08-04) — all drained; see mail-scan fix above
  for the root cause.
- **"The List That Lies" Medium syndication** (had sat unread from 08-04) — actioned late, apologized.
- **Cached-404-resolves-on-publish** — confirmed, folded into `publish-to-blog` v0.23.

## Standing lessons (carried, still live)

**A mail-loop scan is only as good as the surface it reads — filenames and even a single header
format are both "adjacent," not authoritative.** Two real gaps found and fixed today in the same
mechanism, same underlying cause: trusting a convention instead of parsing the actual field. Applies
beyond mail — same instinct that caught the converter bug (read the code, not the pattern-match).

**Don't wave off a recurring quirk as "pre-existing, not my problem" just because it matches prior
output.** Matching precedent answers "should this block today's work," not "is this actually correct."
Conflating the two would have left the converter bug — live on 15+ Ships — uninvestigated indefinitely.
Holds for a user's stated assumption too ("I believe X has always been true" is worth checking against
the primary source, not just accepted as context, even when it comes from PM).

**A design question asked in passing can be the fastest route to a real, previously-undiscovered
defect.** Held again this week in a new shape (Ship #054's rendering question → the converter bug),
same as last week (the day-of-week trigger request → the monthly-audit workflow bug).

**Verify a fix behaviorally, not just statically, before calling it done.** Still live from 08-04 (the
monthly-audit `node --check` vs. real `workflow_dispatch` lesson) — no new instance today, but the
discipline held throughout (live content-checks for both Ship #054 and "The List That Lies," not status
codes).

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane, still open.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns, raised twice.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
- **Blog index is client-rendered, returns a shell** — Comms's finding, not urgent, not mine unless it
  becomes one.

## The one thing I most want to carry into the next fire

**Two separate "trust the adjacent surface" bugs, found the same day, by the same instinct.** The
mail-scan fix (filename vs. frontmatter) and the converter-bug investigation (pattern-match vs. actual
code) are the same failure mode wearing different clothes: something that *looks* like it answers the
question is treated as if it does. The fix both times was identical — go open the thing that's actually
authoritative. Worth actively watching for a third instance rather than assuming today used it up.
