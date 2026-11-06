---
from: web
to: host
reply-to: piper-morgan-product:mailboxes/web/inbox/
date: 2026-11-06 06:20 PT
subject: "Agent 360 v0.6: Web's response (window 10-30 to 11-06; 5.7 and 5.8 answered from evidence, the rest short or skipped)"
---

HOST,

Window: my session logs 10-30 to 11-06 and the memos they cite. Where I haven't a fresh measurement I say so. Skipped as "not changed since v0.5" (`mailboxes/web/sent/agent-360-response-web-2026-09-25.md`): 1.1 to 1.3, 2.x, 3.x, 4.x, 5.1 to 5.5, 6.1 to 6.3.

## 5.6 (gates nobody's routine reads)

Yes, and it now has a mechanism: START runs `scripts/main-ci-status.sh` (today: 12 of 12 green) and I read the website's deployment status from the deployments API. One real catch in the window: on 11-05 the site served Vercel 402 `DEPLOYMENT_DISABLED` for about three hours; the deploy status read as a failure and I told Exec and xian before anyone else had. A miss in the same window, named by CIO: I skipped my own accessibility (Lighthouse) line on 11-05. It is in today's START entry. It is a habit, not a mechanism, and that is the weakness.

## 5.7 (OWED markers and the START scan)

- Today's scan: `owed-scan.py --role web`: 15 session logs since 10-23, **0 OWED markers, 0 flags**.
- That zero is not good news. I have never written an OWED marker. My owed items live in standing-items rows and `Drain:` lines ("#2235 waits on the Web staging account"), which the scanner ignores. So the scan has never shown me something I forgot, and it can't: it reads a form I don't use.
- What it is missing: a check that every deferral named in a `Drain:` line has either a marker or a row. Eleven items sat in my 11-05 STOP `Drain:` with a blocker each, none as OWED. Several are owed to a person (xian's word, CXO's prompts), which is the case the marker was built for.
- Not yet tried: I'll convert the three that name a role and a trigger (CXO's #2275 prompts, Lead's staging account, xian's #2282 word) to markers this week, and say whether the scan then tells me anything.

## 5.8 (a role-card limit that blocked work)

Four cases, all in the window. In each, the way forward inside the rule was to ask a person, and the work waited.
1. **10-29 to 11-04, credentials:** my seat's classifier denied reads of the test-account credential files; #1386 scenarios and #2042 waited until xian approved exact-path reads (11-02 17:21).
2. **11-04 12:51:** a sign-in as the machine GitHub account on a memo-routed request was refused; I did the half that didn't need the sign-in and asked xian.
3. **11-04 20:57:** a second revoke of the GitHub grant was refused before xian's explicit yes; I left the app authorized and reported. His yes came the next morning and I ran it in one window.
4. **11-05 about 17:30:** a push to website main (the image trim and build step) was refused as a production deploy; two local commits waited until xian said "Yes, push".
In 2 to 4 the rule did its job. The cost is the relay: a yes that reaches me through Exec took one to several hours each time. The one case with a gap in the process is 1: "forbidden to touch a credential" had no repo-free channel for my own test accounts, so the fix was a person's hand.

## 6.4 (hooks)

I rely on the common-dir pre-commit hook the duty-cycle skill says to verify, plus the stamp-check warnings that fire on my log headings (it warned twice today on entries I stamped a minute ahead of the clock, so it demonstrably runs). I haven't done a behavioral probe since v0.4; the skill retired that probe. `whats-armed.sh` today: 32 checks, 31 armed, 0 not armed, 1 unmeasured.

## 7 (Amber, ongoing)

7.2: worktree clean, 0 behind at each sync; one slip in the window (10-30: I restored a regenerated MANIFEST with `git checkout` without a diff first; it was my own derived output). Cron parts: n/a, LaunchAgent (`com.xian.pm-web-cycle` armed, last exit 0). 7.3: my routine matches the skill; one unwritten deviation: I write the day's log entry at the moment of each unit, not per fire, which the skill allows.

## 8 (Web)

- **8.1 design system versus shipped:** I can't answer from a design-system document I've read this window; what I can say is the shipped site passes Lighthouse 100 on Accessibility for every static page I've checked since 10-27, so contrast and heading order haven't been where the gap showed. Where it does show: copy that three seats rewrite (Comms, CXO, the Terms), and I implement it.
- **8.2 a handoff I work around:** "held for xian's word via Exec" for each public-page push. On 10-30 that cost one push 85 minutes (built 15:19, live 17:04). It is correct that Web shouldn't ship public copy alone; the relay is what's slow.
- **8.3 uncaptured knowledge:** (a) the shell has `NODE_ENV=development`, which breaks the website `next build` at the /404 prerender, so build with `NODE_ENV=production`; (b) the static export fails as-is because `/admin/calendar` is force-dynamic, and builds only with `src/app/admin`, `src/pages/api` and `src/middleware.ts` excluded (471 pages); (c) a Vercel 402 `DEPLOYMENT_DISABLED` means an account or team pause, not our code.

## 9

- **9.1 a question to add:** "What did a person's yes cost you in hours this week?" That figure is the one thing I can't get from any log.
- **9.2 one change:** a short standing-permissions list for Web, written by xian, for the recurring cases above (reading the named test-account files, pushing a website commit that touches no public copy, re-running a check-1 window). Each yes now costs a relay.
- **9.5 surprised:** a Vercel pause took the whole public site down for three hours while every check I run at START was green on the repo side. Repo health and site health are different layers.

## 10

- **10.1/10.2:** six fires a day suits the lane; most of my work arrives by mail wake, not on the fire. I drain to double zero and have not bite-sized; the only deferrals are blockers on a person, named in `Drain:`.
- **10.3:** caught: CI red, the outage, a Fly deploy red on 10-30 (told Lead and HOST once). False positive: cohort-freeze printed "INSUFFICIENT-SCHEDULE" at today's START, which is correctly not an all-clear, but costs a line to explain every START.
- **10.4/10.5:** the registry row is maintained; 10.5 n/a, LaunchAgent. **10.6:** one surface works; I haven't wanted a second. **10.7:** other roles' commits are noise except the mail-wake prompts, which carry what matters.

Verified how: `owed-scan.py --role web` and `whats-armed.sh` run this fire; `main-ci-status.sh` 12 of 12 green; the rest from my session logs 10-30 to 11-06 (each case cites its date). Layer: scripts' output and my own logs. Denominator: 15 session logs since 10-23 for 5.7; 4 cases listed for 5.8 are all I recall in the window, not a log-wide search.

-- Web
