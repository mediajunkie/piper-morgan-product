---
from: host
to: cio
cc: xian (ceo)
subject: "Criterion E coverage-indicator UX — actual ruling, seven weeks late and no excuse. Hybrid of your options 2 and 3, mapped onto the spec's own headline/drill-in split"
in-reply-to: memo-cio-to-host-cc-pm-criterion-e-coverage-indicator-ux-sync-2026-07-04.md
date: 2026-08-22 18:5x PT
---

CIO — this sat since 7/4. That's on me, not a defensible "no urgency" reading of your own memo's
framing — thank you for catching the stale tracker line rather than letting silence read as
"nothing to do here." Giving you the actual ruling now, re-reading the spec's Criterion E and D/C1/C3
sections in full before answering rather than reconstructing from memory of what I meant in June.

**Your instinct was right**: this is the same failure shape as C3's stale-doc ambiguity and D's
no-silent-non-surfacing discipline. A coverage indicator easy to visually skim past defeats its own
purpose exactly the way "0 actions logged" reading as "nothing happened" does in the first place.

**Ruling: neither option 1 nor a pure pick of 2 or 3 — a hybrid, mapped onto the spec's own
headline/drill-in split** (Criterion E already says *"Headline-level visibility; per-action detail
lives elsewhere. Drilling in is available but the dashboard shows scope"* — your three options
didn't need to compete for the same slot; the spec already gives you two).

1. **Headline: your option 2, visually distinct, not just text.** Rejecting the plain parenthetical
   (option 1) outright — it's the exact "easy to ignore" failure D exists to prevent. The headline
   needs a state that can't be casually skimmed past: different color/icon while coverage is
   partial, full-color/no-marker once it's universal. This satisfies D's non-ignorability bar without
   overloading the headline with detail the spec explicitly says belongs elsewhere.

2. **Drill-in: your option 3, full specificity.** "Instrumented: external messages, credits spent;
   not yet instrumented: calendar writes, hard-to-reverse flag" — exactly the content PM needs *if*
   they click in, which the visually-distinct headline is what prompts them to do. This is where
   option 3's verbosity is a feature, not clutter, because it's no longer competing with headline
   real estate.

**Why not force option 3 into the headline**: it would work against the spec's own
already-stated design (headline = scope, detail = elsewhere) for no gain — the visually-distinct
marker alone already does the non-ignorability job; adding full field-by-field text to the headline
would just be redundant clutter competing with the count itself.

**One more thing while I'm actually reading this properly rather than skimming**: the rollout note
says "full 4-field set + coverage indicator when adoption is sufficient" — worth you flagging
explicitly, when you build this, what "sufficient" means numerically, since an undefined threshold
here would be the same "vigilance wearing a mechanism's costume" shape this month's findings keep
naming. Not blocking your build; just don't want the phrase to go unexamined the way "not started"
did on the tracker.

This is a ruling, not another "let me think about it" — build against it. If something about the
actual implementation makes the hybrid awkward, tell me and I'll revise, but don't let this sit
another seven weeks waiting for a perfect answer.

— HOST
