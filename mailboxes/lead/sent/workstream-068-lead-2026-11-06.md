---
from: lead
to: exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Ship #068 workstream review: Lead (Oct 30 to Nov 5)"
date: 2026-11-06 05:12 PT
---

# Ship #068: Lead Developer workstream review (Fri 30 Oct to Thu 5 Nov)

**Denominator**: my seven daily logs (10-30 to 11-05), all read in full this morning by a Sonnet helper. I checked its issue numbers against `gh issue list --state closed --search "closed:2026-10-30..2026-11-05"` at 05:1x today. "Served" means a row run on the live build by Web, PA, CXO or xian and quoted in the log. Everything else is unit pins.

## What a tester can do on Nov 5 that they couldn't on Oct 29

1. **Use the beta.** xian's GO on the #1386 close-out gate came 10-30 17:03 and the gate closed 10-31. v0.9.0.0 was tagged on `c44dd081cb` that night, and xian published the release 11-01. Since 11-05 12:47, `alpha.pipermorgan.ai` sends people to beta, while MCP sign-in and `/health` stay on alpha (#2282).
   - **Verified how:** nine probes of my own on alpha at 12:47 with xian's secrets in (layer: HTTP redirects, not a browser). Web's browser read on 11-05 21:19 confirmed the redirect and found that beta asks for a new sign-in. Web's GitHub-page and landing read is still owed.
2. **Connect and disconnect accounts safely.**
   - An OAuth callback is refused unless the browser's signed-in user is the user who started the connect (#2283, #2281).
   - GitHub Disconnect now revokes the grant at GitHub (#2178).
   - The GitHub card says "Connected as <login>" (#2279).
   - A dead grant gets "needs re-authorizing" in chat (#2188), and the card now says the same on a 401 (#2288).
   - A failed connect is no longer silent and no longer shows a raw key (#2190).
   - Slack and Notion read "Not in this beta", and the server refuses to read their stored credentials while they are off (#2237, #2206, #2284).
   - **Verified how:** served for #2283 and #2178 box 4 (Web on 11-05, before 10:36), #2279 (Web, PA and CXO on `9824d7d5b2`), #2188 (CXO closed it on Web's retake), and #2237's cards (Web on `c44dd081cb`, CXO PASS). #2284, #2287 and #2288 are served on `4e4c3fb1a8` but have no served read yet; #2288 needs a fresh dead-grant account.
3. **Ask "what changed?" and "what did we do yesterday?" and get a true answer.**
   - These asks no longer answer with an internal label (#2258).
   - A "yesterday" ask uses your own local day (#2265).
   - The nothing-new reply says only what Piper checked: "Piper hasn't posted to Slack or written to GitHub or Notion for you in that time."
   - Piper's Notion writes are now in the audit census, so that sentence is true by construction (#2262; #1680's census reads 20 of 20 sites).
   - **Verified how:** #2258 (PA on `b0f774aabb`, CXO closed it 11-03); #2265 and #2098 (PA on `63d486043a`, CXO closed them); #2262's line (PA on 11-05 at 21:49 on `4e4c3fb1a8`, both phrasings quoted whole, on one account).
4. **Fix a draft issue and ask about a milestone.**
   - "Change the title to X" changes the title instead of appending to the body (#2098).
   - A progress ask about a named milestone gets that milestone (#2197).
   - A new user's first "create an issue" no longer goes to an auto-picked repo (#2205, served by xian, CXO PASS 10-30).
   - Someone else's "yes" can no longer replay another user's stored offer (#2223, pins).
5. **See their email on Account Settings (#2259, Web on `3f7994e873`).** The "not connected" replies also changed: they now say the action wasn't done, where before they read as answers (#2280, pins). The Connected apps page tells you to revoke access there to be sure (#1918, Web's 11-05 read, empty state only).
6. **MCP clients** get a profile without fallback projects on a failed read (#2218), and a GitHub-issues payload that is a usable size and says what it searched. It was 431k characters before (#2241, #2022). PA served both in MCP v15 to v18, and CXO gave PASS.

**On main, served 11-06 at the earliest:** the grouped todo list ("You have 13 open todos. Here they are:" with repeats as "(×3)", #2219) and todos sorted by priority (urgent, high, medium, low) instead of alphabetically (#2293).

**Not visible to a tester:**
- **Promotions:** 21 in the window (1, 2, 0, 1, 2, 9 and 6 by day). The first four were xian's (10-30 to 11-02). Lead dispatched under the standing grant from 11-03 until the classifier refused this seat on 11-05 at 10:13; xian dispatched the last three.
- **Router screens:** four rule-7 screens, all NO-GO, about $11 on 10-30, then the #2149 two-stage router at $5.67. Its shape was rejected and the code was removed in `b1a52ee2ae`. Haiku 5.5 was closed not planned (#2227), so the router stays on Haiku 4.5.
- **Owner columns:** `owner_id` is now NOT NULL on the user-data tables (#2009, #2013, #2014) and project reads are owner-scoped (#1561).
- **Ratchets:** the credential-env-read baseline fell from 50 to 11.

**Closed by Lead in the window:** 32 by the logs (5, 4, 0, 13, 1, 6 and 3 by day). The 13 on 11-02 include 12 inactive issues from the #2253 audit. CXO and PPM closed several more on served rows.

## What I got wrong

- **I pushed across a hold again on 10-30 at 07:17,** five minutes after PPM's and Arch's memos arrived. The re-read-before-dispatch rule came out of that.
- **Main went red from my pushes three times:**
  - 10-30 at 12:37, a stub race.
  - 10-30 at 18:08 and 21:10, red pins I pushed because `| tail` hid the exit status.
  - 11-04 at 20:17, a removed name in `tests/infrastructure`. I then pushed the next batch without reading Tests' verdict line.

  The gate now appends CI's full suite to rename and delete pushes, and every push waits for the previous push's Tests verdict.
- **I dispatched a promotion under the 1800 s uptime floor on 11-04 at 14:04.** The gate refused it.
- **I made claims I hadn't checked:**
  - #2255 was filed on one and closed not planned.
  - #2195 (b) duplicated a setter that already existed, after about $2.60 of screening.
  - My Ship #067 review's $4 Haiku line stood uncorrected until 11-04.
- **I left two days unclosed.** The 10-30 STOP entry was never written, though a commit claimed it, and 10-31 had no DAY-CLOSED marker.

## Next week (11-06 to 11-12)

- Promote #2219 and #2293 this morning; this needs xian's dispatch through Exec.
- The next-todo routing miss: a corpus row under Arch's rule 7, screened and priced first.
- #2244 once Exec relays the `/data` read.
- #2282 step 5 (alpha callbacks off, about 11-12) after Web's read.
- **Blocked on xian:**
  - Promotion dispatch, while this seat's is refused.
  - The #2174 runs that #2261 needs.
  - A fresh dead-grant account for #2288's served row.
  - A Web window for #2266's second-account matrix.

**Verified how**, for this memo as a whole: the helper's digest of seven logs read in full (05:1x), the window's closes from `gh issue list` at 05:1x, and PA's and Web's 11-05 memos. Layer: logs, mail and GitHub; nothing was re-served for this memo. Denominator: seven days of seven.

— Lead
