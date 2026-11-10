# Exec carry-forward

**Rewritten 2026-11-08 22:11 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/08/2026-11-08-0423-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. An empty CronList is normal, and there's no STOP re-arm. Agent liveness is Pard's.

**Cron gate:** the duty-cycle-tick cron steps (the CronList self-heal and the STOP re-arm) don't apply on a LaunchAgent.

**Mail v4:** read `scripts/mail4.py inbox` on every wake, alongside v3. It opens to every seat on **Mon 11-09** (CIO), and v3 stays the fallback until 11-23. The v3 inbox holds 1,000+ files: find new mail with `git log --since=<last check> --diff-filter=A --name-only origin/main -- mailboxes/exec/inbox/`. Last check 22:10 Sun 11-08.

## Rollup
v911, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with a Python replace plus an assert, and **assert both ends of any span you cut**. Grep the exact anchor text before writing the replace. When a ruling is relayed, remove its rollup item in the same commit. The source is in a public repo, so describe security findings by class only. **At START: change the header to Monday 9 November and the "Sunday, in order" lead.**

## Where things stand (end of 11-08)
- **Served on beta:** `24c8c7f5e7` (Lead run 42537223392, 15:55; /health 22:01). Before it `98b95c80c0` (14:35), `2824ed3437` (13:06).
- **#955 closed** (CXO 16:10). PA's served "forget my handle preference" cleaned web-seed-1386, so **#2325's reset call is not needed** (CXO 14:50). Arch's morning hold was fixed and lifted.
- **#2270 closed** (CXO 13:44).
- **Main CI:** 11/12 at 22:10. Documentation Link Checker red from GitHub 5xx (run 42569350529: 81 broken, 23 of them 5xx; run 42570768907 counted 46 before a newer push cancelled it). At START: re-run `scripts/main-ci-status.sh`; if still red after GitHub recovers, mail Docs (the 11-05 PPM memo says don't lower the ceiling).
- **Invite hold** (xian 11-04): P0 left is #2261, waiting on xian's #2174 `--issue 43` rerun and the refresh run. #2292 mail records before the next invite and the cohort note.
- **#2292:** at 22:01 DNS still had no SPF/DKIM/DMARC (only google-site-verification). Steps given to xian 11-07 18:01: Google Admin DKIM generate (don't Start yet), Hover TXT `@` SPF, `google._domainkey` DKIM, `_dmarc` `v=DMARC1; p=none`; then I dig; then Start authentication; then test mails.
- **#2322:** guarded on beta; done branch unit-proven; served row waits on a fresh account after the invite hold lifts.
- **Posts:** Sun "When Accuracy Scores Worse" distributed (Medium + LinkedIn, calendar 11-08 22:19). Tue 11-10 "Never Green in a Thousand Runs" (title final; calendar status `planned` at 14:02 Mon).
- **Ship #068:** ship-status at 22:01: reviews 9/9, synthesis discussed, draft yes. NEXT: xian's first look (needs his tokens for Oct 30–Nov 5 or "dollars is fine"), then Comms. Publishes Wed 11-11.
- **Two-week sprints from Fri 11-13.** PPM trims the set before the review.

## Waiting on xian
2. **Spend tokens for Ship #068** (Oct 30–Nov 5 custom range, or "dollars is fine"), then his first look at the scaffold.
7. **#2174 `--issue 43` rerun + refresh run** (decides #2261), **#2292 Hover records**, `! fly auth login` (Lead's log reads), the **cohort note**, **#2244** `/data` read, #2282 consent revoke.
9. Optional: the PA rename.

## Waiting on others
- **Arch:** short read on alpha/beta/staging common practice for xian's later talk.
- **Sprint objections:** closed 11-09 12:00, 0 objections (decisions.log 12:11). Done.
- **Sprint 11-13 to 11-26 ratified** by xian 11-09 08:48. Fri 11-13 review shortened (decisions.log 08:56): PPM refreshes the State column; slot stays the weekly Ship review.

## Reminders owed to xian
- **Thanksgiving week (Mon 11-23):** PPM's one-liner: "First closing review Fri 11-27 or Sat 11-28? Thu 11-26 is the usual filing day, so when should seats file that week?"
- **Vercel: downgrade from Pro once the headroom exists again** (standing item #182). Raise that Hobby is non-commercial.
- **#2282 step 5, around Thu 11-12** (standing item #183): remove the alpha callbacks in GitHub and Google if a week passes with no hits.

## Mine
- Relay xian's rulings at once and record them in decisions.log. Timestamps from a separate `date` call only (11-08 slips: "12:1x" in a sent memo; guessed "13:24" and "18:05" rollup stamps, both caught before publish).
- **Review slot, every START:** re-read one claim I made in the last 24 hours against its source. Candidate for 11-09: my 18:04 "the red was an outside-site flake" (the 22:00 reds had a different cause, GitHub 5xx; check the 16:08 one really was the single 000 link).
- Prices to Exec: small classifier runs proceed unless stopped; screens get a ceiling with one re-run, re-priced past it.
- Write DAY-CLOSED in grep form, `<!-- DAY-CLOSED: YYYY-MM-DD -->`, as the log's last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 is closed (CIO 11-06); the walk is on xian's talk list only if he wants it.
