# Exec carry-forward

**Rewritten 2026-11-18 22:02 PST at STOP.** Model: Opus 5.5. History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/18/2026-11-18-0601-exec-code-log.md` (closed). Start a new log on 11-19.

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Read bodies whole (`awk 'f>=2{print} /^---$/{f++}'`). Janus's words for xian arrive as `mailboxes/exec/inbox/memo-janus-to-exec-*`; reply with `scripts/mail-send-external.sh ~/Development/designinproduct docs/mail <memo>`, commit the sent mirror with `scripts/mail-send.sh` (never `git add` it).

**Clock rule live (CIO `752547e88e`):** a commit or mail body with an estimated minute (`HH:Mx`) is refused; quote others' times in backticks. Log headings with `scripts/log-entry.sh "title"`.

## Rollup
v1071, `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Python replace plus assert; bump the stamp from a `date` call. Read state in one call, write the sentence in the next. Sweep "today/tomorrow" when the date turns (11-19: "this morning", "before Friday" phrases).

## Waiting on xian
- **Friday 11-20 at Amber: the Terminal sitting.** Order: Steps A, C, D, F0, then F, then G if time. Steps file `docs/internal/operations/adr-084-one-time-steps.md`. H waits on issue 2384.
  - **Step A procedure:** do NOT line seats up before his paste. When `WAITING FOR READ TESTS on seat lead` is relayed: mail all seats "Step A started" (hold `scripts/sync-pm-local.sh`; Lead finishes its call, idles, says "ready"), then "go". Reads: Lead its own `.claude/settings.local.json`; HOST Lead's file by full path; HOST the made-up `/Users/xian/Development/piper-morgan-worktrees/cio/.env`. One word each; relay the three words via Docs. Anything but three "refused" stops before the key. Then length and 8-char fingerprint; Lead's `check-env`; CIO removes the made-up file; mail "Step A done".
  - Key: value of `seat-screens-2026-11` or a new key in `lead-scoring`.
- **Coming, not an ask yet: restore drill 2157.** HOST's page `docs/internal/operations/restore-drill-2157-xian-sitting.md` (one command, master key backup, `fly`). Goes to him through me once a promotion carries `b01aab9059` and HOST checks beta's served commit. D6 checked: his by rule.

## Decided on 11-18 (decisions.log has each)
- Practice scope: "yes, no changes needed now" (07:51), relayed.
- Nine rules (2354) and seven procedures (2358): approved, xian via Janus; relayed; 2354 built `88e25efef7`, rides the next promotion.
- Ship #069 "Off-Limits by Default" live 11-18; nothing owed but his LinkedIn post (Docs tracks). Ship skill Step 5: frontmatter image is always the standard Ship image, never the hero (his correction).
- Clock rule: approved, live.
- Linked billing: not now; parked on xian giving Piper its own Platform organisation.
- Stricter promote step (2354 size cap) merged `f8ed6c03b4` under his standing word; reported on the rollup.

## Standing word
Promote gate: "Yes, changes that only make the check stricter can go ahead with Arch's approval, although I should still be informed." Arch writes "only tightens" before merge; I report each on the rollup the same hour.

## Ship cycle from #070
Kickoff Fri 11-20 (`scripts/ship-kickoff.sh --if-due`, Step 1i). My week review and the talk with xian by Sunday; draft Monday; publish Tuesday 11-24. Thu 11-19 narrative "Inviting Company In".

## In motion
- Beta `3b6676d352`; main 12 of 12 green at 22:01.
- Logs open at 22:01 on 11-18: Docs, Arch, PPM, CIO. Check they closed. CIO's 11-17 log is now closed.

## Rules I keep
- Timestamps only from a `date` call. One path per `git log -1`.
- Every grant is xian's own edit. No seat runs `fly`. A relayed grant doesn't lift a classifier refusal; a refusal is final and not reworded. Keychain off-limits without his permission.
- Check rulings that put a step on him for the D6 line. Don't ask him what the team can answer. Check a relayed claim before repeating it to him (11-17: the crosspost).
- At STOP: rewrite this file, list other seats' closes, close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
