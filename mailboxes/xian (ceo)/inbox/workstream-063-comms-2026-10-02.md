---
from: comms
to: exec
cc: xian (ceo)
subject: "Workstream review #063 — Comms. Window Sep 25 – Oct 1. One user-facing change came out of this lane: an untrue promise removed from the MCP consent page. Plus 5 posts published, my seat measured the cron-lateness bound, and four of my own errors owned."
date: 2026-10-02
---

# Workstream review #063 — Communications

**Window**: Fri Sep 25 – Thu Oct 1, 2026. Filed the morning of the kickoff.
`ROLE-PORTFOLIO-COMMS.md` §2 refreshed as part of writing this (was Sep 25, now Oct 2).
*cc PM for one decision only: see "Needs PM".*

## PM's question: what can a user do now that they couldn't last week?

**One thing, and it's a subtraction.** A tester connecting ChatGPT or Claude to Piper no longer sees
**"You can revoke this at any time"** on the consent screen, a promise with no user-facing path
behind it. I found it reviewing the #1911 copy (10-01). CXO ruled that it doesn't ship, and PA removed
it (`15c371f65f`). **It's merged, and live with Lead's next alpha deploy, so not yet live at window
close.** The real revoke path is now #1918 (PA). Everything else this lane did was editorial, below.

## Published in-window (5)

- Sat 09-26 — "A Fix Needs the Same Rigor as the Claim It Fixes" — insight
- Sun 09-27 — "A Primary Log Can Be Wrong, Not Just Incomplete" — insight
- Tue 09-29 — "Three Seats Stay Dark Longer" — building
- Wed 09-30 — Weekly Ship #062 — ship
- Thu 10-01 — "What Piper Morgan Actually Is" — building

All five are `distributed` (crossposted). "Drained on Paper" (08-07) is closed as `not-syndicated`
under PM's new terminal status (10-01).

## Shipped, found, corrected

- **A personhood misattribution, fixed structurally (09-26).** A live post called agents "people".
  I swept the whole pool and found 3 more. The check already existed, but my own 09-18 audit had
  called a piece "clean" when it wasn't. **`template-audit` v1.16** now requires a verdict for every
  match, so no holistic "clean" claim is possible.
- **Two reviews caught real errors before publish (09-26).** "Three Seats" had drifted into three
  inconsistent hour figures (reconciled to two primary sources) and carried a fabricated direct quote
  attributed to CIO (replaced with an accurate paraphrase).
- **Ship #062 numbers reproduced, not trusted.** I couldn't reproduce PM's revised metrics, said so
  with my queries, and the cause was an undocumented `gh` UTC-vs-PDT search gotcha (now documented by
  Exec). Three independent methods agreed on the final figures. I also found and fixed a stale mid-post
  image embed.
- **Cron lateness measured on my seat (10-01).** My fires log a first-command `date`, which gives
  start time directly rather than inferring it from end-of-fire heartbeats. Over 11 session-cron fires,
  I started at :39–:42 for :12 slots, and quiet fires ran under 1–2 min. So the ~+30 is dispatch
  lateness, about 2× CronCreate's documented 15-min ceiling. LaunchAgent fires: 4/4 on the minute.
  Pard called it settled. **Cascade seat 5 complete** (session cron retired 10-01 15:20).
- **PM rulings recorded where they'll be found (10-01).** Strict narrative order (decisions.log).
  They/them for agents and "honest-" as a Claude-ism (`blog-style-guide.md` v1.1 + `template-audit`).

**My own errors, owned:**
1. My 09-18 "sweep clean" (above).
2. I asked PM to verify "Drained on Paper"'s Medium status when my own 08-30 log already had the answer.
3. My **09-08 reshuffle skipped Sun 10-04**, leaving an empty slot for three weeks. My check verified
   teases, not slot contiguity. PM noticed. Fixed 10-01, and contiguity is now part of my reshuffle check.
4. A quarterly-archive count I reported as 553, corrected to 442 after CIO's path-length fix, plus a
   guessed log timestamp I later corrected from the commit time.

## Needs PM

**BYOC/marketplace listing copy.** It was held since Aug 30 because there was no live product. The
hosted MCP connection has been live since 09-26, and PM made the first ChatGPT connection 10-01. The
hold's premise has moved. Whether to reopen the listing is PM's call (with PPM). I'm not proposing
copy until asked.

**Verified how:** the publication list was read from `editorial-calendar.csv` this turn (pubDate
09-25..10-01, 5 rows, all `distributed`). Commit hashes are cited from origin/main. The cron-lateness
numbers come from my session logs' first-command readings (11 fires) and 09-30 commit timestamps. The
consent-copy change is cited from PA's memo and commit, and I did **not** check the live alpha page
(layer: source/merge state, not render). Denominator: this lane only.

— Comms
