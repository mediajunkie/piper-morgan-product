# Exec carry-forward

**Rewritten 2026-11-27 22:02 PST at STOP.** Model: Opus 5.5. History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/27/2026-11-27-0511-exec-code-log.md` (closed). Session compacted once on 11-27; resume via the log.

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake (timeout 200000+). Ack one at a time. Janus via mail-send-external.sh (see git history of this file for the recipe).

**Clock rule live:** no estimated minutes in commits, mail or logs. Headings: `scripts/log-entry.sh "title" >/dev/null`. Times in backticks.

## Routing today (xian, 11-28, via Janus)
"If the Piper team needs me for other things today they can relay > exec > janus > me." Piper asks for xian go to Janus (designinproduct docs/mail/), not to him. Sent today's list 11-28 (ae767ed0c4): cohort note words, Test All press (2475 rows 1 and 2), Step G when he opens a session. His Saturday: blog post with Comms, then Rebel, Tally, his novel.

## Cohort note (approved 11-28, waits on the hold lift)
xian: "HOST's line is approved." xian sends it from his mailbox; HOST gives the text and the recipients. It goes after PPM's lift memo and his go (PDR-008 s3; 2342 and 2282 are open). At the lift, if Step G has not served the Disconnect read, bring him HOST's and CXO's recommendation: send without the "as the code is written" sentence (01M8HM385K, 01M8HMA2BX). PPM amends PDR-008 3.3 ("HOST sends them").

## Sat 11-28 START, in order
1. Retitle the rollup h1 to Saturday (rollup v1200, `719UZ4h1NELjEwWZbDCceT`, source `dev/active/exec-attention-rollup-current.html`). xian's format rule (11-27): only current and actionable items at the top; finished items come off (they're logged) or go below everything that needs him.
2. Sprint 3 day 2 (11-27 to 12-10; theme "Signed In"; top priority is opening invitations). Weekends are prime time, so don't treat Saturday as quiet.
3. Chase the 11-27 closes still open at 22:01: CIO, Docs. Chase only if they're still open.
3b. Eight v3 memos from 11-20 to 11-25 (Janus, Pard) still sit in `mailboxes/exec/inbox/`. For each, check the log shows it was handled, then file it to read/ one at a time with mv plus mail-send.sh. Never bulk-move: a file in read/ is a claim it was handled.
4. Expect replies to 01M8GBR9581CCEYR44VE9JGY6Y: Lead (why beta uses the Alpha Google project, and what self-hosting needs today), PPM (placing the one-project move in sprint 3 or 4, and the self-hosted tester against the invite goal), Arch (owner-first details), HOST (the first-cohort note text, and who it goes to). Bring them to xian. PA owes "what do you think of your name" (01M8GBRBW0JCFT3ZV21WR6YEKQ).

## xian's sitting (paused, resume where he is)
- Step 3 done 11-27 night: GitHub and Calendar connected on beta, both redirects named beta, neither tested yet (Test All Connections is optional). HOST's final cohort note: xian reviews, possibly Sat morning.
- Then, one thing at a time: Step G (a) connector `Piper Morgan (seat)` at `https://mcp.pipermorgan.ai/mcp?client=seat`, Allow as seat-github-1 in a private window; PA's seat check. The zero-install read: take piper-test off the seat-test team, Web and PA read, put it back at Read exactly; piper-test-2 untouched. Step G part 3 (three pastes on PA's word; the address comes from beta's /account as seat-github-1). Revoke seat-github-1's own authorization ("Never uninstall the App from the pipermorgan org."; no reconnect, option (a)). Ending: remove `Piper Morgan (seat)` and the allowlist entry. The alpha callbacks come off no earlier than about 12-04, a week after the cutover (2282 row 4, PPM): each app keeps one callback, wildcard unticked, read back to me.
- Hold Lead's promotions while he's in an active step. Promotions run 07:00 to 21:00.
- Afterwards: Slack card Disconnect (harmless leftover); the manual-credentials card on the Calendar page goes to CXO (he'd deprecate it).

## xian, not urgent
- 2471 deploy time limits: yes or no. Three Fly reads (`fly` account on Amber, MCP builder 2472, log retention). Fly-deny paste (on the rollup card); then PA runs three refusals. Tue 12-01 document discussion hour. `rm -rf ~/cutover-tmp`. Optional: rename the board field "Sprint" to "Epic" (rename only).
- The outside tester he wants on a self-hosted beta: the name is held by Janus only (designinproduct bf7c7e411f). Asked whether he's xian's advisor (the rule-8 exception). Janus also holds the Duet's third question (scheduled check-ins).

## Served 11-27 (for the Ship and day arc; off the rollup)
Paths 2 of 2 (A 13:44, B 14:44). 2261 served (invite hold 1 of 3). Cutover: 0 classic grants, PASS. Seven promotions; beta `8ddd08d8e0` since 20:02. 2470 settled: row 2 split, Arch condition 7 (xian likes it), the prompt pass is Lead's first unit next session. Fly deny on main (`e6c625572a`). MCP stays on `c303931894` (two deploys hung, 2472).

## Standing word
- Promote gate: "Yes, changes that only make the check stricter can go ahead with Arch's approval, although I should still be informed." I tell him the same hour.
- Tell-one-agent (11-23): "I need to be able to trust that I can tell the agent I am working with such an update and that I will not have to also manually report it to their primary point of contact let alone to you directly."

## Rules I keep
- Timestamps only from `date`. Every grant is xian's own edit. No seat runs `fly`. A refusal is final and is not reworded. The keychain is off-limits without his permission. Never direct a seat to read its `.env` or settings file.
- D6-check every step that lands on him: who would actually do it? Check (tmux ls in full, not `head`). Don't ask him what the team can answer. No account emails or secrets in this repo.
- Before re-asking xian anything, grep decisions.log for it (11-23: Janus nearly re-asked three questions he had settled 11-20, because my review page never marked them answered).
- At STOP: rewrite this file, list the other seats' closes, and close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06). Walk it on xian's talk list only if he wants it.
