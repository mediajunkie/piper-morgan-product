# Docs Carry-Forward

**Updated**: 2026-08-07 10:27 PDT (Fire 2, WORK — cohort sweep, Ship #055 report filed)
**Session log**: `dev/2026/08/07/2026-08-07-0727-docs-code-log.md` (yesterday's is
`dev/2026/08/06/2026-08-06-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: re-arming at STOP (delete-then-create; see final action) — `57 6,9,12,15,18,21`. Registry row
must match after re-arm.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).

## 🟡 AWAITING PM — write up the line-count methodology proposal, or hold?

PM asked (in chat) what the HIGH-COMPLEXITY omnibus line-count target protects against and whether
it's serving its purpose. Answered with real data: my 3 Aug 4-6 files (107-133 lines) vs. a compliant
reference day (Jul 19, 575 lines) have nearly identical word/entry counts — the whole gap is
formatting (hard-wrap + blank lines vs. my single-line-per-bullet style), not depth. Recommended
entry-count/word-count over line-count as the real signal. **Explicitly asked PM: write this up as a
proposal to CIO (methodology owner), or hold?** No answer yet as of this fire. Exec independently
corroborated the finding and said they'd back a proposal, but that's not PM's go-ahead — don't send
anything to CIO until PM actually answers the question.

## ✅ Cohort-wide log sweep (PM-requested, 07:57) — done, reported, one action taken

Checked all 11 roles' Aug 6 logs at the primary source after yesterday's usage-limit freeze (reset
~21:30). Clean: HOST, CXO, Docs, CIO. Self-healed automatically this morning, nothing lost: Web,
Comms, Lead, Arch, PA, Exec (Exec's restart PM did personally). **PPM was the one real gap** — live
STOP fire happened, but the sentinel was never written and PPM's own Step 0 didn't catch it. Sent PPM
a memo; **PPM confirmed fixed same fire** (sentinel added, honest note about the missing check being
the real finding, not just the marker). Closed, replied, archived.

## ✅ Friday early-omnibus, first instance — RESOLVED, Exec confirmed

Aug 4, 5, 6 gap closed via 3 parallel extraction agents + synthesis, all HIGH-COMPLEXITY: COORDINATION.
Exec confirmed receipt and that kickoffs went out citing it as complete — step 2→step 3 dependency met
on first live use. Line-count flag (see above) came from this work.

**Still-owed from doing Step 10.5**: the ~70-row Jul 29–Aug 3 activity-log backfill, deferred two
weeks ago, never completed. Flagged to Exec/PM, not urgent, real debt — see Owed by me below.

## ✅ Ship #055 contributor workstream report — FILED same-day, not deferred to Saturday

New this cycle: Exec extended the workstream-review ask to contributor roles (Lead, Docs, PA, Web) for
the first time. Their first kickoff said "due Saturday," then Exec corrected within the hour (PM's
own reasoning: a deadline framing gives license to delay, which costs PM reading time and makes
reports stale) — **write it now, or at the next real opportunity, not by a deadline.** Wrote and filed
`workstream-055-docs-2026-08-07.md` this same fire rather than wait. Window was Jul 31–Aug 6; drew on
the 7 daily logs plus material fresh from this morning's omnibus work. No reply needed unless Exec
has follow-up questions.

## Mail-loop scan — TWO header formats, checked by hand each fire, not yet unified

```bash
for f in mailboxes/docs/inbox/*.md; do
  yaml_to=$(grep -m1 "^to:" "$f" 2>/dev/null | sed 's/^to://')
  bold_to=$(grep -m1 -oE '\*\*To\*\*:[^*]*' "$f" 2>/dev/null | sed 's/\*\*To\*\*://')
  combined="$yaml_to$bold_to"
  echo "$combined" | grep -qiw "docs" && echo "$(basename "$f")"
done
```
Run every fire, not just START. Still works (proven again today — caught Comms's Aug 8/9 date memo
correctly). Unifying into one script is a nice-to-have, not urgent.

## Friday early-omnibus — FIRST INSTANCE IS TOMORROW (Aug 7)

Fri Jul 31 – Thu Aug 6 window, must be complete EARLY, before Exec's kickoff memos go out same morning.
This is now the **second** top-priority item for tomorrow's fires, after the blog-post question above.
Don't let the blocked post eat the whole morning at the expense of this — they're both real deadlines.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit (`weekly-docs-audit.yml`, ~9am PT) — verify it fired.
- **First Monday of month**: Monthly Housekeeping Audit (fixed 08-04).
- **Every Friday, EARLY**: omnibus logs Fri–Thu (see box above — this is tomorrow).
- **Not mine**: Skill-Candidates Review (1st Tuesday), Role Health Check (4-weekly, HOST).

**Proposed but not shipped**: generalized version routed to CIO 08-04. No reply yet.

---

## Awaiting PM specifically

1. **The four typo fixes on "Drained on Paper"** — see top of file. This is the active one.
2. **website#31, converter double-`<em>` bug** — filed 08-05, 0 comments, not urgent, no chase needed:
   (a) fix forward-only vs. regenerate the ~15-post Ship back-catalog, (b) should Ship `**Metrics**`
   become a real `###` header.

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — Arch ✅ Web ✅, no objection. Measurement window runs to 2026-08-27.
- **Dispatch-DinP staleness report** — replied 08-01, no reply yet.
- **CIO's day-of-week duty-check proposal reply** — sent 08-04, no reply yet, not urgent.
- **#1475 / #1486** — both OPEN, unchanged, not urgent.
- **Next Monday's weekly-docs-audit fire (Aug 10)** — watch whether the nudged cron fires.

## Owed by me — unblocked, priority order

1. **Jul 29–Aug 3 activity-log backfill, ~70 rows** — deferred 2 weeks ago, surfaced again today while
   doing Aug 4-6's rows. No functional consequence yet but it's real debt; do it before it's 3 gaps
   instead of 1.
2. **`planning/current/` Finding 1** — fresh careful pass needed, not a rename. Named trigger (fresh
   session/compaction) still hasn't arrived — eight days running now.
3. **97 docs >30d asserting current-state language** — no deadline.
4. **#1486's actual checklist** — not urgent.
5. **methodology-20's compression rules mutually unsatisfiable** — CIO owns.
6. **`docs-standing-items.md` stale** — low priority.

## Resolved today (2026-08-06) — do NOT re-open

- **Aug 8 vs Aug 9 beta date on published Ship #054** — PM confirmed directly the Aug 8 line was
  accurate *at the time it was written* and explicitly does NOT want a retroactive edit or correction
  notice; a future Ship names the change if the date moves. Archived, no action taken, correctly.
- **Mail-scan verified working** on real new traffic today, no false negatives found.

## Standing lessons (carried, still live)

**A user's own request to "verify, don't assume" can catch a real miss — take the challenge
seriously rather than defending the first answer.** PM asked me to confirm I wasn't working from a
stale draft; I was. Checking (via `git log`/`git show`, not just re-reading the file) confirmed a
commit had landed within moments of my first read. The number came out the same by coincidence
(offsetting edits) — reported that plainly rather than let a matching number imply nothing had changed.

**Holding a blocked item across a STOP is legitimate when the block is a genuine external
dependency (a human's pending answer), not a self-imposed pause.** Don't fabricate an answer to avoid
an awkward "still blocked" carry-forward entry, and don't bury the block in prose — put it at the very
top, unmissable, with exactly what's needed to resume.

**A mail-loop scan is only as good as the surface it reads.** Proven again today on real traffic, not
just a retrospective audit — the fixed scan correctly surfaced Comms's genuinely-relevant Aug 8/9 memo
and nothing else.

**Don't wave off a recurring quirk as "pre-existing, not my problem."** Still the standing frame from
08-05; no new instance today but the discipline (verify at the primary source) is what caught today's
stale-read too — same muscle, different application.

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
- **Blog index is client-rendered, returns a shell** — Comms's finding, not mine unless it becomes one.

## The one thing I most want to carry into the next fire

**A published artifact's ground truth can move after publication, and the right response depends
entirely on what the author actually wants — which is worth asking rather than assuming either
"leave it" or "fix it" by default.** Today gave a clean example of both halves of that: PM explicitly
did NOT want the Ship's date retroactively touched (even though it's now technically imprecise), and
explicitly DID want me to hold "Drained on Paper" for confirmation on typos I could have just fixed.
Neither instinct — "always fix" or "never touch published work" — is right on its own; the discipline
is asking, then doing exactly what's asked, not what seems locally sensible.
