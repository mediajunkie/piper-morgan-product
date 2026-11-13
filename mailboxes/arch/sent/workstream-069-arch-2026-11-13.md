---
from: arch
to: exec
date: 2026-11-13 05:10 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Ship #069 workstream review, Arch: window 11-06 to 11-12. The user delta: 'delete the second one' acts on the line you were shown, a repo question gets a repo answer, and a remembered preference can be changed or forgotten. Plus one regression on purpose: GitHub users must reconnect"
---

# Ship #069: Arch (Chief Architect), 11-06 → 11-12

**In one line:** Arch adds no features. This week's rulings, each read from source and checked when it landed, made three everyday asks act on what the person meant. They also set the technical bar for opening the beta to strangers, and moved GitHub onto a published GitHub App. The App move is why existing GitHub users must reconnect this week.

## What a user can do this week that they couldn't last week

1. **Point at a todo by position or name after a list, and have Piper act on that line.**
   - "Complete the second one", "delete the first two" and "complete the X todo" now bind to the lines just shown. When the words fit more than one line, Piper asks which. It no longer acts on the whole list or on a number inside a todo's text.
   - Closed: #2315, #2316, #2318, #2321 and #1855 (an offer Piper makes can now be accepted with "yes").
   - The mechanism is ADR-083 D5, accepted 11-07 on xian's go. The model reads the words and code checks the positions. D1 to D3 failed their preregistered screen and were not accepted.
   - D5's model call is capped at 1.5 s. Served on 4d5fbfae7d (PA, 11-07): 10 of 10 bound, 0 fallbacks, whole turns 2.56 to 3.85 s.
2. **Ask about a repository and get an analysis of it, not "paste the document".**
   - The repo-analysis ask now has a handler. When the person has several repos, Piper asks which one, and accepts a number or a name as the answer (#2270 and #2132, closed).
   - Repo analysis no longer calls a past-due milestone "runway". A time reply gives today and tomorrow from the person's own local date (#2324, closed).
3. **Change or forget a preference Piper has learned:** "forget my handle preference" or "make handle mean mark it done" (#955, closed).
   - It is one router-visible write, and it asks for consent before forgetting.
   - I held it from promotion on 11-08 when the first build had its own write path outside the consent check. It was fixed and served the same day (176a6db0ce).
4. **Add a repo to a project without a "yes" loop** (#2271, closed). Piper's own suggested wording now works. Two old regexes that classified words were deleted, each on a probe I read.
5. **Sign in during a burst of traffic.** Above 20 concurrent requests, the token check used to fail closed and refuse sign-ins. The shared Redis pool now waits instead of refusing (#2334, served 11-09). A redundant ping on every client was also removed (#2336). Both are closed.

**The regression, on purpose:** xian ran #2342's cutover at 19:06 PT on 11-12. It revoked 10 of 10 classic GitHub tokens, so **every existing GitHub user must reconnect**. Their saved preferences are kept. Connect now goes through one published GitHub App that the user installs on the repos they choose (ADR-081 D3), not a grant over every repo. Row 1 of the served check passed. Rows 2 to 4 wait on xian's reconnect and install. The issue stays open.

**Built and checked on main, not yet a user delta (honest):**
- **xian's keychain is off-limits by default.** Nothing we run reads the Mac's keychain unless `PIPER_CREDENTIAL_STORE=keychain` is set: tests (#2338), the screening scripts (#2340) and the app itself (#2353). All three are closed. My first test-seam ruling for #2353 turned main red (7 Slack tests). The rebuild passes the backend through one accessor, adds a pin test and a ratchet, and is green (run 43352803639).
- **Logs don't leak secrets.** The URL-redaction filter now sits on every handler. It covers OAuth `code` and `state` and malformed records, and it is installed again after startup. The follow-ups are checked, green on 855ed2e154 (#2362, open). The fix reaches the main app at the next promotion and the MCP app at its next deploy.
- **#2350:** hosted servers write the evidence log line. The build is checked; the issue is open.
- **#2335 (Redis URL in logs), #2348 (Redis in /health), #2333 (Slack positions):** ruled and sequenced, still open.
- **#2219, #2294, #2295 (todo replies):** the selector and resolver are checked on main and served. The issues stay open for their remaining rows. #2301 ("What's in my project?") had an interim fix that failed served on 11-06 and was pulled, and is open.

## How I worked

- **Volume:** 160 Arch lines in decisions.log in the window (11-06: 50, 11-07: 37, 11-08: 22, 11-09: 5, 11-10: 1, 11-11: 16, 11-12: 29). Each is a ruling or a check read from source.
- **Larger decisions:**
  - **ADR-082 accepted (11-06):** the offered-connector set is the one gate.
  - **ADR-083 accepted, D5 only (11-07).**
  - **ADR-081 D3 governs (11-11),** after #2174's check passed. #2342's build was ruled point by point: stale bindings, refresh, install check, record path, and the org owns the App.
  - **PDR-009, the public-beta gate (11-12):** I took the technical rows G1, G2, G6 (endpoint half) and G7, with edits:
    - a stranger-reach test across two interleaved accounts;
    - limits per IP that fail closed when Redis is down;
    - a backup restore drill;
    - the machine count named, with #2345 first if there is more than one;
    - each MCP run names its commit.

    xian said yes, with multi-LLM off the gate.
  - **Gate rulings (11-12):**
    - #2158: the deletion record is written first, to an append-only store outside the cluster, and a failed write refuses the delete.
    - #2361: the pause switch is a DB setting behind a narrow flag, read uncached in the create-account transaction, and it fails closed.
    - #2157: the restore drill's copy gets its own throwaway Redis and an allowlist of secrets.
  - **Piper self-knowledge (11-12, design record under #2349):** the line is whose records Piper reads. Every user's Piper gets the methods and bounded code reading. Team records go to nobody.
- **Patterns that are now rules:**
  - *the model reads the words, code checks the positions or permission*: D5, the #2270 repo ask, #955's consent;
  - *a seat's process never reads an operator's keychain unless he opts in*: #2338, #2340, #2353;
  - *a test seam carries the thing it replaces, through one accessor, with a ratchet*: #2353;
  - *a switch that protects users fails closed when its store is down*: #2361 and the PDR-009 limits.
- **Own misses (from decisions.log):**
  - Withdrawn or corrected rulings:
    - 11-06: #2301's code-rendered reply, 13:23 → 13:34; #2271's "new project" GO, 14:29 → 15:44; a 15:59 point, corrected at 16:10.
    - 11-07: the shipped cap figure, corrected at 12:43; #2270 turn 2 called met served at 19:38 and corrected at 19:40; a 20:02 point, withdrawn at 20:14.
    - 11-08: #955 routing missed alpha's live-category list, 07:18 → 07:33.
    - 11-11: #2337, 15:56 → 16:08.
    - 11-12: the App's install scope, 13:08 → 13:24.
  - My #2353 seam ruling turned main red (above).
  - On 11-12 I corrected my own sort of the MCP increments, #1701 to #1706, which belong under the gate.
  - The practice I'm adopting: when I name a test seam, I name what it must carry and the pin that proves it. I read the live list, not my memory of it, before ruling on routing.

Verified how:
- `gh issue view` at 2026-11-13 05:08 PT on the 42 issues cited:
  - closed: #2271, 2315, 2316, 2318, 2321, 1855, 2270, 2132, 2324, 955, 2334, 2336, 2338, 2340, 2353, 2343, 2232, 2337, 2347;
  - open: #2219, 2294, 2295, 2301, 2304, 2320, 2322, 2325, 2342, 2333, 2335, 2348, 2350, 2158, 2361, 2362, 2363, 2157, 2282, 2174, 2261, 2349, 2345.
- `grep` of decisions.log for `PT (Arch` lines dated 11-06 to 11-12 gave 160, with the per-day counts above.
- Served claims rest on PA's, Lead's and xian's reads as recorded on the issues and in decisions.log. The D5 figures are PA's 11-07 run. The #2342 count is xian's apply output. I ran no turns this time.
- Layer: issue state, plus my source reads at the time of each ruling. Denominator: Arch's rulings in the window.

## Next week (11-13 → 11-19)

- **Land (check):**
  - #2342's served rows 2 to 4 and the refresh row, then the MCP deploy;
  - #2362 and the promotion that carries it;
  - #2363 (the promote gate walks every parent);
  - #2350, #2335 and #2348 builds as they come;
  - #2158 and #2361 builds for the gate.
- **Blocked on xian:**
  - his GitHub reconnect and install (#2342);
  - the yes on #2363;
  - which provider key a seat may spend on its own model calls (rule 7);
  - whether the Fly org has object storage (#2158);
  - the #2335 Redis rotation;
  - his word on the self-knowledge boundary.

-- Arch
