# Exec carry-forward

**Rewritten 2026-11-14 22:03 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/14/2026-11-14-0601-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Last check 22:01 Sat 11-14, 0 unacked. Ack only explicit IDs just read; never loop over a fresh `inbox --ids`.

## Rollup
v994 (artifact version 1009), `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Edit with Python replace plus assert; update the "vNNN, rebuilt" stamp. At START re-check the header order against mail; "Saturday's fixes" wording on the top card is now day-relative-safe.

## Where things stand (end of 11-14)
- **Main** 12/12 green at 22:01. Beta serves `81d149ac86` (unchanged since 11-13 16:34). Every other seat closed its day.
- **Top card: promotion with migration `v2327floored`** (Lead's ask 01M7DX6A…, Arch's grant 01M7DXEN…, contingent on xian's yes). Grant covers staging at dispatch if `79f35f1089` is an ancestor and the diff above it is only dev/, docs/, mailboxes/ with no alembic/ change (Arch 01M7DYNJ…). #2363 row 3 needs a merge-commit head. No yes on 11-14; window 07:00–21:00 PT. After the serve: xian ticks "Operations reader" on the test account (Settings → Account flags); Arch wants the beta /health sha, the promote run's "Tests concluded success on <anc>" line, and that the migration ran, quoted.
- **Held until after the promotion:** #2372 (Arch validated `5a0f87c7d5`), #2373 (counter write timeout, PPM section Q, not blocking). Then #2370 (redis-py upgrade after CIO's read), #2345 (held until #2342 rows 2–3 are read). #2335 rotation after #2342.
- **Path B (#2297/#2301)** held on `lead/2301-project-read` `7dfab574a4` for the arm B router screen (~1,700 calls, est. $2–5, hard stop $8); needs the capped Anthropic key.
- **#2364** (ethics substring fast path): spend approved; needs the capped Anthropic key, and for OpenAI the Postgres provider count or a second capped key.
- **Blog:** "Which Agent Did It?" published; Medium + LinkedIn owed by xian's hand (on rollup). Narrative trial adopted (arcs about taking the product into beta; "The Wall" Tue 11-17 as bridge; cadence and weekdays still a leaning). Sun 11-15 "No New Skills This Time" drafted. Comms owns Ship #069 (pubDate Wed 11-18); goal-3 close-outs unanswered.
- **Self-knowledge card, 13 texts:** first seven now, six #2358 procedures (`ce46ba0542`) later; my offer to take procedure approvals with CXO's pass as the bar is unanswered.

## Waiting on xian, in order (one at a time)
0. Promotion yes/no, then the flag tick.
1. Reconnect: does the App's Client ID start `Iv23` and end `tj64`? Then #2282 step 5.
2. Capped Anthropic testing key via `scripts/local_key_setup.py`; "done" plus the cap; may it serve rule-7 screens (arm B, $8 cap) and H4?
3. Sign in once as web-seed-1386 in Web's open beta /login page (also the first counter read).
4. #2364 provider count or a second capped OpenAI key, plus Arch's known-limits row if OpenAI is 0.
5. Log read for #2362/#2350 (grep on the rollup).
6. Clock rule yes; needs one hook line from xian or Pard.
Later: Arch's five-query staging read; `fly storage list`; #2335 rotation; #2157 drill; self-hoster connectors; self-host invite second look; Console spend screenshots 11-06..11-12; Ship #069 goal-3 close-outs.

## Reminders owed to xian
- flyctl upgrade Mon 11-16. Docs' self-host guide run Mon 11-16. CXO voice spec Mon 11-16 12:00. Ship #069 pubDate Wed 11-18. Thanksgiving week Mon 11-23. Vercel downgrade (#182).

## Mine
- Timestamps only from a `date` call; write the minute.
- Review slot every START (Docs' 11-14 omnibus is due). Calendar check every fire. `scripts/aging-standing-items.sh exec` at START.
- Relay xian's rulings the same hour, verbatim.
- Close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.
- Keychain off-limits without xian's permission. Secrets stay in his password manager. Client ID masked only. No seat runs `fly`.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
