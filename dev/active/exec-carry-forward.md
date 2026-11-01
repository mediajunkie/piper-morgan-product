# Exec carry-forward

**Rewritten 2026-10-31 23:1x PDT at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/10/31/2026-10-31-0429-exec-code-log.md` (closed).

**STATE: LIVE.** Cron **`fb8db3e2`** (`38 6,10,14,18,22 * * *`), re-armed 10-31 at STOP from the stored prompt; `seat-prompt.sh exec --check` rc=0. Expires about 11-07; re-arm at each STOP. LaunchAgent `com.xian.pm-exec-cycle` is staged by Pard and not yet loaded (xian's paste, Pard console v184). On Pard's load notice and the first :01 fire that lands work, CronDelete the session cron and flip the registry row (row 179).

**Re-arm only from the store** (duty-cycle-tick v1.60): `scripts/seat-prompt.sh exec` prints the verbatim prompt. Pass it to CronCreate unchanged, then CronList and `--check <file>`. Never rebuild from memory (xian 10-30).

## Rollup
v737, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with Python replace plus an assert, never sed.

## Where things stand (end of 10-31, beta launch day)
- **Beta letters sent** (xian, 13:51). **v0.9.0.0 tagged** on `c44dd081cb` (Lead 22:01, PPM's go 21:51). Alpha and beta serve it (xian's second promotion, run 41272799100). CXO row 2 triage 34/42, no regression; #2245 served PASS.
- **#2229 live** (Web): 0 "alpha", 308 redirect, hero line passed by CXO. Open: Buttondown confirmation-email check.
- **First sprint SET** 21:17 via PPM: 22 issues, #2242 (a), #1300 closed, #2247 Slack source in 1.0, bot Fast Follow, ~30% reserve. Lead's 11-01 START: #2149 enum and #2042 option 1 ahead of #2242 (PPM's call).

## xian's morning: three pastes (rollup hot card)
1. `gh release create v0.9.0.0 …` (command on the rollup). Then tell Lead and Docs (Docs adds the release URL to the briefing Version line, Docs 22:04 memo).
2. `set_default_repo`: printenv, then `fly secrets set` with the value appended. Relay both outputs to CIO, then PA's probe and one row 2.
3. Buttondown: HOST read access to `beta-waitlist`, then one sign-up with his own address. Relay the result to HOST, Comms, Web, CXO. #2229 closes on it.

## Waiting on xian (his word)
- Sprint field (PPM 09:35, one escalation): #1706 edge, rec (a) move #1441 into PUB; five closed ops issues, rec INFRA. PPM applies via assign-sprint-safely.
- PDR-102 ratification (PPM 06:51, v0.3, Arch and CXO reviewed). Relay his answer to PPM, Arch, CXO and Comms; PPM records it. Comms holds "data you own" claims until C7 is verified and C8 has a surface.
- CIO's alpha promotion grant with the reworded review trigger (Exec: yes).
- Fresh test accounts: rec xian signs up, PA quotes his screenshots. Relay to HOST, PA, PPM.
- contribute@ and privacy@ routing. support@ is answered (alias to alpha@, decisions.log 18:33).
- Lead's promotion allow (row 9a, key lead-promote-allow), optional now. Relay to CIO and Lead.
- Ship #067 week review (artifact `4Le3ZyacNXUqo19SQh5GpT`; nine workstream memos in the inbox). The draft waits on it. He also owes first-sprint feedback.
- His hand: ghmint fix (Pard v185), LaunchAgents (v184), two Fly reads (#2244 `ls -la /app/data /data`; #2226 memory panel), web-pat-test, #1514 Slack app submission.
- PA's MCP test plan notes (`docs/internal/operations/mcp-test-plan-pm.md`).
- Rule-8 history whenever he takes it up: HOST's briefing people list; #1509's title; HOST's 10-30 log, two entries.

## Mine
- Relay xian's rulings at once; record them in decisions.log. Timestamps from `date` or the source memo's stamp.
- Briefing-pointer recheck Mon 11-02 (AGENT counts 4/5, #2157 exempt). Ship-kickoff check Fri 11-06. Map diff Fri 11-06.
- Rule 8: outside names stay out of everything I write here.

## Owed rows (owed-scan)
- key: crossposts-1101. Filed: 2026-11-01. Relay xian's Medium and LinkedIn URLs for Check the Machine First to Docs.
- key: exec-launchagent-cutover2. Filed: 2026-10-31. CronDelete the session cron and flip registry row 179 on Pard's load notice.
- key: 1715-review. Filed: 2026-10-31. The #1715 skills walk with xian, due Tue 11-03.
