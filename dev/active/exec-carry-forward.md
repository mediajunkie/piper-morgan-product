# Exec carry-forward

**Rewritten 2026-10-30 23:09 PDT** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/10/30/2026-10-30-0708-exec-code-log.md` (closed).

**STATE: LIVE.** Cron **`b3c6dc73`** (`38 6,10,14,18,22 * * *`), re-armed 10-30 at STOP from the stored prompt; `seat-prompt.sh exec --check` rc=0. Expires about 11-06; re-arm at each STOP. LaunchAgent `com.xian.pm-exec-cycle` (:01 at 6,10,14,18,22, idle-check skip) is staged by Pard and not yet loaded (xian's paste, Pard console v184). On Pard's load notice and the first :01 fire that lands work, CronDelete the session cron and flip the registry row (row 179).

**Re-arm only from the store** (duty-cycle-tick v1.60): `scripts/seat-prompt.sh exec` prints the verbatim prompt. Pass it to CronCreate unchanged, then CronList and `--check <file>`. Never rebuild from memory (xian 10-30).

## Rollup
v708, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with Python replace plus an assert, never sed.

## Where things stand (end of 10-30)
- **MVP closed** on xian's Go (PPM: #1386 and the milestone; hard stop held, 0 days moved). Alpha and beta serve `ac5b69f865` (one machine, `piper-morgan`).
- **Slack inbound gate unset** by xian; PA read "disabled" on beta and alpha (20:25).
- **Beta letters final** (9 known-issue lines, PPM 9/9). Four Gmail drafts in xian's **designinproduct.com** account (ids r-5017300857877623593 1a, r-6829984518040049075 1b, r-9172552273556573429 1c, r-7695891930464179739 2), with no recipients and no codes. HOST mints 9 codes with xian.
- **Promotion freeze** until the letters go. On main and validated, waiting for the next promotion: #2225, the #2230 setter validation, #2236 parts 1 and 2, #2233 and the four fixes (93bd29ccd7), #2237's grey-out plus server guard (a3b3645787), the connect listing (5c7f15d794), #2240's guard (de1d1bd714). PPM holds the re-check list.
- Tracking audit met: 27 product issues, all tracked; label `fix:not-served` for closed-but-unserved. The Sprint field is set on every open Production issue (81 set on xian's yes).

## Saturday 10-31, xian's sequence (rollup hot card)
0. ~~MCP ls~~ moot: #2218 served on MCP v15 at 06:53 10-31 (Fly release time) (PA; Exec's timing call 06:49).
1. Send the letters.
2. Promote main.
3. PPM's re-check list (row 2, row 3 rows, CXO's served reads of #2236 and #2237).
4. xian's by-name word on `set_default_repo`, applied by HOST or CIO with him present.
5. PA's probe, then one row 2.
Then the first-sprint priorities talk toward Production (PPM's four tiers, six decisions).

## Waiting on xian
- PPM: may new Production issues get their plan sprint without a fresh word each time? (Exec: yes.) Waiting: #2238 PROD-RECONNECT, #2239 PUB, #2241 PROD-HONESTY, #2242 PUB.
- Decision 7, #2242 (who may connect the hosted MCP): PPM (a) allowlist; Exec (a), in the sprint.
- PA's MCP test plan, after the letters (`docs/internal/operations/mcp-test-plan-pm.md`); his notes go to PA.
- CIO: keep the promotion grant with the reworded review trigger. (Exec: yes.)
- Ship #067 week review discussion (artifact `4Le3ZyacNXUqo19SQh5GpT`; spend row filled from his screenshots). The draft waits on it.
- ghmint fix paste first (Pard console v185; mediajunkie ea2bdcd: curl retries 4 min, mint every 15 min). CIO 07:4x asks it go first.
- LaunchAgent loads (Pard console v184).
- Rule-8 history, whenever he takes it up: HOST's briefing people list; issue #1509's title; HOST's 10-30 log, two entries naming outside beta candidates (HOST owns the slip).
- Crossposts: Build the Instrument (Medium + LinkedIn, Docs 08:5x), Citation via Hearsay (Medium).
- #2241/#2022 served on MCP v16 09:30; v17 09:35 serves 0.9.0.0 (3d1e7e08e8). Lead closes them.
- 0.9.0 (xian via Docs): Lead owns, the bump lands before step 2, the tag after re-checks. The bump is on main (c9791112d8, 09:30), and xian's word via Docs is 0.9.0.0. PPM's tag rule is in its 09:3x memo. Docs is writing the notes body and the phase-3 docs.
- Older: Lead's promotion allow line (row 167), Docs' Ongoing sort (row 168), the Citation Medium crosspost.

## Mine
- Relay xian's rulings at once; record them in decisions.log. Timestamps from `date`, or the source memo's own stamp, never "xx:5x".
- Briefing-pointer recheck Mon 11-02 (AGENT counts 4/5, #2157 exempt). Ship-kickoff check Fri 11-06. Map diff Fri 11-06.
- Rule 8: outside names stay out of everything I write here.
