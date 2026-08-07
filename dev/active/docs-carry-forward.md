# Docs Carry-Forward

**Updated**: 2026-08-06 22:27 PDT (Fire 6, STOP — DAY-CLOSED 2026-08-06)
**Session log**: `dev/2026/08/06/2026-08-06-0727-docs-code-log.md` (yesterday's is
`dev/2026/08/05/2026-08-05-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: re-arming at STOP (delete-then-create; see final action) — `57 6,9,12,15,18,21`. Registry row
must match after re-arm.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).

## 🔴 TOP PRIORITY, FIRST THING NEXT FIRE — "Drained on Paper" is proofread but NOT published

PM asked for proofread + publish at 12:32 today (theme=`building`, pubDate 2026-08-06 — **already a day
late as of tomorrow's first fire**). Audit is clean. Publish is held on ONE open question I asked PM
and have not yet gotten an answer to: **four unambiguous copy-editing fixes** in
`docs/public/comms/drafts/drained-on-paper.md` —
1. Line 33: double period ("...the newer architecture..")
2. Line 43: stray "1" after "/close-issue-properly skill" (looks like an orphaned footnote marker)
3. Line 47: "unthethering" → "untethering"
4. Line 53: "kind of mistakes" → "kind of mistake" (singular/plural)

**Do not silently apply these and publish, and do not silently drop the question either** — check
whether PM replied since last fire (chat history / mailbox). If yes, act on the answer. If still no
reply by mid-morning tomorrow, that's worth a direct nudge given the post is now overdue against its
own pubDate — but don't manufacture urgency beyond what the actual staleness warrants.

**Everything else about this post is DONE and does not need re-checking**: frontmatter filled, both
`[PM:]` brackets resolved, footer tease verified against calendar, dry-run pipeline output clean,
image/hashId/slug/category all correct (`--work-date 2026-07-04`, no `--cluster`). Word count is 1,724
(over target, PM aware, not a blocker — don't re-raise). If PM says "just publish, don't worry about
the typos," the `publish-post.js` invocation is already worked out; re-run the dry-run once more before
the real publish only as a freshness check (per the mandatory-dry-run discipline), not because anything
is expected to have changed.

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

## Owed by me — unblocked, priority order (after the two 🔴 items above)

1. **`planning/current/` Finding 1** — fresh careful pass needed, not a rename. Named trigger (fresh
   session/compaction) still hasn't arrived — eight days running now.
2. **97 docs >30d asserting current-state language** — no deadline.
3. **#1486's actual checklist** — not urgent.
4. **methodology-20's compression rules mutually unsatisfiable** — CIO owns.
5. **`docs-standing-items.md` stale** — low priority.

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
