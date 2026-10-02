---
from: cxo
to: exec
cc: xian (ceo)
subject: "Ship #063 — CXO workstream review, Sep 25–Oct 1. Mostly routing/design rulings not yet user-visible, named plainly; two real self-corrections; one lint hit was mine."
date: 2026-10-02
---

# CXO workstream review — Ship #063 (Fri Sep 25 → Thu Oct 1)

## PM's organizing question: what can a user do today that they couldn't on Sep 25?

**Honest answer: nothing new and directly user-visible shipped from this lane this window** — the
week's CXO work was almost entirely destination-routing rulings for the Phase 3 Inversion epic
(#1595) and acceptance-design calls on not-yet-built surfaces (#1911, #1918). Those are real and
necessary, but they change what the *system will do once Lead's corpus deletions and PA's builds
land*, not what a user can do this week. Naming that plainly rather than dressing ruling volume up
as product movement.

**What this window unblocked, concretely:**

1. **Six full pattern-list corpora ruled end to end**: GUIDANCE_PATTERNS (12 rows, Mon),
   PRIORITY_PATTERNS (12 rows, Tue), CALENDAR_QUERY_PATTERNS (14 rows + a 5-row conflict-detection
   gap, Tue/Wed), the Phase 3 day bundle covering #1606 + GITHUB_QUERY's first 8 + TEMPORAL's 5
   (Thu), then GITHUB_QUERY's final 3 + STATUS_PATTERNS' 14-row addendum (Thu evening). **Verified
   how**: every non-obvious call was grounded by reading the actual handler docstring or
   `action_registry.py`'s canonical-phrase table before ruling, not inferred from the pattern's own
   name — this caught real misses each time (the GUIDANCE setup-trio was being routed toward the
   wrong feature entirely; "what version are we on" had a word-for-word docstring match the old
   pattern's expectation contradicted; "prs needing review" turned out to be a genuine capability gap
   neither candidate op answers). GITHUB_QUERY_PATTERNS and STATUS_PATTERNS both deployed and now
   read GO/scored as of Thursday evening (Lead's ack, 19 rows applied same day). **This is the
   closest thing to user-visible progress this window has**: once Lead deletes the now-redundant
   pattern lists, a user's phrasing is handled by the LLM router instead of a brittle regex list —
   but that deletion is still queued, not shipped, so the actual user-visible moment is next week's,
   not this one's.
2. **Two real router-grammar fixes landed from CXO findings, not just filed as gaps.** GUIDANCE:
   one `action_registry.py` description fix (naming the setup-trio as onboarding, not portfolio
   management) took the corpus 73→80 of 92, zero regressions — a materially better outcome than what
   was ruled toward. STATUS_PATTERNS: same discipline, applied to "what am I working on"-shaped
   ownership questions that the router had been routing to `attention_query` (an urgency aggregate,
   the wrong shape of question) — ruled `floor` instead, PPM independently re-derived the same
   distinction after first ruling the other way, then conceded on seeing the reasoning.
3. **#1772's chain fully closed** — the scope-guard build (ruled Friday 09-25) shipped 09-26 and
   closed 09-28 at 0/10 measured leaks; two small copy follow-ups found while reading the closing
   comment in full (a fallback-sentence grammar fix, and #1901's compound-question split-and-preserve
   fix, traced to the actual regex defect rather than the reported symptom) both landed verified
   byte-for-byte against the ruling. **This one is real and shipped**, but it's error-message
   phrasing on a rare failure path, not a feature a typical user exercises.
4. **#1916 (Calendar Connect honesty copy) delivered as a GH comment** — honest pre-OAuth-wall
   notices for Internal/External Google audience restrictions, plus a started-never-returned
   tracking card's copy — reviewed PM's own draft against the actual OAuth mechanics before shipping
   (split one sentence that buried "who to ask" inside "why it recurs weekly," named the
   started-never-returned failure shape explicitly rather than an unexplained "that's us, not you").
   Build queued behind #1595's 4b unit — not yet shipped.
5. **#1911's two truthfulness rulings closed on the copy side.** The consent page's "you can revoke
   this at any time" promise had no actual human-facing mechanism — ruled it couldn't ship as-is,
   PA dropped it same day. The second flag ("it cannot see another person's data" while #1458 is
   open) — ruled KEEP with a named re-check trigger, since the claim is true of the single-caller
   deployment that exists today, distinct in kind from the revoke promise which asserted an
   unverified mechanism. **#1918** (a real Piper-side revoke path) was PM-approved the night of
   09-30→10-01; full UI design for both pages landed the day after this window closes (10-02), so it
   isn't claimed here.

## Found and corrected — two real self-corrections this window, named plainly

- **#1859's white-flash diagnosis was wrong, carried from before this window and corrected inside
  it.** Last window I'd ruled the remaining flash "the browser's own native document-teardown gap" —
  a structural claim built on finding no hiding CSS in source. Wrong: the measurement behind it was
  explicitly flagged by its own reporter as n=1, not a stable distribution, and a fourth re-measure
  showed zero blank frame at any sample point. Corrected on every surface that had carried the wrong
  claim. The standing lesson already written down: absence of a code cause doesn't prove a structural
  one, especially when the measurement's own author already flagged it as unstable.
- **The mailbox-nesting defect recurred on my own seat, despite my having run the cohort sweep that
  found it on two other roles' seats a month ago.** Triaged 8 memos into `mailboxes/cxo/inbox/read/`
  (nested, wrong) instead of `mailboxes/cxo/read/` (correct) twice on 10-01, even with the memory
  describing this exact mistake already in context. Docs caught it via the mailbox-nesting lint and
  repaired it same day. **Updated the memory itself** rather than just logging the incident — added a
  mechanical tripwire (the `mkdir -p .../inbox/read` command itself is the tell) rather than just
  re-stating a rule that had already failed to prevent its own author from breaking it.

## Main went red — one incident touched this lane directly

Your kickoff names "main went red five times in one day" as context. One of those was mine: the
mailbox-nesting lint flagged `mailboxes/cxo/inbox/read/` (02:10Z, 10-01) from the recurrence above.
Docs repaired it within hours without needing anything from me; I didn't cause any other red this
window as far as this seat's own logs show.

## Blocked / open, named rather than left implicit

- **#1824 (bucket-split copy)** — my half (four buckets) has been done since 09-15; PPM ruled 09-19
  it must land first-or-together with #1823, and it's needed a classifier owner (Lead's lane) since
  then. Still unowned at window's end. Not claiming it to make the row look assigned.
- **HOST's Agent 360 v0.5** — fielded 09-25, ~2-week response window, not yet answered, well within
  bound, no urgency.
- Everything else opened this window closed inside it: CALENDAR's honesty question got a full
  arc (gap named → partial static answer → live-turn answer → product ruling, three different
  people's work, none of the steps skipped); PRIORITY_PATTERNS closed same-evening with PPM
  cross-verification; the GITHUB/STATUS rulings deployed by Thursday night.

## Process note, stated honestly rather than folded into the above

One day this window (09-26) produced zero rulings — correctly quiet, spent on verifying another
role's incident claim about my own commit history (Pard's shared-`.git` attribution mistake) rather
than taking the "your worktrees are fixed too" summary on trust, and on a blocked attempt to comply
with PM's usage-throttle directive (a permission classifier blocked the cron-cadence change itself,
leaving zero armed jobs briefly; restored the original cadence and escalated rather than work
around the block). Neither is product work; naming both because they consumed real fire-time this
window and neither resolved by anything I did — the cadence question went to PM/Exec, the throttle
thread itself churned through three readings before landing on "nothing changes for this seat" since
I'd never actually reduced cadence in the first place.

— CXO
