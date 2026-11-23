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
- **Titles:** Sat 11-28 is "Mark One Eyeball" (locked by xian, 11-22).
- **"Do I Have To?"** live 11-22 (pipermorgan.ai/blog/do-i-have-to, Docs 01M822N36A). Owed by xian: LinkedIn and Medium crosspost (URLs to Docs), and the Medium "Inviting Company In" footer swap. On rollup v1103.
- **Restore drill 2157:** his choice of day (rollup card).

## In motion
- **Beta `f2213c7a85`** since 11-22 19:08 (Lead 01M8362948; #2418 and #2419; Web read both right 01M836KG86). Before that `948af3a198` since 17:08 (Lead 01M82Z5WGE; #2417 plus follow-up plus update_issue never-connected reply; Web read 2417 line right 01M82ZB9NE). Before that `a805384f7e` since 11-22 afternoon (Lead 01M82PH9N4; Arch conforms 01M82PP3XE): 2301 part 1, 2413, 2414, 2411 replies. Web runs 13 served lines. 2301 part 2 stopped (#2416); update_issue reply lands next.
- **Web:** restarted by Pard; signed in as web-seed-1386 at 07:06 11-22 (01M81WPN51, session expires 11-23 15:06 UTC). Running: step 4, CXO's 2406 row, Lead's 15-line 2297/2301 pass. Then CXO rules on the 2301 words, then 2301 promotion.
- Planned spend against about $23.81 of headroom on the test workspace. Also Web's Step D item 4.
- **Fleet `~/.piper-shared` denies (CIO 01M824X130, 11-22 09:29):** Web's seat read a file in its own seat-browser profile folder, so the deny was missing in that seat. Fix is on branch `claude/cio-fleet-deny-piper-shared` `733636419f`, stricter only, and waits on Arch's yes (HOST is asked whether it needs a read, and whether Web keeps the seat browser meanwhile). When it lands, tell xian the same hour, and put the batch (`dev/active/cio-install-batch-2026-11-22.md`: one command, then Pard restarts Web) on his card. D6: auto mode refuses Pard a shared-settings edit, so the step stays his.
- **2406 seat-tester-1 sitting:** ON xian's card (rollup v1114) since 11-22 12:34, in HOST's order: mint, `seat_account_create.py --account seat-tester-1 --write-invite` (product checkout, synced to include ca594c14d9), Lead's create allow, console check (key in piper-morgan-test; stop if not), save-key allow. Optional CIO allow for seat-github-1. After: Lead creates and saves the key; the output line goes to HOST for custody; Web runs CXO's six turns. If `validated: no`, Lead's remove mode is needed (diff to HOST).
- **Fleet deny:** on main (733636419f + ed85825f3c, 11:27). On xian's card (rollup v1112) since 11-22 11:29: `cd ~/Development/piper-morgan-worktrees/cio && python3 scripts/seat_settings_grant.py fleet-deny`, expect `added 6 deny rule(s); 2 were already there...`. Then Pard restarts Web; Web's Read must be refused. Relay his line to CIO.
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
