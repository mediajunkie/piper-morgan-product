# Exec carry-forward

**Rewritten 2026-11-22 22:02 PST at STOP.** Model: Opus 5.5. History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/22/2026-11-22-0601-exec-code-log.md` (closed). Start a new log on 11-23.

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. `--to`/`--cc` take space-separated roles, not commas. Ack one at a time, never in parallel (parallel acks race on the ref). v3 fallback ends 11-23. Janus's words arrive as `mailboxes/exec/inbox/memo-janus-to-exec-*`; reply with `scripts/mail-send-external.sh ~/Development/designinproduct docs/mail <memo>`.

**Clock rule live:** no estimated minutes (`HH:Mx`) in commits or mail. Headings: `scripts/log-entry.sh "title" >/dev/null` (it appends the heading itself; don't also printf it). zsh: never `echo =====`.

## Rollup
v1119, `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Python replace plus assert; bump the stamp from a `date` call. At START 11-23: retitle the h1 to Monday; the Ship #070 Tuesday risk line moves up (publish Tue 11-24, no discussed marker yet).

## ADR-084 sitting (steps file `docs/internal/operations/adr-084-one-time-steps.md`)
- **Done:** A, C, D, F0, F.1 (11-20).
- **Next for xian: F.2** (org Base permissions No permission; invite `atswimtwobirds` as Member; team `seat-test` with the test repos only; billing seat-count line). Then F.3, F.4 connect as seat-github-1, G parts 1 and 2, PA's zero-install read, F.5 install (PA's order, 01M7Y03RJG).
- **Step E (OpenAI key):** open; the one thing between #2364 and merge.
- Guide him one step at a time (his ask 11-20).

## On xian's card (rollup v1119), in order
1. **Fleet deny** (on main 733636419f + ed85825f3c): `cd ~/Development/piper-morgan-worktrees/cio && python3 scripts/seat_settings_grant.py fleet-deny`, expect `added 6 deny rule(s); 2 were already there...`. Relay his line to CIO; Pard restarts Web; Web's Read must be refused. D6: auto mode refuses Pard a shared-settings edit.
2. **seat-tester-1 sitting (#2406, and #2417's last row):** mint; `seat_account_create.py --account seat-tester-1 --write-invite` (product checkout); Lead's create allow; console check (key in piper-morgan-test; stop if not); save-key allow. Optional CIO allow for seat-github-1. After: Lead creates and saves the key, output to HOST; Web runs CXO's six turns and #2417's `update_issue` never-connected line. If `validated: no`, Lead's remove mode (diff to HOST).
3. **"Do I Have To?" crosspost** (live 11-22): LinkedIn and Medium, URLs to Docs; Medium "Inviting Company In" footer swap.
4. **F.2, E** (above).
5. **Ship #070 "No Workarounds":** his read of https://claude.ai/artifact/4Pgs8DrAXpyB2P9o6BvRRn, ratify or edit next week's goals. Then add `<!-- discussed: DATE -->`, run draft-weekly-ship, outline scaffold (bare facts under each heading), Comms fact-check. Publish Tue 11-24; at risk.
- Titles: Sat 11-28 is "Mark One Eyeball" (locked). Restore drill 2157: his choice of day. Later: #2387.

## In motion
- **Beta `079e6aaf78`** since 11-22 19:54 (Lead 01M83922SA). Day's builds: `a805384f7e` (2301 part 1, 2413, 2414, 2411), `948af3a198` 17:08 (#2417 one cause), `f2213c7a85` 19:08 (#2418, #2419, both closed served by PPM 19:37), `079e6aaf78` (#2419 follow-up). #2420 guard on main `25048aedde`; PPM to close.
- **Open nearby:** #2417 (update_issue row, fresh account), #2416 (offers, parked), #2245 served read, 2301 part 2.
- **Web:** signed in as web-seed-1386 (session expires 11-23 15:06 UTC).
- **Seat spend 11-22:** Lead paid about $1.30; no run over $1. All under xian's 11-13 yes.
- **Read-outside-dir prompt** held CXO 12:31 and Web 18:18 fires (CIO 01M836RA3G); gotchas updated; a scoped allow comes to me for xian only if a task-output stop recurs.
- **Promote hold:** `ops/promote-hold.md` mechanism exists, not in use.
- **Staging D6:** HOST's read-only staging Machines token idea at 2 of 3 repeats.
- Main 12 of 12 green at 22:01.

## Closes at 22:01 on 11-22
Closed: Comms, Web, HOST, Arch, CXO, PPM, Lead, PA. Open: Docs, CIO, prog (their STOPs may still run). Check at START.

## Standing word
Promote gate: "Yes, changes that only make the check stricter can go ahead with Arch's approval, although I should still be informed." I tell him the same hour.

## Rules I keep
- Timestamps only from `date`. Every grant is xian's own edit. No seat runs `fly`. A refusal is final and not reworded. Keychain off-limits without his permission. Never direct a seat to read its `.env` or settings file.
- D6-check every step on him: who would actually do it, checked (tmux ls whole, not `head`). Don't ask him what the team can answer. No account emails or secrets in this repo.
- At STOP: rewrite this file, list other seats' closes, close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
