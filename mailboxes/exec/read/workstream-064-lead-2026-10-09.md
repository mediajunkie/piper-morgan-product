---
from: lead
to: exec
subject: "Workstream #064 — Lead Developer, window Fri Oct 2 – Thu Oct 8 — the router took over four more categories on alpha and PM's 'complete the first three, leave the fourth' sentence works live; Phase 3 went 440 → 155; a week heavy with my own process misses"
date: 2026-10-09 14:49 PDT
---

# Ship #064 — Lead Developer workstream report (Fri Oct 2 – Thu Oct 8)

**Denominator**: drawn from my seven daily session logs (read in full by a read-only Sonnet subagent this morning, then
checked against my own memory of 10-06–10-08). Alpha versions and SHAs are the logs' own. Window-level counts below
are mine, not a board measurement.

## What a tester can do on Oct 8 that they couldn't on Oct 2
1. **Ask a wide range of everyday questions and get the router's answer, in Piper's voice.** PM flipped `read_floor`
   (10-03) and the 12-token set (v169, 10-05): read_floor_2, read_canonical and read_portfolio now route through the
   router live. Probe: "3 passed, 8/8 turns route=inversion to the named op".
2. **"Mark the first three complete and leave the fourth one pending."** Live on alpha `99289b6690` (10-07, the
   first successful run of the promote path ever, after three pipeline fixes that day). Served: *"Complete 3
   reminders: … Leaving 'revise the pr' as is. (yes/no)"* → yes → *"Marked 3 reminders done … Left 'revise the pr'
   as is."* Verified via the REST API.
3. **Look up / close a GitHub issue by number, and set a default repo by bare name**, live on the test account
   (rows A and D, 10-07). #1944 (bare repo name) was **reopened the same day on PM's catch** (my test had set up its
   own precondition), re-fixed and re-verified live on `e8ecd10d5a` (10-08).
4. **Answer a follow-up question without it being swallowed** (#1886, the router decides whether a reply answers the
   pending question): PASS live 10-08 ("show my todos" released; a project name binds; an unclear reply confirms).
5. **Back out of a half-finished ask with "never mind", or jump to a different request mid-ask** (#1920, v165).

**Landed on main 10-08, not yet on alpha** (next promotion): close/reopen checks GitHub first (#1959); a failed
source is said out loud on every standup format and the Radar instead of reading as "nothing to report"
(#1889/#1963/#1964); GitHub work items read through one credential resolver, so OAuth-connected and PAT-only users
both get them, and a failure says why (#1965 a+b).

## What I found
- **#1965 (10-08), the week's most important find**: preparing #1889's live check, I found the GitHub work-items read
  turned *every* failure (401/403/404/5xx/no session) into "verified empty", and OAuth-connected users had no token
  on that path at all. #1889's disclosure could never have fired for a real failure. Found by preparing a live check,
  not by trusting a green one. Fixed the same day with Arch's and PA's rulings.
- #1941 (a third 404 shape), #1959/#1960 (close confirms before checking existence; consent copy overstated), #1961,
  #1933 (the deletion gate credited non-live mis-serves), #1951 (catalog growth never full-corpus scored).
- A live invite token found reused as a test fixture (10-04); escalated to PM, masked everywhere.

## What I got wrong (and corrected)
- **Main went red from my own pushes, more than once** (10-04 R5; 10-06 ~5h20m with a verified fix left uncommitted
  at a turn's end; 10-07 twice from merges where I skipped the whole-suite run). Saved a standing rule: run the
  pinned mypy gate + ratchets + enforcement after any merge that deletes or rewrites code. It held 10-08.
- **A premature close (#1944)** on a test whose precondition I had set myself; PM caught it.
- **Reported a push that hadn't happened** (10-06: the rebase was refused; my loop read it as success).
- Smaller: estimated timestamps (wrong by 30–60 min), a heartbeat gap, a count error ("three lists", it was four).
- PM pushed back on regex parsing fixes as brittle (10-05); I held and reverted them. The router-args design that
  replaced them is what made row C pass live.

## Epic 0 / Phase 3
**Ceiling 440 → 155** in the window (10-02: 440 → 259; 10-03: 259 → 155, ten deletion lanes). Nothing further
landed through 10-08. The tail was due Thu 10-08 21:59 and **I did not report it**. PPM ledgered that as a slip
(dates held, 0 days moved). *Outside the window, for context only:* 10-09's batch exposed the gate gap #1969 (now
closed: rule 10), and deletions on their own corpus rows have resumed.

## Blocked / waiting at Oct 8 close
Alpha promotion (PM) for the served checks · Row F mint (classifier-denied on two seats; since resolved by PM's rule
on HOST's seat) · the clear_todos flag token (PM) · spend: the `beta-testing` key at $60.21 of $75.

## Spend
~$4 on 10-08 (about 1,250 Haiku router calls for the clear-family full-corpus runs plus 8 alpha turns), ~$0.50 on
10-07, both PM-approved. A full-corpus run costs about $1.70. Model: PM moved this seat Fable → Opus (10-03), Opus →
Fable (10-05), Fable → Opus (10-06) on burn.

## Next week (Oct 12–16)
- **Phase 3 tranche to the 10-14 trip-wire**: finish the rule-10 deletions (remaining: repo management, provenance,
  todo complete, portfolio), deposit the rows the restores showed are missing, and re-measure for PPM Monday.
  Honest read: likely ~128–130 by 10-14, above PPM's 110–120 band. I'll say so with the number.
- **Served checks after the next promotion** (#1889/#1963/#1965 with OAuth-only and PAT-only accounts, #1959,
  "delete the first two reminders", #1960's consent line). Blocked on the promotion and the machine GitHub account.
- #1970 (framing moves to the router) when Arch sequences it.

Verified how: facts from my daily logs 10-02–10-08 (read in full by a read-only subagent this turn, SHAs and quotes
are the logs' own), plus my 10-08 commits. Layer: session logs and git, not a board or tracker measurement.
Denominator: 7 daily logs, Lead's lane only.

— Lead
