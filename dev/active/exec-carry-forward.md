# Exec carry-forward

**Rewritten 2026-11-21 22:03 PST at STOP.** Model: Opus 5.5. History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/21/2026-11-21-0601-exec-code-log.md` (closed). Start a new log on 11-22.

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. `--to`/`--cc` take space-separated roles, not commas. Ack one at a time, never in parallel (parallel acks race on the ref). Janus's words arrive as `mailboxes/exec/inbox/memo-janus-to-exec-*`; reply with `scripts/mail-send-external.sh ~/Development/designinproduct docs/mail <memo>`, mirror with `scripts/mail-send.sh`.

**Clock rule live:** no estimated minutes (`HH:Mx`) in commits or mail; quote others' in backticks. Headings with `scripts/log-entry.sh "title"`. zsh: never `echo =====` (`=cmd` expansion).

## Rollup
v1095, `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Python replace plus assert; bump the stamp from a `date` call. Top card rewritten Sat 11-21 06:03 (F.2 next). At START 11-22: retitle the h1 to Sunday and change "Today's insight" (Sat 11-21) to say it missed its slot unless his prose arrived.

## ADR-084 sitting (steps file `docs/internal/operations/adr-084-one-time-steps.md`)
- **Done 11-20:** A (key 106 chars, sha256 b5d48364), C (Web's allows), D (seat browser :9333), **F0** (invite file by xian; Lead's allow at 27; `seat-github-1 created` 18:36; the script's missing +x fixed by Lead, CIO added a test), **F.1** (machine account `atswimtwobirds`, public by design).
- **Next for xian: F.2** (org Base permissions No permission; invite the account as Member; team `seat-test` with the test repos only; report the billing seat-count line). Then F.3 (no App install), **F.4 connect** as seat-github-1 (first sign-in to that account) → **G parts 1 and 2** → PA's zero-install read → **F.5 install** (PA's order, 01M7Y03RJG). If G is awkward, F whole first.
- **Step E (OpenAI key):** open, independent. The one thing between #2364 (PASS on rerun) and merge.
- Guide him one step at a time (his ask 11-20).

## Waiting on xian, other
- **Ship #070 "No Workarounds"** (his 18:12 rulings, relayed 01M7XY16WB, three decisions.log lines). An outline scaffold by Exec, bare facts under each heading, err on including. **Discussed marker held until he says he's read the review** (https://claude.ai/artifact/4Pgs8DrAXpyB2P9o6BvRRn) and ratifies or edits next week's goals. Then add `<!-- discussed: DATE -->`, run the draft-weekly-ship skill, scaffold, Comms fact-check. Publish Tue 11-24.
- **Sprints don't stretch** (his ruling): sprint 2 closes 11-26; #071 reports the score as it stands. My forecast to him: seats and self-host goals on track, GitHub move at risk, named items partial. PPM: 2301's read half misses 11-26.
- **Sat 11-28 title:** his to replace ("Test the Page You Draw" is out). Comms holds it open.
- **Sat 11-21 insight** "A Blocker Framed as Yes or No": still `drafted` at 22:01 Sat, no prose from xian; the slot passed. Ask Comms at START 11-22 whether it rides Sunday or moves; ask xian only if Comms can't place it.
- **Restore drill 2157:** his choice of day (rollup card).

## In motion
- **Beta `d66f15c538`** since 20:25 (2297 attach). **2301 handler-only on main `74522e25ec`**, CI green, not promoted. It isn't promoted on its own before Web's sitting; it may go with other work (CXO 20:51). Nobody reads the block as ruled until CXO rules on Web's quotes.
- **Web:** session restart pending (CIO's launcher). Then CXO's 2406 row on the empty account, then Lead's 15-line 2297/2301 pass. Planned spend against about $23.81 of headroom on the test workspace. Also Web's Step D item 4.
- **Promote hold:** `ops/promote-hold.md` exists as a mechanism (CIO 0bfeebc8de, Arch-approved stricter-only, xian told 21:26). Not in use.
- **Staging D6:** HOST's read-only staging Machines token idea is at 2 of 3 repeats; propose it on the third.
- **Seat spend 11-20:** Lead's paid today $14.19 (no run over $10). Arch's 2364 arms plus Lead's screens all under xian's 11-13 yes.
- Main 12 of 12 green at 22:01.

## Closes at 22:01 on 11-21
Closed: Web, Comms, HOST, Arch, CXO, PPM, Lead, PA. Open: Docs, CIO (their STOPs may still run). Check at START; Docs's Step 1d nudges.

## Standing word
Promote gate: "Yes, changes that only make the check stricter can go ahead with Arch's approval, although I should still be informed." I tell him the same hour.

## Rules I keep
- Timestamps only from `date`. Every grant is xian's own edit. No seat runs `fly`. A refusal is final and not reworded. Keychain off-limits without his permission. Never direct a seat to read its `.env` or settings file.
- D6-check every step on him. Don't ask him what the team can answer. Don't put account emails or secrets anywhere in this repo.
- At STOP: rewrite this file, list other seats' closes, close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
