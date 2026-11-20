# Exec carry-forward

**Rewritten 2026-11-19 22:02 PST at STOP.** Model: Opus 5.5. History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/19/2026-11-19-0601-exec-code-log.md` (closed). Start a new log on 11-20.

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Read bodies whole (`awk 'f>=2{print} /^---$/{f++}'`). Janus's words for xian arrive as `mailboxes/exec/inbox/memo-janus-to-exec-*`; reply with `scripts/mail-send-external.sh ~/Development/designinproduct docs/mail <memo>`, commit the sent mirror with `scripts/mail-send.sh` (never `git add` it).

**Clock rule live (CIO `752547e88e`):** a commit or mail body with an estimated minute (`HH:Mx`) is refused; quote others' times in backticks. Log headings with `scripts/log-entry.sh "title"`.

## Rollup
v1077, `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Python replace plus assert; bump the stamp from a `date` call. Read state in one call, write the sentence in the next. Sweep "today/tomorrow" when the date turns (11-20: "today, Thursday 11-19", "before Friday (tomorrow)", "since 08:44 today", "Today&rsquo;s narrative is live").

## Waiting on xian
- **TODAY Friday 11-20 at Amber: the Terminal sitting.** Also Ship #070 kickoff today (Step 1i). Order: Steps A, C, D, F0, then F, then G if time. Steps file `docs/internal/operations/adr-084-one-time-steps.md`. H waits on issue 2384.
  - **Step A procedure:** do NOT line seats up before his paste. When `WAITING FOR READ TESTS on seat lead` is relayed: mail all seats "Step A started" (hold `scripts/sync-pm-local.sh`; Lead finishes its call, idles, says "ready"), then "go". Reads: Lead its own `.claude/settings.local.json`; HOST Lead's file by full path; HOST the made-up `/Users/xian/Development/piper-morgan-worktrees/cio/.env`. One word each; relay the three words via Docs. Anything but three "refused" stops before the key. Then length and 8-char fingerprint; Lead's `check-env`; CIO removes the made-up file; mail "Step A done".
  - Key: value of `seat-screens-2026-11` or a new key in `lead-scoring`.
- **Restore drill 2157: ready, his choice of day** (card on the rollup since v1074; Terminal on Amber, master key backup, `fly`). Beta `f34fe7bef5` still carries `b01aab9059`. If beta moves, check the ancestor again. Proofs 1, 2, 5 best today; proof 4 is his line; 3 waits on 2158.
- **Saturday 11-21 insight "A Blocker Framed as Yes or No":** scaffold, waits on his prose (Comms holds; title locked 11-19).

## Decided on 11-18 and 11-19 (decisions.log has each)
- Practice scope, nine rules (2354), seven procedures (2358): approved and relayed; 2354 served on beta since 11-19 07:03.
- Ship #069 live 11-18 and distributed. Ship skill Step 5: frontmatter image always the standard Ship image.
- Clock rule live. Linked billing parked. Stricter promote step `f8ed6c03b4` reported.
- 11-19: "Inviting Company In" written by him in the admin UI, live 17:02, Medium done (distributed).

## Standing word
Promote gate: "Yes, changes that only make the check stricter can go ahead with Arch's approval, although I should still be informed." Arch writes "only tightens" before merge; I report each on the rollup the same hour.

## Ship cycle from #070
Kickoff Fri 11-20 (`scripts/ship-kickoff.sh --if-due`, Step 1i). My week review and the talk with xian by Sunday; draft Monday; publish Tuesday 11-24. Thu 11-19 narrative "Inviting Company In".

## In motion
- Beta `f34fe7bef5` since 11-19 08:44 (disconnect unit; Web's signed-in pass). Main 12 of 12 green at 22:01.
- Logs open at 22:01 on 11-19: Docs, PPM, CIO (their STOPs may still run). Arch and PPM 11-18 logs were still unclosed at 22:01 11-19 (Docs's Step 1d nudge); check again at START and nudge if Docs hasn't.

## Rules I keep
- Timestamps only from a `date` call. One path per `git log -1`.
- Every grant is xian's own edit. No seat runs `fly`. A relayed grant doesn't lift a classifier refusal; a refusal is final and not reworded. Keychain off-limits without his permission.
- Check rulings that put a step on him for the D6 line. Don't ask him what the team can answer. Check a relayed claim before repeating it to him (11-17: the crosspost).
- At STOP: rewrite this file, list other seats' closes, close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
