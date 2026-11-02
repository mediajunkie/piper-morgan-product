# Exec carry-forward

**Rewritten 2026-11-01 23:1x PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/01/2026-11-01-0429-exec-code-log.md` (closed).

**STATE: LIVE.** Cron **`ed995092`** (`38 6,10,14,18,22 * * *`), re-armed 11-01 at STOP from the stored prompt; `seat-prompt.sh exec --check` rc=0. Expires about 11-08; re-arm at each STOP. LaunchAgent `com.xian.pm-exec-cycle` is staged by Pard and not yet loaded (xian's paste, Pard console v184). On Pard's load notice and the first :01 fire that lands work, CronDelete the session cron and flip the registry row (row 179).

**Re-arm only from the store** (duty-cycle-tick v1.60): `scripts/seat-prompt.sh exec` prints the verbatim prompt. Pass it to CronCreate unchanged, then CronList and `--check <file>`. Never rebuild from memory (xian 10-30).

## Rollup
v745, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with Python replace plus an assert, never sed. Re-check every xian-gated item live on each fire (I missed his 11:10 release page until Janus said so).

## Where things stand (end of 11-01)
- **v0.9.0.0 complete.** xian published the release page at 11:10 PST; Lead confirmed at 20:15 that the tag is the served sha and the post-release audit is clean. Docs adds the URL to the briefing Version line (told at 20:2x).
- **Served (23:08 read):** alpha and beta 0.9.0.0 `c44dd081cb`. Last promotion dispatch 04:21Z 11-01. CI 12/12 green.
- **#2242 order is final** (PPM withdrew add-first 07:50; Arch 07:45): promote, then `mcp_allow.py add`/`--apply`/`list` in the container, reconnect the Piper connector in Claude once if disconnected, then PA's MCP deploy and checks. The script isn't in `c44dd081cb`, so add-first can't run.
- **#2149:** two-stage routing rejected ($5.67, parity failed twice); #2197/#2184 by op-local resolution; #2250 on main.

## xian's hand, in order (rollup hot card)
1. ghmint fix (Pard console v185, mediajunkie `ea2bdcd`). Three outages (10-30, 10-31, 11-01 13:28–14:00). Relay to CIO and Pard; row 9d closes when mints are 15 minutes apart.
2. `set_default_repo`: printenv, then `fly secrets set` with the value appended. Relay both outputs to CIO.
3. Promote (dispatch line), then the #2242 allowlist add (three lines with his email), reconnect if needed. Relay `list` to PA, Lead, Arch, PPM.
4. Buttondown: HOST read access to `beta-waitlist`, or one sign-up with his own address (HOST prefers the sign-up). Relay to HOST, Comms, Web, CXO. #2229 closes on it.
- Also his hand: web-pat-test sign-in, Notion key on staging for #2238, LaunchAgents (v184), Fly reads #2244 and #2226, #1514.

## Waiting on xian (his word)
- #327: close as not planned? (rec yes, PPM too). Relay to PPM.
- CIO's alpha promotion grant (Exec: yes). Lead's promotion allow (row 9a, v4 01M69F0FT2HW9Z00BZP5MXB11P left unacked on purpose). Relay to CIO and Lead.
- Fresh test accounts: rec xian signs up, PA quotes his screenshots. Relay to HOST, PA, PPM.
- contribute@ and privacy@ routing.
- Ship #067 week review (artifact `4Le3ZyacNXUqo19SQh5GpT`); the draft waits on it. First-sprint feedback.
- PA's MCP test plan notes; rule-8 history whenever he takes it up (HOST's briefing people list; #1509's title; HOST's 10-30 log, two entries; ROLE-PORTFOLIO-HOST line 48, a tester's first name, live (Docs 11-02); ROLE-PORTFOLIO-PA history at 6af12656e9 and earlier, three names, removed from the current file by PA's rewrite 11-02).

## Answered 11-02 12:0x (via Janus, decisions.log)
PDR-102 ratified; #1441 into PUB; five ops issues INFRA; #2253 step dropped; PPM may close the six (one time); CIO may edit check-branch.sh (one time); #1683 answered. All relayed 12:3x.

## Mine
- Relay xian's rulings at once; record them in decisions.log. Timestamps from `date` only.
- Briefing pointers: done 11-02 (11/13 full; gaps only ETA dormant and AGENT #2157 exempt). #1715 skills walk Tue 11-03. Ship-kickoff and map checks Fri 11-06.
- DAY-CLOSED in grep form `<!-- DAY-CLOSED: YYYY-MM-DD -->` as the log's last line.

## Owed rows (owed-scan)
- key: exec-launchagent-cutover2. Filed: 2026-10-31. CronDelete the session cron and flip registry row 179 on Pard's load notice.
- key: 1715-review. Filed: 2026-10-31. The #1715 skills walk with xian, due Tue 11-03.
