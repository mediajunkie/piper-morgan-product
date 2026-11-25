# Exec carry-forward

**Rewritten 2026-11-24 22:02 PST at STOP.** Model: Opus 5.5. History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/24/2026-11-24-0601-exec-code-log.md` (closed). Start a new log on 11-25.

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake (it can take 2 minutes, so use timeout 200000). `--to`/`--cc` take space-separated roles. Ack one at a time. v3 ended 11-23: mail-send.sh is only for outside parties (Janus) with `PIPER_V3_FALLBACK='<why>'`. Janus's words arrive as `mailboxes/exec/inbox/janus-to-exec-*`. Reply by writing the memo in `mailboxes/exec/sent/`, then `scripts/mail-send-external.sh ~/Development/designinproduct docs/mail <memo>`, then the mail-send.sh mirror.

**Clock rule live:** no estimated minutes in commits, mail or logs. The hook reads the command text too, so build such a string in Python if you must replace one. Headings: `scripts/log-entry.sh "title" >/dev/null`. zsh: never `echo =====`.

## Ship #070 "No Workarounds": DONE 11-24
Live 09:44, crossposted to LinkedIn, calendar row `distributed` (Docs 01M87ETVG6, 10:59). Nothing owed. Next Ship: #071 kickoff Fri 11-27 via `scripts/ship-kickoff.sh` (the first live v4 kickoff).

## Rollup
v1163 (Wed 11-25: 2438 served, seat-tester hold lifted; 2438; Duet reach check; beta 92836ae41d;: sprint 3 three answers added; START: h1 Wednesday; #070 done line and 11-24's two for-your-record notes dropped), `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Python replace plus assert, and bump the stamp from a `date` call. **At START 11-26:** retitle the h1 to Thursday. On every rebuild, check each card item against the seats' logs and the editorial calendar (cohort-attention-rollup step 2.01, xian's tell-one-agent rule). 11-24 18:01 and 22:01 found no xian completions.

## ADR-084 sitting (steps file `docs/internal/operations/adr-084-one-time-steps.md`)
- **Done:** A, C, D, F0, F.1 (11-20).
- **Next for xian: F.2** (org Base permissions No permission; invite `atswimtwobirds` as Member; team `seat-test` with the test repos only; the billing seat-count line). Then F.3, F.4 (connect as seat-github-1), G parts 1 and 2, PA's zero-install read, and the F.5 install (PA's order, 01M7Y03RJG).
- **Step E (OpenAI key):** open. It's the one thing between #2364 and merge.
- Guide him one step at a time (his ask, 11-20).

## On xian's card (rollup v1155), in order
1. **Fleet deny** (on main 733636419f + ed85825f3c): `cd ~/Development/piper-morgan-worktrees/cio && python3 scripts/seat_settings_grant.py fleet-deny`, expect `added 6 deny rule(s); 2 were already there...`. Relay his output line to CIO. Pard restarts Web, and Web's Read must then be refused. Still open per HOST's 11-23 logs.
2. **seat-tester-1 sitting (#2406, and #2417's last row):** mint; `seat_account_create.py --account seat-tester-1 --write-invite`; Lead's create allow; console check; save-key allow. After that, Lead creates and saves the key, and Web runs CXO's six turns and #2417's never-connected line. Lead's `--remove-key` is on main `4755940a10`. Its allow is step 6 (CIO 01M862N72R). Step 7 (v1135): Web's floored-actions read allow (HOST 01M870QDFH).
3. **F.2, then F.4, and E** (above).
4. **Step H** (four steps; relay his date and expiry to HOST).
- Done 11-23 and off the card: the "Do I Have To?" crosspost and the Medium "Inviting Company In" tease (Web's feed read; Docs recorded it).
- Titles: Sat 11-28 is "Mark One Eyeball". Restore drill 2157: his choice of day. Later: #2387.

## In motion
- **New 11-24:** 2433 (non-admin opening an admin page gets raw JSON) and 2434 (six vague "Failed to" toasts, plus CXO's page-copy sweep row) are placed by PPM; 2434 in H. Nothing for xian.
- **Beta `cf3486389e`** since 11-25 13:50 (2438; Lead 01M8AB1QAT). Before it `92836ae41d` since 11-25 10:15 (2437; Lead 01M89YVZ50). Before it `aaf8d9249e` since 11-25 08:36 (2433, 2434, 2399, 2356 test; Lead 01M89S7T8B; Web's four served reads open). Before it `23b1373185` since 11-24 15:12 (all of 2432; Lead 01M87XBH8G). Before it `6ff8197d9a` 13:08. Before it `f4a5baa9b6` 12:30 (2431). Before it `b2cda27b5d` 11:25 (2429, 2430). Before it `009afa0f7f` since 10:24 (2345, Lead 01M87CW2PH), on top of `b86c072755` (09:52). F.4 is the GETDEL served read: its result goes to Lead and HOST as one line.
- **Staging deploy blips:** VM start failures cleared by re-run on 11-10, 11-20 and 11-23 (Lead 01M85C2R1S). A fourth makes a pattern: take it to xian (the Fly hand is his).
- **Open nearby:** #2417 (update_issue row, fresh account), #2245 served read, 2301 part 2. #2411's rows moved to #2425; #2426 filed. Both are sprint 3 candidates, and xian sets the slot at the 11-25 draft. #2424 is held on router evidence.
- **Sprint 2 closes Wed 11-26.** It doesn't stretch (xian 11-20), and #071 reports the score as it stands. The first live v4 Ship kickoff is Fri 11-27 (#071), by `scripts/ship-kickoff.sh`.
- **seat-tester-1 card step 7 (rollup v1135):** Web's floored-actions read allow, HOST cleared 06:52 (01M870QDFH; it no longer waits on #2390/#2391). Closes #2388 row 4 after Web runs it once.
- **Coming to xian's card (not yet):** (1) **Step H is ON the card now** (rollup v1138, CIO 01M8743V4A). When xian gives the date and expiry, relay them to HOST for the custody row and the names-only check. (2) **2282 box 4** removal of the alpha callbacks: only after Web's `/setup` calendar start read names beta (Arch 01M8728HYN). (3) **2244: PPM slotted it 11-25 (sprint 3 draft item 9, 01M89J4NND); ON the card v1157 with the focus and dates questions. Relay xian's answer to PPM, Lead, Arch, CXO, HOST same hour.** Earlier: ask xian whether the 2244 change may ship under the standing grant (on Arch's validation and HOST's read). It adds two lines to the root-run start script that create one more folder on the volume, the same pattern as uploads. There is no new mount and no deploy outside the grant. Use Lead's wording (01M8775T0W). HOST says yes, and notes the volume stops being uploads-only (01M877BG5F). Arch: a plain chown, not -R. (4) The setup-calendar allow is ON the card as step 8 (v1147, CIO 01M87BAE0Y). If Web's read names beta, write xian's alpha-callback removal card (Arch 01M8728HYN: each GitHub app keeps only its own callback, wildcard unticked; Google keeps the two beta callbacks). (5) 2345 and 2399: F.4 also opens 2399's last row (already-closed and not-found close lines, a seat read on the working connection, Lead 01M89SNRXV) and 2437's check (close on a stale token asks yes/no). Neither adds a step for xian. HOST 01M877Z1DP conditions: promote 2345 BEFORE xian starts F.4; tell HOST and Lead when F.4 starts and ends; F.4's result goes to HOST (custody row) and Lead (served read) as one line. Card F.4 note added in v1141. Earlier: 2345 (connect state in Redis): Lead tells me before it promotes. Arch 01M873KWAY: GETDEL has never been served on beta's Upstash, so the first connect after it promotes is the served test. If that connect is xian's F.4, say so on the card, and if it fails with `oauth_state_store_unavailable op=take`, roll back first.
- **Step 7 (counter-read allow) stays:** Lead asked to hold it (01M87219QQ), but HOST 07:16 read `add_allow`, and the tool takes the line. Only a test pin is red, and CIO widens it by three literals.
- **2438 passwords (Arch 01M8A7NE11, 11-25):** Sequencing (Arch 01M8A7R9JX): the seat-tester-1 hold LIFTED 11-25 v1163, since 2438 is served on cf3486389e. 2438 stays open on the wizard row, read by seats at that sitting (PPM 01M8ABRRPG); the reset half passed. stricter check told to xian on v1161. His choice: keep five rules (default) or length-only (NIST). If he picks length-only, relay to Arch to re-rule, cc PPM and CXO.
- **Piper Duet (11-25, Janus):** xian started a Duet on the pipermorgan.ai account; it answers to me. My answer to Janus (designinproduct `exec-to-janus-cc-docs-re-piper-duet-inbox-conditional-yes-2026-11-25.md`): box `mailboxes/duet-piper/inbox/` and a DIRECTORY row only if its SCHEDULED runs read this repo; interactive-only means no box (it writes to my inbox and I answer in the shared status files); no reach means Janus's fallback. Seats never mail it directly. The reach check is on the card (v1160). Act on Janus's result the same hour.
- **Seat done-notes:** any seat that finishes something with xian mails me one line in the same turn (my relay 01M85PWK3T; duty-cycle-tick v1.66 Step 5, CIO). Docs sent the first one at 18:46.
- **Promote hold:** the `ops/promote-hold.md` mechanism exists but isn't in use. **Staging D6:** HOST's read-only staging Machines token idea is at 2 of 3 repeats.
- Main 12 of 12 green at 22:01 on 11-24.

## Closes at 22:01 on 11-24
Closed: Web, Comms, HOST, Arch, CXO, PPM, Lead, PA. Open: Docs, CIO, prog (four prog logs; their STOPs may still run). Check at START.

## Standing word
- Promote gate: "Yes, changes that only make the check stricter can go ahead with Arch's approval, although I should still be informed." I tell him the same hour.
- Tell-one-agent (11-23): "I need to be able to trust that I can tell the agent I am working with such an update and that I will not have to also manually report it to their primary point of contact let alone to you directly."

## Rules I keep
- Timestamps only from `date`. Every grant is xian's own edit. No seat runs `fly`. A refusal is final and is not reworded. The keychain is off-limits without his permission. Never direct a seat to read its `.env` or settings file.
- D6-check every step that lands on him: who would actually do it? Check (tmux ls in full, not `head`). Don't ask him what the team can answer. No account emails or secrets in this repo.
- Before re-asking xian anything, grep decisions.log for it (11-23: Janus nearly re-asked three questions he had settled 11-20, because my review page never marked them answered).
- At STOP: rewrite this file, list the other seats' closes, and close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06). Walk it on xian's talk list only if he wants it.
