# Exec carry-forward

**Rewritten 2026-11-12 22:03 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/12/2026-11-12-0423-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Last check 22:01 Thu 11-12, 0 unacked. Ack only the explicit IDs just read; never loop over a fresh `inbox --ids`. A mail4 "NOT MEASURED" on a fetch-lock race goes away on a retry. My own `grep -v "^- "` filter drops a memo's bullet lines, so read memos unfiltered when the bullets matter.

## Rollup
v966 (artifact version 981 after the timestamp fix), `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with Python replace plus assert. Current at 22:02 Thu 11-12, top card only. The "Your word" items are as of 18:04 and still valid.

## Where things stand (end of 11-12)
- **Main** 12/12 green at 22:01. Beta serves `d4fd55e6c5`, MCP `4666e38493`.
- **#2342 switchover DONE** at 19:06 PT: 10 of 10 classic tokens revoked at GitHub, 0 left. The half-state window ran 17:26–19:06 (HOST recorded it as 100 min late). Row 1 (connector cutover line) PASS (PA read, CXO ruled). **Next: xian reconnects GitHub, sign-in only, no install.** Exec tells PA, PA reads row 2, then xian installs on his own account, then row 3. Row 4 is marked not served. HOST still needs the secret's creation date and the masked client ID (xian, from the App page). The optional `fly secrets list` names-and-dates read was offered.
- **Promotion** refused at 20:36 by the promote gate's first-parent walk (#2363). It goes Fri after 07:00, carrying #2350, #2362, #2333, #2348, #2351 words, #2353 and #2347. **#2363 yes/no** for xian (`^@`, Arch and CIO agree). Lead's workaround: push last before dispatch.
- **PDR-009 public-beta gate: xian yes.** PUB cleared by PPM per item. #1612 is off the gate. Estimate: likeliest sprint 6–7 (01-08 to 02-04), earliest sprint 5. Map: `docs/internal/planning/public-beta-gate-map-2026-11-12.md`. Legal review #2063 is xian's to start.
- **Local running (#2351):** helper `scripts/local_key_setup.py` is on main. Docs' guide `docs/installation/self-host-guide.md` gets its run-check Mon 11-16. Invite code stays (xian). A self-hoster mints their own code. Keychain opt-in only (#2353 validated). Key-in-docs lint is wired.
- **Self-knowledge #2349:** xian said Tier 1 first, leans 1+2+4, Q1 yes (humanized), Q2 self-hosters, Q3 research. Arch's revised boundary (Tier 2 dissolves) awaits xian's yes; #2358/#2359 wait on it. #2354–#2357 are filed. CXO voice spec Mon 11-16 12:00. CIO's conduct draft is on main.
- **Arch rulings:** #2158 deletion record in a write-only bucket (needs Fly object storage; xian checks with `fly storage list`). #2361 pause switch goes in sprint 6. xian said yes to a pause-only HOST account as permission only; none gets made now, and HOST's and Arch's custody conditions apply. xian believes he is the only admin.
- **Thu post "The Server Has No Key"** is still `planned`; xian "will try". It rolls to Fri if unwritten. Don't nudge.

## Waiting on xian (he said these need context or discussion; walk one at a time, the key first)
1. Test-key question (#2340 / Q3 #2357): (a) dedicated capped Anthropic key via local_key_setup.py (recommended), (b) per run, (c) keychain per run.
2. Arch's revised self-knowledge boundary: yes/no.
3. Self-hoster connectors (PPM: same as beta; xian might contradict).
4. Self-host invite second look (owner-first, optional).
5. #2363 yes/no. #2328 key=value copy or read permission (PA reminder 21:49). Fly object storage check. Secret creation date and masked ID.
6. Older: #2335 Redis rotation (Terminal, after #2342 rows), #2157 drill hour, #2282 step 5 (now after the switchover; check `redirect_uri` names beta), #2264 read.

## Reminders owed to xian
- flyctl upgrade 11-16. Thanksgiving week Mon 11-23 (PPM closing review; v4 review). Vercel downgrade (#182).

## Mine
- Timestamps only from a `date` call. "HH:Mx" trips stamp-check; write the minute.
- Review slot every START. Calendar check every fire. `scripts/aging-standing-items.sh exec` at START.
- Relay xian's rulings the same hour, with verbatim quotes.
- Close the log with the exact line `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line (Docs greps that form; the plain form missed on 11-12).
- Keychain off-limits without xian's permission. Secrets stay in his password manager.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
