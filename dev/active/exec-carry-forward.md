# Exec carry-forward

**Rewritten 2026-11-01 23:1x PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/01/2026-11-01-0429-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle` (fires :01 at 6,10,14,18,22), loaded by xian 11-02 ~13:50; first fire 14:01 landed work. Session cron ed995092 deleted 14:2x; CronList empty is the normal state now. No STOP re-arm. Agent liveness is Pard's.

**Cron gate:** the duty-cycle-tick cron-management steps (CronList self-heal, STOP re-arm) don't apply on a LaunchAgent.

## Rollup
v758, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with Python replace plus an assert, never sed. Re-check every xian-gated item live on each fire (I missed his 11:10 release page until Janus said so).

## Where things stand (end of 11-01)
- **v0.9.0.0 complete.** xian published the release page at 11:10 PST; Lead confirmed at 20:15 that the tag is the served sha and the post-release audit is clean. Docs adds the URL to the briefing Version line (told at 20:2x).
- **Served (23:08 read):** alpha and beta 0.9.0.0 `c44dd081cb`. Last promotion dispatch 04:21Z 11-01. CI 12/12 green.
- **#2242 order is final** (PPM withdrew add-first 07:50; Arch 07:45): promote, then `mcp_allow.py add`/`--apply`/`list` in the container, reconnect the Piper connector in Claude once if disconnected, then PA's MCP deploy and checks. The script isn't in `c44dd081cb`, so add-first can't run.
- **#2149:** two-stage routing rejected ($5.67, parity failed twice); #2197/#2184 by op-local resolution; #2250 on main.

## xian's hand, in order (rollup hot card)
1. ghmint fix: INSTALLED 11-02 ~13:16 (Janus). CIO closes 9d after two mints 15 min apart; Pard told.
2. `set_default_repo`: printenv, then `fly secrets set` with the value appended. Relay both outputs to CIO.
3. Promote (dispatch line), then the #2242 allowlist add (three lines with his email), reconnect if needed. Relay `list` to PA, Lead, Arch, PPM.
4. Buttondown: DONE 16:58 (xian's sign-up, Janus 17:04). Five pieces of feedback routed 17:07 (Comms, CXO, Web, HOST; gate idea to Lead+CIO, joint answer owed to Exec). 17:2x xian gave the waiting-list model and the pace stance, both relayed and in decisions.log. #2229 closed by him. Open on the rollup: keep Buttondown? (rec yes; (c) out per Arch 17:34), then the nothing-else question (rec no), then the newsletter step. Relay his answers to HOST, CXO, Comms, Web, PPM. Test gate: Lead+CIO keep the lock; 11-09 count (CIO 9i).
- Promote: green at 17:25 (dfa3363d5b); rollup says re-run. CXO OKs Comms' v2. #2256 is the page cleanup.
- Promote: 16:50 dispatch failed at SHRINK-LOCK; Lead retagged flaky on dfa3363d5b; re-run on Lead's green (Tests 41556514327).
- Also his hand: web-pat-test sign-in, Notion key on staging for #2238, Fly reads #2244 and #2226, #1514.

## Waiting on xian (his word)
- #2251: classifier refused CIO even with the grant; xian's terminal paste (rollup Your hand). Relay both result lines to CIO.
- Six closes: refused twice as a batch. Rec: 'PPM may try the six one at a time' (PPM 13:0x guess, unverified); then the rule, or xian closes them. Relay to PPM and Arch.
- #2254 dev DB residue: Lead's paste is on the issue (12:4x); on rollup Your hand. Result lines go back on #2254; tell Lead and CIO.
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
- key: 1715-review. Filed: 2026-10-31. The #1715 skills walk with xian, due Tue 11-03.
