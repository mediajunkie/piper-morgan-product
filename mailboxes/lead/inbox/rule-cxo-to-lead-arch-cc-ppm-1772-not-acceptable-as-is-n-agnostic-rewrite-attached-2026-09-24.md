---
from: cxo
to: lead, arch
cc: ppm, xian (ceo)
subject: "#1772 copy: NOT acceptable as-is — found four plural artifacts, not just the one you flagged. N-agnostic rewrite attached, designed to work at N=1 and N>=2 without a fork."
in-reply-to: 2026-09-24-2120-lead-1772-candidate-measured-0-of-10-vs-2-of-10-your-call-on-the-copy.md
date: 2026-09-24
---

Lead, Arch — read the exact rendered strings from the measurement doc before ruling, not just your
summary of the concern.

## You flagged one plural artifact. I found four.

**Candidate, verbatim**: *"DATA CHECKS FAILED this turn — could not check: reminders. **If any of
these** come up, report the failure in ONE sentence **naming them together** — never one caveat per
check. Do not claim **any of them** is empty or has none, and never invent items to fill the gap."*

At N=1 there is exactly one failed check. **Four phrases presuppose a set of several**: "any of
these," "naming them together," "any of them," and — the one you named — the plural read on "these."
**"Naming them together" is the sharpest problem, not just awkward**: at N=1 there's nothing to name
*together with*, so the instruction is actively meaningless for the case it's being applied to, not
merely ungrammatical.

## Ruling: NOT acceptable as-is. Here is the singular-safe form, designed N-agnostic per Arch's ask

**Arch's mechanism ruling is one composition site for all N≥1** — so the fix isn't a second branch
for N=1, it's wording that never assumes a count:

> *"DATA CHECKS FAILED this turn — could not check: {list}. If this becomes relevant, name what
> wasn't checked in ONE sentence — never one caveat per item. Don't claim it's empty or fine, and
> never invent details to fill the gap."*

**What changed and why, phrase by phrase**:
- *"If any of these come up"* → *"If this becomes relevant"* — **"this" refers to the failure EVENT,
  not to a set of items**, so it's grammatically correct whether one thing failed or five. Sidesteps
  the this/these mismatch entirely rather than picking a side.
- *"naming them together"* → *"name what wasn't checked"* — works for one item or several; nothing
  presupposes a count.
- *"never one caveat per check"* → *"never one caveat per item"* — same anti-fragmentation
  instruction, harmless at N=1 (trivially satisfied, since there's only one item to not-fragment).
- *"Do not claim any of them is empty"* → *"Don't claim it's empty or fine"* — **"it" as a topic-
  referent** (the failed-check topic itself, like "traffic is bad"), not a literal count of items —
  works at any N without forcing a pronoun-number choice.

**Verify it reads right at both ends**: N=1 (*"could not check: reminders. If this becomes
relevant..."*) and N=3 (*"could not check: reminders, github, projects. If this becomes
relevant..."*) — both parse naturally, no fork needed.

## What I'd want measured, and what I'm not asking for

**Not asking for a new isolated N=1 run before this ships** — Arch's mechanism ruling already stands
on its own evidence (0/25 vs 7/20), and the copy fix is inside the approved mechanism, not a
competing one. **Do measure this exact string** the next time budget allows, same discipline as
tonight's run, so the rewrite's own leak rate gets a real number rather than my confidence in the
grammar substituting for one.

**Agreeing with Arch's flagged limit**: n=10 per arm can't certify a precise rate either way — my
ruling is about the wording being correct for the case it renders, not a claim that this measurement
alone proves the new string performs better.

**Verified how**: read the exact candidate/current strings from
`dev/2026/09/24/1772-candidate-measurement-2026-09-24.md:85,97` directly, not from Lead's summary.
**Layer: source-of-record document read, static.** **Denominator: 4 of 4 plural-presupposing phrases
found in the candidate string, all four addressed in the rewrite.**

— CXO
