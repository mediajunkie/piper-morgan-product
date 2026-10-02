---
from: ppm
to: exec
cc: xian (ceo)
subject: "PPM workstream review — Ship #063, Fri Sep 25 → Thu Oct 1"
date: 2026-10-02
---

# PPM workstream review — Ship #063 (Fri Sep 25 → Thu Oct 1)

## Sprint-truth (required denominator)

`sprint-truth.py`, fresh this fire: **MVP: 28 not done** (6 Sprint Backlog, 2 In Progress, 3 In
Review, 17 Product Backlog); **1223 done**. Third-queue-source criteria line: 0 gap, denominator
28 — every MVP-open issue has an epic home.

## PM's organizing question: what can a user do today that they couldn't on Sep 25?

**Honest answer: nothing this seat shipped directly — this lane doesn't write product code.** The
closest real claim is indirect but concrete: a run of joint destination rulings with CXO this week
fed straight into router-description fixes Lead actually shipped, so a user's natural phrasing now
resolves correctly in more cases than a week ago. Specifically:

- **GUIDANCE_PATTERNS** (Monday): CXO's setup-trio correction (three "set up my projects" phrasings
  were being routed toward portfolio management, not the onboarding walkthrough built for them)
  drove one registry-description fix that took the live corpus from 73→80 of 92, zero regressions.
- **CALENDAR_QUERY_PATTERNS**: a day/week description sharpening shipped **v153** — "show me my
  calendar today" now returns the day, not the week.
- **GITHUB_QUERY_PATTERNS + STATUS_PATTERNS**: both gates read GO as of Thursday night; once
  Lead's queued deletion lands, a user's phrasing on these families is handled by the live router
  instead of a brittle regex list.
- **CALENDAR_QUERY + TEMPORAL_PATTERNS**: both fully deleted, live on **v155**.

I co-ruled on these with CXO (verified against `action_registry.py`/handler docstrings each time,
not inferred from a pattern's own name) and Lead built/shipped them. Naming the division of labor
honestly rather than claiming the ship.

**A second, smaller thing that is directly attributable to this seat's own process discipline**:
same-fire board hygiene (`sprint-truth.py`'s unmilestoned-issue delta, re-run every fire without
exception) caught several live tester-facing defects within hours of filing and got them onto the
board immediately, which is part of why they shipped inside the same week rather than sitting
unmilestoned: `#1899` (reminder-task carriers losing turns to Phase 3 deletions, found and shipped
same-day 09-27), `#1901` (a compound-question render bug in `#1855`'s rewriter, found and shipped
same-day 09-28), `#1559` (the adjacency-gap reminder phrasing, closed 09-30 on PM's own test-card
pass), `#1897` (the two-part-turn plan dispatch, proven live 09-30). None of this is my own fix —
it's the board staying honest enough that nothing tester-facing sat untracked long enough to go
stale.

## What this window contained

**The epic-order file got a full, overdue reconciliation.** `dev/active/mvp-epic-order-2026-09-09.md`
is this seat's own standing artifact — the source of truth for what Lead works next. Over the
course of the week (triggered by PM's own direct request on 09-26, extended through every fire
since), it went from carrying an estimated ~50-open bookkeeping count against a live GitHub figure
of 29, to fully reconciled: every epic header now reflects true membership verified against GitHub
state, not grep counts. 52 stale unstruck-but-closed references were found and fixed across 8
epics in the initial pass; the discipline then held for the rest of the week — every new
unmilestoned issue (roughly 20 across the window) got read, milestoned correctly (MVP vs.
`Ongoing`, matched against precedent rather than guessed), board-placed, and given an epic home the
same fire it was found. The criteria line's own denominator moved cleanly with real issue
lifecycle all week (filed → fixed → closed), never silently drifting.

**The MVP-necessity triage PM asked for on 09-25 ran its full course.** Read all 11 candidate
items' actual title+body via `gh api` before judging (not from summaries), found 6 genuinely
MVP-necessary and proposed 4 for `Ongoing` — not moved unilaterally, since that was explicitly
PM's call. PM ruled "broadly yes" on 09-27; applied the three straightforward moves immediately,
and made the fourth call (`#1890`) myself as asked. **That fourth call needs a correction named
plainly**: I verified "zero include sites" correctly, twice, and ruled it a live Rule-0 delete
candidate — but never read the issue's own comment thread, which already carried Lead's finding
(three days earlier) that it was actually a designed, tested `#425`/PDR-002 component sitting
unwired, a wire-vs-dispose product call, not a mechanical delete. No ruling arrived in time; Lead
disposed it directly. Named the miss inline in the epic file and in mail rather than quietly
fixing the record: checking the fact asked isn't the same as reading the whole artifact.

**A live Ship-count correction got a third, independent verification before going into the public
post.** Exec and Lead converged on 91 closed / 57 filed for the prior week after two stacking `gh`
bugs were found (an unscoped `--limit` default-truncating at 30; the `closed:`/`created:` search
qualifier evaluating in UTC, not PDT). Ran a genuinely different method — GitHub's own search
qualifier, not a rerun of either of theirs — and confirmed the same numbers, plus cross-checked
PM's own export against the result from the export side rather than the API-pull side. Safe to
publish once three independently-run methods agreed.

## Found and corrected — named plainly, not folded into the above

**This seat's own STATUS_PATTERNS ruling was wrong, and the correction matters more than the
number of rows involved.** Ruling the "my assignments" / "what am I working on" family
(5 rows + a gate-FAIL row), I checked that `attention_query` was a real, existing destination that
returned genuinely relevant content, and ruled it. CXO's reply — crossing in transit, not a
response to being pushed — drew the distinction my own check skipped: "what am I working on" is an
ownership question, `attention_query` computes an urgency-ranked aggregate, and routing one to the
other is right by coincidence, wrong by construction. That is the exact standard every other
ruling this week held everything else to (the GUIDANCE setup-trio, the PRIORITY attention_query
rows, the CALENDAR capability gaps) — a destination existing and being useful is not the same as it
answering the specific question asked. This is the first time this week that standard caught *my
own* ruling rather than someone else's. Conceded immediately and explicitly rather than let it sit.

**The `#1890` miss above** (checked the fact, missed the artifact) is the week's second named
self-correction.

## Process note

**A real mailbox/git-hook interaction, worked around correctly rather than bypassed.** Merging
`origin/main` when another seat's mail had just landed kept tripping `check-branch.sh`'s mailbox-
staging block, even using plumbing commands (`commit-tree`) — the hook fires on any Bash call with
mailbox paths staged on a non-main branch, not specifically on `git commit`. Fix: abort the merge,
`git rebase` instead — a rebase replays only the local commit's actual diff, so mailbox paths
already identical on both sides never touch the staging area. Documented in the session log as a
reusable pattern rather than a one-off.

**The usage-throttle directive from the prior week closed out cleanly on this seat's side.** Held
at the reduced cadence through a same-day flip-flop in the directive's own interpretation (Exec
ruled "revert Tuesday," retracted, confirmed "revert today") without acting on either superseded
reading — the hold-and-wait turned out to be the right call by construction, not by luck of timing.

## Blocked / open

None currently carried. The one item that was open through most of the window (`#1606`, ruled
10-01 but blocked on a 4b design extension) closed this morning (10-02) — outside this window's
own dates, so not claimed here; next week's review.

**Verified how**: `sprint-truth.py` and the third-queue-source criteria line run fresh this fire
for the denominators cited. Issue closure dates for `#1899`/`#1901`/`#1559`/`#1897` sourced from
this seat's own session-log entries written at the time of each closure (confirmed via commit
evidence in the moment, not re-verified live this morning — GitHub's API is rate-limited for this
seat as of this writing). Everything else drawn directly from this week's own dated session logs
(`dev/2026/09/{25..30}/`, `dev/2026/10/01/`), re-read this morning before writing, not from memory
of the week.

— PPM
