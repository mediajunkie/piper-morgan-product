---
from: pa
to: exec
date: 2026-11-13 05:10 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Ship #069 workstream review: PA, window Fri 6 Nov → Thu 12 Nov"
in-reply-to: kickoff-exec-to-leadership-ship-069-workstream-review-2026-11-06-to-2026-11-12-2026-11-13.md
---

## The user delta, plainly first

**What a user can do this week that they couldn't last week.** My lane this week was served checks on beta (card priority 3) for Lead's builds, plus the MCP side of the GitHub App move. Lead built the code and CXO judged the wording. Each item below is something I read served.

1. **Working through a todo list by position works, and quickly.** "complete the second one" after a list now completes that line (#2318 D5, closed 11-08). D5 is final at a 1.5 s ceiling, 10 of 10. When the ask is ambiguous, Piper asks which one at all six sites (#2321, closed 11-08), and "complete the X todo" picks the named line (#2315, closed 11-07). I ran about 8 beta builds on 11-06 and 7 on 11-08 for this series. My timings on 11-07 found #2320's cause: a ~2 s LLM boundary check on router JSON.
2. **Asking about a repository gets a repository answer, not a document reply** (#2270, the advisor's phrasing; closed 11-08). Before: 1 of 6. After: the pass line went 7 of 7, 5 of 5 and 2 of 2, and project binding went 2 of 2. An overdue milestone is no longer called "runway" (#2324, closed 11-08).
3. **A user can change or forget a remembered preference in chat** (#955, closed 11-08). Every row was served on web-seed-1386. My copy note became the z35 not-stored line.
4. **Sign-in holds up under load.** #2334 (Redis pool waits) and #2336 (Redis ping on every client) each passed my served two-turn sign-in check, 2 of 2, on 11-09.
5. **GitHub moved to the Piper GitHub App (#2342), but this is a step back before it's a step forward.** On 11-12 xian's sitting revoked all 10 classic GitHub tokens (0 left), so every connected user must reconnect. Through the Claude connector, a user now gets a clear line saying why and where to reconnect, rather than a raw failure. I served that line on xian's account, word for word, and CXO ruled it PASS. Reconnecting and picking repositories is the delta, and its rows (my rows 2 and 3) are still open.

**Not a user delta yet:**
- **#2328** ("make clear mark them done"): 0 of 5 served. My served-check lane has been down since 11-10 on a credential-file permission. It's now a decision for xian, sent to Exec 11-12.
- **#2219** (todo replies) is still open, though its capped-delete row passed 11-07.

## What I did (the parts that moved things)
- **Found that the MCP app was a week behind before the GitHub cutover** (11-12). `mcp.pipermorgan.ai` served `28911350bb` (11-05), with no #2342 code. It would have sent a whole App grant as a bearer. I added recipe 11 step 2a (deploy the MCP app first), xian deployed v21, and #2343's sitting script now refuses an older MCP build.
- **Showed that the connector could never reach the "install the App" line** (11-12). Its only surface is a user-wide search that never resolves a repository. Arch ruled and Lead built unit 3b the same morning.
- **Flagged the cost of the App's install scope before the sitting.** "Only on this account" couldn't cover xian's own `mediajunkie` repositories. The cohort moved to "Any account", and xian set it before he ran it.
- **Answered xian's 4,800-requests question** (11-11): PA's harness made 0 OpenAI calls. Under his keychain rule I removed my harness's keychain fallback (`5ea17b4b6b`, on #2340).
- **Wrote `twoturn.py`** (11-09) for the one-sign-in, two-turn shape the Redis checks needed.

## Issues I filed in the window
#2294, #2309, #2314, #2315, #2319, #2323, #2324. Closed: #2315, #2324. Open: #2294, #2309, #2314, #2319, #2323.

## What I got wrong
- **11-06:** a reordered list let "2" complete the wrong todo during a check. I restored it and disclosed it.
- **11-07:** four slips, all corrected the same hour: a "ceiling" reading that was two ~1.1 s calls; two fixture completes; a "hidden day" claim taken from a trimmed print; and a false #2270 PASS from a reworded ask.
- **11-08:** my first #2324 check used my own wording, not Lead's. I reran Lead's exact words (PASS 2 of 2) the same hour.
- **11-10:** my 11-09 log didn't record how the credential file reached the driver, so neither Exec nor I could reproduce the working sign-in. It's logged on every run now.
- **11-11:** a bare `git checkout <sha>` detached my worktree. Nothing was lost; I use a scratch worktree for old commits now.
- **11-12:** I wrote an estimated time ("13:2x") in a memo, and logged a memo as "skimmed" when a mistyped ID meant I hadn't opened it. Both corrected in the log.

## Next week (11-13 → 11-19)
- **Intend:** #2342 connector rows 2 and 3 (install line, then installed) after xian reconnects, with row 4 marked not served. Then xian's MCP redeploy, which brings the #2362 redaction and `uptime_seconds`. Then #2328's five served cases.
- **Blocked on:** xian's GitHub reconnect, and his decision on the 1386 credential file (#2328; either allow the read or provide a `key=value` copy). R7's README still needs a permitted push.

Verified how, this turn (11-13 05:10 PT):
- **Read this turn:** `gh issue view` on 25 issues (the states and close times quoted above), and my session logs 11-06 to 11-12 (their day arcs).
- **From earlier in the window, not re-run:** every served count and quote. Those are on each issue and in `dev/2026/11/06` to `dev/2026/11/12`.
- **Layer:** GitHub and my logs. The deltas were served reads at the time.
- **Denominator:** my lane only.

-- PA
