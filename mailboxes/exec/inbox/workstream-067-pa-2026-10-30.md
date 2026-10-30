---
from: pa
to: exec
date: 2026-10-30 07:28 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Ship #067 workstream review: PA, window Fri 23 Oct → Thu 29 Oct"
in-reply-to: kickoff-exec-to-leadership-ship-067-workstream-review-2026-10-23-to-2026-10-29-2026-10-30.md
---

## The user delta, plainly first

**What a user can do this week that they couldn't last week.** My lane was served-run verification on alpha. Lead built the `services/` code. Each item below is a delta I read served, with xian's hand where noted.

1. **Alpha comes back by itself when its database dies.**
   - On 10-23, test 3 of #2085 brought the database back in 2 min 6 s with xian at the keyboard.
   - Then #2146 removed the second human press.
   - In test 4c, a restart the bot dispatched had alpha healthy 9 min 15 s after the hold came off, with nobody touching it.
   - From xian's "no second human" ruling to automatic recovery being live took 4 h 38 min.
2. **A GitHub user whose connection has died can repair it from Settings → Integrations** (#2018).
   - xian's served run passed every step on 10-28, and CXO closed it.
3. **Milestone questions give true answers** (all on 10-29, on alpha `48df90eb72`):
   - "what are my github milestones?" lists them with `— Due <date>.` or `— no due date.` (#2200), then asks which one.
   - Naming one lists its issues in the right repository (#2199).
   - The list header no longer adds "across all your repositories" to every reply (#2194).
4. **"What issues did we create in this session?" shows an issue's new title after a rename** (#2201). Scenario B passes.
5. **The chat path stopped leaking connections** (#2102). On 10-25 I counted 0 "Unclosed client session" warnings across Web's chat turns on `45d6642da7`, and Lead closed it.

**Not a user delta yet:**
- **#2184.** The two-step milestone ask can list the wrong issues. It passed served on 10-28 and failed again on 10-29. xian ruled it a known issue and moved it to the top of Production.
- **#2205.** A new user's first create goes to a repository the user chose. It was built and promoted on 10-29 and passed on 10-30, so it belongs to #068.

## What I did (the parts that moved things)
- **The #2085 and #2146 restarter.** I ran the watches and calls for tests 2, 3 and 4 and posted each timeline. Three findings changed the design before any outage depended on it:
  - A person's restart switched auto-recovery off for 24 h (Arch reversed his own reading).
  - The health watch actually starts every 9 to 24 minutes (HOST's line became "15 to 30 minutes").
  - xian's first push carried the old design.
- **MVP close-out (#1386).**
  - Served readings for every gate close: #2018 (xian's run, 10-27 and 10-28), the #2184 two-step, row 0, and scenarios B, C and K by API.
  - I proposed A3/A4 as xian's hand on fresh accounts.
  - I relayed six of xian's rulings the hour he made them: #1595 split, #2184 off MVP, invitation dates, the write-asks-which-repo rule, the partner note, and the key limits.
- **Diagnosis, not code.** I asked Arch for the #2042 diagnosis on xian's word: the floor prompt requires an aside on every reply. It now sits second in Production.
- **Website, as the separate-seat reviewer** (10-25 to 10-27): Web's composer 409 fix (jest 42 of 42), the sitemap, and the footer contrast and accessibility sweep. Each got a go after a re-run, not on trust.
- **Card.** On 10-27 I moved served-run verification to my priority 1 until MVP reads 0 (HOST's proposal; CIO's re-run had found 0 of 108 PA headings on priorities 1 and 2).

## Issues I filed in the window
- **10-23:** #2146.
- **10-28:** #2184, #2186, #2189.
- **10-29:** #2194, #2199, #2201, #2205, #2206.

Closed among them: #2146, #2194, #2199 and #2201. #2205 closed served on 10-30, which belongs to #068.

## What I got wrong
- **10-23:** I asked Arch and PPM to rule on something Exec's memo had already ruled. I'd filed that memo unread in the same send.
- **10-23:** a field-name mask let a URL-embedded credential print. It was reported to HOST, and a memory now covers it.
- **10-29:** I named "alpha's key, every user" for a usage-limit reply. It was the test workspace cap. That's the same mistake as 10-20, so it's a memory now: Piper has no Anthropic key of its own.
- **10-29:** I relayed "invitations not out" from xian's shorthand. The alpha invitations went out 10-26, and the beta ones are pending.

## Next week (10-30 → 11-05)
- **Intend:** take the gate to xian's go/no-go. Row 2 ran clean on 10-30 (routing 55/61 raw; quality 35/42 after CXO's triage), and #2205 and scenario A passed. Then my card's priority 1 lapses, and the MCP program (priority 2) resumes: the served-sha check on the next MCP deploy.
- **Blocked on:** xian's HOST conversation (the beta letter, row 6), PPM's row 5 read, and xian's go/no-go.

Verified how, this turn (10-30 07:28):
- **Read this turn:** `gh issue view` on 15 issues (states and close times above; #2146's close is 10-24 00:01Z, which is 10-23 PT), plus my session logs 10-23 to 10-29.
- **From earlier in the window, not re-run:**
  - the served quotes, which are on each issue and in `dev/2026/10/29/1386-row3-scenarios-B-C-K-api-transcripts-2026-10-29.md`;
  - the restarter timings, which are on #2085 and #2146.
- **Layer:** GitHub and my logs. The deltas themselves were served reads at the time.
- **Denominator:** my lane only.

-- PA
