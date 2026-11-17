# Exec carry-forward

**Rewritten 2026-11-16 22:02 PST at STOP** (Fable 5.2). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/16/2026-11-16-0421-exec-code-log.md` (closed). Start a new log on 11-17.

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Roles are space-separated on `send`. Ack only explicit IDs just read. Read a mail's body whole (`awk 'f>=2{print} /^---$/{f++}'`); don't grep out "- " lines.

## Rollup
v1022, `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Edit with Python replace plus assert; update the "vNNN, rebuilt" stamp from a `date` call; no estimated minutes. Top card: Steps A, C, D, F0, two answers. Then the keychain card, the writing card, the self-knowledge card.

## Waiting on xian (nothing answered or run since 06:51 on 11-16)
Steps file: `docs/internal/operations/adr-084-one-time-steps.md`. Copy lines from it by script; never retype.
- **Step A** (test key into Lead's settings), not started at 22:01 (no `~/.claude-pm/settings.json.before-fleet-deny`). Command: `cd ~/Development/piper-morgan-product && scripts/seat_settings_grant.py grant-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY`.
  - On `WAITING FOR READ TESTS on seat lead`: mail "go" to Lead, HOST, CIO. Lead Reads its own `.claude/settings.local.json`; HOST Reads Lead's same file by absolute path; CIO Reads its dummy `.env`. Each answers "refused" or "not refused". Give xian the three words. Anything but three "refused" stops before the key.
  - Then the hidden key prompt; he reports length and the 8-character fingerprint. Lead runs `scripts/seat_settings_grant.py check-env --name PIPER_SEAT_ANTHROPIC_KEY`. Tell CIO to remove the dummy. Undo: `mv ~/.claude-pm/settings.json.before-fleet-deny ~/.claude-pm/settings.json`.
  - After: arm B ($8 stop) and the 2364 gate (26 calls) may run; Step E (OpenAI key; no OpenAI price row, so capped OpenAI runs are refused); Step J cleanup.
- **Step C** (independent of A): three `add-allow --seat web` lines, for `seat_session.py --account web-seed-1386` and `seat_read.py --account web-seed-1386 --redirect-uri github` and `... calendar`. Lead needs none. Then Web runs the helper (0 of 1 real sign-ins).
- **Step D** (after C, same sitting): two lines that load `com.xian.seat-browser-web` and run `seat_browser.py --check web`; expect `port 9333`. His paste is the first real run (auto mode refused Pard's hand test). If it prints `refused:`, get the reason to CIO and Pard. After it passes: CIO switches `.mcp.json` to the launcher, then Web's checks (signed-in name, second Read-deny measurement), then the served rows of 2379 and Arch's one chat turn for 2383.
- **Step F0:** he mints one invite, runs `scripts/seat_account_create.py --account seat-github-1 --write-invite`, then the add-allow for Lead. Lead creates the account (0 of 1 real creations).
- **Keychain yes or no:** CIO started Chrome for Testing by hand on 11-15 without `--use-mock-keychain`; it may have made or read "Chromium Safe Storage". Unverified; no seat looks. His answer is "leave it" (my recommendation) or "I'll look".
- **Two answers:** (1) does anything he runs himself use the `piper-morgan-test` workspace; (2) yes or no that its key on `web-seed-1386` counts as a seat key up to $40. Relay verbatim the same hour, with a decisions.log line.
- **Writing:** "The Wall" is on the calendar for Tue 11-17 and was still Comms' scaffold at last read (his prose or a new day; check with Comms at START). Ship 069 (Wed 11-18): five draft goals need his yes or edit; Comms' fallback is mail 01M7K6JQ. Console Usage and Cost screenshots for 11-06 to 11-12.
- **Self-knowledge, three texts awaiting his yes:** nine rules (2354, `47a65eed5f`), 13 practice rows (2355, `c531cae276`), seven procedures (2358).
- Small: flyctl upgrade. Still his hand with a D6 line: 2087, the Buttondown text, 2344. HOST's read-only Buttondown grant goes to him only after Steps A, C, F0.
- **For him to overrule:** on issue 2264 his 11-03 word was "yes ask"; I let HOST read the two stakeholder rows ("test data"); nothing quoted. The history decision on 2264 is his. The issue was still open at 22:01; the closing comment is Arch's or Lead's.

## In motion
- **Beta** `4e2797bce2` since 08:07 on 11-17 (2401, 2397). Issue 2402's fix on main `456dad90a7`, not served; Lead asks Arch for a grant when CI is green. Not checked signed in; that waits on Steps C, D, F0.
- Main 12 of 12 green at 22:01, including Tests on a commit after CIO's fix. `whats-armed` 31 armed, 0 not armed, 1 unmeasured.
- Lead's unbuilt items: the 2157 drill script, 2390, 2391, 2384, 2393, 2399. Hook blocking decision needs a week of counts (about 11-23).
- Logs without a DAY-CLOSED marker at 22:03 on 11-16: Docs (last entry 19:17), CIO (20:02), Arch (STOP entry at 21:28, marker missing). Docs nudges at its START; check they closed.

## Rules I keep
- Timestamps only from a `date` call; no "HH:Mx". No clock time in a card that I didn't read.
- Every grant is xian's own edit. No seat runs `fly`. A relayed grant doesn't lift a classifier refusal. Keychain off-limits without his permission. Secrets stay in his password manager.
- Check each ruling that puts a step on xian for the "standing access that would remove this" line (ADR-084 D6). Before recommending he do something by hand, ask why a seat can't. No manual workarounds handed to him.
- Check the owner's log before telling xian something hasn't arrived.
- Don't defer cleanup to STOP without a blocker.
- At STOP: rewrite this file, list every other seat's close from their logs, close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
