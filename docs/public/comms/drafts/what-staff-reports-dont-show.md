---
image:
alt:
caption:
---

# What Staff Reports Don't Show

*May 20, 2026*

I was drafting a weekly progress post a few days ago — the kind of synthesis post where I review what the team of role-named agents on my project shipped during the past week and report it out. I'd opened all six of the role-specific weekly memos. Read them carefully. Synthesized what they said. Drafted the post. Sent it for review.

The reviewer flagged that I'd missed the entire engineering arc of the week. Half a dozen issue closures had landed in the codebase. None of them appeared in any of the six memos I'd read.

[FACT-CHECK NOTE for PM: Ship #043 v0.2 draft; engineering arc included #921 / #857 / #1071 / #1021 / M2f closure / M2g-A + M2g-B / #1070 / #304 / #1090 per memory pin. Confirm if the public version should mention specifics or stay at "half a dozen issue closures."]

# The mistake

I'd been treating the six memos as the source set. They weren't. The memos were each role's *perspective* on the week — what that role wanted to surface from its own corner of the project's activity. The source set was something bigger: the daily omnibus logs the documentation role kept aggregating cross-team activity, the individual session logs each role wrote at the end of its working sessions, and the actual artifacts produced over the week — commits, issue closures, code changes, memos filed.

The six memos summarized what each role wanted me to know. The source set described what was happening. Those are two different deliverables. I'd been reading the first and assuming I had the second.

# Why staff reports filter

This isn't a bug in how the role-memos were written. Filtering is what role-memos are *for.* Each role writes from its perspective on what's important from its role's vantage. The documentation role notes things the documentation role notices. The engineering role notes things the engineering role notices. None of the roles writes a comprehensive log of everything that happened in the week — that would defeat the purpose of having role-specific reports, which is to give the reader a quick view from each angle.

The filtering is well-intentioned and structurally appropriate at the level of each individual report.

The problem is what happens when you only read the reports. You get the cross-product of everybody's filter — every event that some role thought was important enough to mention. That cross-product is smaller than what actually happened. There are events that nobody's role surfaces because nobody's role views it as in-scope. There are events multiple roles surface from different angles and the angles don't reconcile. There are events the source data has but no role mentions because the role didn't think it mattered.

The chief who reads only the staff reports gets a coherent narrative built from the union of the staff's filters. That narrative isn't ground truth. It's the staff's view of ground truth.

# Why I almost didn't notice

The reason staff-reports-only is the seductive failure mode is that the staff reports are *compact.* They're written for the reader's attention. They distill. They make synthesis fast. If you're under time pressure or attention pressure, the staff reports are an enormous bandwidth saver. You can cover the week in an hour. You can cover the quarter in a day. You can cover the year in a week.

The problem is that the bandwidth saver isn't free. It costs coverage. The ten-times-more-ground you can cover by reading only staff reports is a thinner version of the ground. You've formed views on the staff's interpretation of what happened, not on what happened.

Most of the time, the gap between staff-interpretation and ground-truth is small, and your views built from the staff reports are good enough to make the call you needed to make. The cost of also reading the source set would have been more than the value it added. The lazy version of the discipline is right most days.

But the gap isn't always small. Sometimes the staff misses something. Sometimes two roles surface contradictory framings of the same event and the staff reports each treat it as resolved when it isn't. Sometimes an emerging pattern is visible in the source data and not yet surfaced by any role because no role's vantage has the right view of it. The chief reading only staff reports has no way to notice these.

The chief reading the source set can.

# What the source set looks like

For my project, the source set has three components.

The first is omnibus logs — a daily aggregation document the documentation role keeps, listing each role's session activity in chronological cross-team order. Reading the day's omnibus shows me what happened across all roles on that day, not just what each role decided to surface in its weekly memo.

The second is session logs — each role's per-session record of what it actually did, including the mistakes, the dead ends, the unfinished work, the things that almost got filed but didn't. Session logs are where I see the texture of the work. The staff memos are where I see the conclusions.

The third is the actual artifacts. The commits in the repository. The issues closed. The memos filed in the mailbox system. The architecture decisions, the methodology entries, the design documents. These are the durable record of what changed. Anything the staff reports describe should be verifiable against these. Anything not described by the staff reports but visible in the artifacts is something I might have missed.

Reading these three layers gives me coverage of what happened. Reading the staff reports gives me coverage of what the staff want me to think happened. Both are useful. Only the first is ground truth.

# The discipline

The chief reads the logs. Not as a substitute for the staff reports — the staff reports are still doing useful work, and a chief who never reads them would have a different blind spot, missing the staff's framing of the priorities. The discipline is to read both, and to form views on the source set rather than on the staff-mediated summary.

In time-constrained moments, this is hard. The temptation is to skip the source set because the staff reports are right there. The discipline is to not skip it consistently. A chief who reads the source set once a quarter has a different posture than a chief who reads it once a year. The chief who never reads it develops blind spots that compound invisibly — invisible because by definition the blind spots are made of things the staff filter dropped, and the chief who only reads the filter doesn't know what's dropped.

The compounding is the thing that matters most. The first time you skip the source set, the cost is approximately zero. The hundredth time, the cost is that your model of the project has drifted from reality by a hundred small unnoticed events, and you no longer have the calibration to detect the drift.

# The generalization

This isn't really about chiefs of staff. It's about any role that consumes filtered reports from front-line workers.

PMs reading status updates from engineers versus reading the production-incident logs and the customer-support tickets and the actual code commits. Executives reading dashboards versus reading the underlying metrics' raw distributions and the support-ticket transcripts. Professors reading TA-graded summaries versus reading the student essays themselves. Journalists reading press releases versus reading primary-source documents and talking to the people who were in the room.

Same shape in each case. The filter is well-intentioned and structurally appropriate. The filter saves bandwidth. The filter also costs coverage. The mature consumer of filtered reports periodically reads the source set, to calibrate the filter and notice what the filter is dropping.

The maturity isn't being suspicious of the staff. It's understanding what staff reports are *for* — which is filtered surfacing, not ground-truth replacement — and reading accordingly.

# What changed for me

The weekly post I'd drafted from staff-reports-only got rewritten. The second pass started from the omnibus logs instead, and the engineering arc came back in. The quality of the synthesis improved. More importantly, the act of reading the source set surfaced two other small patterns the staff hadn't yet named — patterns I could carry into the next week's reviews.

The chief reading the source set wasn't a luxury. It was the difference between a synthesis that reflected what happened and a synthesis that reflected what the staff wanted to surface. Those two are usually close. Sometimes they aren't. The discipline is being able to tell which week you're in.

---

*Next on Building Piper Morgan: "What the Running System Found" — the system had been running for three days when we discovered six of nine agents had been quietly doing their logging wrong, and had all self-corrected the same day without anyone noticing.*

*Where in your work do you consume filtered reports from front-line workers? When was the last time you read the source set instead? What did you find that the filter had dropped?*
