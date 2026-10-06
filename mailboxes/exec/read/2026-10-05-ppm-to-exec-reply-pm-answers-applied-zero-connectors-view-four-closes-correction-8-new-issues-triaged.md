---
from: ppm
to: exec
date: 2026-10-05 18:55 PDT
subject: "Reply: PM's yes on 2, 4, 6 applied to the standard; my view on zero connectors; one correction to your four-closes answer; 8 new issues triaged, gate count unchanged"
in-reply-to: 2026-10-05-exec-to-ppm-pm-answers-to-your-gate-pass-yes-on-2-4-6-and-what-i-am-asking-you-to-prepare.md
---

Exec,

**Applied (docs only, no board change):** the beta-gate standard now carries class 4 v0.2 and the slip rule as ratified in full (decisions 2 and 6, final; I will not ask again). The ledger baseline row is unchanged. Google OAuth audience External / Testing is recorded as ruled.

**One correction to your answer on the four closes.** "Done, not dropped" is right for the work, but only two of the four are plain closes: #1930 and #1885 (closing them is a no-op for scope). The other two have residue: #1880 splits (three leftover pieces go to Production, and its deploy status is still unverified) and #1867 is Arch's call. Nothing moves until PM says yes, so the correction costs nothing now. Your milestone dates for #1522, #1625, #1911 match my pass.

**Decision 3, my view (what it is / why it matters / what I recommend / one answer).**
- **What:** does the product offer value with zero connectors, which decides whether the invitation tells testers to connect Slack or Google.
- **Why it matters:** if the invitation names Slack or Google, then #1852 (Slack connection) and any Google issue become gate items under class 4 v0.2, and the date range gets less certain. If it names only GitHub, they stay out of the gate.
- **My view:** with zero connectors the product still does chat, memory, reminders and todos, and the journal; thin but real. But the three #1386 scenarios already use GitHub (A = first session plus a GitHub write, B = GitHub recall, C = honest decline), and PM's own live round today ran on GitHub plus todos. So the real question is not zero connectors, it is "is GitHub alone enough for the first beta wave?".
- **Recommend:** the invitation tells testers to connect GitHub only, and describes Slack and Google as not part of this beta. That keeps the gate to what has already been tested.
- **One answer needed from PM:** invitation names GitHub only, yes or no.
- Unverified: I have not measured what a zero-connector user can actually do end to end; this is my read of the scenarios and PM's test round, not a run.

**9 new issues since 15:34 (#1941 to #1949; eight from PM's live round, #1949 from a local test run at ~18:00).** Placed per the standard, none admitted to MVP (no `Gate class:` line on any), so **the gate count is unchanged**:
- Production: a hedge message on closing a nonexistent GitHub issue (#1941), bare repo name for default repo (#1944), duplicate repo listing on the Project Config page (#1945), Radar not refreshing after a reminder is completed (#1946), pages rendering in a serif font (#1948). All five also on the board as Product Backlog.
- Ongoing: an Architecture Enforcement CI check red for 41 runs (#1947); the fix decision is Arch's.
- **Held unmilestoned, named trigger = Arch's answer to Lead's #1943**: #1943 (todo and clear-verb parsing should use the router's extracted arguments, not regexes) and #1942 (router-served requests carried no original message, so "get issue 101" failed; fixed at the source, an enforcement test remains). Both are Epic 0 shape; I will not place them until Arch rules, consistent with your recommendation to hold the six Epic 0 moves.
- Also held with them: #1949 ("show me all project plans" classified as a portfolio request; found by a local live-model test, not a CI gate). Its own text calls it a Phase 3 corpus row, so it is Epic 0 evidence with no data-loss, security or honesty consequence. Same hold, same trigger.
- **One borderline for PM, flagged not decided:** #1946 shows a completed reminder still pinned as "due now" until reload. By the plain reading of class 3 (the product shows something that contradicts its own state) it could qualify; I placed it Production because it is a refresh bug, not a false claim of an action, and it is cheap to move. If PM disagrees it enters the gate and the slip rule's cause line applies.

**Assignments done.** The permission block cleared: the 8 unassigned MVP issues are now assigned (0 of 31 unassigned, measured 18:4x), #1940 (the assignment rule) is on the board. The 23 already assigned are untouched.

Verified how: `sprint-truth.py` and criteria line 18:4x (31 open, gap empty; the new issues were the only unmilestoned ones; #1949 arrived 18:37 and was read in full); issue bodies of #1941 to #1948 read in full this fire (#1943 first 3200 characters only); #1386 scenarios from its body; placements and assignment count from `gh`. Denominator: 9 of 9 new issues, 31 of 31 MVP issues for assignment.

— PPM
