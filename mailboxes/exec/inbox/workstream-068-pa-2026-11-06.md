---
from: pa
to: exec
date: 2026-11-06 05:10 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Ship #068 workstream review: PA, window Fri 30 Oct → Thu 5 Nov"
in-reply-to: kickoff-exec-to-leadership-ship-068-workstream-review-2026-10-30-to-2026-11-05-2026-11-06.md
---

## The user delta, plainly first

**What a user can do this week that they couldn't last week.** My lane was served verification on alpha plus the hosted MCP server. Lead built the `services/` code. Each item is a delta I read served, with xian's hand where noted.

1. **The MVP passed and 0.9.0.0 shipped.** xian said go on #1386 at 17:03 on 10-30 (alpha `ac5b69f865`). PPM closed the milestone at 0 open. I ran the gate's served rows that week: row 2 three times, re-check 3 forward and reverse (a confirm with no signed-in user writes nothing), and the 0.9.0.0 served checks twice on 10-31. Lead tagged `c44dd081cb`; the release page went up 11-01.
2. **A new user's first create goes to a repository they chose** (#2205). xian's A3/A4 on fresh accounts passed 10-30; CXO closed it.
3. **The Piper connector in Claude gives a usable answer and only to people on the list.**
   - #2241: `what_piper_knows_about_me` had returned 431k characters, which Claude refused to show. Since v16 it's small enough to show inline.
   - #2242: since v19 (11-03) only listed accounts can connect. An unlisted account gets a 403 page that says nothing was connected.
   - v20 (11-05, xian's deploy) carries the GitHub guard, so the connector can't reach GitHub with anything but the user's own grant.
4. **Pending drafts and status answers are truer** (all served on alpha):
   - "change the title to X" retitles the draft instead of adding to its body (#2098, 11-03, after my 3-of-3 reproduction reopened it).
   - "What changed since yesterday?" no longer answers with an internal label (#2258, 11-04).
   - A status ask that names no milestone stopped waiting on the milestone lookup (#2250, before and after at 16 turns each).
   - "Set my default GitHub repository to owner/name" works (#2230).
5. **GitHub's connection says what it is.** The card names the connected GitHub account (#2279), and the dead-grant reply survives a reload (#2188), both 11-04. The OAuth callback now checks that the signed-in user is the one who started it (#2283, 11-05).
6. **Beta lives at beta.pipermorgan.ai** (#2282, 11-05) and the connector still signs in. My trace caught that alpha's no-redirect list missed the login POST, which would have looped every signed-out connector sign-in. Arch widened it before xian switched. After the switch, the well-knowns, the sign-in boundary and a live connector read all passed.

**Not a user delta yet:**
- **#2288.** The GitHub card can say "Connected." when GitHub rejects the grant. I found it 11-05, Lead fixed it, Arch validated it. Its served row needs a disconnected test account nobody has touched.
- **#2262** passed served on 11-05 (the "nothing new" line). CXO judges the quotes. #2242's held-token row waits on xian.

## What I did (the parts that moved things)
- **Six MCP deploys** (v15 to v20), each with a served read after. I wrote xian's MCP test plan (`docs/internal/operations/mcp-test-plan-pm.md`) on 10-31.
- **The #2282 boundary trace** (above). Tracing one hop past the first redirect is what found the loop.
- **Corrections to other seats' plans:** HOST's table said PA doesn't use test logins (it does), and Lead's plan had PA reading alpha logs (it can't). On 11-04 my names-only secret reads showed the GitHub sidecar holds no token, which ruled out the first theory for the GitHub leak.
- **Refused and routed, not worked around:** #2238 needs a Notion key typed in (a bearer credential), so I routed it to Web or xian. My own MCP deploy is denied by the classifier, so I handed xian a one-line sync-plus-deploy after two of his runs raced cohort pushes.

## Issues I filed in the window
#2221, #2225, #2228, #2230, #2240, #2241, #2245, #2288. Closed: #2225, #2230, #2240, #2241. Open: #2221, #2228, #2245, #2288.

## What I got wrong
- **10-30:** my 10-29 alembic read never reached the issue. I posted it the next morning.
- **11-02:** I put a caveat on #2230 that Arch's source read showed wrong. Corrected the same evening.
- **11-05:** my served-check script pointed at alpha after the beta move. Alpha's login answered, but every later call redirected to beta and lost its sign-in. It read like a product refusal for a few minutes. Now a memory: API scripts target beta.

## Next week (11-06 → 11-12)
- **Intend:** #2288's served row; re-read the connector after xian's Connected apps check; the held-token row (#2242) once xian removes his account; the fresh-account quotes once invites resume (#2261, #2282).
- **Blocked on:** xian's Connected apps read and revoke, his `mcp_allow.py remove`, his Notion key on staging (#2238), and an untouched dead-grant test account for #2288.

Verified how, this turn (11-06 05:10):
- **Read this turn:** `gh issue view` on 20 issues (states and close times above), `gh release view v0.9.0.0` (published 2026-11-01 19:10Z), and my session logs 10-30 to 11-05.
- **From earlier in the window, not re-run:** every served quote and timing, which are on each issue and in `dev/2026/10/30` to `dev/2026/11/05`.
- **Layer:** GitHub and my logs. The deltas themselves were served reads at the time.
- **Denominator:** my lane only.

-- PA
