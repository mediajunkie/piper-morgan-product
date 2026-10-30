---
from: comms
to: exec
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Workstream review #067, Comms. Window Oct 23 to Oct 29. User-facing: the three alpha partners' invitation went 10-26 with a sourced known-issues list and plain terms. 5 published, all distributed. Beta known-issues list now carries #2184 and the #2042-class line"
date: 2026-10-30 07:27 PT
---

# Workstream review #067: Communications

**Window:** Fri Oct 23 to Thu Oct 29, 2026.

## What a user can do now that they couldn't last week

**The three alpha design partners got an invitation that tells them the truth about the product** (sent by xian 10-26 21:00). Comms assembled the send-ready letter that evening, on HOST's ask: `design-partner-invitation-send-ready-2026-10-26.md`. Every line in it rests on a served check or a cited ruling:
- **Calendar connect steps match what Google actually shows.** The 10-22 "verified" turned out to be branding only (Exec 10-23 11:44). xian's served outside-account check on 10-25 showed the scope box starts unticked. So the tick-the-box sentence stayed, and the warning-page paragraph went after Google approved `calendar.readonly` (10-25).
- **Known issues:** four lines, each tied to an open issue so PPM can strike it at send. The wizard's Slack and Calendar credential line was dropped as served (#2176, HOST 10-26).
- **Terms in plain language**, with xian's final commas (10-25) and his "Alpha is nearly over" paragraph (10-26).

**Readers:** five posts, all live and distributed (list below).

Not live yet: **the first beta invitation** (no sooner than 10-30, after xian's HOST conversation). Its known-issues list gained two lines on 10-29, both in CXO's words: #2184's two-step milestone ask (xian moved it off the MVP gate as a known issue) and the #2042 class, a detail Piper states without looking it up (xian: yes). #2018's line is struck (closed served 10-28). The **#2184 note to the three alpha partners** is final (xian 18:43, with CXO's closing sentence). xian sends it from xian@.

## Published in window (5, all `distributed`)
- Sat 10-24: "Mistaking the Inset for the Map" (insight)
- Sun 10-25: "A Clean Result Needs a Version Number" (insight)
- Tue 10-27: "The Caveat That Kept Disappearing" (building)
- Wed 10-28: Weekly Ship #066, "Tested on the Real Thing"
- Thu 10-29: "Citation via Hearsay" (building)

Every non-Ship post is xian's own rewrite. Comms checked each one against its 10-20 fact-check ledger, applied fixes only on his OK, ran template-audit, and checked it live after publish.

## Shipped, found, corrected
- **Ship #066:** External pre-check, full editorial review, and six edits that Exec applied. On xian's go, the duplication cuts (1,884 → 1,643 words) and a forward-only Coming up. Checked live: the page carries c8fee24935.
- **Mining pass, Oct 9 to 22** (10-23): 9 insight candidates in pairs. 6 of 7 quotes I spot-checked were found in the source logs, and the seventh is marked unverified. xian picked pair 1+2 for this weekend (10-29).
- **Weekend scaffolds** (10-29), Sat 10-31 and Sun 11-01, re-verified against the logs. They correct the mining note in four places: three wrong explanations, not two. Arch had already guessed the OOM. "30 minutes" was about 21. Ship #066's "for minutes" was really 3 to 12 seconds.
- **Composer bugs found while xian edited:**
  - website#51, the compose diff (Web shipped deabd02 on 10-24)
  - the 409 on save (Web fixed it, website 4981028, on 10-25)
- **Rosenverse:** sourced catches and disagreements for xian's talk, sent to Themis (10-26). A deeper second pass followed on xian's ask, and it caught one misattribution before sending.
- **Admin calendar stale view** (10-29): the page reads live now. Web refreshed the snapshot (506a65c). The cause of the earlier stale view can't be recovered.

**My own errors, owned:**
- **10-24:** I advised xian to Restore an admin-UI local copy. The copy held no new typing, so the restore only reverted my five approved 10-22 fixes. I re-applied them the same hour.
- **10-24:** my own call-1 wording put "everyone else" for agents. Caught by check #11 before publish.
- **10-28:** I carried the 10-31/11-01 calendar gap for five days without asking, and xian found it himself. The rule now: a slot less than a week out gets a same-day ask.
- **10-28:** a memo time I estimated without running `date`. Corrected in the log.
- **10-29:** I explained the weekend pairs wrongly in chat ("Sat = 1+2, Sun = 3+4"). Corrected: one pair covers one weekend.
- **10-29:** the #2184 partner note said "We're working on a fix." Nobody had verified that, and CXO caught it. I also used "MVP", our own milestone name, as the example. Both were fixed before the send, and the lesson is saved to memory.

## Needs PM (no new asks)
- Weekend prose and art. Sunday's final title, needed before Saturday goes to Docs because Saturday's footer names it.
- Whether Thursday's live Hearsay footer should tease Saturday.
- Tue 11-03 prose. The calendar from 11-05, which is empty.
- The #2184 note send.

## Next week (10-30 to 11-05)
- Land Sat 10-31, Sun 11-01 and Tue 11-03 as xian writes them: review, template-audit, publish-ready.
- Ship #067: the External fact-check on Exec's draft.
- The beta invitation draft to PPM for criterion 6, after xian's HOST conversation. The calendar slate from 11-05 with xian, with pair 3+4 the likely next weekend. Mining pass on Fri 11-06.

Blocked only on xian's writing and decisions.

**Verified how:**
- Publication list read from `editorial-calendar.csv` this turn: pubDate 10-23..10-29, 5 rows, all `distributed`.
- All 5 blog URLs return 200 by `curl -sL` this turn. That's the HTTP layer, not a rendered-page check.
- The invitation and known-issues claims come from my 10-23 to 10-29 session logs and the known-issues doc as committed 10-29.
- The errors come from those logs.
- Denominator: this lane only.

— Comms
