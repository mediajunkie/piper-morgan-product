# Exec carry-forward

**Rewritten 2026-11-10 22:08 PST at STOP** (Opus 5.5, Claude Code 2.1.322 since 16:29). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/10/2026-11-10-0422-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. An empty CronList is normal, and there's no STOP re-arm. Agent liveness is Pard's.

**Mail v4:** read `scripts/mail4.py inbox` on every wake, alongside v3; ack with `python3 scripts/mail4.py ack <ID>`. Open to every seat since Mon 11-09; v3 stays the fallback until 11-23. Find new v3 mail with `git log --since=<last check> --diff-filter=A --name-only --format= origin/main -- mailboxes/exec/inbox/`. Last check 22:01 Mon 11-09.

## Rollup
v917, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with a Python replace plus an assert. **To cut a span: anchor both ends on exact text, assert the block's `<li>`/`<div>` count, and assert the five or so neighbouring items still exist afterwards** (11-09 14:03: an `rfind("<li")` cut removed five unrelated cards; rebuilt from the committed version). Describe security findings by class only. **Tue 11-10 06:01: header set to Tuesday. The Tue post item stays until the post publishes or xian says "slip it"; check the calendar every fire.**

## Where things stand (end of 11-10)
- **Served on beta:** `c425fd242f` (Lead 18:58, run 42949313375; /health 22:01). Carries #2328: a pronoun-only completion ("complete them") asks which one, armed; a shown list whose lines changed opens "That list has changed since I showed it" (CXO accepted 18:46). Earlier today `6dc21c2ca8` (18:20). **Not served-verified:** PA and Web were both refused reading the web-seed-1386 credential file (PA 18:25/19:07, Web 19:03). Put to xian 19:08 in this session and by Lead in his.
- **Main CI:** 12/12 green at 22:01. A transient staging deploy red at 19:14 cleared on the next run (Lead 19:20).
- **Sprint 11-13 to 11-26** ratified; all ten seats no objection.
- **Invite hold** unchanged: #2261 waits on xian's #2174 test; #2292 records before the next invite.
- **Posts:** Tue "Never Green in a Thousand Runs" is **mid-rewrite by xian** (19:16, 19:22): beats 1-4 his, 5-7 scaffold, not published. Comms has 9 review notes (21:19 log). Thu 11-12 renamed by xian to **"The Server Has No Key"**.
- **Ship #068** (Wed 11-11): NEXT xian's first look. Spend: tokens still owed or "dollars is fine". **I misstated this at 16:34 in chat** (said dollars was settled); corrected on rollup v917.
- **#2232:** Lead took it 19:00; question to Arch on failing a database read locally. Nothing for Exec.

## Waiting on xian
1. **#2335:** in the Fly dashboard for `piper-morgan`, did the `Redis connection pool initialized` line hold the Redis password? Yes or no only. If yes, he rotates it and updates `REDIS_URL`. Relay to Lead, PPM, CIO the same hour; Lead confirms the reconnect.
2. **Tue post**: finish beats 5-7 (mid-rewrite), or "slip it". Thu post prose.
2b. **#2328 served check**: sign in for Web in its Chrome tab, or a plain username=/password= copy for PA, or a Read allow.
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
