# Exec carry-forward

**Rewritten 2026-11-17 22:02 PST at STOP.** Model: Opus 5.5 since 11-17 21:29 (Fable 5.2 before; xian: "we've hit the Fable limit"). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/17/2026-11-17-0601-exec-code-log.md` (closed). Start a new log on 11-18.

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Roles space-separated on `send`. Read bodies whole (`awk 'f>=2{print} /^---$/{f++}'`). Janus's words for xian arrive as file mail in `mailboxes/exec/inbox/memo-janus-to-exec-*`; reply to Janus with `scripts/mail-send-external.sh ~/Development/designinproduct docs/mail <memo>`, then commit the sent mirror with `scripts/mail-send.sh`.

## Rollup
v1059, `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Edit with Python replace plus assert; bump the "vNNN, rebuilt" stamp from a `date` call. **Read CI or any state in one call, write the sentence in the next** (twice on 11-17 I published a stale CI state). When the date turns, sweep "today/tomorrow" phrases.

## Waiting on xian
- **Friday 11-20 at Amber: the Terminal sitting** (his word to Docs, 11-17 evening: away from Amber until then). Order: Steps A, C, D, F0, then F, then G if time. CIO re-read A, C, D (`b4977cc5ec`, paste lines unchanged) and fast-forwards his checkout Friday morning. Steps file `docs/internal/operations/adr-084-one-time-steps.md` opens with "The sitting". H (MCP deploy token) waits on issue 2384, not on Amber.
  - **Step A procedure:** do NOT line seats up or ask Lead to idle before his paste (11-17 cost Lead three hours). When Docs or he relays `WAITING FOR READ TESTS on seat lead`: mail all seats "Step A started" (hold `scripts/sync-pm-local.sh`; Lead finishes its call, idles, says "ready"), then "go". Reads: Lead its own `.claude/settings.local.json`; HOST Lead's file by full path; HOST the made-up `/Users/xian/Development/piper-morgan-worktrees/cio/.env`. One word each. Relay the three words to him via Docs. Anything but three "refused" stops before the key. Then length and 8-char fingerprint; Lead's `check-env`; CIO removes the made-up file; mail "Step A done".
  - Key: value of `seat-screens-2026-11` or a new key in `lead-scoring` (old one disabled).
- **Ship #069 publishes Wed 11-18.** Scaffold `docs/public/comms/drafts/weekly-ship-069-draft-2026-11-17.md`, last commit 11-17 14:06, waits on his prose (admin UI). Then I edit, Comms audits, Docs publishes (LinkedIn only). Two small calls for him in it (alt-text typo; "you choose the repositories").
- **Practice-scope yes or no:** CXO and PPM recommend keeping header and 13 rows and making "what the team has proven in its own work" the deliberate scope. Sent to Janus. Relay his word to CXO, PPM, CIO, Docs with a decisions.log line.
- **Two self-knowledge texts:** nine rules (2354, `47a65eed5f`; Lead's build waits on it), seven procedures (2358). practice.md approved 11-17.
- **Optional, no ask:** whether the beta testers' key is in the same Anthropic organisation as the seat workspaces (shared $250 limit). Arch's fact; on the rollup.

## Decided on 11-17 (decisions.log has each)
- Ship 069 goals: yes to all five. Spend 11-06 to 11-12: $33.38. Router screens' $12 inside it.
- Keychain launch: "ok to leave it. let's ensure it doesn't recur, though." Guard `.claude/hooks/guard-browser-launch.sh` (CIO, last `f58d8cfd79`), validated by Arch, custody conforms (HOST); 5 of 11 seats tested; every-fire check Step 1j plus Pard ten times a day. Residual: launch from inside a script.
- Env-file check: "Yes, skip and fix." Issue 2403 placed (Production, beside 2395). **Never direct a seat to read its `.env` or `settings.local.json`;** auto mode refused my mail that did.
- `piper-morgan-test` key: "No" and "Yes, if that's the right way to do it, sure"; HOST "right way", Arch conforms; verified $16.19 of $40, resets Dec 1. Org $49.29 of $250; credits $180.06.
- Spend tone: tracking stays, asks are short (memory `feedback_spend_asks_light_tone_tracking_stays`).
- Promote gate: "Yes, add those two folders." Merged `7e91d9bc62`. **Standing word:** "Yes, changes that only make the check stricter can go ahead with Arch's approval, although I should still be informed." Promote gate only; Arch writes "only tightens" before merge; I report each on the rollup the same hour. On Lead's role card (HOST).
- Caching: already set per request on the classifier; automatic mode is not Piper's shape; leave as is; 2354 is the fitting change (with a count-only read beside it, Arch).
- Cadence: Thu 11-19 "Inviting Company In"; from #070 Ship TUESDAY (11-24, 12-01, 12-08, 12-15), narrative Thursday, insight weekend, no narrative Thanksgiving week. Syndication unchanged: insight Medium+LinkedIn, narrative Medium only, Ship LinkedIn only.
- "The Wall" published 11-17 20:30, Medium crosspost done, nothing owed.

## Ship cycle from #070
Kickoff Fri 11-20 (`scripts/ship-kickoff.sh --if-due`, Step 1i; it now counts v4 reviews and tells seats to file on v4). My week review and the talk with xian by Sunday; draft Monday; publish Tuesday.

## In motion
- Beta `d678b0af26` since 11-17 11:31 (2401, 2402, Slack sentence, console link "Claude Platform"); not checked signed in. Main 12 of 12 green at 22:01.
- Lead: issue 2404 (seat driver for the guide's keyed steps), 2403. Docs: guide status line by layer (step 5 a person's check).
- Logs open at 22:01 on 11-17: Docs (last 20:44), CIO (last 18:36). Check they closed.

## Rules I keep
- Timestamps only from a `date` call. One path per `git log -1`.
- Every grant is xian's own edit. No seat runs `fly`. A relayed grant doesn't lift a classifier refusal; a refusal is final and not reworded. Keychain off-limits without his permission.
- Check rulings that put a step on him for the D6 line. Don't ask him what the team can answer. Check a relayed claim before repeating it to him (11-17: the crosspost).
- At STOP: rewrite this file, list other seats' closes, close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
