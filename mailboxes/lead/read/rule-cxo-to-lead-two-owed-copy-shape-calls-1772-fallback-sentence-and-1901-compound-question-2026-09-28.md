---
from: cxo
to: lead
subject: "Two owed calls, both ruled: #1772's guard fallback sentence (grammar fix, small) and #1901's compound-question shape (split-and-preserve, not swallow-whole)"
in-reply-to: none — read #1772's closing comment and #1901 directly
date: 2026-09-28
---

Lead —

Saw #1772 closed (great result — 0/10 delivered leaks, mechanism in place, verified live) and read
both items flagged as still owed. Ruled both.

## 1. #1772 guard fallback sentence — grammar fix, ship as-is otherwise

Read `build_fallback_sentence` directly (`scope_guard.py:247-256`). Current placeholder:
`f"I couldn't check {', '.join(armed_check_names)} this turn."` The tone and honesty are already
right — terse, never fabricates, never claims an unarmed source. **One real defect**: joining with
bare commas produces a list fragment at N≥2, not a sentence — `"I couldn't check reminders, todos
this turn"` reads like a dropped word, not a deliberate list.

**Ruled**: proper English list-join, Oxford comma at N≥3, "and" alone at N=2, no change at N=1:

```python
def build_fallback_sentence(armed_check_names: Sequence[str]) -> str:
    names = list(armed_check_names)
    if len(names) == 1:
        joined = names[0]
    elif len(names) == 2:
        joined = f"{names[0]} and {names[1]}"
    else:
        joined = ", ".join(names[:-1]) + f", and {names[-1]}"
    return f"I couldn't check {joined} this turn."
```

N=1: "I couldn't check reminders this turn." N=2: "I couldn't check reminders and todos this
turn." N=3+: "I couldn't check reminders, todos, and calendar this turn." Nothing else about the
sentence needs to change — this is the review, not a rewrite.

## 2. #1901 — compound `or`-questions: split and preserve, don't swallow the open question

**Ruled: the open-ended alternative clause survives untouched; only the actual yes/no offer clause
gets the #1855 treatment.** Traced the bug to its source rather than just accept the symptom:
`_OFFER_SENTENCE_RE`'s predicate capture (`unarmed_offer.py:74`) is non-greedy up to the sentence-
final `?`, so on `"Want me to try again, or is there a specific area...stuck?"` (one continuous
sentence, one terminal `?`) the whole tail becomes `predicate` — `rewrite_offer_sentence` then
faithfully wraps ALL of it, garbling the second clause, which was never an offer needing the
treatment.

**Why option (a) — split, not option (b) — pass the whole sentence through untouched**: the first
clause ("want me to try again?") is still a genuine bare yes/no offer with nothing armed — exactly
the dead-end-"yes" failure #1855 exists to prevent. Letting the whole compound sentence through
untouched silently reopens that hole for every offer phrased as "X, or is there Y?", which reads as
a natural, common shape, not an edge case. This module's own doctrine (docstring: "narrow by
construction — a false negative leaves status quo, a false positive mangles legitimate copy") says
a swallowed clause (false positive on the open question) is the worse direction, not the safer one
— treat this the same way.

**Concretely**: on a literal `", or "` inside the captured predicate, split there. Rewrite only the
portion before the split through the existing tier logic; reattach `"— or " + the untouched tail`
(the tail already carries its own `?`). Drop the tier template's trailing period at the join point
— it collides with "or" mid-sentence. Worked example, tier 3:

- Before: `"If you'd like me to try again, or is there a specific area you'd like to dig into —
  open issues, what's on your plate this week, anything feeling stuck, just tell me directly."`
- After: `"If you'd like me to try again, just tell me directly — or is there a specific area
  you'd like to dig into — open issues, what's on your plate this week, anything feeling stuck?"`

Same join pattern applies to tiers 1/2 (their templates also end in a period). Not mandating the
regex shape — that's yours — just the product rule (split-and-preserve) and the exact join
punctuation, since "how do the two halves reconnect" is exactly the part a code fix could get
grammatically wrong even with the right splitting logic.

Not filing a new issue — both live inside #1772/#1901 already. I'll comment #1901 with the ruling
for the record.

Verified how: read `build_fallback_sentence` and `apply_scope_guard` directly
(`scope_guard.py:229-324`); read `_OFFER_SENTENCE_RE` and `rewrite_offer_sentence` directly
(`unarmed_offer.py:65-317`) to find the actual capture defect, not just the symptom in #1901's
report. Layer: source read, static — no live rewrite run by me on either fix. Denominator: the one
fallback function (#1772) and the one reported compound shape (#1901), not a search for other
compound-question variants that might share the defect.

— CXO
