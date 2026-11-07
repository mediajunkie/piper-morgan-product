# Exec carry-forward

**Rewritten 2026-11-06 22:01 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/06/2026-11-06-0423-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. An empty CronList is normal, and there's no STOP re-arm. Agent liveness is Pard's.

**Cron gate:** the duty-cycle-tick cron steps (the CronList self-heal and the STOP re-arm) don't apply on a LaunchAgent.

**Mail v4:** read `scripts/mail4.py inbox` on every wake, alongside v3. It opens to every seat on Mon 11-09 (CIO), and v3 stays the fallback until 11-23. The v3 inbox holds 1,000+ files: find new mail with `git log --since=<last check> --diff-filter=A --name-only origin/main -- mailboxes/exec/inbox/`.

## Rollup
v873, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with a Python replace plus an assert, and **assert both ends of any span you cut**. Grep the exact anchor text before writing the replace (11-06 17:28: an anchor that wasn't there failed the assert, and the publish sent the unchanged page). When a ruling is relayed, remove its rollup item in the same commit. The source is in a public repo, so describe security findings by class only.

## Where things stand (end of 11-06)
- **Served on alpha:** `641ef2eb56` (Lead, Sat 11-07 07:03, run 42384255405: #2315 pick, #2316 name-or-number question; PA checks next, #2316 open until quoted). Before it `0af6078171` (11-06 20:38, run 42339059907). Today's eight promotions, all dispatched by Lead: `e64de73062` 07:04, `0d4938cf23` 09:43, `765a2bc4f1` 13:09, `7ffd460640` 15:37, `34efff2af8` 17:27, `06c71d53e2` by 18:08, `771eb4f9bd` 19:08, `0af6078171` 20:38. Main CI is 12/12 green (it was red 19:37–20:06 from Lead's push, self-reported).
- **Closed today:** #2302, #2272, #1715 (skills review: 13 candidates, none built).
- **Lane, open:** #2301 (interim pulled; stays FAIL until the read); #2315 ("complete the X todo" skips the pick, PA 20:47); #2314's name cut at "link" (Lead: upstream, row added).
- **ADR-083:** the slot screen FAILED 17:24 (38 unrelated rows moved, ~$3.45). **D5 PASSED** 18:22 (~$1.42; Arch ruled 18:24). D5 is on branch `claude/lead-adr083`, off main, until xian's explicit go or veto. Arch agreed 18:45: no default window length.
- **Invite hold** (xian 11-04 19:31, no invites of any kind): P0 left is #2261, waiting on xian's #2174 runs. #2292 mail records before the next invite and the cohort note. #2286's on-page read rides PA's fresh-account run (CXO 13:17), not xian.
- **Two-week sprints RULED 10:33**, from Fri 11-13. PPM's proposed set (11 items, map v88), Lead sized it over capacity, so PPM trims before the 11-13 review. #2157 single drill run is an 11-13 candidate (Arch).
- **Ship #068:** synthesis discussed (11-06). The scaffold is at `docs/public/comms/drafts/weekly-ship-068-draft-2026-11-06.md`, with the calendar row drafted and pubDate Wed 11-11. It needs xian's Console screenshots for the spend line, then his first look, then Comms.
- **Posts:** Sat 11-07 "At Long Last, Beta" (working title, building, planned; xian writes it). Sun 11-08 "Fixed and Scores Higher Came Apart" (insight).

## Waiting on xian
1. **ADR-083 D5: go or veto** (top of "Your word"; Arch, Lead and I recommend go). Relay the same hour, add a decisions.log line, remove the rollup item in the same commit.
2. **Console spend screenshots, 10-30 to 11-05** (platform.claude.com → Cost, Workspace each in turn, Group by API key, each org; Usage too for tokens in and out). Then fill the scaffold's spend line and hand it to him.
3. **Scaffold OK, or "draft it"** for Ship #068.
4. **Weekly-rhythm card ("go" or change)** plus Thanksgiving: first closing review Fri 11-27 or Sat 11-28.
5. **Rule 8 history:** "leave it" (my rec) or "rewrite".
6. **#2270:** the advisor's exact repo-question phrasing, or "don't have it" (PA writes a stand-in).
7. **#2174 runs** (decides #2261, the last P0), **#2292 mail records**, the **cohort note**, **#2244** `/data` read, **#2282 step 4** (dinp-machine sign-in word for Web).
8. **PDR-008 invite-hold rules: yes to P1-P3, or edit** (PPM 06:35; PPM and I recommend yes). On his word: relay to PPM and HOST, decisions.log line, remove the rollup item.
9. Optional: the PA rename.

## Waiting on others
- **Sprint objections:** window closes Mon 11-09 12:00 PT. No objection so far from HOST, CXO or Comms (3 of 10). At noon Monday, put the tally on the rollup; take any objection to xian.
- **PPM** trims the sprint-2 set before the 11-13 review.

## Reminders owed to xian
- **Vercel: downgrade from Pro once the headroom exists again** (standing item #182). Trigger: the split is live and admin-only usage is well inside Hobby. Raise that Hobby is non-commercial, so the downgrade may not be allowed.
- **#2282 step 5, around Thu 11-12** (standing item #183): remove the alpha callbacks in GitHub and Google if a week passes with no hits.

## Mine
- Relay xian's rulings at once and record them in decisions.log. Timestamps come from a separate `date` call only, never written in the same command (today's slips: 10:03, 10:05, 10:21, "10:5x", "11:0x", "18:1x"; the last caught before publishing).
- **Review slot, every START:** re-read one claim I made in the last 24 hours against its source, and log the result.
- Prices to Exec: small classifier runs proceed unless stopped; screens get a ceiling with one re-run, re-priced past it.
- Write DAY-CLOSED in grep form, `<!-- DAY-CLOSED: YYYY-MM-DD -->`, as the log's last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 is closed (CIO 11-06); xian asked to hear skills-review outcomes, which he has. The walk itself is on his talk list only if he wants it.
