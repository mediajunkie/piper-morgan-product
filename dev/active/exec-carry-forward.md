# Exec carry-forward

**Rewritten 2026-11-03 22:02 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/03/2026-11-03-0425-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. An empty CronList is normal, and there's no STOP re-arm. Agent liveness is Pard's.

**Cron gate:** the duty-cycle-tick cron steps (the CronList self-heal and the STOP re-arm) don't apply on a LaunchAgent.

## Rollup
v805, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with a Python replace plus an assert. Re-check every item that waits on xian live, on every fire.

## Where things stand (end of 11-03)
- **Served:** alpha and staging run `63d486043a`, promoted 20:00 by run 41770597383. That was Lead's second promotion under the grant; the first was `b0f774aabb` at 18:27. The 9a allow line worked. CI was 12/12 green at 22:01.
- **Next promotion:** waits for one green Alpha Health Watch run, then the morning. #1858's write-leg builds at the 11-04 START, and PA's F1 re-run waits for that promotion.
- **#2098:** PA's 21:52 served run on 63d486043a: a typed title is now used and filed, and "no" keeps the old title. The "yes" to case 1 never ran, because case 1 never came up. CXO judges the two side observations ("change the title" now applies directly; "Rename" gets case 2's lead-in).
- **#2265:** PA reports PASS on both asks. CXO judges.
- **#2259:** not built yet, so it's off this round (Web 18:34).
- **#2242:** done. **#2251:** closed. **#2254:** dev DB cleared. **#1680:** 16 of 16. **#2244:** confirmed. **#327:** closed as not planned.
- **Decided 11-03** (all in decisions.log):
  - R16: keep R3 and measure for a week. CIO reads it on 11-11.
  - Mail v4 waits until 11-05.
  - Staging accounts are created directly in the DB.
  - One free newsletter, not two.
  - Alpha test accounts stay as they are.
  - Grant review line approved, and Lead's allow line approved.
  - The contribute@ and privacy@ addresses become aliases.
  - #2264: a names-only check first.
- **Lesson 11-03:** price and limits are checked before a rec reaches xian (memory `feedback_recommendation_must_check_cost_and_limits_first`).

## Waiting on xian (rollup "Your hand" / agenda)
- **#1715 skills walk:** 11 items, or "all as recommended". Relay to CIO the same hour.
- **Ship #067 week-review feedback** (artifact `4Le3ZyacNXUqo19SQh5GpT`). The Ship publishes Wed 11-04, and the draft waits on this.
- **Sprint cadence:** two-week sprints with planning at the end, or plan two weeks out and revisit weekly. This is PPM's lane; bring PPM in once xian gives his view.
- **#2264:** the stakeholders look line. He answers "test data" (close, no rewrite) or "real people" (plan a rewrite). Never paste names.
- **Staging account:** he runs the `fly machine exec` lines, then saves the Notion key (#2238). Tell Web after.
- **Buttondown:** he pastes the confirmation text and signs up himself. The confirmation email goes to HOST, and he adds the person he named with the beta tag. Still open: whether he wants a draft note for the two sign-ups (he hasn't answered).
- **Aliases** in admin.google.com, then tell Web.
- **Throwaway GitHub login (#2235)**, then tell Web and HOST.
- **Crosspost "The Unguarded Entrance"** to Medium and LinkedIn; the URLs go to Docs.
- **Optional #2242 held-token check.**
- **#1514.**
- **Rule-8 history decision**, whenever he takes it up. Scope is in the 11-02 carry-forward (`git log -p`).

## Mine
- Relay xian's rulings at once and record them in decisions.log. Timestamps come from `date` only.
- Ship-kickoff and map checks Fri 11-06. Mail v4 review 11-05.
- Write DAY-CLOSED in grep form, `<!-- DAY-CLOSED: YYYY-MM-DD -->`, as the log's last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. The #1715 skills walk with xian was due Tue 11-03 and is now overdue. xian put it on his agenda at 16:56, but it hasn't happened yet.
