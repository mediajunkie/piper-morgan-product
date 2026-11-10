# Exec carry-forward

**Rewritten 2026-11-09 22:02 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/09/2026-11-09-0422-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. An empty CronList is normal, and there's no STOP re-arm. Agent liveness is Pard's.

**Mail v4:** read `scripts/mail4.py inbox` on every wake, alongside v3; ack with `python3 scripts/mail4.py ack <ID>`. Open to every seat since Mon 11-09; v3 stays the fallback until 11-23. Find new v3 mail with `git log --since=<last check> --diff-filter=A --name-only --format= origin/main -- mailboxes/exec/inbox/`. Last check 22:01 Mon 11-09.

## Rollup
v914, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with a Python replace plus an assert. **To cut a span: anchor both ends on exact text, assert the block's `<li>`/`<div>` count, and assert the five or so neighbouring items still exist afterwards** (11-09 14:03: an `rfind("<li")` cut removed five unrelated cards; rebuilt from the committed version). Describe security findings by class only. **Tue 11-10 06:01: header set to Tuesday. The Tue post item stays until the post publishes or xian says "slip it"; check the calendar every fire.**

## Where things stand (end of 11-09)
- **Served on beta:** `727dd31596` (Lead run 42704401059, 13:37; /health 22:01 healthy). It carries #2334 (Redis pool waits instead of failing sign-ins), #2335 (startup log shows host and port only) and #2336 (Redis health ping every 30 s, not per request). PA's served two-turn sign-in checks passed on `f0e6505de8` (12:12) and `727dd31596` (13:45).
- **Main CI:** 12/12 green at 22:01. The Link Checker is green again since 11-08 22:20.
- **Sprint 11-13 to 11-26 ratified** (xian 08:48). Objection window closed 12:00 with 0 objections (decisions.log 12:11). Fri 11-13 review shortened (decisions.log 08:56): PPM refreshes the State column; the slot stays the weekly Ship review.
- **Invite hold** (xian 11-04): the P0 left is #2261, waiting on xian's #2174 `--issue 43` rerun and refresh run. #2292 mail records come before the next invite and the cohort note.
- **#2292:** DNS at 22:01 still only google-site-verification. Steps went to xian 11-07 18:01.
- **#2322:** guarded on beta; served row waits on a fresh account after the hold lifts.
- **Posts:** Tue 11-10 "Never Green in a Thousand Runs" (building, title final) was still Comms' 11-05 scaffold at 22:01 Mon, with the calendar row `planned`. The prose is xian's. On the rollup with a "slip it" option. At START: check whether it published or slipped.
- **Ship #068:** reviews 9/9, synthesis discussed, draft yes. NEXT: xian's first look (needs tokens for Oct 30–Nov 5 or "dollars is fine", $37.61), then Comms. Publishes Wed 11-11.

## Waiting on xian
1. **#2335:** in the Fly dashboard for `piper-morgan`, did the `Redis connection pool initialized` line hold the Redis password? Yes or no only. If yes, he rotates it and updates `REDIS_URL`. Relay to Lead, PPM, CIO the same hour; Lead confirms the reconnect.
2. **Tue post prose**, or "slip it".
3. **Ship #068** tokens and first look.
4. **#2174 `--issue 43` rerun + refresh run** (decides #2261), **#2292 Hover records**, **#2157 drill hour** (book early in the sprint), `! fly auth login`, the **cohort note**, **#2244** `/data` read, #2282 consent revoke.
5. Optional: the PA rename.

## Waiting on others
- **Arch:** short read on alpha/beta/staging common practice for xian's later talk.

## Reminders owed to xian
- **#2282 step 5, around Thu 11-12** (standing item #183): remove the alpha callbacks in GitHub and Google if a week passes with no hits.
- **Thanksgiving week (Mon 11-23):** PPM's one-liner: "First closing review Fri 11-27 or Sat 11-28? Thu 11-26 is the usual filing day, so when should seats file that week?"
- **Vercel: downgrade from Pro once the headroom exists again** (standing item #182). Raise that Hobby is non-commercial.

## Mine
- Relay xian's rulings at once and record them in decisions.log. Timestamps from a `date` call in the same command; **never write a stamp a few minutes ahead "for when it publishes"** (11-09: 14:05 and 14:06 written at 14:02 and 14:04, both caught before publish).
- **Review slot, every START:** re-read one claim from the last 24 hours against its source. 11-10 done: the #2151/#2155 "same stream" claim held (Arch's 10-24 15:29 comment on #2151: commit a3bc9a89c8 carries the #2155 copy line). Candidate for 11-11: pick at START from the last 24 hours.
- **Calendar check every fire**, not only at START: rows `published` in the last 7 days, and the next post's status. 11-09: a syndicated post stayed on the rollup as "needs Medium/LinkedIn" for 16 hours.
- **A tally or ruling written to decisions.log also goes out by mail the same hour** (11-09: the sprint tally sat in decisions.log only; PPM waited all afternoon; mailed 11-10 04:22).
- **At START, run `scripts/aging-standing-items.sh exec` and close any row whose subject has closed** (11-10: PPM flagged row 10, #1386, 11 days after the gate closed).
- Write DAY-CLOSED in grep form, `<!-- DAY-CLOSED: YYYY-MM-DD -->`, as the log's last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 is closed (CIO 11-06); the walk is on xian's talk list only if he wants it.
