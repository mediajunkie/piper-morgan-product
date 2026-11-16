# Exec carry-forward

**Rewritten 2026-11-15 22:04 PST at STOP** (Fable 5.2 since 19:10 on 11-15; xian's bump for the seat-harness work). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/15/2026-11-15-0601-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Last check 22:01 Sun 11-15, 0 unacked. Ack only explicit IDs just read. Sends and acks can hit a fetch ref-lock race ("cannot lock ref"): re-run once.

## Rollup
v1002 (artifact version 1018), `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Edit with Python replace plus assert; update the "vNNN, rebuilt" stamp; no estimated minutes in card text (take them from the log). At START: header date to Monday, re-check the order against mail.

## The main thread: ADR-084 (xian's 19:11 ruling, 11-15)
- xian refused "you run it in Terminal" for #2364 and said, verbatim (ruling-relay 01M7H5DC…): "We need to solve that problem, not assign me manual tasks as a workaround for a poorly conceived solution." and "We keep changing how provider keys are used , how github is used, how piper morgan is used by our agents and it's become a tangled mess that keeps becoming my problem to manually navigate." He put Exec, Arch and CIO on Fable 5.2 for it and said "You all have my full confidence."
- My proposal: `docs/internal/operations/seat-test-harness-proposal-2026-11-15.md` (draft 2 `7c571b8fec`). Arch's **ADR-084, PROPOSED**, on main: `docs/internal/architecture/adrs/adr-084-seat-resources-are-separate-granted-once-and-bounded.md`. D1 the class (seat resources: separate, granted once through the harness, bounded where a seat can't pass, standing); D2 the seat key as an `env` entry in the seat's own `.claude/settings.local.json`, used through the binder's command-line source, budget rule, one cap enforcer (#2383); D3 a seat holds a session, never a password (`seat_session.py` under an exact allow; browser half proven on a dummy by CIO); D4 `ops_reader` count routes, counters not log reads; D5 a database per seat; D6 a ruling that puts a step on xian names the standing access that would remove it.
- **Every grant is xian's own paste** (auto mode refuses Pard and any seat editing another seat's settings). Guard installs stay his, batched by CIO. Don't present that row as solved.
- **Asked of xian, unanswered at STOP (rollup top card):** (1) yes or no to ADR-084, with the per-run figure a seat may spend without asking (proposed $10; the lead-scoring workspace's $150 monthly limit is the hard cap); (2) "Does anything you run still use the `lead-scoring-2026-10` key?" If no, he revokes it and tonight's key and workspace serve as is.
- On his yes: relay verbatim the same hour; decisions.log line; Arch flips the ADR to ACCEPTED; bring him the ten one-time rows from the steps file I asked CIO and Arch to pre-write (01M7HF64…, suggested `docs/internal/operations/adr-084-one-time-steps.md`), first three: seat key in Lead's settings, "Operations reader" tick, the helper's allow. Add the cleanup: remove the key stored 11-15 18:42 via `local_key_setup.py` and the lead folder's `.env` after the settings route serves one run.
- **Paid runs are stopped until his yes** (#2364's gate; arm B, bar set by Arch on issue 2301, priced batch 1 2,226 requests upper $6.75, batch 2 up to 480 upper $1.46, $8 stop in code; his "Yes" to arm B on the testing key stands, 18:43 in decisions.log).
- **Withdrawn from his list by his ruling:** running the gate or arm B by hand, CXO's on-screen checks as routine, the 1386 sign-in sitting, the provider count read, the log grep. Don't hand these back to him piecemeal.

## Where things stand (end of 11-15)
- **Main** 12/12 green at 22:01 (red 20:11 to about 20:55: CI's shallow checkout couldn't read a Tier 1 approval sha; Lead's `fetch-depth: 0` fix). **Beta** `460b837a47` (three promotions 11-15: 07:44 with `v2327floored` on xian's word; 09:08; 17:22 with #2374, #2376, #2375). **MCP** `dfebe7f0b7` (xian's deploy, carries #2374).
- **07:00 Mon promotion granted by Arch** (ten files, six conditions): #2382 (stateless MCP server), #2375's revisions (a card not a link, "Manage repositories", "Add another repository"), the Tier 1 checker change. #2382's served row then needs an MCP deploy (#2384, the deploy job, waits on ADR-084).
- **GitHub:** xian's reconnect works (re-saved callback row); App installed on `pipermorgan/piper-test`; #2342 rows 2 (card) and 3 PASS (CXO); connector reach PASS after the MCP deploy. His own `mediajunkie/piper-morgan-product` is not readable through the App until he installs it there (told him). #2380 one-trip connect filed (Arch's nonce condition). #2381 screen atlas (Web owns, CXO's state matrix).
- **Testing key:** `seat-screens-2026-11`, lead-scoring workspace, 90-day expiry, stored 18:42 in the lead folder's database store (a route seats can't use; to be replaced under ADR-084).
- **Blog:** "No New Skills This Time" published and distributed 11-15. "The Wall" Tue 11-17 drafted. Ship #069 Wed 11-18 (Comms owns; goal-3 close-outs unanswered).
- **Tier 1:** xian approved how-i-act, cant-read, stance and stand-ins in Docs' chat; practice.md final at `c531cae276`, put to him by Docs.
- **Open with xian, small:** did any hand-sent email link an `ALPHA_` doc page (HOST, before Docs removes the stubs)? "Operations reader" tick (now row 6 of ADR-084's list).

## Reminders owed to xian (Monday 11-16)
- flyctl upgrade. Docs' self-host guide run (fresh clone, own Postgres; stops before the key step unless he offers a key). CXO voice spec 12:00. Then: Ship #069 Wed 11-18; Thanksgiving week Mon 11-23; mail v3 fallback review 11-23; Vercel downgrade (#182).

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
