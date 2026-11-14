# Exec carry-forward

**Rewritten 2026-11-13 22:01 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/13/2026-11-13-0519-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Last check 22:01 Fri 11-13, 0 unacked. Ack only explicit IDs just read; never loop over a fresh `inbox --ids`. Acks can be slow under fetch contention; run long batches in the background.

## Rollup
v988 (artifact version 1003), `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Edit with Python replace plus assert; update the "vNNN, rebuilt" stamp. Content current as of 19:37 Fri 11-13; at START re-check the header order against mail.

## Where things stand (end of 11-13)
- **Main** 12/12 green at 22:01. Beta serves `81d149ac86` (promoted 16:34: #2366, #2367, #2368). MCP app on `4666e38493` (behind #2362); offer to let Lead deploy MCP under the standing grant is unanswered.
- **#2363** on main `7062d35d70`, Arch validated; row 3 closes on the next real promotion. **#2369** on main `70f926747b`, closes on Code Quality green.
- **#2364** (ethics substring fast path): xian approved spend and fix. Lead's step 1 held on `lead/2364-step1` `b16b83dcef`. Run needs the capped Anthropic key; OpenAI needs the Postgres provider count (and xian's known-limits yes) or a second capped key (Arch's 13:55 rule).
- **Lead's week of 11-16 order (PPM 01M7BVV9…, Lead accepted):** Path B (#2297, #2301); #2364 run the day the key exists; todo replies (#2328, #2219, #2295, #2294); named set; #2333.
- **Ship #069:** theme "Off-Limits by Default" (Comms cc Docs). Week review `7D6Yxe4rdXSpaPmd25CzQ1` v2: "2 met, 3 substantial progress". Goal-3 close-out items (six built ones to sprint 2) unanswered by xian. pubDate Wed 11-18.
- **Self-knowledge card ("Your word"), 13 texts** with commits listed on the rollup; recommended order: first seven now, six #2358 procedures (`ce46ba0542`) on a quieter day. I offered to take procedure approvals with CXO's pass as the bar; no answer. On his answer, quote it on #2354/#2355/#2358 with commits.

## Waiting on xian, in order (one at a time; he said "Let's continue through one thing at a time in order.")
1. **Reconnect:** GitHub said "redirect_uri is not associated". Callback list is correct (his screenshot). Asked: does the App's Client ID start `Iv23` and end `tj64` (what beta sent), and does the redirect_uri end `github%2Fcallback`? If IDs differ, beta's App client ID and secret get reset in Terminal (his job; I bring steps). Then #2282 step 5 (redirect_uri names beta on GitHub and Calendar Connect, and /setup calendar step; don't finish).
2. **Capped Anthropic testing key** via `scripts/local_key_setup.py`; tell me "done" plus the cap. Also: same key for rule-7 screens (Path B, #2186, #2184) and H4?
3. **1386 sign-in** once in Web's chrome-devtools page on beta /login; Web then runs #2364 rows, #2328 five, #2366/#2367 reads, PA's Q12 rows.
4. **Provider count** Postgres read, or a second capped OpenAI key; plus Arch's known-limits row if OpenAI is 0.
5. **Log read** for #2362/#2350 (grep on the rollup).
6. **Clock rule yes** (CIO/HOST): needs one hook line from xian or Pard.
Later: Arch's five-query staging read; `fly storage list`; #2335 Redis rotation; #2157 drill; self-hoster connectors; self-host invite second look; Console spend screenshots 11-06..11-12.

## Reminders owed to xian
- flyctl upgrade Mon 11-16. Docs' self-host guide run Mon 11-16 (needs a real provider key). CXO voice spec Mon 11-16 12:00. Ship #069 pubDate Wed 11-18. Thanksgiving week Mon 11-23. Vercel downgrade (#182).

## Mine
- Timestamps only from a `date` call; write the minute.
- Review slot every START. Calendar check every fire. `scripts/aging-standing-items.sh exec` at START.
- Relay xian's rulings the same hour, verbatim.
- Close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.
- Keychain off-limits without xian's permission. Secrets stay in his password manager. Client ID masked only.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
