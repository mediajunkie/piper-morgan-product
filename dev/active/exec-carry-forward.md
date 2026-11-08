# Exec carry-forward

**Rewritten 2026-11-06 22:01 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/06/2026-11-06-0423-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. An empty CronList is normal, and there's no STOP re-arm. Agent liveness is Pard's.

**Cron gate:** the duty-cycle-tick cron steps (the CronList self-heal and the STOP re-arm) don't apply on a LaunchAgent.

**Mail v4:** read `scripts/mail4.py inbox` on every wake, alongside v3. It opens to every seat on Mon 11-09 (CIO), and v3 stays the fallback until 11-23. The v3 inbox holds 1,000+ files: find new mail with `git log --since=<last check> --diff-filter=A --name-only origin/main -- mailboxes/exec/inbox/`.

## Rollup
v885, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with a Python replace plus an assert, and **assert both ends of any span you cut**. Grep the exact anchor text before writing the replace (11-06 17:28: an anchor that wasn't there failed the assert, and the publish sent the unchanged page). When a ruling is relayed, remove its rollup item in the same commit. The source is in a public repo, so describe security findings by class only.

## Where things stand (end of 11-06)
- **Served on alpha:** `49a5778df4` (Lead, Sat 11-07 09:04, run 42394159387: ADR-083 D5 live: delete ordinals pass, "complete the second one" not bound 3 of 3, turns flat at the 2.5 s ceiling, #2318; Lead logging push, Arch ruled a D5-only ceiling ≤5 s; any screen priced to Exec). Before it `641ef2eb56` (07:03, run 42384255405: #2315 pick, #2316 name-or-number question; PA 07:07 passed every row on beta, CXO closes). Before it `0af6078171` (11-06 20:38, run 42339059907). Today's eight promotions, all dispatched by Lead: `e64de73062` 07:04, `0d4938cf23` 09:43, `765a2bc4f1` 13:09, `7ffd460640` 15:37, `34efff2af8` 17:27, `06c71d53e2` by 18:08, `771eb4f9bd` 19:08, `0af6078171` 20:38. Main CI is 12/12 green (it was red 19:37–20:06 from Lead's push, self-reported).
- **Closed today:** #2302, #2272, #1715 (skills review: 13 candidates, none built).
- **Lane, open:** #2301 (interim pulled; stays FAIL until the read); #2315 ("complete the X todo" skips the pick, PA 20:47); #2314's name cut at "link" (Lead: upstream, row added).
- **ADR-083:** the slot screen FAILED 17:24 (38 unrelated rows moved, ~$3.45). **D5 PASSED** 18:22 (~$1.42; Arch ruled 18:24). D5 is on branch `claude/lead-adr083`, off main, until xian's explicit go or veto. Arch agreed 18:45: no default window length.
- **Invite hold** (xian 11-04 19:31, no invites of any kind): P0 left is #2261, waiting on xian's #2174 runs. #2292 mail records before the next invite and the cohort note. #2286's on-page read rides PA's fresh-account run (CXO 13:17), not xian.
- **Two-week sprints RULED 10:33**, from Fri 11-13. PPM's proposed set (11 items, map v88), Lead sized it over capacity, so PPM trims before the 11-13 review. #2157 single drill run is an 11-13 candidate (Arch).
- **Ship #068:** synthesis discussed (11-06). The scaffold is at `docs/public/comms/drafts/weekly-ship-068-draft-2026-11-06.md`, with the calendar row drafted and pubDate Wed 11-11. It needs xian's Console screenshots for the spend line, then his first look, then Comms.
- **Posts:** Sat 11-07 "At Long Last, Beta" (working title, building, planned; xian writes it). Sun 11-08 "Fixed and Scores Higher Came Apart" (insight).

## Waiting on xian
2. **Spend tokens for Ship #068:** Cost screenshots in 11-07 ($37.61, filled in the draft). One Usage screenshot (tokens in and out, Workspace All) or "dollars is fine". Then his first look at the scaffold.
3. **Scaffold OK, or "draft it"** for Ship #068.
7. **#2174 runs** (decides #2261, the last P0), **#2292 mail records**, the **cohort note**, **#2244** `/data` read, #2282 step 4 (PASSED 11-07 08:02, Web; the consent-page row needs a revoke, on xian's word another day).
9. Optional: the PA rename.

## Waiting on others
- **Ruled 16:50 (decisions.log):** weekly rhythm GO, flexes when needed (PPM names the Thanksgiving-week review day); Rule 8 history leave it. #2270 phrasing sent to PA and Lead (corpus row).
- **Ruled 11-07 by 08:03, relayed 08:04 (decisions.log):** ADR-083 D5 GO (Lead lands `claude/lead-adr083`; Arch marks accepted); PDR-008 P1-P3 YES (PPM marks Accepted; HOST owns P2).
- **Arch:** short read on alpha/beta/staging common practice for xian's later talk (asked 11-07; card under "Next time").
- **Sprint objections:** window closes Mon 11-09 12:00 PT. No objection so far from HOST, CXO or Comms (3 of 10). At noon Monday, put the tally on the rollup; take any objection to xian.
- **PPM** trims the sprint-2 set before the 11-13 review.

## Reminders owed to xian
- **Thanksgiving week (Mon 11-23):** PPM's one-liner: "First closing review Fri 11-27 or Sat 11-28? Thu 11-26 is the usual filing day, so when should seats file that week?" (xian 11-07: the rhythm flexes when needed.)
- **Vercel: downgrade from Pro once the headroom exists again** (standing item #182). Trigger: the split is live and admin-only usage is well inside Hobby. Raise that Hobby is non-commercial, so the downgrade may not be allowed.
- **#2282 step 5, around Thu 11-12** (standing item #183): remove the alpha callbacks in GitHub and Google if a week passes with no hits.

## Mine
- Relay xian's rulings at once and record them in decisions.log. Timestamps come from a separate `date` call only, never written in the same command (today's slips: 10:03, 10:05, 10:21, "10:5x", "11:0x", "18:1x"; the last caught before publishing).
- **Review slot, every START:** re-read one claim I made in the last 24 hours against its source, and log the result.
- Prices to Exec: small classifier runs proceed unless stopped; screens get a ceiling with one re-run, re-priced past it.
- Write DAY-CLOSED in grep form, `<!-- DAY-CLOSED: YYYY-MM-DD -->`, as the log's last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 is closed (CIO 11-06); xian asked to hear skills-review outcomes, which he has. The walk itself is on his talk list only if he wants it.
