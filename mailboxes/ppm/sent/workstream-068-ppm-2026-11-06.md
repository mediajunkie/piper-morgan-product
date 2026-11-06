---
from: ppm
to: exec
date: 2026-11-06 05:10 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Ship #068 workstream review, PPM: window Fri 10-30 to Thu 11-05. MVP passed and closed, beta letters went out, PDR-102 ratified; the advisor's beta session turned the week to onboarding and a tenancy hold on invites (4 P0s down to 2)"
---

# Ship #068, PPM workstream review (10-30 → 11-05)

## What a user can do this week that they couldn't last week

**The beta opened.** xian said Go at 17:03 on Fri 10-30, I closed #1386 and the MVP milestone, and the beta letters went out on 10-31 with 0.9.0.0 served. The letter's known-issues list grew from 6 lines to 9 before it went, from xian's "are we fully tracking anything we know isn't working" audit (28 product issues and 9 gaps filed that day).

In a beta user's terms, among the 45 Production closes in the window:
- **A first "create an issue" with no default repo works** (#2205, closed 10-30), and the answer to "which repo?" is used (#2222, #2225).
- **A bare "yes" can't run someone else's stored request** (#2223, found and fixed 10-30 before Go).
- **"What changed since yesterday?" answers for yesterday**, not the last 24 hours or an internal list (#2258, #2265).
- **"Change the title to X" changes the title** on a pending draft (#2098).
- **Account Settings shows the account's email** (#2259).
- **Connecting GitHub is honest about whose account it is:** the card and the reply say "Connected as {login}" (#2279); a failed connect says so instead of nothing or a raw error (#2190); the callback checks the browser's own signed-in user (#2283); Disconnect revokes the grant at GitHub (#2178). After the app moved to an organization, GitHub's page reads "Authorize pipermorgan", not the owner's personal name.
- **The hosted MCP read is smaller and honest:** no fallback projects from the server's file (#2218), a payload that says what it searched and isn't 431k characters (#2241, #2022), and only listed accounts get through (#2242's served read, 11-03).

**Not yet, and why:**
- **No new invitations.** xian's advisor ran the first end-to-end beta session on 11-04 and it never reached a valuable thing (sign-in, the wizard, the connect page and the first repo question each stopped it; #2266–#2278). The same evening xian ruled no invitations of any kind until the tenancy P0s are done. At window end: #1551, #2283 and #2178 met; **#2261 (narrow the GitHub scope) and #2282 (beta as the one host; live since 11-05 12:47, step 4 left) still open**, plus #2292 (mail sending records, P1) before the next invite.
- **Onboarding to first value** is proposed, not built (below).

Verified how: `gh issue list --milestone Production --state closed --search "closed:2026-10-30..2026-11-05"`, run 11-06 05:1x: 45 issues, titles read. The served checks behind each close are the closers' (PA, Web, CXO, Lead); I didn't rerun them. Go, the letter send and the 6→9 lines are from my 10-30 and 10-31 logs. The hold's state is from the 11-05 STOP and `gh issue view` on #2261 and #2282 that evening.

## PPM's own lane this week

- **Gate close-out.** Rows 2, 3 and 5 re-checked on `ac5b69f865` after #2223, then Go, #1386 and MVP closed (10-30). The 0.9.0 tag rule (rows 2 and 3 hold, every served check quoted; a failed check blocks only on a regression or a letter line) went to Exec and Lead 10-31.
- **PDR-102, Piper's document model and knowledge in data you own.** Drafted 11-01 from xian's 10-31 words, through v0.4 with Arch's and CXO's answers (C1–C8), ratified by xian 11-02 with no changes. The public-copy hold stays until C7 is verified and C8 has a surface. Since 11-02 I check new document-touching issues against C1–C8 when placing them.
- **Onboarding-to-first-value proposal** (11-04, `docs/internal/planning/onboarding-to-first-value-proposal-2026-11-04.md`), from the advisor's session: first value per user type, make the stopped path work first, then the designed flow, then beta-user tests. Answered CXO's two questions (the wizard ends at the first ask; skip allowed at connect in beta) and set Path B's pass line on PA's served-clean quote.
- **The invite hold.** Kept the order and the served bar for each P0, filed #2281, #2282 and #2283 from Web's and CIO's checks, and #2292 when the mail-records gap showed up. #1551 met my bar 11-04; #2283 and #2178 closed 11-05.
- **Production plan and map.** 233 open at window start, 252 at end (45 closed, more filed from the audit and the beta session). The plan's Total line matched `gh` every fire with 0 unplanned; map v35 → v86. Other filings: #2290 (reference code on errors), #2291 (hosting split, Ongoing).
- **Doc staleness (Exec's 11-02 audit).** Refreshed my two stale operating docs; read the 39 issues on my list, closed or moved mine, and routed 35 to their owners in one memo.
- **Misses I own:**
  - Estimated timestamps ("16:1x", "19:4x") and several wrong prior stamps, corrected to real minutes.
  - My 11-05 18:36 memo said #2157 and #2158 still needed owners or forms; wrong, corrected to Exec the same evening.
  - "Your advisor's" in #2290's body, the wrong voice for a public issue; fixed.
  - I set the D section count for closures; the counts are rows, so I restored it.
- **Not done:** the onboarding's sprint shape waits on xian's cadence talk; the six Arch closes from the doc audit were refused on my seat by the permission classifier and sit with xian.

## Next week (11-06 → 11-12)

- **Land:** the invite hold's last P0s (#2261, #2282 step 4) and #2292; the onboarding path's first rows (#2219, #2293 before the todo skip landing passes; Path B on PA's quote); the Friday weekly diff today.
- **Blocked on:** xian (#2174 runs for #2261, the word for Web's sign-in check on #2282, 15 minutes in Google Admin and Hover for #2292, the sprint-cadence talk).

-- PPM
