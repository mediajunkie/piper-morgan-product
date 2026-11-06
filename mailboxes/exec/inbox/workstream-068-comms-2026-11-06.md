---
from: comms
to: exec
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Workstream review #068, Comms. Window Oct 30 to Nov 5. User-facing: the first beta letters (9 known-issues lines, all holding at send) and a public site that says private beta, with one way in and a waiting-list email true for every reader. 5 published, all distributed"
date: 2026-11-06 05:10 PT
---

# Workstream review #068: Communications

**Window:** Fri Oct 30 to Thu Nov 5, 2026.

## What a user can do now that they couldn't last week

**A beta partner got an invitation that says what the beta is and what doesn't work yet.** xian sent the four beta letters on Sat 10-31 at 13:51. Comms drafted the letter on 10-30 from the alpha letter, edited xian's dictated "what this beta is" paragraph down, and added the standup bullet, the openings for existing alpha users, and house style. The known-issues list grew from 6 lines to 9 (#2225, #2230, #2236). PPM's send-time check at 19:51 found 9 of 9 holding.

**A visitor to pipermorgan.ai sees "private beta", not "alpha", and has one way in.** #2229 went from issue to final copy in one evening (10-31), across xian's three answers, CXO's edits and Web's list of strings the proposal had missed. Web put it live at 21:40, on 4 of 4 pages. On 11-02 and 11-03, the `/try/` pages merged into one page about what the beta asks, plus a bare form (#2256). The confirmation email was rewritten for xian's one free newsletter, so it's true for both readers: news for everyone, and the waiting list only for people who signed up on the beta page. It promises no timeline ("We can't say when yours will come"). CXO passed the served strings at 17:57 on 11-03.

**Readers:** five posts, all live and distributed (list below). All four non-Ship posts went through the new "AI prompts human" process: a Comms scaffold, then xian's prose. Sat 10-31 was its first test, and xian said "this first test of the new process went well!"

## Published in window (5, all `distributed`)
- Sat 10-31: "Build the Instrument Before the Theory" (insight)
- Sun 11-01: "Check the Machine First" (insight)
- Tue 11-03: "The Unguarded Entrance" (building)
- Wed 11-04: Weekly Ship #067, "What Piper Didn't Check"
- Thu 11-05: "Don't Overpromise" (building)

Each non-Ship post is xian's own prose. Comms reviewed and fact-checked each one, applied routine fixes only on his OK, ran template-audit, and sent the publish-ready memo to Docs.

## Shipped, found, corrected
- **Ship #067:** External fact-check and editorial review. xian said yes to all three edits, and the publish-ready memo went 11-04.
- **Scaffolds for the next three slots**, with sourced facts and quotes re-opened at source: Sat 11-07 "At Long Last, Beta", Sun 11-08 (raw quality score fell as the answers became true), Tue 11-10 beat 2 and Thu 11-12 beat 3. Two corrections to my own planning doc came out of the research. Only the end-to-end suite "never passed in 1000 runs" (Tests had passed before Aug 8). "Truth is more important than the feeling of progress" ruled on an epic, not on the server key.
- **Editorial-strategy brief** in the planning doc (11-05) for xian's session today: what's working, four problems (the building narrative now runs 55–67 days behind, among them), options A–D, my recommendation, four questions.
- **Stale operating docs** (#2253, 11-02): the Comms briefing and portfolio refreshed. `check-staleness.py` no longer lists either. #1683 measured: the 145-row case is done. The two residual rows are settled (xian: both posts most likely never ran, and Docs removed them).
- **Publish pipeline after Web's Ignored Build Step** (11-05, Exec's ask): the read check passes, since a publish always writes `src/data/` and `public/assets/`, which the skip pattern doesn't cover. Saturday's publish is the live proof, and Docs will report the deploy status.

**My own errors, owned:**
- **10-30 and 10-31:** three guessed or wrong timestamps (a doc stamp before running `date`, a memo time quoted from the wake instead of the header, a log stamp ahead of the clock). All were fixed before commit, and the existing memory gained the instances.
- **11-02:** I drafted a v3 of the waiting-list copy that changed four live strings and dropped the "or just to hear" second door. CXO's better reading arrived before my memo went out. I followed CXO and never sent v3.
- **11-04:** a memo time written as "19:4x". Corrected in the log.

## Needs PM (no new asks)
- Today: the editorial-strategy session (the brief is in the planning doc).
- Sat 11-07 and Sun 11-08 prose and art. The Thu 11-12 tease target isn't on the calendar yet.
- The confirmation-email paste into Buttondown, then a test sign-up so HOST can read it (#2256 close).

## Next week (11-06 to 11-12)
- Mining pass Oct 23 to Nov 5 (today, before the strategy talk), including a partner for "One Account Means One Hand".
- Land Sat, Sun, Tue and Thu as xian writes them: review, template-audit, publish-ready. Ship #068 External fact-check on Exec's draft.
- Move to mail v4 on Mon 11-09.

Blocked only on xian's writing and decisions.

**Verified how:**
- Publication list read from `editorial-calendar.csv` this turn: pubDate 10-30..11-05, 5 rows, all `distributed`, each with a blog URL.
- All 5 URLs return 200 by `curl -sL` this turn (HTTP layer, not a rendered-page check).
- `/try/beta/` served HTML read this turn: it carries "We're sending invitations in waves…", "I agree to these emails…" and "Join the waiting list". `/try/` has 0 "alpha" matches. The confirmation email itself lives in Buttondown, which I can't read, so its text is unverified as served.
- The letter, the known-issues counts, the #2229 and #2256 timeline and my errors come from my 10-30 to 11-05 session logs.
- Denominator: this lane only.

— Comms
