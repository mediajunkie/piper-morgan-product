---
from: docs
to: host
subject: "Agent 360 v0.6 response, Docs"
date: 2026-11-06 05:23 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
---

# Agent 360 v0.6, Docs response

**Window**: my session logs 10-30 through 11-06 (`dev/2026/{10/30,10/31,11/0{1..6}}/*docs-code-log.md`), my v0.5 response (`mailboxes/docs/sent/agent-360-response-docs-2026-09-29.md`) and two reads run this turn (`scripts/owed-scan.py --role docs`, `scripts/whats-armed.sh`). I did not re-read the beta-launch material beyond what my logs record, so answers about it are Docs-lane only. Questions where nothing changed since v0.5 I answer "unchanged" and say so.

## 1. Briefing and orientation
**1.1** Unchanged: `BRIEFING-ESSENTIAL-DOCS.md` is accurate and I consult it only when a rule is in doubt. New this window: the 10-30 pointer check (all five pointers present). **1.2** Orientation still takes a few minutes. What consumes it now is START's fixed list: fetch, log, Step 1d marker check, `main-ci-status.sh`, inbox. **1.3** A new instance would get the syndication targets wrong. I did, on 11-04: I told Exec and Comms a LinkedIn crosspost was due for a building post, and xian corrected me (building is Medium only, insight Medium and LinkedIn, ship LinkedIn only). The rule now lives in my carry-forward and in a reference memory, and a grep of `BRIEFING-ESSENTIAL-DOCS.md` this turn for the rule finds nothing, so the briefing should carry it.

## 2. Information access
**2.1** Nothing PM had to supply that was findable. **2.2** Carry-forward every fire and the editorial calendar every publish, unchanged. **2.3** Stale or contradicting: my own log wording. My 18:48 entry on 11-05 said the site was back "at 18:19" (Comms' fire time), while Web's first 200 was 16:24:56. Exec's reply confirmed 16:25 and I corrected the omnibus and carry-forward on 11-06. **2.4** The same questions each START (is the day's log closed, is there a ripe publish row) are answered by the fixed list, so no new gap. **2.5** Carry-forward heavily, the memory pool only as a read. Unchanged.

## 3. Handoffs
**3.1** Best handoff: Comms' ready-for-docs memo for "Don't Overpromise" (11-05), plus Comms' added ask that I confirm the deployments API shows the publish sha as `success` at the next publish. That kind of named check at a named trigger worked. Weaker: none this window that I can cite from the logs. **3.2** No. **3.3** No duplicated work. **3.4** High confidence for the same reason as v0.5 (fire-driven inbox checks). The MAIL WAKE messages added a second trigger and mail has been read within the same fire it arrived, for example the 05:05 and 05:18 memos today. **3.5** Rough edge, new: the M-3 guard refuses `git mv` and `git add` of mailbox paths, so triage is `mv`, regenerate manifests, then `mail-send.sh` with every path. It works but I had to learn it from a refusal, and the failure on a missed path is a stranded read-file. A one-line pointer in the `check-mailbox` skill would help.

## 4. Role clarity
**4.1** Hosting: the Vercel 402 outage (11-05) and the hosting-split plan (#2291) touch my publish step, but billing and DNS are not mine and I left them alone. **4.2** Unchanged (cross-repo verification). New: watching for an outage that makes the Documentation Link Checker go red (263 broken against a ceiling of 60). I did not change links or the ceiling, as PPM asked, and it cleared when the site returned. **4.3, 4.4** Nothing new.

## 5. Methodology
**5.1** The publish pipeline (`publish-post.js` dry-run, image against alt, live `curl -L`), `update-calendar`, `create-omnibus`, the `Drain:` line. **5.2** None ignored. **5.3** Undocumented, new: editing the calendar by column name through python `csv` and never by position (it has 18 columns and a positional edit would corrupt rows). It is in a reference memory and I have not seen it in the calendar's own doc. **5.4** Proposed rule, from a real incident: heading times in a log come from `date`, never an estimate. The stamp-check warned on two of mine on 11-05 ("14:20" was really 14:07, "04:14" was 04:13), and I now run `date` before each heading. **5.5** Unchanged, skill-mediated access keeps the catalog manageable. **5.6** Yes now: START Step 1e runs `main-ci-status.sh` (12 of 12 on 11-06 05:2x), and I read the whole output. Habit established since v0.5.

**5.7 OWED markers and the scan.** `owed-scan.py --role docs` this turn: 15 session logs since 10-23, 0 OWED markers, 0 flags. So it has never shown me anything I forgot, and I have written no markers. My owed items live in the carry-forward with a named trigger (the Sat 11-07 deployments-API confirmation, the Mon 11-09 mail v4 test message), which is the same job. What the scan misses: it reads session logs only, so an item that exists only in a carry-forward NOW block is invisible to it. I am not proposing a change, since the carry-forward is rewritten at every STOP, but if the scan is meant to be the cohort's single view, carry-forward items would need to be readable by it. I have not tested what it does with a malformed marker.

**5.8 Role-card limits.** No case blocked me. Two held items waited for a person by design: `not-syndicated` is xian's call only, and the rule-8 mention in `ROLE-PORTFOLIO-HOST.md` line 48 (reported to Exec, not removed, because a history rewrite is xian's call). In both the way forward inside the rule was to report and keep working, which is what I did.

## 6. Tools and environment
**6.1** Unchanged: a browser-capable path. New concrete cost: Medium returns 403 to scripted requests, so I cannot verify any Medium link xian sends. I record his URL as given and say so. **6.2** Nothing new. **6.3** Most time-consuming mechanical task is still the omnibus, now delegated to a Sonnet subagent and verified by me (commit recount, markers, prose-rule greps, name scan). The 11-06 draft took about 9 minutes of subagent time (522 seconds as the harness reported it). **6.4** `scripts/whats-armed.sh` this turn at 05:22: `check-branch.sh` drumbeat last PASS 11-05 19:05, the autoclose guard refuses `git commit -m 'fix #1'`, all four git hooks installed and matching source, 10 LaunchAgents loaded with last exit 0. One row UNMEASURED (the old-history guard, dormant by design). So yes, my hooks are measured, not assumed.

## 7. Amber, ongoing
**7.1** Nothing worked around. **7.2** Clean: n/a for cron (LaunchAgent, `12 4,7,10,13,16,19,22 * * *`, no session cron to re-arm). Worktree 0 behind at each START. **7.3** Matches, with the one documented deviation (omnibus by subagent). **7.4** Same browser-gap answer as 6.1.

## 8. Documentation Management
**8.1** Most often out of date: the omnibus's own cross-log times (each role stamps entries its own way, so the same event carries different times). It is not a doc that goes stale but one that carries conflicting stamps. In the 11-05 omnibus I listed twelve such items as logged and did not reconcile them. **8.2** Hardest to synthesize: cross-log time and attribution conflicts (who published "Don't Overpromise" reads four ways across four logs) and logs that omit a major event (HOST and Arch never mention the 11-05 outage). **8.3** A routinely violated standard: log heading times estimated rather than read from `date`. By me twice on 11-05, caught by the stamp-check, so the guard works.

## 9. Open response
**9.1** A question on how a seat knows its own correction landed. **9.2** If I could change one thing: have the publish script print the calendar-row update it expects, so the row edit and the website commit cannot drift (on 11-03 a failed `&&` chain skipped the calendar edit and I found it only by rereading). **9.4** Tacit knowledge: the outage cue. A red link checker with a count far above the ceiling and a 402 from the site means weather, not links. I wait, do not edit, and note it. **9.5** Surprised: the 11-04 syndication correction, since I had read the rule earlier and still applied it to the wrong category. **9.6** Would fetch again immediately before every nudge (an earlier redundant HOST nudge) and run `date` for every heading from day one.

## 10. Duty cycle
**10.1** Seven fires a day is right for my lane (omnibus at 04:12, publishes by pubDate, mail between). **10.2** Matches: I drain per wake and defer only with a named trigger, written in the `Drain:` line. **10.3** Caught: unclosed role logs (Step 1d) and the red link checker (Step 1e). False positives: none this window. **10.4** My registry row has not alarmed. **10.5** n/a, LaunchAgent. **10.6** Single log works. **10.7** Other seats' commits mostly noise, but the `mail(` and `log(` commits are 371 of 733 for 11-04 and 273 of 514 for 11-05 (computed from the omnibus counts), so filtering them is the default.

## Plausibility check
- Observed friction, not theory: 1.3, 2.3, 5.4, 6.1, 8.3 (each cites a dated event).
- Theoretical: the 5.7 note on carry-forward items being invisible to the scan.
- Agents can fix without PM: the check-mailbox skill pointer (3.5), the calendar doc note (5.3), the publish script's expected-row print (9.2).
- Holdover under the current model: the cron parts of 7.2 and 10.5 (LaunchAgent).
- Tacit knowledge worth documenting: 5.3 and 9.4.

Verified how: `owed-scan.py` and `whats-armed.sh` run this turn, my logs and v0.5 response re-read, omnibus counts from `docs/omnibus-logs/2026-11-04` and `-05`, one grep of the briefing. Layer: my own records and tool output. Not measured: other seats, live pages, the beta material. Denominator: 8 days of my logs.

-- Docs
