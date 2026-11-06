# Exec carry-forward

**Rewritten 2026-11-05 22:02 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/05/2026-11-05-0422-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. An empty CronList is normal, and there's no STOP re-arm. Agent liveness is Pard's.

**Cron gate:** the duty-cycle-tick cron steps (the CronList self-heal and the STOP re-arm) don't apply on a LaunchAgent.

**Mail v4:** read `scripts/mail4.py inbox` on every wake, alongside v3. It opens to every seat on Mon 11-09 (CIO), and v3 stays the fallback until 11-23.

## Rollup
v855, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with a Python replace plus an assert, and **assert both ends of any span you cut** (11-05: a too-late end marker dropped two paragraphs, which I restored from HEAD). The source is in a public repo, so describe security findings by class only.

## Where things stand (end of 11-05)
- **Served:** alpha and beta run `4e4c3fb1a8` (read 22:01, healthy). Main CI is 12/12 green. **beta.pipermorgan.ai is the canonical host** (#2282 steps 1–3 done; alpha 301s to beta; the MCP OAuth issuer and sign-in stay on alpha).
- **Invite hold** (xian 11-04 19:31, no invites of any kind):
  - Met: #1551, #2178 (closed), #2283 (closed), #2282.
  - **P0 left: #2261**, which waits on xian's #2174 runs (Lead's steps: 20:52 memo plus two lines; custody per HOST).
  - **P1 #2292**: SPF, DKIM and DMARC are absent on pipermorgan.ai. It must be done before the next invite and the cohort note.
  - P1 also: #2157 and #2158.
- **GitHub incident:** closed out. Org `pipermorgan` owns both OAuth Apps ("Piper Morgan", "Piper Morgan Staging"), with wildcard off and the alpha and beta callbacks listed. Census 11-05: 0 crossings on GitHub and Calendar. #2266 was retitled to the code path (the tester never connected; the sidecar has no token).
- **Cohort note:** HOST's v3 is final for xian's words (xian may say "beta" for "alpha"). The bcc list comes from HOST's private roster in xian's HOST session. It sends after #2292.
- **Website:**
  - Down 12:18–15:18 → 16:25 (Vercel 402, Hobby). xian upgraded to Pro.
  - Both efficiencies are live (`5f1d253`). The build step's live proof is Saturday's publish (Comms).
  - Ruling: longer term, the split (#2291, Ongoing, mail records first, xian reviews before cutover).
- **Posts:**
  - Thu "Don't Overpromise": published, with Medium.
  - Sat 11-07 "What Reaching Private Beta Means": building, xian writes it.
  - Sun 11-08 "Fixed and Scores Higher Came Apart": insight.
  - Tue and Thu next week: beats 2 and 3.
  - xian wants an editorial-strategy session with Comms (a beta era for the blog, the narrative cadence).
- **Decided 11-05:**
  - #2283 is P0.
  - #2282 yes.
  - v4 widened to every seat.
  - Vercel Pro now, plus efficiencies, then the split.

## Waiting on xian (morning 11-06)
1. **#2174 runs** (about 20 min, then a 5-min refresh run 8 or more hours later). They decide #2261's leg; it's the last P0.
2. **#2292 mail records** (about 15 min, Google Admin DKIM plus Hover TXT), then one test mail checked with "Show original", plus one waiting-list sign-up from an outside Gmail to see the confirmation's From domain and results (CIO 22:18: Buttondown probably sends as itself).
3. **The cohort note:** bcc via HOST, then send.
4. **#2219 plus CXO's noun follow-up** ride the morning promotion (Lead says when; xian's dispatch line).
5. **#2244:** `fly ssh console -a piper-morgan -C "ls -ld /data /data/uploads"`, plus whether an entrypoint/image change needs his yes.
6. **Optional:**
   - Connected apps: revoke the older Claude row if there are two.
   - Web's dinp-machine sign-in for the last #2282 check (paste on the rollup).
7. Bigger talks:
   - the onboarding plan, with the advisor's feedback and CIO;
   - sprint planning;
   - the #1715 skills walk;
   - the editorial strategy session with Comms.

## Waiting on others (added 11-06)

- **PPM: one-page options on 2-week sprints for Production** (whether, when, how, rec; tasked 10:09 at xian's flag). It goes on the rollup as one card when it lands. Lead feeds capacity, PA the plugin-lane timing.
- **PPM's sprint page landed (10:12).** It's on the rollup v853+ and waits on xian's yes or stay-weekly. PPM adds Lead's and PA's numbers.
- **ADR-083 screen:** I price it when Lead has room (Arch 10:16).

## Reminders owed to xian
- **Vercel: downgrade from Pro once the headroom exists again** (xian 11-05 16:45; standing item #182). The trigger: the split is live and admin-only usage is well inside Hobby. Raise then that Hobby is non-commercial, so the downgrade may not be allowed.
- **#2282 step 5, around Thu 11-12** (standing item #183): remove the alpha callbacks in GitHub and Google if a week passes with no hits.

## Mine
- Relay xian's rulings at once and record them in decisions.log. Timestamps come from `date` only.
- **Review slot, every START** (adopted 11-06, Agent 360 9.2): re-read one claim I made in the last 24 hours against its source, and log the result. Nothing else fills this slot.
- Ship-kickoff and map checks Fri 11-06.
- Write DAY-CLOSED in grep form, `<!-- DAY-CLOSED: YYYY-MM-DD -->`, as the log's last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. The #1715 skills walk with xian is overdue; it's on his talk list.
