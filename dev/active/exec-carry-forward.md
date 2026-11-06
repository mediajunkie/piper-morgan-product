# Exec carry-forward

**Rewritten 2026-11-04 22:02 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/04/2026-11-04-0423-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. An empty CronList is normal, and there's no STOP re-arm. Agent liveness is Pard's.

**Cron gate:** the duty-cycle-tick cron steps (the CronList self-heal and the STOP re-arm) don't apply on a LaunchAgent.

## Rollup
v841, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with a Python replace plus an assert. Re-check every item that waits on xian live, on every fire. The source is in a public repo, so describe security findings by class only, with no steps.

## Where things stand (end of 11-04)
- **Served:** alpha `72bd53546a` (read 22:01, healthy). Main CI is 12/12 green. The next promotion carries #2178 (`b5df29d4e6`, validated by Arch at 21:02).
- **Ship #067 "What Piper Didn't Check"** published 11-04 (https://pipermorgan.ai/shipping-news/weekly-ship-067-what-piper-didnt-check). xian wrote it from my scaffold. **The LinkedIn URL is still owed** by xian; then Docs marks it distributed.
- **GitHub incident, settled by observation** (decisions.log 20:13):
  - GitHub's button names the OAuth App's owner. The census showed 0 crossings.
  - Org `pipermorgan` created. Both OAuth Apps transferred and renamed: "Piper Morgan" (alpha, Ov23…QBmR) and "Piper Morgan Staging" (Ov23…zgot).
  - Wildcard redirect matching is off on both. xian's alpha Test passed at 20:55.
- **Invite hold** (xian 19:31: no invitations of any kind; no design partners yet; no lawyer yet):
  - P0s left:
    - #2261: scope; waits on #2174's runs.
    - #2178: built; rides the next promotion.
    - #2283: callback session-binding tenancy. PPM filed it under the 19:31 rule; Lead builds it at the 11-05 START, and it covers #2281.
  - #1551: met (Tests green on `56b284defb`).
  - P1: #2157 (the drill; its precondition is met) and #2158.
- **Held cohort note (HOST):** waits for #2283 to land, then Lead's census rerun plus a Calendar counterpart, then HOST's re-read.
- **Posts:**
  - Thu 11-05 "Don't Overpromise": xian's voice pass in the morning, plus Saturday's title for its footer.
  - Sat 11-07 "What Reaching Private Beta Means": building, Medium only, xian writes it.
  - Sun 11-08 "Fixed and Scores Higher Came Apart": insight.
  - Tue 11-10 and Thu 11-12: beats 2 and 3.
  - xian wants an editorial-strategy session with Comms.
- **Closed today:** #2188 and #2279 (CXO 21:48). #2284 filed: a stored Slack token still feeds answers; Lead's to fix.

## Waiting on xian (morning, after his blog post)
1. Confirm #2283 as P0 (it is already labelled). Decide whether #2281 joins; #2283 mostly covers it.
2. **#2282:** make beta.pipermorgan.ai the one public host. PPM, CXO and Exec all say yes. If yes, it is Lead's unit, before the first invite.
3. **"Yes, second revoke"** for Web's after-transfer check 1 (expect "Authorize pipermorgan"), and a glance at the Staging app's callback list to see whether the beta.* line is gone.
4. **#2174's two runs:**
   - Lead's steps are in his 20:52 memo (on main at `466b51ffdd`), plus his two later lines: see that `d3-not-installed` exists first, and treat the old token's 401 as information only.
   - The second run comes 8 hours after the first.
   - Custody, per HOST: the secret and tokens stay only in xian's password manager.
5. The Ship #067 LinkedIn URL.
5a. **MCP deploy, not landed** (PA 21:47; still v19). Both of xian's runs were refused because pushes landed between the sync and the run. The fix is one line in PA's session: `! git fetch -q origin main && git merge -q --ff-only origin/main && scripts/deploy-mcp.sh`. I wrongly told him at 19:49 that it had gone through.
6. Sprint planning (PPM's onboarding proposal, sprint length) and the #1715 skills walk.
7. Smaller items:
   - the Buttondown confirmation paste and sign-up test;
   - the staging account and the Notion key;
   - the #2264 look;
   - #1514.

## Reminders owed to xian
- **Vercel: downgrade from Pro once the headroom exists again** (xian 11-05 16:45). The trigger: the split is live (public site off Vercel) and the usage page shows the admin-only project well inside Hobby. Caveat to raise then: Hobby is for non-commercial use, and Web reads an admin tool for a commercial product as commercial, so the downgrade may not be allowed even with headroom. Check vercel.com/pricing and the terms at that time.
- **#2282 step 5, around Thu 11-12:** remove the alpha callbacks in GitHub and Google if a week passes with no hits.

## Mine
- Relay xian's rulings at once and record them in decisions.log. Timestamps come from `date` only; stamp-check catches estimates.
- Ship-kickoff and map checks Fri 11-06. Mail v4 review 11-05.
- Write DAY-CLOSED in grep form, `<!-- DAY-CLOSED: YYYY-MM-DD -->`, as the log's last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. The #1715 skills walk with xian was due Tue 11-03 and is overdue. xian named it for the 11-05 morning.
