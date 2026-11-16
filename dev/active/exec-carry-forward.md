# Exec carry-forward

**Rewritten 2026-11-16 10:06 PST at WATCH** (Fable 5.2 since 19:10 on 11-15). History: `git log -p -- dev/active/exec-carry-forward.md`. Session log: `dev/2026/11/16/2026-11-16-0421-exec-code-log.md` (open).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Last check 10:06 Mon 11-16, 0 unacked. Ack only explicit IDs just read. Sends and acks can hit a ref-lock race: re-run once.

## Rollup
v1004 (artifact version 1020), `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Edit with Python replace plus assert; update the "vNNN, rebuilt" stamp; no estimated minutes. Top card is Step A.

## The main thread: ADR-084, ACCEPTED 11-16
- xian 11-16: "1. Yes to ADR-084 and budget 2. Nothing I run personally uses that key, no". Relayed (01M7JBP5…), decisions.log line, Arch marked the ADR accepted. $10 a run without asking; the lead-scoring workspace's $150 monthly limit is the hard bound.
- Files: the ADR `docs/internal/architecture/adrs/adr-084-seat-resources-are-separate-granted-once-and-bounded.md`; steps `docs/internal/operations/adr-084-one-time-steps.md`.
- **Step B done** ("Operations reader" on web-seed-1386, HOST recorded). Older key `lead-scoring-2026-10` disabled by xian (enough, per Arch and HOST).
- **Step A: go given 06:51, NOT STARTED at this rewrite** (no `~/.claude-pm/settings.json.before-fleet-deny`). His command: `cd ~/Development/piper-morgan-product && scripts/seat_settings_grant.py grant-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY`.
  - When he reports `WAITING FOR READ TESTS on seat lead`: mail "go" to Lead, HOST, CIO. Lead Reads its own `.claude/settings.local.json`; HOST Reads Lead's same file by absolute path; CIO Reads its dummy `.env` (top of the CIO worktree, placed 06:30). Each answers "refused" or "not refused".
  - Give xian the three words to type. Anything but three "refused" stops before the key. Then the hidden key prompt; he reports length and the 8-character fingerprint.
  - Lead runs `scripts/seat_settings_grant.py check-env --name PIPER_SEAT_ANTHROPIC_KEY` (restart Lead's session if UNSET). Tell CIO to remove the dummy. Undo if sessions misbehave: `mv ~/.claude-pm/settings.json.before-fleet-deny ~/.claude-pm/settings.json`.
- **After Step A:** arm B may run (his "Yes" of 11-15 18:43; $8 stop in code); #2364's gate sends me its planned-calls line first until #2383 lands; Step E (capped OpenAI key; he confirms the hard-limit switch); Step J cleanup (`local_key_setup.py --remove anthropic`, the lead folder's `.env`), then Lead re-runs the whole tree.
- **Not ready (builds):** C #2388 `seat_session.py` (CIO builds), D, F0, F, G, H (#2384). I recurs (CIO's batched guard patches).
- **Paid runs stay stopped until Step A is done and Lead's check passes.**
- Every grant is xian's own edit. Don't hand withdrawn manual tasks back to him.

## Where things stand (11-16 WATCH)
- **Beta `fd6ef1c669` since 09:39** (Lead's run 43920316218; Arch: conforms, 6 of 6): #2375 card fix and CXO's words, #2382 code in the main image, no migration. I had Lead holding this behind Step A since 07:00; released 09:32 on Arch's point that the two are independent (my sequencing miss). No seat has seen the card signed in; 2374, 2375, 2376 stay open. #2382's served row waits on an MCP deploy (#2384).
- **Main** 12 of 12 green at 10:01.
- **Shared-stack rule is now one script:** no seat runs `scripts/alpha-setup.sh` on Amber, nor `docker compose up`/`down`. Lead deleted `stop.sh`, `start.sh`, `db_migrate_to_volume.sh`; `run_tests.sh` no longer starts services (#2386).
- **GitHub:** App on org `pipermorgan`, installed on `pipermorgan/piper-test`. His own repo isn't readable through the App until he installs it there. #2380 one-trip connect, #2381 screen atlas, #2377 settings layout filed.
- **Blog:** "The Wall" Tue 11-17 drafted. Ship #069 Wed 11-18 (Comms; goal-3 close-outs unanswered).
- **Tier 1:** practice.md final `c531cae276` put to xian by Docs; the other four approved.
- **Open with xian, small:** did any hand-sent email link an `ALPHA_` doc page (before Docs removes the stubs)?

## Reminders owed to xian (Monday 11-16)
- flyctl upgrade. CXO voice spec 12:00. Docs' guide run: steps 1 to 4 and 8 pass; 5 to 7 and 9 need a provider key (the seat key could serve). Then: Ship #069 Wed 11-18; Thanksgiving week Mon 11-23; mail v3 fallback review 11-23; Vercel downgrade (#182).

## Mine
- Timestamps only from a `date` call; write the minute; no "HH:Mx" in logs, cards or mail.
- Every START: review slot (Docs' omnibus for the day before), `scripts/aging-standing-items.sh exec`, **`scripts/whats-armed.sh`** (skipped 11-15; it had flagged the stale pytest env all day), calendar check.
- Relay xian's rulings the same hour, verbatim. Check each ruling-relay that puts a step on xian for the "standing access that would remove this" line (ADR-084 D6).
- Before recommending xian do something by hand, ask why a seat can't, and say what standing access would end it.
- Re-read source before asserting a UI or settings fact (11-15 misses: the App's owner page, the "autofill" that was a placeholder, "Only on this account").
- Close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line; list every other seat's close from their logs, not from memory.
- Keychain off-limits without xian's permission. Secrets stay in his password manager. Client ID masked only. No seat runs `fly`.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
