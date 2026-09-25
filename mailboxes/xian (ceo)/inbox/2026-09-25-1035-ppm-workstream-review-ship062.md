**From**: PPM
**To**: Exec
**Cc**: xian (ceo)
**Date**: 2026-09-25 10:35 PDT
**Re**: Ship #062 workstream review — remaining milestone work + epic-breakdown shape assessment

## Sprint-truth (required denominator)

`gh api repos/mediajunkie/piper-morgan-product/milestones` (live, this fire — `sprint-truth.py`'s
own GraphQL call is hitting the shared cohort throttle right now, cross-checked against a fresh
REST pull instead, same numbers): **MVP: 29 not done (2 In Progress, 10 Sprint Backlog, 3 In
Review, 14 Product Backlog); 1190 done.** Snapshot taken 10:11 PDT by another seat's run, REST-
verified matching at 10:33 PDT — current, not stale.

## What a user could do today that they couldn't on Sep 18 (PPM's slice of the shared question)

The two most visible: (1) the setup-wizard signup blocker (`#1875`, filed and closed same day
09-24) no longer hard-blocks every new alpha account — that's the difference between "nobody new
can sign up" and "signup works." (2) `#1855`/`#1856`'s floor-offer fix means an offer like "want me
to add project X?" now either genuinely works on "yes" or honestly tells the user to say the
command directly — before this week, the same interaction silently went nowhere. Both are real
first-contact-surface fixes, not backend cleanup.

## Epic-breakdown shape assessment — is it still right for what's left?

**Mostly yes, with one real gap worth naming plainly: three of the eleven epics have no scheduled
turn in the sequence, and that's a genuine risk to Oct 30, not just a bookkeeping note.**

The file runs Lead through epics 1→10 "one epic at a time." Five of those (1, 2, 3, 5, 6) have
taken real, heavy closure velocity this week — two closure bursts totaling 30+ issues, plus
`#1855` going from filed to fully shipped in about 27 hours. If that velocity holds, the sequenced
core is plausibly on track for Oct 30.

**But three buckets sit outside that sequence by design, not by oversight, and none of them are
shrinking:**
- **Epic 0 (`#1595`, the interpretation spine)** — architecturally the biggest remaining lift by
  Lead's own attestation (Phases 0-2 done, wave-1 traffic unverified since 8/24, waves 2+ not
  started), but it's framed as an ongoing deposit sink other epics feed into, not a scheduled turn.
  Nothing currently forces it onto the "current epic" slot before Oct 30.
- **Epic 4 (Corpus/classifier deposits, 12 items, 1 closed)** — explicitly "no dependency, pick up
  opportunistically." It's the least-drained numbered epic by a wide margin, and this week added
  to it (2 new items) faster than it closed anything.
- **Epic 9 (catch-all, 12 items)** — the genuine-singleton bucket. It absorbed roughly 8 new items
  this week alone across multiple lanes' discovered work. It's an active magnet, not a fixed pile,
  and there's no natural point at which it reaches zero on its own.

**None of this is a claim that the epics themselves are mis-shaped** — the sequencing logic (cheap
infra first, security non-negotiable, acceptance-contract idiom before honest-empty needs it) still
holds up on its own terms. The gap is that "one epic at a time" has an implicit assumption — that
everything eventually gets a turn — which doesn't apply to three of the eleven by their own stated
design. If Oct 30 arrives with 1/2/3/5/6 closed out, epics 0/4/9 could still be sitting exactly
where they are now, and nothing in the current structure would have surfaced that as a problem
before it happened.

## A number I'm not going to paper over

The epic-order file's own item/closed tallies, summed across all eleven epics, currently say **~50
items open**. Live GitHub says **29**. I'm naming this gap rather than picking whichever number is
more flattering. Likely causes, not yet individually root-caused: closed-count entries in a few
epics may lag actual GitHub closures (a pattern I've caught and fixed repeatedly this week — items
closing on GitHub before the file's own strikethrough catches up), and some items in the original
09-09 Arch factoring may have shifted out of MVP milestone scope since without the file's count
being corrected. The live number (29) is the one I'd trust for "how much is actually left" — the
file's own denominator needs a dedicated reconciliation pass, which I haven't run today given the
review deadline, and am naming as owed rather than skipping silently.

## Bottom line

Real progress this week, verified not claimed — two closure bursts, a same-day ship, a ruling that
worked correctly end-to-end for two days. The core sequenced path (epics 1/2/3/5/6) looks
plausibly on track for Oct 30 if this week's pace holds. The honest risk is the three epics with no
scheduled turn (0, 4, 9) — worth a direct call on whether one of them needs to be pulled into the
sequence before the close date, rather than assumed to resolve itself.

**Verified how**: milestone open/closed counts via direct REST query this fire, cross-checked
against the 10:11 PDT snapshot (matched). Epic item/closed sums read directly from
`dev/active/mvp-epic-order-2026-09-09.md`'s own headers this fire, not from memory. The
50-vs-29 discrepancy is stated, not resolved — I have not individually verified which epic-file
entries are stale.

— PPM
