---
from: ppm
to: exec
date: 2026-10-30 0734 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Ship #067 workstream review, PPM: window Fri 10-23 to Thu 10-29. The gate went 6 -> 2 open (10 closes, 7 admissions, 1 known-issue removal); partners were invited; Production got a plan, a map and 1.0 promises"
---

# Ship #067, PPM workstream review (10-23 → 10-29)

## What a user can do this week that they couldn't last week

**Design partners got their invitations on Fri 10-23.** Through the week, the gate list fell from 6 open MVP to 2: 10 closes, 7 admissions (all found by running the gate's own scenarios) and 1 removal to known issues. In a partner's terms:

- **Send feedback from inside the app** (#2096).
- **Not lose Piper to a database that dies quietly.** The 10-19 failure, where Postgres died inside a running machine and nothing restarted it or raised an alert, is closed (#2085). The close row cites its check.
- **Get honest answers where they used to get confident wrong ones:**
  - Calendar connect no longer says "Connected" when Google's calendar box was left unticked (#2148).
  - "Analyze this document" with no document in the chat no longer answers with repository metrics (#2132).
  - "Tell me more about the GitHub integration" no longer mixes in their calendar (#2142).
  - A failed preferences read no longer shows defaults, and Save no longer writes those defaults over their real settings (#2154).
- **Recover a dead GitHub connection from Settings** without our help (#2018).
- **Trust GitHub list headers and session recaps:**
  - A milestone-scoped issue list no longer claims "across all your repositories" (#2194).
  - "What did we create this session?" shows an issue's edited title, not its old one (#2201).
- **Behind all of it, the understanding-layer inversion is closed** (#1595, by split). One constrained routing call does the understanding. The 61 remaining catalog rows continue as #2195, in Production.

**Not yet:**
- **Asking about a named milestone can list the wrong issues** (#2184). xian moved it to known issues on 10-29, and it's in the partner note and the beta letter.
- **A new user's first "create an issue" with no default repo** (#2205) was fixed and live on alpha by the window's end (`e234776150`, 10-29 evening). Its served check passed on 10-30, so it belongs to next week's Ship.

Verified how: the ledger rows dated 10-23 to 10-29 in `docs/internal/planning/beta-gate-standard.md`, read this run: admissions 39th to 45th (7 rows), 10 close rows and 1 removal; 6 + 7 − 10 − 1 = 2. I took the issue titles from `gh issue view` on all 11, this run. Each close row cites the served check its closer ran (CXO, PA, Web or Lead); I didn't rerun them. The partner invitation date comes from the briefing's "Dates" line.

## PPM's own lane this week

- **The Production plan (xian's 10-23 ask: "start … organizing them into potential sprints").** `production-sprint-proposal-2026-10-23.md` puts every open Production issue in one of ten sprints: PUB, H, D, C, V, E, T, Doc, Dist and Q. It was 230 at the start and 224 at window end (209 on 10-24, after 27 moved to Ongoing and 3 closed). The plan's Total line has matched `gh` every day, with 0 unplanned.
  - **The production map:** `docs/internal/planning/production-map.html`, rebuilt from the board each day and published to claude.ai (v1 to v28 in the window).
  - **The 1.0 promises:** `docs/internal/product/promises.yaml`, ratified by xian 10-25, with promise, journey and seam labels applied.
  - **The board catches up:** H, D and V got Sprint options (xian added them), and 92 rows were relabelled per item. On 10-29, at xian's ask, 110 closed Production issues were backfilled with their sprint, with 5 set aside for his call. Every write was per item; the field still has 60 options.
- **Gate stewardship.**
  - **Seven admissions.** Four were my judgment under xian's 10-16 standing ruling (#2184, #2194, #2201, #2205), each with a Gate class line, ledgered the same turn.
  - **No slip rows.** No dates moved.
  - **The #1386 run order:** row 0, then the freeze, then rows 2 to 5. Three fix promotions inside the freeze, each on green Tests plus xian's dispatch.
- **Rulings:** the #2042 class goes to xian as one known-issues line, not as admissions (he agreed). #2204's calendar window is local midnight plus 7 days, kept out of the gate build. Row 3 co-signed with CXO with every defect's path named.
- **Misses I own:**
  - I filed CXO's "MVP" substitution under #2042 rung 3. It's #2209, a small fix; CXO caught it and I corrected it the same hour.
  - My mail-send loop staged mailbox renames twice, which the hook blocked.
  - One guessed "16:3x" timestamp.
- **Not done:** no PDR edits. The Production plan is the week's roadmap work, so the drift my role card names is smaller than last week, but it's not zero.

## Next week (10-30 → 11-05)

- **Land:**
  - #1386's last rows: row 4's two Fly reads (xian), row 5 at go/no-go (mine), row 6's known-issues check at send time (mine, on Comms's letter);
  - then xian's go/no-go;
  - after it, PUB's first moves: #2195, #2042, #2197, #2209, #2184, waitlist #2164.
- **Blocked on:** xian (the two Fly reads, his HOST conversation, go/no-go, the 5 set-aside issues and #1706's sprint move).

-- PPM
