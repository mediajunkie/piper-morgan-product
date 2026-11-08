# Exec carry-forward

**Rewritten 2026-11-07 22:02 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/07/2026-11-07-0427-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. An empty CronList is normal, and there's no STOP re-arm. Agent liveness is Pard's.

**Cron gate:** the duty-cycle-tick cron steps (the CronList self-heal and the STOP re-arm) don't apply on a LaunchAgent.

**Mail v4:** read `scripts/mail4.py inbox` on every wake, alongside v3. It opens to every seat on Mon 11-09 (CIO), and v3 stays the fallback until 11-23. The v3 inbox holds 1,000+ files: find new mail with `git log --since=<last check> --diff-filter=A --name-only origin/main -- mailboxes/exec/inbox/`. Last check 22:01 Sat 11-07.

## Rollup
v897, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with a Python replace plus an assert, and **assert both ends of any span you cut**. Grep the exact anchor text before writing the replace. When a ruling is relayed, remove its rollup item in the same commit. The source is in a public repo, so describe security findings by class only.

## Where things stand (end of 11-07)
- **Served on beta:** `f9b4c737f7` (Lead run 42446024382, 20:18; /health 22:01): #2321 N1 words (CXO 18:47) and #2325's admin reset route. PA passed N1 on it. Before it `4d5fbfae7d`. Main 12/12 green at 22:02.
- **D5 / #2320 / #2318:** final at 1.5 s, 10 of 10 in PA's chats, no fallback (Arch 18:28). Done.
- **#2270:** turn 2 passed on `debb7bef3b`; turn 1's handler (Arch approved 20:14) being built by Lead, not yet on beta. PPM: turn-1 fix in sprint, armed-read offer is #2326. Lane traffic; nothing for Exec.
- **#2322:** guarded on beta; done branch unit-proven; served row needs #2325 (xian's admin call, option a) or Q8's fresh account (b).
- **Invite hold** (xian 11-04): P0 left is #2261, waiting on xian's #2174 `--issue 43` rerun and the refresh run. #2292 mail records before the next invite and the cohort note.
- **#2292:** at 22:01 DNS still had no SPF/DKIM/DMARC (only google-site-verification). Steps given to xian 18:01: Google Admin DKIM generate (don't Start yet), Hover TXT `@` SPF, `google._domainkey` DKIM, `_dmarc` `v=DMARC1; p=none`; then I dig; then Start authentication; then test mails.
- **Two-week sprints from Fri 11-13.** PPM trims the set before the review.
- **Ship #068:** scaffold `docs/public/comms/drafts/weekly-ship-068-draft-2026-11-06.md`, pubDate Wed 11-11. Needs xian's tokens in/out for Oct 30–Nov 5 (his 16:49 screenshot was Last 30 days, so a custom range is still owed, or "dollars is fine"), then his first look, then Comms. xian: the Ship waits behind the weekend insight posts and Tuesday's narrative.
- **Posts:** Sat "At Long Last, Beta" distributed (Medium + LinkedIn URLs from xian); Docs re-filed it as **insight** 18:54 (weekend slots are insights; CIO added a weekday-slot check to publish-to-blog v0.27). My own 18:47 reply to xian repeated "building posts go to Medium only": wrong, the same miss. Sun "When Accuracy Scores Worse" (insight) on Comms' ready memo.

## Waiting on xian
2. **Spend tokens for Ship #068** (Oct 30–Nov 5 custom range), then his first look.
3. **Scaffold OK, or "draft it"** for Ship #068.
7. **#2174 `--issue 43` rerun + refresh run** (decides #2261), **#2292 Hover records**, `! fly auth login` (Lead's log reads), **#2325 a or b**, the **cohort note**, **#2244** `/data` read, #2282 consent revoke.
9. Optional: the PA rename.

## Waiting on others
- **Ruled 11-07 16:50 (decisions.log):** weekly rhythm GO, flexes when needed; Rule 8 history leave it. #2270 phrasing sent.
- **Arch:** short read on alpha/beta/staging common practice for xian's later talk.
- **Sprint objections:** window closes Mon 11-09 12:00 PT (xian's own window, decisions.log 3133). At noon Monday, put the tally on the rollup; take any objection to xian.
- **PPM** trims the sprint-2 set before the 11-13 review.

## Reminders owed to xian
- **Thanksgiving week (Mon 11-23):** PPM's one-liner: "First closing review Fri 11-27 or Sat 11-28? Thu 11-26 is the usual filing day, so when should seats file that week?"
- **Vercel: downgrade from Pro once the headroom exists again** (standing item #182). Raise that Hobby is non-commercial.
- **#2282 step 5, around Thu 11-12** (standing item #183): remove the alpha callbacks in GitHub and Google if a week passes with no hits.

## Mine
- Relay xian's rulings at once and record them in decisions.log. Timestamps from a separate `date` call only (11-07 slips: "12:3x", "16:5x", "16:4x", "17:4x", "22:0x"; all caught before commit or send).
- **Review slot, every START:** re-read one claim I made in the last 24 hours against its source. Candidate for 11-08: my 18:47 "building posts go to Medium only" (already known wrong; check the calendar row reads insight + distributed).
- Prices to Exec: small classifier runs proceed unless stopped; screens get a ceiling with one re-run, re-priced past it.
- Write DAY-CLOSED in grep form, `<!-- DAY-CLOSED: YYYY-MM-DD -->`, as the log's last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 is closed (CIO 11-06); the walk is on xian's talk list only if he wants it.
