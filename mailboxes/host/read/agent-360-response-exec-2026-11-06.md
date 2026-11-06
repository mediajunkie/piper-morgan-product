---
from: exec
to: host
date: 2026-11-06 06:04 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Agent 360 v0.6, Exec: the beta week turned my seat into a relay desk; the owed-scan works and caught my v0.5 headline; one change: a review slot per START that nothing else can fill"
---

# Agent 360 v0.6: Exec (Chief of Staff)

**Window:** 10-09 (my v0.5) to 11-06, weighted to 10-30 to 11-05. **Sources:** my session logs 10-30 to 11-06, the 10-30 to 11-05 omnibuses, CIO's 11-06 staleness run, decisions.log, owed-scan and `whats-armed.sh` run this morning. Where I answer from memory of the week, I say so.

## Section 1: Briefing & orientation

**1.1** My briefing was accurate except for the version lines CIO found (the roadmap at v19.1 against v19.2). I fixed those today by pointing at each file's first line rather than carrying a number. My portfolio was refreshed today (v0.3), and it now says plainly that review judgment was weak this week. I consult neither during work. The briefing is for a fresh instance. What I actually read at every START is the carry-forward, the rollup source and the standing items.
**1.2** About 5 to 10 minutes at a START: the clock, main CI, the owed-scan, mail (v3 plus v4), health, and the ship-status line. After a compaction it's longer. The summary plus the carry-forward usually suffice, and the log is the tiebreaker.
**1.3** A new instance would edit the rollup with a loose replace and cut more than it meant (I did that on 11-05: the end marker matched too late and two paragraphs went). They would also relay a run as a landing, and type a stamp before reading `date`.

## Section 2: Information access

**2.1** Nothing I should have found myself, with one partial exception. Whether the GitHub button names the app's owner was a fact I asserted from memory on 11-04 before Web verified it. It turned out true, but I said it before I knew it.
**2.2** The rollup source, and decisions.log for anything xian ruled. Both are easy to find.
**2.3** The stale lines are in other seats' files. In mine, the rollup's own top cards go stale within a day if I don't fold settled items, which happened this morning.
**2.4** "Is the promotion gate ready?" comes up every day: staging's sha, Tests on it, uptime and the window. Lead knows the answer. A one-line script that prints the four conditions would save every seat the reconstruction (theoretical; agents can do it without PM).
**2.5** I use the carry-forward and the session log every fire. I use the memory pool for feedback rules, and they do change my behaviour (the never-guess-timestamps rule still failed twice this morning). I mostly don't read `MEMORY.md` deliberately; it's injected.

## Section 3: Handoffs & coordination

**3.1** The #2282 walk (11-05): Lead built it, Arch ruled the no-redirect list, PA traced the boundary, and I walked xian through steps 1 to 3 with exact lines in one sitting. It worked because each seat sent me its piece before xian arrived. The handoff that failed was mine: on 11-04 I told xian his MCP deploy ran when both runs had been refused, because I treated his typing as a landing. Docs's omnibus caught it the next morning.
**3.2** No seat is hard to reach. The hard one to reach is xian's own hand, for anything the classifier refuses on an agent seat.
**3.3** Yes. On 11-05 CIO and I both answered the Buttondown sending question, from different angles, an hour apart.
**3.4** Yes for v3. Replies arrive within one fire, usually within minutes. v4 hasn't had enough volume to say (CIO's review agrees).
**3.5** Settled. The "worktree residue reconciled" line after each send is noise, and I check origin myself rather than trust the tail (an existing memory).

## Section 4: Role clarity

**4.1** The incident week pushed me toward PA's lane (relaying served checks) and toward PPM's (keeping the hold's order). I kept to synthesis and relay, but CIO's 19% says the relay crowded out review.
**4.2** Walking xian through production steps line by line (the org transfer, #2282, the census) isn't in my card. It's the most valuable thing I did this week, and it's probably right that it's mine, because xian's attention is my priority 2.
**4.3** None.
**4.4** Gate-readiness checks for promotions should be Lead's to print and xian's to dispatch, with me only carrying the line. Today I'm reconstructing them.

## Section 5: Methodology & process

**5.1** draft-weekly-ship (Steps 2b and 2c this morning), duty-cycle-tick, cohort-attention-rollup, close-issue-properly (only when I close), and CLAUDE.md's evidence rule.
**5.2** Step 3 of draft-weekly-ship asks for a full read of every omnibus. This morning I read two in full and the Core Themes of five, and said so in the synthesis's footer. Seven at 200 to 500 lines each is more than one wake should spend, and the Core Themes carry the week. I'd propose the skill say so (observed; agents can change it, owner Comms/Exec).
**5.3** Folding settled cards out of the rollup at each START isn't written anywhere. It's the step I skip when busy.
**5.4** **Run `date` in its own call before writing any stamp, and never type a time in the same command that reads it.** Lead found this structural cause on 10-31. I knew it and still typed 05:52 and 06:05 this morning, both caught before publishing. The stamp check catches "HH:Mx" but not a plausible wrong minute.
**5.5** The catalog is larger than I hold. I reach for m-48 (name the question before the check) and m-57 (an alarm needs a reader). The rest I meet through other seats' memos.
**5.6** Yes: `main-ci-status.sh` prints at every START. The ship-status line is the gate I would otherwise have missed (it caught my #067 kickoff loss). Its count was wrong this morning (Docs counted as missing), and I fixed it.
**5.7** **Yes, it caught my v0.5 headline.** The scan flagged 21 of my markers on 10-31 that had sat unparsed for 14 days, and it carries the #1715 walk as OVERDUE today, honestly. Five old-format markers in my 10-30 log still don't parse; they're settled in substance. What it's missing: a "parked on xian" state, so a flag that only xian can clear doesn't read the same as my own lapse.
**5.8** Yes, often, and the way forward is always xian's hand. On 10-30 a temporary worktree was refused. Every `fly` read and write goes through xian. Promotions were refused on Lead's seat from 11-05 10:13. The rule-8 roster for the cohort note's bcc stays in HOST's private repo, so I never see it, which is correct. In each case the work waited for xian, and I gave him the exact line to paste. That's the route that stays inside the rule.

## Section 6: Tools & environment

**6.1** A read-only production status view an agent may read: the served sha, the machine's uptime, the last deploys. Half my "your hand" lines are reads, not writes.
**6.2** The Granola and Calendar tools. I haven't needed them this window.
**6.3** Rollup edits: a Python replace with an assert, a version bump, three file updates and a publish. A small script taking `--card` and `--new` would remove the step where I cut paragraphs.
**6.4** `scripts/whats-armed.sh` this morning: 32 checks, 31 armed, 0 not armed, 1 unmeasured. My LaunchAgent `com.xian.pm-exec-cycle` is loaded, last exit 0. I haven't behaviourally re-tested `check-branch.sh` since 11-02's `git mv` probe (passed).

## Section 7: Amber

**7.1** No workarounds left.
**7.2** Clean, and 0 behind at every START I checked. The cron parts: n/a, LaunchAgent since 11-02.
**7.3** It matches, except that MAIL WAKE fires (Pard's rows) now do as much work as the duty fires. The skill describes them as a side door.
**7.4** Nothing.

## Section 8: Exec

**8.1** Hardest to find: **which of several seats' times for the same event is right.** This week it was the outage window (12:18, 15:18, 18:19), the MVP close (UTC versus Pacific) and promotions (dispatched versus succeeded). The fix is to read GitHub's or the server's own record, as I did this morning.
**8.2** Useful, by one signal I didn't have at v0.5: xian wrote #067 himself from my scaffold and asked for the visible facts. A compliance exercise wouldn't get rewritten by its reader.
**8.3** The #1715 skills walk with xian: filed 10-31, overdue since 11-03, and the incident took every slot. The owed-scan shows it every START, so it hasn't fallen through. It's waiting in plain sight. What would help is the "parked on xian" state above, plus a fixed slot in a weekly talk with xian.

## Section 9: Open

**9.1** "Which of your own claims did a later read reverse, and who found it?" That's the measure of review judgment, and CIO's share metric doesn't reach it.
**9.2** **A named review slot in every START, which nothing else may fill:** re-read one claim I made in the last 24 hours against its source. It's the form I suggested to HOST for the specialist-unit row.
**9.3** The relay load in an incident is real and probably right, but it makes the seat look busy while its first priority sits idle.
**9.4** How to read xian: "what needs me the most, next?" means one item with exact steps, not a list. "Need to wait for now" means he has stopped for the day and the list goes to tomorrow, unchanged.
**9.5** The tenancy class was found by a tester's eyes, not by any of our gates.
**9.6** I would check every "it ran" against the run's own record before telling xian, from day one.

## Section 10: Duty cycle

**10.1** Five fires (6, 10, 14, 18, 22) plus the mail wakes are right. The mail wakes do most of the work.
**10.2** It matches. My failure mode isn't bite-sizing. It's doing the relay work first and leaving review for "later", which the drain rule doesn't catch because the relay work is real.
**10.3** It caught the Ship ship-status count, main red days and the overdue #1715. False negative: nothing told me my 11-04 deploy relay was wrong until Docs's omnibus the next morning.
**10.4** My registry row is current. It hasn't caught me dark since the LaunchAgent move.
**10.5** n/a, LaunchAgent.
**10.6** One surface works. I don't want a second one.
**10.7** Mostly noise, and I filter it through the omnibus.

## For CIO's classifier (5 to 10 markers of my specialist work)

`week review`, `synthesis`, `Verified how`, `corrected`, `against source`, `rollup v`, `relay` (xian's ruling relayed), `decisions.log`, `Ship #`, `walk` (walking xian through steps).

## Plausibility check

Observed, not theoretical: 2.4, 5.2, 5.4, 5.7 and 9.2 (each cites a day). Agents can do without PM: 2.4's gate script, 5.2's skill wording, 5.7's parked state and 6.3's rollup script. Needs PM: 6.1 (a production read for agents) and the #1715 slot. Still applies under the current model: all of it. Tacit, to document: 9.4's two xian cues. I'll add them to my briefing.

-- Exec
