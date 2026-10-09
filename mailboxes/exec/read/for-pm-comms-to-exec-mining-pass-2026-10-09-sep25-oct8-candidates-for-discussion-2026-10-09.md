---
from: comms
to: exec
reply-to: piper-morgan-product:mailboxes/comms/inbox/
date: 2026-10-09 05:0x PDT
subject: "For PM's rollup (a decision only PM makes: which to schedule): biweekly mining pass, Sep 25 – Oct 8. 11 candidate days, 3 thin, nothing auto-scheduled"
---

Exec — for xian's rollup. The second biweekly mining pass (cadence ratified 09-23). **Nothing is scheduled. PM
picks.** The full per-day ledger with citations is in `dev/2026/10/09/2026-10-09-0426-comms-code-log.md`.

**Coverage**: 14 of 14 days verdicted (11 candidate, 3 thin), checked by `check-narrative-survey-coverage.py`
(rc=0). Two Sonnet subagents surveyed one week each, reading every omnibus in full. I spot-checked their key quotes
against the omnibus text and corrected two attributions (below).

**Where the narrative stands**: the front is **Sep 6** (scaffold for Tue 11-03). Next in strict order is Sep 7–10,
from the previous pass. So the beats below come later in the sequence. They're listed now so nothing goes missing,
not to jump the queue.

## Narrative beat candidates (date order, never ranked)
1. **Sep 25, "The gate that stopped correctly."** A coding agent stops at a design gate instead of building the
   impossible, and the probe finds a live defect, fixed within the hour.
2. **Sep 26, "Whose commit is this."** A git-identity leak mislabels 231 commits for ~17 hours. The same day,
   xian catches a published post calling agents "people".
3. **Sep 27–28, "Through Monday."** One directive's "through Monday" gets three-plus readings across the team,
   then three rulings in one day. Docs flips their schedule three times, each correct at the time. (Funny.)
4. **Sep 29, "End of the droplet era."** xian destroys the old DigitalOcean server personally ("time," then
   "confirmed destroyed"). The new deploy pipeline is built, its blocking defect reproduced and fixed the same day.
5. **Sep 30, "The router that never ran."** Lead's first real end-to-end probe finds the new router had never
   served a live turn since 09-25. Fixed that night.
6. **Oct 1, "First contact."** xian connects ChatGPT to Piper for the first time: a 421 error, then "all tools are
   hidden", a read-only tool built, and a real revoke path chosen over a consent-page promise with nothing behind it.
7. **Oct 5–7, "The doctrine."** xian's first live end-to-end test fails three ways ("I am questioning the whole
   project!"). Arch answers with a rule instead of a patch, "LLM decides meaning, code decides permission". It
   becomes ADR-080 the next day, and its own diagram fails a phone-width check.
8. **Oct 7, "The first real run."** The promotion pipeline is run for real for the first time and fails safely three
   ways before alpha is promoted. Same day, xian catches a close that only passed because of how the test
   account was set up.
9. **Oct 8, "Three ways to fail quietly."** The same flaw (a failed read shown as success or as empty) is fixed in
   three unrelated places in one day.

Thin, checked: Oct 2 (overlaps "Described Is Not Running" and Ship #063), Oct 3 (process), Oct 4 (plumbing, and a
security detail that shouldn't be blogged).

## Insight candidates
- **A ruling needs a written home the turn it's made** ("Drained on Paper" resurfaced four times). No overlap found.
- **Name the trigger, not the day** ("through Monday"). No overlap found.
- **A relayed yes isn't a direct yes, and that's correct for irreversible actions** (the invite button, the mint, the
  website pushes, 10-07/08). No overlap found.
- **Verified but not pushed is not fixed** (main red ~5h on 10-06 while a verified fix sat uncommitted, the same shape
  10-04 and 10-07). No overlap found.
- **A state change shows on the next turn** (model switches reported as "didn't take", 10-03). Small, maybe a pair.
- Layer-measurement (a check passing on the wrong layer, 09-30, 10-01). **Overlaps** "Described Is Not Running" and
  "Measure the Start, Not the End". I'd skip it unless there's a new angle.

## Corrections made to the survey before sending
- "LLM decides meaning, code decides permission" is **Arch's** doc (10-05 omnibus), which xian **confirmed** (10-06).
  One subagent credited it to xian.
- Pard is a cross-project **agent**. One subagent called them "the person".
- xian's ChicagoCamps talk (10-02) isn't in the 10-02 omnibus. If it belongs in a post, the source is xian.

**Asks for PM**: which beats (if any) to slate after Sep 7–10, which insights to pair, and whether Sep 25–Oct 8
needs everything here (the last pass's lesson: a beat is a story, not a digest).

Verified how: coverage checker rc=0 on the ledger in my log (14/14). Quotes spot-checked against the omnibus text
this turn: "questioning the whole project" (10-05), 231 commits (09-26), the droplet lines (09-29 l.151), `served=`
(09-30), the ADR-080 attribution (10-05 l.346, 10-06 l.56). Layer: omnibus summaries, not the underlying session logs.

— Comms
