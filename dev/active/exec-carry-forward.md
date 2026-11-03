# Exec carry-forward

**Rewritten 2026-11-02 22:0x PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/02/2026-11-02-0423-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle` (fires :01 at 6,10,14,18,22). An empty CronList is normal and there's no STOP re-arm. Agent liveness is Pard's.

**Cron gate:** the duty-cycle-tick cron-management steps (CronList self-heal, STOP re-arm) don't apply on a LaunchAgent.

## Rollup
v764, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with Python replace plus an assert, never sed. Re-check every xian-gated item live on each fire.

## Where things stand (end of 11-02)
- **Served:** alpha and beta are on `3297ea797b`, promoted 18:14 by run 41564549158. It contains the #1680 landings and `scripts/mcp_allow.py`. Fly-deploy runs since then were push (staging) runs, not promotions. CI was 12/12 green at 22:01.
- **#2242:** xian is on the allowlist by user ID (18:3x). Next: xian reconnects the Piper connector once, then PA deploys the MCP side and its first check confirms the list. Relay the reconnect to PA, Lead, Arch and PPM.
- **#1680 row half:** route 1. xian opens `/api/v1/admin/consequential-actions?days=1` while signed in and pastes the JSON (Lead and Arch: counts only). Relay to Lead, PA and PPM.
- **Waiting list:** xian's model and pace stance ("not racing anyone or anything") are in decisions.log. Open on the rollup: keep Buttondown as a second newsletter (rec yes; (b) is the fallback, (c) is out), then the nothing-else question (rec no), then the newsletter step. Relay to HOST, CXO, Comms, Web and PPM. #2229 closed by xian. /try/ cleanup live (#2256).
- **GitHub connect scope** is `repo`, tracked as #2261 (blocked by #2174). The throwaway-login rule holds for the #2235 OAuth-only account. Closed loop.
- **#2098 reopened** by CXO (pending-draft retitle regression). That's Lead's or Arch's; nothing for xian.
- **Test gate:** Lead and CIO keep the lock; CIO counts on 11-09.
- **Lesson 11-02:** I cited `output: 'export'` without its `STATIC_EXPORT` condition, then corrected it. Read the condition around a config line before citing it.

## Waiting on xian (rollup "Your word" / "Your hand")
- Buttondown keep, the nothing-else question, and the newsletter step (above).
- Fresh test accounts (HOST, PA, Web): the 10-29 pattern; Web's account must be a throwaway GitHub login with one repository. Relay to HOST, PA, Web and PPM.
- CIO's promotion grant (rec yes); Lead's promotion allow (9a, v4 `01M69F0FT2HW9Z00BZP5MXB11P` left unacked on purpose). Relay to CIO and Lead.
- #327 close as not planned (rec yes). Relay to PPM.
- contribute@ and privacy@ routing.
- Hand: #2251 CIO paste; #2254 dev DB paste (tell Lead and CIO); Fly reads #2244 and #2226; Notion key on staging (#2238); #1514.
- Ship #067 week review (artifact `4Le3ZyacNXUqo19SQh5GpT`); the draft waits on it.
- Rule-8 history decision whenever he takes it up (HOST's briefing people list; #1509's title; HOST's 10-30 log, two entries; ROLE-PORTFOLIO-HOST line 48; ROLE-PORTFOLIO-PA history at 6af12656e9 and earlier).

## Mine
- Relay xian's rulings at once and record them in decisions.log. Timestamps from `date` only.
- #1715 skills walk Tue 11-03. Ship-kickoff and map checks Fri 11-06.
- DAY-CLOSED in grep form `<!-- DAY-CLOSED: YYYY-MM-DD -->` as the log's last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. The #1715 skills walk with xian, due Tue 11-03.
